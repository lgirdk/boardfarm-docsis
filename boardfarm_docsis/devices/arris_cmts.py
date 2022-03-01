# Copyright (c) 2018
#
# All rights reserved.
#
# This file is distributed under the Clear BSD license.
# The full text can be found in LICENSE in the root directory.
import ipaddress
import logging
import re
import sys
from ipaddress import IPv4Address, IPv6Address
from typing import Any, Dict, List, Optional

import netaddr
import pexpect
from boardfarm.devices import connection_decider
from boardfarm.lib.regexlib import AllValidIpv6AddressesRegex, ValidIpv4AddressRegex

from boardfarm_docsis.devices.base_devices.cmts_template import CmtsTemplate

logger = logging.getLogger("bft")


class ArrisCMTS(CmtsTemplate):
    """Connects to and configures a ARRIS CMTS"""

    prompt = ["arris(.*)>", "arris(.*)#", r"arris\(.*\)> ", r"arris\(.*\)# "]
    model = "arris_cmts"

    def __init__(self, *args, **kwargs) -> None:
        """Constructor method"""
        # self.before is set to empty str to avoid the pylint unsupported-membership-test
        self.before = ""
        super().__init__(*args, **kwargs)
        self.conn_cmd = kwargs.get("conn_cmd", None)
        self.connection_type = kwargs.get("connection_type", "local_serial")
        self.username = kwargs.get("username", "boardfarm")
        self.password = kwargs.get("password", "boardfarm")
        self.password_admin = kwargs.get("password_admin", "boardfarm")
        self.ssh_password = kwargs.get("ssh_password", "boardfarm")
        self.mac_domain = kwargs.get("mac_domain", None)
        self.channel_bonding = kwargs.get("channel_bonding", 32)  # 24x8 : total 32
        self.connlock = None
        if self.conn_cmd is None:
            # TODO: try to parse from ipaddr, etc
            raise Exception("No command specified to connect to Arris CMTS")
        self.name = kwargs.get("name", self.model)

    @CmtsTemplate.connect_and_run
    def interact(self, escape_character=None, input_filter=None, output_filter=None):
        """To open interact session"""
        super().interact()

    def __str__(self):
        txt = [
            f"name: {self.name}",
            f"command: {self.conn_cmd}",
            f"class: {type(self).__name__}",
        ]
        return "\n".join(txt)

    def connect(self) -> None:
        """This method is used to connect cmts, login to the cmts based on the connection type available
        :raises Exception: Unable to get prompt on ARRIS device
        """
        self.connection = connection_decider.connection(
            self.connection_type,
            device=self,
            conn_cmd=self.conn_cmd,
            ssh_password=self.ssh_password,
        )
        self.connection.connect()
        try:
            try:
                self.expect_exact("Escape character is '^]'.", timeout=5)
            except Exception:
                pass
            self.sendline()
            idx = self.expect(["\r\nLogin:", pexpect.TIMEOUT] + self.prompt, timeout=10)
            if 0 == idx:
                self.sendline(self.username)
                self.expect("assword:")
                self.sendline(self.password)
                self.expect(self.prompt)
            elif idx > 1:
                # if we get a prompt we have probably ssh to the device
                pass
            else:
                # Over telnet we come in at the right prompt
                # over serial we could have a double login
                # not yet implemented
                raise Exception("Failed to connect to Arris via telnet")
            self.sendline("enable")
            if 0 == self.expect(["Password:"] + self.prompt):
                self.sendline(self.password_admin)
                self.expect(self.prompt)
            self.sendline("config")
            self.expect(
                "Enter configuration commands, one per line. End with exit or quit or CTRL Z"
            )
            self.expect(self.prompt)
            self.sendline("no pagination")
            self.expect(self.prompt)
            self.logfile_read = sys.stdout
            return
        except Exception:
            self.close()
            self.pid = None
            raise Exception("Unable to get prompt on Arris device")

    def logout(self) -> None:
        """Logout of the CMTS device"""
        try:
            self.sendline("exit")
            self.sendline("exit")
        except Exception:
            self.close()

    def _is_cm_online(
        self,
        ignore_bpi: bool = False,
        ignore_partial: bool = False,
        ignore_cpe: bool = False,
    ) -> bool:
        """Unittest helper invoked by is_cm_online
        Returns True if the CM status is operational
        see is_cm_online(...)
        """
        b = self.check_output(f"show cable modem {self.board_wan_mac} detail")
        if not re.search(r"State=(Operational|Online-d)", b):
            return False
        if ignore_bpi is False and not re.search(r"Privacy=Ready((\s){1,})Ver=BPI", b):
            return False
        if ignore_partial is False and self._check_PartialService(self.board_wan_mac):
            logger.debug("Cable modem in partial service")
            return False
        return ignore_cpe is not False or not re.search(r"State=Online-d", b)

    @CmtsTemplate.connect_and_run
    def is_cm_online(
        self,
        ignore_bpi: bool = False,
        ignore_partial: bool = False,
        ignore_cpe: bool = False,
    ) -> bool:
        """Returns True if the CM status is operational
        :param ignore_bpi: returns True even when BPI is disabled
        :type ignore_bpi: boolean
        :param ignore_partial: returns True even when the CM is in partial service
        :type ignore_partial: boolean
        :param ignore_cpe: returns True even when LAN<->WAN forwarding is disabled
        :type ignore_cpe: boolean
        :return: True if the CM is operational, False otherwise
        :rtype: boolean
        """
        return self._is_cm_online(
            ignore_bpi=ignore_bpi, ignore_partial=ignore_partial, ignore_cpe=ignore_cpe
        )

    def _check_online(self, cm_mac: str) -> bool:
        """Internal fuction to Check the CM status from CMTS function checks the encrytion mode and returns True if online
        It is not decarated by CmtsTemplate.connect_and_run
        :param cm_mac: mac address of the CM
        :type cm_mac: string
        :return: True if the CM is operational else actual status on cmts
        :rtype: string / boolean
        """
        cm_mac = self.get_cm_mac_cmts_format(cm_mac)
        self.sendline("no pagination")
        self.expect_prompt()
        self.sendline(f"show cable modem | include {cm_mac}")
        self.expect_prompt()
        if "Operational" in self.before:
            return True
        else:
            try:
                # Regex matches any status after digit (e.g 24x8) up until first space
                r = re.findall(r"(?!(\d+)\s+)([A-Z])\w+[^\s]+", self.before)[0].strip()
            except Exception:
                r = "Offline"
        return r

    def check_online(self, cm_mac: str) -> bool:
        """Check the CM status from CMTS function checks the encrytion mode and returns True if online
        :param cm_mac: mac address of the CM
        :type cm_mac: string
        :return: True if the CM is operational else actual status on cmts
        :rtype: string / boolean
        """
        return self._check_online(cm_mac)

    @CmtsTemplate.connect_and_run
    def _clear_offline(self, cm_mac: str) -> None:
        """Clear the CM entry from cmts which is offline -clear cable modem <mac> delete
        :param cm_mac: mac address of the CM
        :type cm_mac: string
        """
        cm_mac = self.get_cm_mac_cmts_format(cm_mac)
        self.sendline("exit")
        self.expect(self.prompt)
        self.sendline(f"clear cable modem delete {cm_mac}")
        self.expect(self.prompt)
        self.sendline("configure")
        self.expect(self.prompt)

    def clear_offline(self, cm_mac: str) -> None:
        """Clear the CM entry from cmts which is offline -clear cable modem <mac> delete
        :param cm_mac: mac address of the CM
        :type cm_mac: string
        """
        self._clear_offline(cm_mac)

    def clear_cm_reset(self, cm_mac: str) -> None:
        """Reset the CM from cmts using cli -clear cable modem <cm_mac> reset
        :param cm_mac: mac address of the CM
        :type cm_mac: str
        """
        self._clear_cm_reset(cm_mac)

    @CmtsTemplate.connect_and_run
    def _clear_cm_reset(self, cm_mac: str) -> None:
        """Reset the CM from cmts using cli -clear cable modem <mac> reset
        :param cm_mac: mac address of the CM
        :type cm_mac: string
        """
        cm_mac = self.get_cm_mac_cmts_format(cm_mac)
        self.sendline("exit")
        self.expect(self.prompt)
        """ NB: this command does not reboot the CM, but forces it to reinitialise """
        self.sendline(f"clear cable modem delete {cm_mac}")
        self.expect(self.prompt)
        self.sendline("configure")
        self.expect(self.prompt)
        self.expect(pexpect.TIMEOUT, timeout=5)
        online_state = self._check_online(cm_mac)
        if online_state is True:
            logger.debug("CM is still online after 5 seconds.")
        else:
            logger.info("CM reset is initiated.")

    @CmtsTemplate.connect_and_run
    def _get_mtaip(self, cm_mac: str, mta_mac: str = None) -> Optional[str]:
        """Get the MTA IP from CMTS
        :param cm_mac: mac address of the CM
        :type cm_mac: string
        :param mta_mac: mta mac address
        :type mta_mac: string
        :return: MTA ip address or "None" if ip not found
        :rtype: string
        """
        cm_mac = self.get_cm_mac_cmts_format(cm_mac)
        self.sendline(f"show cable modem {cm_mac} detail | include MTA")
        self.expect(r"CPE\(MTA\)\s+.*IPv4=(" + ValidIpv4AddressRegex + ")\r\n")
        result = self.match.group(1)
        output = result if self.match is not None else "None"
        self.expect(self.prompt)
        return output

    def get_mtaip(self, cm_mac: str, mta_mac: str = None) -> Optional[str]:
        """Get the MTA IP from CMTS
        :param cm_mac: mac address of the CM
        :type cm_mac: string
        :param mtamac: mta mac address
        :type mtamac: string
        :return: MTA ip address or "None" if ip not found
        :rtype: string
        """
        return self._get_mtaip(cm_mac=cm_mac, mta_mac=mta_mac)

    @CmtsTemplate.connect_and_run
    def get_ip_from_regexp(self, cm_mac: str, ip_regexpr: str) -> Optional[str]:
        """Gets an ip address according to a regexpr (helper function)
        :param cm_mac: cable modem mac address
        :type cm_mac: string
        :param ip_regexpr: regular expression for ip
        :type ip_regexpr: string
        :return: ip addr (ipv4/6 according to regexpr) or None if not found
        :rtype: string
        """
        cm_mac = self.get_cm_mac_cmts_format(cm_mac)
        self.sendline(f"show cable modem | include {cm_mac}")
        if (
            self.expect(
                [cm_mac + r"\s+(" + ip_regexpr + ")", pexpect.TIMEOUT], timeout=2
            )
            == 1
        ):
            output = "None"
        else:
            result = self.match.group(1)
            output = result if self.match is not None else "None"
        self.expect(self.prompt)
        return output

    def get_cmip(self, cm_mac: str) -> Optional[str]:
        """Get the IP of the Cable modem from CMTS
        :param cm_mac: mac address of the CM
        :type cm_mac: string
        :return: ip address of cable modem or "None"
        :rtype: string
        """
        return self.get_ip_from_regexp(cm_mac, ValidIpv4AddressRegex)

    def get_cmipv6(self, cm_mac: str) -> Optional[str]:
        """Get IPv6 address of the Cable modem from CMTS
        :param cm_mac: mac address of the CM
        :type cm_mac: string
        :return: ipv6 address(str) of cable modem or "None"
        :rtype: string
        """
        return self.get_ip_from_regexp(cm_mac, AllValidIpv6AddressesRegex)

    @CmtsTemplate.connect_and_run
    def get_cm_mac_domain(self, cm_mac: str) -> Optional[str]:
        """Get the Mac-domain of Cable modem
        :param cm_mac: mac address of the CM
        :type cm_mac: string
        :return: mac_domain of the particular cable modem
        :rtype: string
        """
        mac_domain = None
        self.sendline(f"show cable modem {cm_mac} detail | include Cable-Mac=")
        if self.expect(["Cable-Mac= ([0-9]{1,3}),", pexpect.TIMEOUT], timeout=5) == 0:
            mac_domain = self.match.group(1)
        self.expect(self.prompt)
        return mac_domain

    @CmtsTemplate.connect_and_run
    def _check_PartialService(self, cm_mac: str) -> bool:
        """Helper function for check_PartialService"""
        cm_mac = self.get_cm_mac_cmts_format(cm_mac)
        self.sendline(f"show cable modem {cm_mac}")
        self.expect(self.prompt)
        return bool(1) if "impaired" in self.before else bool(0)

    def check_partial_service(self, cm_mac: str) -> bool:
        """Check the cable modem is in partial service
        :param cm_mac: mac address of the CM
        :type cm_mac: string
        :return: 1 if is true else return the value as 0
        :rtype: int
        """
        return self._check_PartialService(cm_mac)

    def DUT_chnl_lock(self, cm_mac: str) -> List[int]:
        """Check the CM channel locks based on cmts type
        :param cm_mac: mac address of the CM
        :type cm_mac: string
        :returns: Locked channels of upstream and downstream
        :rtype: list
        """
        cm_mac = self.get_cm_mac_cmts_format(cm_mac)
        self.sendline(f"show cable modem  {cm_mac} bonded-impaired")
        self.expect(self.prompt)
        bonded_impared_status = self.before
        if "No CMs were found" in bonded_impared_status:
            self.sendline(f"show cable modem  {cm_mac} ")
            self.expect(r"(\d+)x(\d+)")
            downstream = int(self.match.group(1))
            upstream = int(self.match.group(2))
            self.expect(self.prompt)
        else:
            downstream = int(
                re.findall(r"(\d+x\d+)", bonded_impared_status)[1].split("x")[0]
            )
            upstream = int(
                re.findall(r"(\d+x\d+)", bonded_impared_status)[1].split("x")[1]
            )
        return [upstream, downstream]

    @CmtsTemplate.connect_and_run
    def save_running_config_to_local(self, filename: str) -> None:
        """save the running config to startup"""
        self.sendline("no pagination")
        self.expect(self.prompt)
        # show running-config will display the current running config file of CMTS
        self.sendline("show running-config")
        self.expect(r"arrisc4\(config\)\#")
        with open(filename, "w") as f:
            f.write(self.before)
            f.write(self.after)

    @CmtsTemplate.connect_and_run
    def save_running_to_startup_config(self) -> None:
        """Copy running config to local machine"""
        self.sendline("exit")
        self.expect(self.prompt)
        self.sendline("copy running-config startup-config")
        self.expect(self.prompt)
        self.sendline("config")
        self.expect(self.prompt)

    @CmtsTemplate.connect_and_run
    def get_qam_module(self) -> str:
        """Get the module of the qam
        :return: Module of the qam
        :rtype: string
        """
        self.sendline("show linecard status | include DMM/DMM")
        self.expect(self.prompt)
        return self.before.split("\n", 1)[1]

    @CmtsTemplate.connect_and_run
    def get_ups_module(self) -> list:
        """Get the upstream module of the qam
        :return: list of module number of the qam
        :rtype: list
        """
        self.sendline("show linecard status | include CAM/CAM")
        self.expect(self.prompt)
        return list(map(int, re.findall(r"(\d+)    CAM ", self.before)))

    @CmtsTemplate.connect_and_run
    def set_iface_ipaddr(self, iface: str, ipaddr: IPv4Address) -> None:
        """This function is to set an ip address to an interface on cmts
        :param iface: interface name ,
        :type iface: string
        :param ipaddr: <ip></><subnet> using 24 as default if subnet is not provided.
        :type ipaddr: string
        """
        self.sendline(f"interface {iface}")
        self.expect(self.prompt)
        self.sendline(f"ip address {str(ipaddr)}/24")
        self.expect(self.prompt)
        self.sendline("no shutdown")
        self.expect(self.prompt)
        self.sendline("exit")
        self.expect(self.prompt)

    @CmtsTemplate.connect_and_run
    def set_iface_ipv6addr(self, iface: str, ipaddr: IPv6Address) -> None:
        """Configure ipv6 address
        :param iface: interface name
        :type iface: string
        :param ipaddr: ipaddress to configure
        :type ipaddr: string
        """
        self.sendline(f"interface {iface}")
        self.expect(self.prompt)
        self.sendline(f"ipv6 address {str(ipaddr)}")
        self.expect(self.prompt)
        self.sendline("no shutdown")
        self.expect(self.prompt)
        self.sendline("exit")
        self.expect(self.prompt)

    @CmtsTemplate.connect_and_run
    def unset_iface_ipaddr(self, iface: str) -> None:
        """This function is to unset an ipv4 address of an interface on cmts
        :param iface: interface name
        :type iface: string
        """
        self.sendline(f"interface {iface}")
        self.expect(self.prompt)
        self.sendline("no ip address")
        self.expect(self.prompt)
        self.sendline("exit")
        self.expect(self.prompt)

    @CmtsTemplate.connect_and_run
    def unset_iface_ipv6addr(self, iface: str) -> None:
        """This function is to unset an ipv6 address of an interface on cmts
        :param iface: interface name.
        :type iface: string
        """
        self.sendline(f"interface {iface}")
        self.expect(self.prompt)
        self.sendline("no ipv6 address")
        self.expect(self.prompt)
        self.sendline("exit")
        self.expect(self.prompt)

    @CmtsTemplate.connect_and_run
    def del_file(self, f: str) -> None:
        """delete file on cmts
        :param f: filename to delete from cmts
        :type f: string
        """
        self.sendline("exit")
        self.expect(self.prompt)
        self.sendline(f"delete {f}")
        self.expect(self.prompt)

    @CmtsTemplate.connect_and_run
    def check_docsis_mac_ip_provisioning_mode(self, index: str) -> str:
        """
        Get the provisioning mode of the cable modem from CMTS
        :param index: mac domain of the cable modem
        :type index: string
        :return: mode of the provisioning(ipv4, ipv6, dual-stack, apm)
        :rtype: string
        """
        self.sendline(
            f"show running-config interface cable-mac {index} | include cm-ip-prov-mode"
        )
        self.expect(self.prompt)
        result = self.before.split("\n")[1].split(" ")[-1]
        if "ipv4" in result.lower():
            result = "ipv4"
        elif "dual" in result.lower():
            result = "dual-stack"
        elif "ipv6" in result.lower():
            result = "ipv6"
        elif "apm" in result.lower():
            result = "apm"
        return result

    @CmtsTemplate.connect_and_run
    def modify_docsis_mac_ip_provisioning_mode(
        self, index: str, ip_pvmode: str = "dual-stack"
    ) -> None:
        """Change the ip provsioning mode
        :param index: mac domain of the cable modem configured
        :type index: string
        :param ip_pvmode: provisioning mode can ipv4, ipv6 or 'dual-stack', defaults to 'dual-stack'
        :type ip_pvmode: string
        """
        if "dual-stack" in ip_pvmode.lower() and "c4" in self._get_cmts_type():
            logger.error(
                "dual-stack ip provisioning modem is not supported on Chassis Type : C4 please choose apm"
            )
            return
        self.sendline(f"interface cable-mac {index}")
        self.expect(self.prompt)
        self.sendline(f"cable cm-ip-prov-mode {ip_pvmode}")
        self.expect(self.prompt)
        self.sendline("exit")
        self.expect(self.prompt)
        self.sendline(
            f"show running-config interface cable-mac {index} | include cm-ip-prov-mode"
        )
        self.expect(self.prompt)
        check_docsis_mac_ip_provisioning_mode = (
            self.check_docsis_mac_ip_provisioning_mode(index)
        )
        if check_docsis_mac_ip_provisioning_mode in ip_pvmode:
            logger.info("The ip provision mode is successfully set.")
        else:
            logger.error("An error occured while setting the ip provision mode.")

    @CmtsTemplate.connect_and_run
    def add_route(self, ipaddr: str, gw: str) -> None:
        """This function is to add route
        :param ipaddr: <network ip></><subnet ip> take subnet 24 if not provided,
        :param ipaddr: string
        :param gw: gateway ip.
        :type gw: string
        """
        self.sendline(f"route net {ipaddr} /24 gw {gw}")
        self.expect(self.prompt)
        if "error" in self.before.lower():
            logger.error("An error occured while adding the route.")
        self.sendline("show ip route")
        self.expect(self.prompt)
        if gw in self.before:
            logger.info("The route is available on cmts.")
        else:
            logger.info("The route is not available on cmts.")

    @CmtsTemplate.connect_and_run
    def add_route6(self, net: str, gw: str) -> None:
        """This function is to add route6
        :param net: <network ip></><subnet ip> take subnet 24 if not provided,
        :param net: string
        :param gw: gateway ip.
        :type gw: string
        """
        self.sendline(f"ipv6 route {net} {gw}")
        self.expect(self.prompt)
        if "error" in self.before.lower():
            logger.error("An error occured while adding the route.")
        self.sendline("show ipv6 route")
        self.expect(self.prompt)
        if str(ipaddress.IPv6Address(str(gw))).lower() in self.before.lower():
            logger.info("The route is available on cmts.")
        else:
            logger.info("The route is not available on cmts.")

    @CmtsTemplate.connect_and_run
    def del_route(self, ipaddr: str, gw: str) -> None:
        """This function is to delete route
        :param ipaddr: <network ip></><subnet ip> take subnet 24 if not provided
        :type ipaddr: string
        :param gw: gateway ip
        :type gw: string
        """
        self.sendline(f"no route net {ipaddr} /24 gw {gw}")
        self.expect(self.prompt)
        if "error" in self.before.lower():
            logger.error("An error occured while deleting the route.")
        self.expect(pexpect.TIMEOUT, timeout=10)
        self.sendline("show ip route")
        self.expect(self.prompt)
        if gw in self.before:
            logger.debug("The route is still available on cmts.")
        else:
            logger.info("The route is not available on cmts.")

    @CmtsTemplate.connect_and_run
    def del_route6(self, net: str, gw: str) -> None:
        """This function is to delete ipv6 route
        :param net: <network ip></><subnet ip> take subnet 24 if not provided,
        :type net: string
        :param gw: gateway ip
        :type gw: string
        """
        self.sendline(f"no ipv6 route {net} {gw}")
        self.expect(self.prompt)
        if "error" in self.before.lower():
            logger.error("An error occured while deleting the route.")
        self.sendline("show ipv6 route")
        self.expect(self.prompt)
        if (
            str(ipaddress.ip_address(str(gw)).compressed).lower() in self.before.lower()
            or gw.lower() in self.before.lower()
        ):
            logger.debug("The route is still available on cmts.")
        else:
            logger.debug("The route is not available on cmts.")

    @CmtsTemplate.connect_and_run
    def add_ip_bundle(
        self,
        index: str,
        helper_ip: str,
        ipaddr: str,
        secondary_ips: Optional[List[Any]] = None,
    ) -> None:
        """This function is to add ip bundle to a cable mac
        :param index: cable mac index,
        :type index: string
        :param helper_ip: helper ip to be used,
        :type helper_ip: string
        :param ipaddr: actual ip to be assiged to cable mac in the format  <ip></><subnet> subnet defaut taken as 24 if not provided,
        :type ipaddr: string
        :param secondary_ips: list of seconday ips  in the format  <ip></><subnet> subnet defaut taken as 24 if not provided, defaults to empty list []
        :type secondary_ips: list
        """
        if secondary_ips is None:
            secondary_ips = []
        self.sendline(f"interface cable-mac {index}")
        self.expect(self.prompt)
        self.sendline(f"ip address {ipaddr} /24")
        self.expect(self.prompt)
        for ip2 in secondary_ips:
            self.sendline(f"ip address {ip2} /24 secondary")
            self.expect(self.prompt)
        self.sendline(f"cable helper-address {helper_ip} cable-modem")
        self.expect(self.prompt)
        self.sendline(f"cable helper-address {helper_ip} mta")
        self.expect(self.prompt)
        self.sendline(f"cable helper-address {helper_ip} host")
        self.expect(self.prompt)
        self.sendline("exit")
        self.expect(self.prompt)
        self.sendline(
            f"show running-config interface cable-mac {index} | include ip address"
        )
        self.expect(self.prompt)
        if str(ipaddr) in self.before:
            logger.info("The ip bundle is successfully set.")
        else:
            logger.error("An error occured while setting the ip bundle.")

    @CmtsTemplate.connect_and_run
    def add_ipv6_bundle_addrs(
        self,
        index: str,
        helper_ip: str,
        ipaddr: str,
        secondary_ips: Optional[List[str]] = None,
    ) -> None:
        """This function is to add ipv6 bundle to a cable mac.
        :param index: cable mac index,
        :type index: string
        :param helper_ip: helper ip to be used,
        :type helper_ip: string
        :param ip: actual ip to be assiged to cable mac in the format  <ip></><subnet> subnet defaut taken as 24 if not provided,
        :type ip: string
        :param secondary_ips: list of seconday ips  in the format  <ip></><subnet> subnet defaut taken as 24 if not provided.
        :type secondary_ips: list
        """
        if secondary_ips is None:
            secondary_ips = []
        self.sendline(f"interface ip-bundle {index}")
        self.expect(self.prompt)
        self.sendline(f"ipv6 address {ipaddr}")
        self.expect(self.prompt)
        for ip2 in secondary_ips:
            self.sendline(f"ipv6 address {ip2} secondary")
            self.expect(self.prompt)
        self.sendline(f"cable helper-ipv6-address {helper_ip}")
        self.expect(self.prompt)
        self.sendline("exit")
        self.expect(self.prompt)
        self.sendline(f'show interface ip-bundle {index} | include "ipv6 address"')
        self.expect(self.prompt)
        if str(ipaddress.ip_address(str(ipaddr[:-3])).compressed) in self.before:
            logger.info("The ipv6 bundle is successfully set.")
        else:
            logger.error("An error occured while setting the ipv6 bundle.")

    @CmtsTemplate.connect_and_run
    def set_iface_qam(
        self, index: str, sub: str, annex: str, interleave: str, power: str
    ) -> None:
        """Configure the qam interface with annex, interleave and power
        :param index: index number of the qam
        :type index: string
        :param sub: qam slot number
        :type sub: string
        :param annex: annex a or b or c to configure
        :type annex: string
        :param interleave: interleave depth to configure
        :type interleave: string
        :param power: power level
        :type power: string
        """
        self.sendline(f"interface cable-downstream {index}/{sub}")
        self.expect(self.prompt)
        self.sendline(f"cable power {power}")
        self.expect(self.prompt)
        self.sendline("no shutdown")
        self.expect(self.prompt)
        self.sendline("exit")
        self.expect(self.prompt)

    @CmtsTemplate.connect_and_run
    def wait_for_ready(self) -> None:
        """Check the cmts status"""
        max_iteration = 5
        self.sendline("show linecard status")
        while self.expect(["Down | OOS"] + self.prompt) == 0 and max_iteration > 0:
            max_iteration -= 1
            self.expect(self.prompt)
            self.expect(pexpect.TIMEOUT, timeout=5)
            self.sendline("show linecard status")

    @CmtsTemplate.connect_and_run
    def set_iface_qam_freq(self, index: str, sub: str, channel: str, freq: str) -> None:
        """Configure the qam interface with channel and frequency
        :param index: index number of the qam
        :type index: string
        :param sub: qam slot number
        :type sub: string
        :param channel: channel number
        :type channel: string
        :param freq: frequency for the channel
        :type freq: string
        """
        self.sendline(f"interface cable-downstream {index}/{sub}")
        self.expect(self.prompt)
        self.sendline(f"cable frequency {freq}")
        self.expect(self.prompt)
        self.sendline("no shutdown")
        self.expect(self.prompt)
        self.sendline("exit")
        self.expect(self.prompt)

    @CmtsTemplate.connect_and_run
    def add_service_group(
        self,
        index: str,
        qam_idx: str,
        qam_sub: str,
        qam_channels: str,
        ups_idx: str,
        ups_channels: str,
    ) -> None:
        """Add a service group
        :param index: service group number
        :type index: string
        :param qam_idx: slot number of the qam
        :type qam_idx: string
        :param qam_sub: port number of the qam
        :type qam_sub: string
        :param qam_channels: channel number of the qam
        :type qam_channels: string
        :param ups_idx: upstream slot number
        :type ups_idx: string
        :param ups_channels: channel number of the upstream
        :type ups_channels: string
        """
        logger.debug(
            "Service group is auto configured in ARRIS once mac domain is created."
        )

    @CmtsTemplate.connect_and_run
    def mirror_traffic(self, macaddr: str = "") -> None:
        """Send the mirror traffic
        :param macaddr: mac address of the device if avaliable, defaults to empty string ""
        :type macaddr: string
        """
        logger.error(
            "Mirror traffic feature is not supported in ARRIS unless we use lawful intercept functionality."
        )

    @CmtsTemplate.connect_and_run
    def unmirror_traffic(self) -> None:
        """stop mirroring the traffic"""
        logger.error(
            "Unmirror traffic feature is not supported in ARRIS unless we use lawful intercept functionality."
        )

    def is_cm_bridged(self, mac: str, offset: int = 2) -> bool:
        """This function is to check if the modem is in bridge mode
        :param mac: Mac address of the modem,
        :param offset: ignored in casa specific to arris, defaults to 2
        :return: Returns True if the modem is bridged else False.
        :rtype: boolean
        """
        mac = self.get_cm_mac_cmts_format(mac)
        self.sendline(f"show cable modem {mac} detail")
        self.expect(self.prompt)
        mac = netaddr.EUI(mac)
        ertr_mac = netaddr.EUI(int(mac) + offset)
        ertr_mac.dialect = netaddr.mac_cisco
        return str(ertr_mac) not in self.before

    def get_ertr_ipv4(self, mac: str, offset: int = 2) -> Optional[str]:
        """Getting erouter ipv4 from CMTS
        :param mac: mac address of the cable modem
        :type mac: string
        :param offset: ignored in casa specific to arris, defaults to 2
        :return: returns ipv4 address of erouter else None
        :rtype: string
        """
        mac = self.get_cm_mac_cmts_format(mac)
        self.sendline(f"show cable modem {mac} detail")
        self.expect(self.prompt)
        mac = netaddr.EUI(mac)
        ertr_mac = netaddr.EUI(int(mac) + offset)
        ertr_mac.dialect = netaddr.mac_cisco
        ertr_ipv4 = re.search(f"({ertr_mac}) .*=({ValidIpv4AddressRegex})", self.before)
        if ertr_ipv4:
            return ertr_ipv4.group(2)
        else:
            return None

    def get_ertr_ipv6(self, mac: str, offset: int = 2) -> Optional[str]:
        """Getting erouter ipv6 from CMTS
        :param mac: mac address of the cable modem
        :type mac: string
        :param offset: ignored in casa specific to arris, defaults to 2
        :return: returns ipv6 address of erouter else None
        :rtype: string
        """
        mac = self.get_cm_mac_cmts_format(mac)
        self.sendline(f"show cable modem {mac} detail")
        self.expect(self.prompt)
        mac = netaddr.EUI(mac)
        ertr_mac = netaddr.EUI(int(mac) + offset)
        ertr_mac.dialect = netaddr.mac_cisco
        ertr_ipv6 = re.search(
            f"({ertr_mac}) IPv6=({AllValidIpv6AddressesRegex})", self.before
        )
        if ertr_ipv6:
            return ertr_ipv6.group(2)
        else:
            return None

    @CmtsTemplate.connect_and_run
    def get_center_freq(self, mac_domain=None) -> int:
        """This function is to return the center frequency of cmts
        :param mac_domain: Mac Domain of the cable modem
        :type mac_domain: string
        :return: Returns center frequency configured on the qam
        :rtype: string
        """
        if mac_domain is None:
            mac_domain = self.mac_domain
        assert mac_domain is not None, "get_center_freq() requires mac_domain to be set"
        self.sendline("no pagination")
        self.expect(self.prompt)
        self.sendline("show interface cable downstream")
        self.expect(self.prompt)
        freq_list = []
        for row in self.before.split("\n")[3:]:
            match_grp = re.match(
                r"\d{1,2}/\d{1,2}\s+" + str(mac_domain) + r"\s.*\s(\d{6,10})\s+\w+", row
            )
            if match_grp is not None and match_grp.groups(0)[0] is not None:
                freq_list.append(match_grp.groups(0)[0])
        freq_list_new = map(int, freq_list)
        return int(min(freq_list_new))

    @CmtsTemplate.connect_and_run
    def set_iface_upstream(
        self, ups_idx: str, ups_ch: str, freq: str, width: str, power: str
    ) -> None:
        """Configure the interface for upstream
        :param ups_idx: upstream index number of the interface
        :type ups_idx: string
        :param ups_ch: upstream channel number for the interface
        :type ups_ch: string
        :param freq: frequency to configure the upstream
        :type freq: string
        :param width: width of the qam
        :type width: string
        :param power: power of the qam
        :type power: string
        """
        self.sendline(f"interface cable-upstream {ups_idx}/{ups_ch}")
        self.expect(self.prompt)
        self.sendline(f"cable frequency {freq}")
        self.expect(self.prompt)
        self.sendline(f"cable channel-width {width}")
        self.expect(self.prompt)
        self.sendline(f"cable power-level {power}")
        self.expect(self.prompt)
        self.sendline("cable modulation-profile 64")
        self.expect(self.prompt)
        self.sendline("cable mini-slot-size 2")
        self.sendline("no shutdown")
        self.expect(self.prompt)
        self.sendline("exit")
        self.expect(self.prompt)

    @CmtsTemplate.connect_and_run
    def get_cm_bundle(self, mac_domain: str) -> str:
        """Get the bundle id from cable modem
        :param mac_domain: Mac_domain of the cable modem connected
        :type mac_domain: string
        :return: bundle id
        :rtype: string
        """
        self.sendline(
            "show running-config interface cable-mac %s | include cable-mac [0-9]+.[0-9]+"
            % mac_domain
        )
        index = self.expect(["(interface cable-mac )([0-9]+.[0-9]+)"] + self.prompt)
        if index != 0:
            assert 0, "ERROR:Failed to get the CM bundle id from CMTS"
        bundle = self.match.group(2)
        self.expect(self.prompt)
        return bundle

    def get_cmts_ip_bundle(
        self, cm_mac: Optional[str] = None, gw_ip: Optional[str] = None
    ) -> str:
        """Get CMTS bundle IP
        :param cm_mac: mac address of the CM
        :type cm_mac: string
        :param gw_ip: gateway ip address
        :type gw_ip: string
        :return: returns cmts ip configured on the bundle
        :rtype: string
        """
        mac_domain = self.get_cm_mac_domain(cm_mac)
        self.get_cm_bundle(mac_domain)
        self.sendline(
            f"show running-config interface cable-mac {mac_domain} | include secondary"
        )
        self.expect(self.prompt)
        cmts_ip_match = re.search(f"ip address ({gw_ip}) .* secondary", self.before)
        if gw_ip is None:
            return self.before
        if cmts_ip_match:
            cmts_ip = cmts_ip_match.group(1)
        else:
            assert 0, "ERROR: Failed to get the CMTS bundle IP"
        return cmts_ip

    @CmtsTemplate.connect_and_run
    def reset(self) -> None:
        """Delete the startup config and Reboot the CMTS"""
        self.sendline("erase nvram")
        self.expect(self.prompt)
        self.sendline("reload")
        self.expect(self.prompt)

    @CmtsTemplate.connect_and_run
    def add_service_class(
        self, index, name, max_rate, max_burst, max_tr_burst=None, downstream=False
    ):
        """Add a service class
        :param index: service class number
        :type index: string
        :param name: service name
        :type name: string
        :param max_rate: maximum traffic rate
        :type max_rate: string
        :param max_burst: maximum traffic burst
        :type max_burst: string
        :param max_tr_burst: If anything, defaults to None
        :type max_tr_burst: optional
        :param downstream: True or False, defaults to False
        :type downstream: boolean
        """
        self.sendline(
            "qos-sc name %s max-tr-rate %s max-tr-burst %s max-burst %s"
            % (name, max_rate, max_tr_burst, max_burst)
        )
        self.expect(self.prompt)
        if downstream:
            self.sendline(f"qos-sc name {name} dir 1")
            self.expect(self.prompt)

    @CmtsTemplate.connect_and_run
    def add_iface_docsis_mac(
        self,
        index,
        ip_bundle,
        qam_idx,
        qam_ch,
        ups_idx,
        ups_ch,
        qam_sub=None,
        prov_mode=None,
    ):
        """configure docsis-mac domain
        :param index: docsis mac index
        :type index: string
        :param ip_bundle: bundle id of the cable modem
        :type ip_bundle: string
        :param qam_idx: slot number of the qam to configure
        :type qam_idx: string
        :param qam_ch: qam channel number
        :type qam_ch: string
        :param ups_idx: upstream slot number
        :type ups_idx: string
        :param ups_ch: upstream channel number
        :type ups_ch: string
        :param qam_sub: port number of the qam, defaults to None
        :type qam_sub: string , optional
        :param prov_mode: provisioning mode if any, defaults to None
        :type prov_mode: string, optional
        """
        if "/" not in ip_bundle:
            ip_bundle += "/24"
        ip_bundle = ipaddress.IPv4Interface(str(ip_bundle))
        self.sendline(f"interface cable-mac {index}")
        self.expect(self.prompt)
        self.sendline("no shutdown")
        self.expect(self.prompt)
        self.sendline("cable ranging-interval 2000")
        self.expect(self.prompt)
        self.sendline("cable tftp-enforce")
        self.expect(self.prompt)
        self.sendline("cable dynamic-secret reject")
        self.expect(self.prompt)
        self.sendline(f"cable cm-ip-prov-mode {prov_mode}")
        self.expect(self.prompt)
        self.sendline("cable mcast-fwd-by-dsid no")
        self.expect(self.prompt)
        self.sendline("cable dynamic-rcc")
        self.expect(self.prompt)
        self.sendline("cable downstream-bonding-group dynamic enable")
        self.expect(self.prompt)
        self.sendline("cable mult-tx-chl-mode")
        self.expect(self.prompt)
        self.sendline("cable upstream ranging-poll t4-multiplier")
        self.expect(self.prompt)
        self.sendline("cable privacy mandatory bpi-plus")
        self.expect(self.prompt)
        self.sendline(f"ip address {ip_bundle.ip} {ip_bundle.netmask}")
        self.expect(self.prompt)
        self.sendline("exit")
        self.expect(self.prompt)
        for ch in qam_ch:
            self.sendline(
                f"interface cable-downstream {qam_idx}/{ch} cable cable-mac {index}"
            )
            self.expect(self.prompt)
            self.sendline(f"interface cable-downstream {qam_idx}/{ch} no shutdown")
            self.expect(self.prompt)
        for ch in ups_ch:
            self.sendline(
                f"interface cable-upstream {qam_idx}/{ch} cable cable-mac {index}"
            )
            self.expect(self.prompt)
            self.sendline(f"interface cable-upstream {qam_idx}/{ch} no shutdown")
            self.expect(self.prompt)

    @CmtsTemplate.connect_and_run
    def _get_cmts_type(self) -> str:
        """This function is to get the product type on cmts
        :return: Returns the cmts module type.
        :rtype: string
        """
        self.sendline("show linecard status | include chassis")
        self.expect("Chassis Type:(.*)\r\n")
        result = self.match.group(1)
        output = result if self.match is not None else "None"
        self.expect(self.prompt)
        return output.strip().lower()

    def get_qos_parameter(self, cm_mac: str) -> Dict[str, List[dict]]:
        """To get the qos related parameters of CM
        Example output format : {'DS':  [{'Sfid': '1' ..},
                                         {'Sfid': '2' ..}
                                 'US': [{{'Sfid': '1' ..},
                                  'Maximum Burst': '128000',
                                  'IP ToS Overwrite [AND-msk, OR-mask]':
                                  ['0x00', '0x00'], ...},
                                  {'Sfid': '1' ..}}
        The units for measuring are
        1) Peak rate, Maximum Sustained rate,
           Minimum Reserved rate -- bits/sec
        2) Maximum Burst, Minimum Packet Size -- bytes
        3) Admitted Qos Timeout, Maximum Latency -- seconds
        4) Current Throughput -- [bits/sec, packets/sec]
        :param cm_mac: mac address of the cable modem
        :type cm_mac: string
        :return: containing the qos related parameters.
        :rtype: dictionary
        """
        cm_mac = self.get_cm_mac_cmts_format(cm_mac)
        self.sendline("no pagination")
        self.expect(self.prompt)
        qos_dict: Dict[str, list] = {"US": [], "DS": []}
        self.sendline(f"show cable modem qos {cm_mac} verbose")
        self.expect(self.prompt)
        service_flows = re.split(r"\n\s*\n", self.before)[1:-1]
        strip_units = ["bits/sec", "bytes", "seconds", "packets/sec", "usecs"]
        for service_flow in service_flows:
            service_flow_list = [i for i in service_flow.splitlines() if i]
            qos_dict_flow = {}
            for service in service_flow_list:
                service = service.split(":")
                key, value = (i.strip() for i in service)
                for i in strip_units:
                    value = value.replace(i, "").strip()
                if "scheduling type" in key:
                    qos_dict_flow[key] = value
                elif (
                    "ip tos" not in key.lower()
                    and "current throughput" not in key.lower()
                ):
                    qos_dict_flow[key] = value
                else:
                    qos_dict_flow[key] = [
                        value.split(" ")[0].replace(",", ""),
                        value.split(" ")[1].replace(",", ""),
                    ]
            if bool(qos_dict_flow):
                if "US" in str(qos_dict_flow.get("Direction")):
                    qos_dict["US"].append(qos_dict_flow)
                else:
                    qos_dict["DS"].append(qos_dict_flow)
        return qos_dict

    @CmtsTemplate.connect_and_run
    def ping(
        self,
        ping_ip: str,
        ping_count: int = 4,
        timeout: int = 4,
    ) -> bool:
        """This function to ping the device from cmts
        :param ping_ip: device ip which needs to be verified
        :ping_ip type: string
        :param ping_count: Repeating ping packets, defaults to 3
        :ping_count type: integer
        :param timeout: timeout for the packets, defaults to 10 sec
        :type timeout: integer
        :return: True if ping passed else False
        """
        mode = f"ipv{ipaddress.ip_address(ping_ip).version}"
        basic_ping = (
            f"ping repeat-count {ping_count} timeout {timeout}"
            if mode == "ipv4"
            else "ping ipv6"
        )
        self.check_output("end")
        self.sendline(f"{basic_ping} {ping_ip}")
        self.expect(self.prompt)
        match = re.search(
            f"{ping_count} packets transmitted, {ping_count} packets received",
            self.before,
        )
        return bool(match)

    @CmtsTemplate.connect_and_run
    def check_output(self, cmd: str) -> str:
        """get check_output out from parent class"""
        return super().check_output(cmd)

    def get_current_time(self, fmt: str = "%Y-%m-%dT%H:%M:%S%z"):
        """Returns the current time on the CMTS
        :return: the current time as a string formatted as "%Y-%m-%dT%H:%M:%S%z"
        :raises CodeError: if anything went wrong in getting the time
        """
        self.current_time_cmd = "show clock"
        self.dateformat = "%Y %B %d %H:%M:%S"
        return super().get_current_time(fmt)
