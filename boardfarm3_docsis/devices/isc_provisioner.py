"""ISC DHCP cable modem provisioner module."""

import ipaddress
import logging
import re
from argparse import Namespace

import pexpect
from boardfarm3 import hookimpl
from boardfarm3.devices.base_devices import LinuxDevice
from boardfarm3.exceptions import ConfigurationFailure, FileLockTimeout
from boardfarm3.lib.utils import get_nth_mac_address

from boardfarm3_docsis.templates.provisioner import Provisioner

_LOGGER = logging.getLogger(__name__)

_DHCPV4_MASTER_CONFIG = """log-facility local0;
option log-servers ###LOG_SERVER###;
option time-servers ###TIME_SERVER###;
default-lease-time 604800;
max-lease-time 604800;
allow leasequery;

class "CM" {
  match if substring (option vendor-class-identifier, 0, 6) = "docsis";
}
class "MTA" {
  match if substring (option vendor-class-identifier, 0, 4) = "pktc";
}
class "HOST" {
  match if ((substring(option vendor-class-identifier,0,6) != "docsis") and (substring(option vendor-class-identifier,0,4) != "pktc"));
}

option space docsis-mta;
option docsis-mta.dhcp-server-1 code 1 = ip-address;
option docsis-mta.dhcp-server-2 code 2 = ip-address;
option docsis-mta.provision-server code 3 = { integer 8, string };
option docsis-mta.kerberos-realm code 6 = string;
option docsis-mta.as-req-as-rep-1 code 4 = { integer 32, integer 32, integer 32 };
option docsis-mta.as-req-as-rep-2 code 5 = { integer 32, integer 32, integer 32 };
option docsis-mta.krb-realm-name code 6 = string;
option docsis-mta.tgs-util code 7 = integer 8;
option docsis-mta.timer code 8 = integer 8;
option docsis-mta.ticket-ctrl-mask code 9 = integer 16;
option docsis-mta-pkt code 122 = encapsulate docsis-mta;

option space docsis code width 1 length width 1;
option docsis.tftp_server code 2 = ip-address;
option docsis.acsserver code 6 = { integer 8, string };
option space vivso code width 4 length width 1;
option vivso.iana code 0 = string;
option vivso.docsis code 4491 = encapsulate docsis;
option op125 code 125 = encapsulate vivso;

subnet ###PROV_IPV4### netmask ###PROV_NETMASK### {
  interface ###IFACE###;
  ignore booting;
}

shared-network boardfarm {
  interface ###IFACE###;
  subnet ###CM_IPV4### netmask ###CM_NETMASK###
  {
    option routers ###CM_GATEWAY###;
    option broadcast-address ###CM_BROADCAST###;
    option dhcp-parameter-request-list 43;
    option domain-name "local";
    option time-offset ###TIMEZONE###;
    option docsis-mta.dhcp-server-1 ###MTA_DHCP_SERVER1###;
    option docsis-mta.dhcp-server-2 ###MTA_DHCP_SERVER2###;
  }
  subnet ###MTA_IP### netmask ###MTA_NETMASK###
  {
    option routers ###MTA_GATEWAY###;
    option broadcast-address ###MTA_BROADCAST###;
    option time-offset ###TIMEZONE###;
    option domain-name-servers ###WAN_IP###;
    option docsis-mta.kerberos-realm 05:42:41:53:49:43:01:31:00 ;
    option docsis-mta.provision-server 0 ###MTA_SIP_FQDN### ;
  }
  subnet ###OPEN_IP### netmask ###OPEN_NETMASK###
  {
    option routers ###OPEN_GATEWAY###;
    option broadcast-address ###OPEN_BROADCAST###;
    option domain-name "local";
    option time-offset ###TIMEZONE###;
    option domain-name-servers ###WAN_IP###;
  }
  pool {
    range ###MTA_START_RANGE### ###MTA_END_RANGE###;
    allow members of "MTA";
  }
  pool {
    range ###CM_START_RANGE### ###CM_END_RANGE###;
    allow members of "CM";
  }
  pool {
    range ###OPEN_START_RANGE### ###OPEN_END_RANGE###;
    allow members of "HOST";
  }
}"""  # noqa: E501

_DHCPV6_MASTER_CONFIG = """log-facility local1;
preferred-lifetime 7200;
default-lease-time 43200;
option dhcp-renewal-time 3600;
option dhcp-rebinding-time 5400;

allow leasequery;
prefix-length-mode prefer;

option dhcp6.info-refresh-time 21600;
option dhcp6.ia_pd code 25 = { integer 32, integer 32, integer 32, integer 16, integer 16, integer 32, integer 32, integer 8, ip6-address};
option dhcp6.gateway code 32003 = ip6-address;
option space docsis code width 2 length width 2;
option docsis.device-type code 2 = text;
option docsis.tftp-servers code 32 = array of ip6-address;
option docsis.configuration-file code 33 = text;
option docsis.syslog-servers code 34 = array of ip6-address;
option docsis.device-id code 36 = string;
option docsis.time-servers code 37 = array of ip6-address;
option docsis.time-offset code 38 = signed integer 32;
option docsis.cm-mac-address code 1026 = string;
option docsis.PKTCBL-CCCV4 code 2170 = { integer 16, integer 16, ip-address, integer 16, integer 16, ip-address };
option docsis.acsserver code 40 = { integer 8, string };
option vsio.docsis code 4491 = encapsulate docsis;


# TODO: move to host section
option dhcp6.aftr-name  code 64 = string ;
# aftr-name aftr.boardfarm.com
option dhcp6.aftr-name 04:61:66:74:72:09:62:6f:61:72:64:66:61:72:6d:03:63:6F:6D:00;
option dhcp6.name-servers ###PROV_IPV6###;
option dhcp6.domain-search "boardfarm.com";

class "CM" {
  match if option docsis.device-type = "ECM";
}
class "EROUTER" {
  match if option docsis.device-type = "EROUTER";
}

subnet6 ###PROV_NW_IPV6### {
  interface ###IFACE###;
  ignore booting;
}

shared-network boardfarm {
  interface ###IFACE###;
  subnet6 ###CM_NETWORK_V6### {
    pool6 {
      range6 ###CM_NETWORK_V6_START### ###CM_NETWORK_V6_END###;
      allow members of "CM";
      option docsis.time-servers ###TIME_IPV6###;
      option docsis.syslog-servers ###PROV_IPV6### ;
      option docsis.time-offset 5000;
      option docsis.PKTCBL-CCCV4 1 4 ###MTA_DHCP_SERVER1### 2 4 ###MTA_DHCP_SERVER2###;
      option docsis.time-offset ###TIMEZONE###;
    }
"""  # noqa: E501

_DHCPV6_MASTER_OPEN_NW_CONFIG = """    pool6 {
      range6 ###OPEN_NETWORK_V6_START### ###OPEN_NETWORK_V6_END###;
      allow members of "EROUTER";
      option dhcp6.solmax-rt   240;
      option dhcp6.inf-max-rt  360;
      prefix6 ###EROUTER_NET_START### ###EROUTER_NET_END### /###EROUTER_PREFIX###;
    }
    pool6 {
      range6 ###OPEN_NETWORK_HOST_V6_START### ###OPEN_NETWORK_HOST_V6_END###;
      allow unknown-clients;
      option dhcp6.solmax-rt   240;
      option dhcp6.inf-max-rt  360;
    }
  }
}"""

_DHCPV4_CABLE_MODEM_CONFIG = """host cm-###BOARD_NAME### {
   hardware ethernet ###CM_MAC_ADDRESS###;
   filename "###CM_BOOTFILE_PATH###";
   option bootfile-name "###CM_BOOTFILE_PATH###";
   option docsis.tftp_server ###TFTP_SERVER_IP###;
   option dhcp-parameter-request-list 2, 3, 4, 6, 7, 12, 43, 122;
   option docsis-mta.dhcp-server-1 ###MTA_DHCP_SERVER1###;
   option docsis-mta.dhcp-server-2 ###MTA_DHCP_SERVER2###;
   option domain-name-servers ###TFTP_SERVER_IP###;
   option time-offset ###TIMEZONE###;
   next-server ###TFTP_SERVER_IP###;
}
host erouter-###BOARD_NAME### {
   hardware ethernet ###EROUTER_MAC_ADDRESS###;
   default-lease-time ###DEFAULT_LEASE_TIME###;
   max-lease-time ###MAX_LEASE_TIME###;
   option domain-name-servers ###TFTP_SERVER_IP###;
}"""

_DHCPV6_CABLE_MODEM_CONFIG = """host cm-###BOARD_NAME### {
   host-identifier option dhcp6.client-id 00:03:00:01:###CM_MAC_ADDRESS###;
   option docsis.configuration-file "###CM_BOOTFILE_PATH###";
   option dhcp6.name-servers ###TFTP_SERVER_IP###;
   option docsis.tftp-servers ###TFTP_SERVER_IP###;
   option docsis.PKTCBL-CCCV4 1 4 ###PROV_IPV4### 1 4 ###PROV_IPV4###;
}
host erouter-###BOARD_NAME### {
   host-identifier option dhcp6.client-id 00:03:00:01:###EROUTER_MAC_ADDRESS###;
   hardware ethernet ###EROUTER_MAC_ADDRESS###;
   option dhcp6.name-servers ###TFTP_SERVER_IP###;
   fixed-prefix6 ###FIXED_PREFIX_IPV6###;
   fixed-address6 ###FIXED_ADDRESS_IPV6###;
}"""


class ISCProvisioner(LinuxDevice, Provisioner):
    """ISC DHCP cable modem provisioner."""

    _ipv6_prefix = 64

    def __init__(self, config: dict, cmdline_args: Namespace) -> None:
        """Initialize ISC DHCP Provisioner.

        :param config: device configuration
        :param cmdline_args: command line arguments:type cmdline_args: Namespace
        """
        super().__init__(config, cmdline_args)
        self._prov_ipv4_address = self._config.get("prov_ip", "192.168.3.1")
        prov_ipv6_interface = ipaddress.IPv6Interface(
            self._config.get("prov_ipv6", f"2001:dead:beef:1::1/{self._ipv6_prefix}")
        )
        self._prov_ipv6_address = prov_ipv6_interface.ip
        self._prov_ipv6_network = prov_ipv6_interface.network
        # we're storing a list of all /56 subnets possible from erouter_net_interface.
        # As per docsis, /56 must be the default pd length
        erouter_ipv6_net_interface = ipaddress.IPv6Interface(
            self._config.get("erouter_net", "2001:dead:beef:e000::/51")
        )
        self._erouter_ipv6_network_list = list(
            erouter_ipv6_net_interface.network.subnets(
                56 - erouter_ipv6_net_interface._prefixlen  # type: ignore
            )
        )

    @hookimpl
    def boardfarm_server_boot(self) -> None:
        """Boardfarm hook implementation to boot ISC provisioner."""
        _LOGGER.info("Booting %s(%s) device", self.device_name, self.device_type)
        self._connect()

    @hookimpl
    def boardfarm_shutdown_device(self) -> None:
        """Boardfarm hook implementation to shutdown ISC provisioner."""
        _LOGGER.info("Shutdown %s(%s) device", self.device_name, self.device_type)
        self._disconnect()

    def _get_timezone_offset(self) -> int:
        """Get time zone offset."""
        offset = 0
        timezone = self._config.get("timezone", "UTC")
        if timezone.startswith("GMT") or timezone.startswith("UTC"):
            match = re.search(r"[\W\D\S]?\d{1,2}", timezone)
            if match and match.group(0).isdigit():
                offset = int(match.group(0))
        # offset should be from GMT -11 to GMT 12
        if offset in range(-11, 13):
            offset = 3600 * offset
        else:
            _LOGGER.warning("Invalid Timezone. Using UTC standard")
            offset = 0
        return offset

    @staticmethod
    def _replace_keywords_from_string(string: str, keywords: dict) -> str:
        for keyword, value in keywords.items():
            string = string.replace(keyword, str(value))
        return string

    def _get_common_keywords_to_replace(self) -> dict:
        timezone_offset = self._get_timezone_offset()
        common_keywords = {
            "###IFACE###": self.eth_interface,
            "###BOARD_NAME###": self._cmdline_args.board_name,
            "###TIMEZONE###": timezone_offset,
            "###MTA_DHCP_SERVER1###": self._prov_ipv4_address,
            "###MTA_DHCP_SERVER2###": self._prov_ipv4_address,
        }
        return common_keywords

    def _get_dhcpv4_master_config(self) -> str:
        cm_network_ipv4 = ipaddress.IPv4Network(
            self._config.get("cm_network", "192.168.200.0/24")
        )
        cm_gateway_ipv4 = self._config.get("cm_gateway", "192.168.200.1")
        mta_network_ipv4 = ipaddress.IPv4Network(
            self._config.get("mta_network", "192.168.201.0/24")
        )
        mta_gateway_ipv4 = self._config.get("mta_gateway", "192.168.201.1")
        open_network_ipv4 = ipaddress.IPv4Network(
            self._config.get("open_network", "192.168.202.0/24")
        )
        open_gateway_ipv4 = self._config.get("open_gateway", "192.168.202.1")
        prov_network_ipv4 = ipaddress.IPv4Network(
            self._config.get("prov_network", "192.168.3.0/24")
        )
        syslog_server = self._config.get("syslog_server", self._prov_ipv4_address)
        time_server_ipv4 = self._config.get("time_server", self._prov_ipv4_address)
        sip_fqdn = self._config.get(
            "sip_fqdn",
            "09:53:49:50:43:45:4e:54:45:52:09:42:"
            "4f:41:52:44:46:41:52:4d:03:43:4F:4D:00",
        )
        keywords_to_replace = {
            "###LOG_SERVER###": syslog_server,
            "###TIME_SERVER###": time_server_ipv4,
            "###MTA_SIP_FQDN###": sip_fqdn,
            "###PROV_IPV4###": prov_network_ipv4[0],
            "###PROV_NETMASK###": prov_network_ipv4.netmask,
            "###CM_IPV4###": cm_network_ipv4[0],
            "###CM_NETMASK###": cm_network_ipv4.netmask,
            "###CM_START_RANGE###": cm_network_ipv4[5],
            "###CM_END_RANGE###": cm_network_ipv4[120],
            "###CM_GATEWAY###": cm_gateway_ipv4,
            "###CM_BROADCAST###": cm_network_ipv4[-1],
            "###MTA_IP###": mta_network_ipv4[0],
            "###MTA_NETMASK###": mta_network_ipv4.netmask,
            "###MTA_START_RANGE###": mta_network_ipv4[5],
            "###MTA_END_RANGE###": mta_network_ipv4[120],
            "###MTA_GATEWAY###": mta_gateway_ipv4,
            "###MTA_BROADCAST###": mta_network_ipv4[-1],
            "###OPEN_IP###": open_network_ipv4[0],
            "###OPEN_NETMASK###": open_network_ipv4.netmask,
            "###OPEN_START_RANGE###": open_network_ipv4[5],
            "###OPEN_END_RANGE###": open_network_ipv4[120],
            "###OPEN_GATEWAY###": open_gateway_ipv4,
            "###OPEN_BROADCAST###": open_network_ipv4[-1],
            "###WAN_IP###": self._prov_ipv4_address,
        }
        keywords_to_replace.update(self._get_common_keywords_to_replace())
        return self._replace_keywords_from_string(
            _DHCPV4_MASTER_CONFIG, keywords_to_replace
        )

    def _get_dhcpv6_master_config(self) -> str:
        cm_network_ipv6 = ipaddress.IPv6Interface(
            self._config.get(
                "cm_gateway_v6", f"2001:dead:beef:4::cafe/{self._ipv6_prefix}"
            )
        ).network
        cm_network_ipv6_start = self._config.get(
            "cm_network_v6_start", "2001:dead:beef:4::10"
        )
        cm_network_ipv6_end = self._config.get(
            "cm_network_v6_end", "2001:dead:beef:4::100"
        )
        open_network_ipv6 = ipaddress.IPv6Interface(
            self._config.get(
                "open_gateway_v6", f"2001:dead:beef:6::cafe/{self._ipv6_prefix}"
            )
        ).network
        open_network_ipv6_start = ipaddress.IPv6Address(
            self._config.get("open_network_v6_start", "2001:dead:beef:6::10")
        )
        open_network_ipv6_end = ipaddress.IPv6Address(
            self._config.get("open_network_v6_end", "2001:dead:beef:6::100")
        )
        time_server_ipv6 = self._config.get("time_server6", self._prov_ipv6_address)
        keywords_to_replace = {
            "###PROV_IPV6###": self._prov_ipv6_address,
            "###TIME_IPV6###": time_server_ipv6,
            "###PROV_NW_IPV6###": self._prov_ipv6_network,
            "###CM_NETWORK_V6###": cm_network_ipv6,
            "###CM_NETWORK_V6_START###": cm_network_ipv6_start,
            "###CM_NETWORK_V6_END###": cm_network_ipv6_end,
            "###OPEN_NETWORK_V6###": open_network_ipv6,
            "###OPEN_NETWORK_V6_START###": open_network_ipv6_start,
            "###OPEN_NETWORK_V6_END###": open_network_ipv6_end,
            # Increment IP by 200 hosts
            "###OPEN_NETWORK_HOST_V6_START###": open_network_ipv6_start + 256 * 2,
            "###OPEN_NETWORK_HOST_V6_END###": open_network_ipv6_end + 256 * 2,
            # keep last ten /56 prefix in erouter pool. for unknown hosts
            "###EROUTER_NET_START###": self._erouter_ipv6_network_list[
                -10
            ].network_address,
            "###EROUTER_NET_END###": self._erouter_ipv6_network_list[
                -1
            ].network_address,
            # pylint: disable=protected-access
            "###EROUTER_PREFIX###": self._erouter_ipv6_network_list[
                -1
            ]._prefixlen,  # type: ignore
        }
        keywords_to_replace.update(self._get_common_keywords_to_replace())
        dhcp_ipv6_master_config = _DHCPV6_MASTER_CONFIG
        if cm_network_ipv6 != open_network_ipv6:
            dhcp_ipv6_master_config += "  }\n  subnet6 ###OPEN_NETWORK_V6### {\n"
        dhcp_ipv6_master_config += _DHCPV6_MASTER_OPEN_NW_CONFIG
        return self._replace_keywords_from_string(
            dhcp_ipv6_master_config, keywords_to_replace
        )

    def _get_dhcp_cable_modem_config(
        self, cm_mac: str, bootfile_path: str, tftp_server: str, is_dhcpv6: bool
    ) -> str:
        default_lease_time = 604800
        erouter_fixed_ipv6_start = ipaddress.IPv6Interface(
            self._config.get("erouter_fixed_ip_start")
        )
        erouter_mac = get_nth_mac_address(cm_mac, 2)
        station_no = int(self._cmdline_args.board_name.split("-")[-1])
        keywords_to_replace = {
            "###PROV_IPV4###": self._prov_ipv4_address,
            "###PROV_IPV6###": self._prov_ipv6_address,
            "###CM_MAC_ADDRESS###": cm_mac,
            "###CM_BOOTFILE_PATH###": bootfile_path,
            "###TFTP_SERVER_IP###": tftp_server,
            "###EROUTER_MAC_ADDRESS###": erouter_mac,
            "###DEFAULT_LEASE_TIME###": default_lease_time,
            "###MAX_LEASE_TIME###": default_lease_time,
            "###FIXED_PREFIX_IPV6###": self._erouter_ipv6_network_list[station_no],
            "###FIXED_ADDRESS_IPV6###": erouter_fixed_ipv6_start.ip + station_no,
        }
        keywords_to_replace.update(self._get_common_keywords_to_replace())
        return self._replace_keywords_from_string(
            _DHCPV6_CABLE_MODEM_CONFIG if is_dhcpv6 else _DHCPV4_CABLE_MODEM_CONFIG,
            keywords_to_replace,
        )

    def _update_dhcp_config(
        self, cm_mac: str, tftp_server: str, cm_bootfile: str, is_dhcpv6: bool
    ) -> None:
        if not is_dhcpv6:
            dhcp_config_path = "/etc/dhcp/dhcpd.conf"
            master_config = self._get_dhcpv4_master_config()
        else:
            dhcp_config_path = "/etc/dhcp/dhcpd6.conf"
            master_config = self._get_dhcpv6_master_config()
        board_name = self._cmdline_args.board_name
        cm_config_path = f"{dhcp_config_path}.{board_name}"
        master_config_path = f"{dhcp_config_path}-{board_name}.master"
        self._create_dhcp_config_file(master_config, master_config_path)
        dhcp_cm_config = self._get_dhcp_cable_modem_config(
            cm_mac, cm_bootfile, tftp_server, is_dhcpv6
        )
        self._create_dhcp_config_file(dhcp_cm_config, cm_config_path)
        self._console.execute_command(
            f"cat {dhcp_config_path}.* >> {master_config_path}"
        )
        self._console.execute_command(f"mv {master_config_path} {dhcp_config_path}")

    def provision_cable_modem(
        self, cm_mac: str, cm_bootfile: str, tftp_ipv4_addr: str, tftp_ipv6_addr: str
    ) -> None:
        """Provision cable modem with given mac address.

        :param cm_mac: cable modem mac address
        :param cm_bootfile: cable modem boot file path
        :param tftp_ipv4_addr: tftp server IPv4 address
        :param tftp_ipv6_addr: tftp server IPv6 address
        """
        lock_file = "/etc/init.d/isc-dhcp-server.lock"
        try:
            self._acquire_device_file_lock(lock_file)
            self._update_dhcp_config(cm_mac, tftp_ipv4_addr, cm_bootfile, False)
            self._update_dhcp_config(cm_mac, tftp_ipv6_addr, cm_bootfile, True)
            self._restart_dhcp_service()
        finally:
            self._release_device_file_lock(lock_file)

    def _restart_dhcp_service(self) -> None:
        dhcp_service_path = "/etc/init.d/isc-dhcp-server"
        self._console.execute_command("ps auxwww | grep dhcpd")
        self._console.execute_command(f"{dhcp_service_path} stop")
        self._console.execute_command("killall -15 dhcpd")
        success_message = "Stopped DHCP service."
        num_processes = "ps aux | grep -v grep | grep dhcpd | wc -l"
        command = f"[ $({num_processes}) == 0 ] && echo {success_message}"
        output = self._console.execute_command(command)
        if success_message not in output:
            raise ConfigurationFailure("Failed to stop DHCP service.")
        self._console.execute_command("rm -f /run/dhcpd*.pid")
        self._console.execute_command(f"{dhcp_service_path} start")
        success_message = "DHCP Restarted successfully."
        command = f"[ $({num_processes}) == 2 ] && echo {success_message}"
        output = self._console.execute_command(command)
        if success_message not in output:
            _LOGGER.error("Failed to restart DHCP service.")
            self._console.execute_command("tail /var/log/syslog -n 100")
            self._console.execute_command("cat /etc/dhcp/dhcpd.conf")
            self._console.execute_command("cat /etc/dhcp/dhcpd6.conf")
            raise ConfigurationFailure("Failed to apply DHCP config.")

    def _acquire_device_file_lock(
        self, lock_file_path: str, timeout: int = 200, file_handle: int = 9
    ) -> None:
        """Acquire file lock on the device.

        :param lock_file_path: lock file path
        :param timeout: timeout in seconds. defaults to 200.
        :param file_handle: lock file handle number. defaults to 9.
        :raises FileLockTimeout: when failed to acquire lock within timeout
        """
        self._console.execute_command(f"exec {file_handle}>{lock_file_path}")
        self._console.sendline(f"flock -x {file_handle}")
        if not self._console.expect(
            [pexpect.TIMEOUT] + self._shell_prompt, timeout=timeout
        ):
            raise FileLockTimeout(f"Failed to acquire lock on file {lock_file_path}")

    def _release_device_file_lock(
        self, lock_file_path: str, file_handle: int = 9
    ) -> None:
        """Release file lock on the device.

        :param lock_file_path: lock file path
        :param file_handle: lock file handle number. defaults to 9.
        """
        self._console.execute_command(f"flock -u {file_handle}")
        self._console.execute_command(f"rm {lock_file_path}")

    def _create_dhcp_config_file(self, config: str, config_path: str) -> None:
        """Create DHCP config on the server.

        :param config: config file content
        :param destination_path: config file path
        """
        self._console.sendline(f"cat > {config_path} << EOF\n{config}\nEOF")
        self._console.expect(self._shell_prompt)
