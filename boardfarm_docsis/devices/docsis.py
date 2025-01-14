import logging
import random
import string
import time

import pexpect
from boardfarm.devices import openwrt_router
from boardfarm.exceptions import CodeError
from boardfarm.lib import SnmpHelper
from boardfarm.lib.DeviceManager import device_type
from boardfarm.lib.network_helper import valid_ipv4, valid_ipv6
from boardfarm.lib.SNMPv2 import SNMPv2
from netaddr import EUI, mac_unix_expanded
from termcolor import colored

from boardfarm_docsis.lib.docsis import base_cfg
from boardfarm_docsis.lib.docsis import cm_cfg as cm_cfg_cls
from boardfarm_docsis.lib.docsis import mta_cfg as mta_cfg_cls
from boardfarm_docsis.use_cases.cmts_interactions import is_bpi_privacy_disabled

logger = logging.getLogger("bft")


class DocsisInterface:
    """Docsis class used to perform generic operations"""

    cm_cfg = cm_cfg_cls
    mta_cfg = mta_cfg_cls

    swdl_info = {
        "tftp": {"proto": "1", "dest": "/tftpboot"},
        "http": {"proto": "2", "dest": "/var/www/html"},
    }
    default_swdl_protocol = "http"  # either http(2) or tftp(1)

    # The possible configurations for the CM
    cm_mgmt_config_modes = {"dual", "ipv4", "ipv6"}

    # The possible configurations for the eRouter
    disabled = {
        "disabled",
    }  # this will add an erouter initialisation (TLV 202) set to  0
    erouter_config_modes = (
        cm_mgmt_config_modes | disabled | {"dslite", "none"}
    )  # "none" will NOT add any eRouter initialisation to the config file

    def get_cm_mgmt_cfg(self):
        """This method attempts to obtain the CM management interface configuration. It queries the CMTS for the mac-domain configuration.

        :return: the status of the CM mgmt interface (currently one of 'ipv4', 'ipv6', 'dual-stack', 'apm', or (python)None)
        :rtype: string
        """
        mac_dom_config = None
        try:
            if self.has_cmts:
                # gets the mac-domain configuration from the cmts
                cmts = self.dev.get_device_by_type(device_type.cmts)
                mac_dom_config = cmts.check_docsis_mac_ip_provisioning_mode(
                    cmts.mac_domain
                )
        except AttributeError:
            logger.error("Failed on get_cm_mgmt_cfg: has_cmts no set")
        return mac_dom_config

    def get_cmStatus(self, wan, wan_ip, status_string=None):
        """This method gets the cm status via snmp.

        :param wan: wan device
        :type wan: object
        :param wan_ip: wan ip address
        :type wan_ip: string
        :param status_string: the cm status to be used for match, defaults to None
        :type status_string: string
        :return: the status of the CM
        :rtype: string
        """
        status = ["Timeout: No Response from", r"(INTEGER: \d+)"]
        for _ in range(100):
            # TODO: wan ip could change after reboot?
            wan.sendline(
                "snmpget -v 2c -t 2 -r 10 -c public %s %s.2"
                % (wan_ip, self.mib["docsIf3CmStatusValue"])
            )
            i = wan.expect(status)
            match = wan.match.group() if i in [1, 0] else None
            wan.expect(wan.prompt)

            # wait up to 100 * 5 seconds for board to come online
            # ideally this was board. but that's not passed in here for now
            wan.expect(pexpect.TIMEOUT, timeout=1)
            self.arm.expect(pexpect.TIMEOUT, timeout=4)
            if match == status_string:
                return match

            # this can be a lot longer than 5 minutes so let's touch each pass
            self.touch()
        return False

    def check_valid_docsis_ip_networking(self, strict=True, time_for_provisioning=240):
        """This method is to check the docsis provision on CM

        :param strict: used to raise Exception if specified as True and provision false, defaults to True
        :type strict: boolean
        :param time_for_provisioning: the maximum time allowed for the CM to provision, defaults to 240
        :type time_for_provisioning: int
        """
        start_time = time.time()

        wan_ipv4 = False
        wan_ipv6 = False
        erouter_ipv4 = False
        erouter_ipv6 = False
        mta_ipv4 = True
        mta_ipv6 = False  # Not in spec

        # this is not cm config mode, it's erouter prov mode
        cm_configmode = self.cm_cfg.cm_configmode

        # we need to fetch the CM config mode from CMTS, skippin wan0 validation for the time being.

        if cm_configmode == "disabled":
            # TODO
            pass
        if cm_configmode == "ipv4":
            erouter_ipv4 = True
        if cm_configmode in ["dslite", "ipv6"]:
            erouter_ipv6 = True
        if cm_configmode == "dual-stack":
            erouter_ipv4 = True
            erouter_ipv6 = True

        failure = "should not see this message"
        while time.time() - start_time < time_for_provisioning:
            try:
                if wan_ipv4:
                    failure = "wan ipv4 failed"
                    valid_ipv4(self.get_interface_ipaddr(self.wan_iface))
                if wan_ipv6:
                    failure = "wan ipv6 failed"
                    valid_ipv6(self.get_interface_ip6addr(self.wan_iface))

                if hasattr(self, "erouter_iface"):
                    if erouter_ipv4:
                        failure = "erouter ipv4 failed"
                        valid_ipv4(self.dev.cmts.get_ertr_ipv4(self.cm_mac))
                    if erouter_ipv6:
                        failure = "erouter ipv6 failed"
                        valid_ipv6(self.dev.cmts.get_ertr_ipv6(self.cm_mac))

                if hasattr(self, "mta_iface"):
                    if mta_ipv4:
                        failure = "mta ipv4 failed"
                        mta_mac = str(
                            EUI(int(EUI(self.cm_mac)) + 1, dialect=mac_unix_expanded)
                        )
                        valid_ipv4(self.dev.cmts.get_mtaip(self.cm_mac, mta_mac))
                    if mta_ipv6:
                        failure = "mta ipv6 failed"
                        valid_ipv6(self.get_interface_ip6addr(self.mta_iface))

                # if we get this far, we have all IPs and can exit while loop
                break
            except KeyboardInterrupt:
                raise
            except Exception:
                self.arm.sendline()  # switches to the arm console
                self.arm.expect_prompt()
                if time.time() - start_time > time_for_provisioning:
                    if strict:
                        raise AssertionError(
                            "Failed to provision docsis device properly = " + failure
                        )
                    else:
                        logger.warn("WARN: board not ready, retrying")
                time.sleep(20)

    def get_cm_model_type(self):
        """This methods returns the model of the CM

        :raises Exception: to be implemented
        """
        raise Exception(
            "Not implemented! should be implemented to return the cm model name"
        )

    def reset_defaults_via_console(self):
        if self.env_helper.has_image():
            cm_fm = self.env_helper.get_image(mirror=False)
            if "nosh" in cm_fm.lower():
                raise CodeError(
                    "Failed FactoryReset via CONSOLE on NOSH Image is not possible"
                )

        return self.reset_defaults_via_os()

    def factory_reset(self):
        return self.reset_defaults_via_console()

    def is_erouter_honouring_config(self, method="snmp"):
        """Checks if the ErouterInitModeControl is set to honour what is stated
        in the boot file. This check can be performed via snmp or dmcli.

        :param method: one of "snmp"(default) or "dmcli"
        :type method: string

        :return: True if ErouterInitModeControl is set to follow the bootfile,
        False otherwise
        :rtype: bool
        """
        if "snmp" == method:
            ip = self.dev.cmts.get_cmip(self.cm_mac)
            if ip == "None":
                raise CodeError("Failed to get cm ip")
            out = SnmpHelper.snmp_v2(self.dev.wan, ip, "esafeErouterInitModeControl")
            return "5" == out
        elif "dmcli" == method:
            param = "Device.X_LGI-COM_Gateway.ErouterModeControl"
            out = self.dmcli.GPV(param)
            return "honoreRouterInitMode" == out.rval
        else:
            raise CodeError(f"Failed to get esafeErouterInitModeControl via {method}")

    def copy_cmts_provisioning_files(self, config, tftp_dev, board):
        """This can be overridden to cater for special encoding methods"""
        base_cfg.copy_cmts_provisioning_files(config, tftp_dev, board)

    def reprovision(self, provisioner):
        """Provision the board with config file
        :param provisioner: provisioner device
        :param cm_cfg: cable modem config, defaults to None
        :type cm_cfg: string, optional
        :param mta_cfg: MTA config, defaults to None
        :type mta_cfg: string, optional
        :param erouter_cfg: erouter config, defaults to None
        :type erouter_cfg: string, optional
        """
        if self.cm_cfg is None:
            cm_cfg = self.dev.board.env_helper.get_board_boot_file()
            self.cm_cfg = cm_cfg_cls(cfg_file_str=cm_cfg)
        if self.mta_cfg is None:
            if self.dev.board.env_helper.has_board_boot_file_mta():
                mta_cfg = self.dev.board.env_helper.get_board_boot_file_mta()
                self.mta_cfg = mta_cfg_cls(mta_file_str=mta_cfg)

        self._update_config()

        provisioner.tftp_device = self.dev.board.tftp_dev
        return self.cm_cfg, self.mta_cfg

    def _update_config(self):
        """Get the mac address of CM, MTA and erouter, add extra provisioning to the config"""
        config = self.config
        # TODO: use EUI to parse cm_mac
        if "cm_mac" not in config:
            print("MAC addresses not in config, some provisioning might not work!")
            return

        if "mta_mac" not in config:
            from netaddr import EUI, mac_unix_expanded

            mac = EUI(config["cm_mac"])
            config["mta_mac"] = f"{EUI(int(mac) + 1, dialect=mac_unix_expanded)}"

        if "erouter_mac" not in config:
            from netaddr import EUI, mac_unix_expanded

            mac = EUI(config["cm_mac"])
            config["erouter_mac"] = f"{EUI(int(mac) + 2, dialect=mac_unix_expanded)}"

        config["tftp_cfg_files"] = [self.cm_cfg, self.mta_cfg]

        if hasattr(self.dev, "provisioner") and hasattr(
            self.dev.provisioner, "prov_ip"
        ):
            wan = self.dev.wan
            provisioner = self.dev.provisioner

            config["extra_provisioning"] = {
                "cm": {
                    "hardware ethernet": config["cm_mac"],
                    "filename": '"' + self.cm_cfg.encoded_fname + '"',
                    "options": {
                        "bootfile-name": '"' + self.cm_cfg.encoded_fname + '"',
                        "dhcp-parameter-request-list": "2, 3, 4, 6, 7, 12, 43, 122",
                        "docsis-mta.dhcp-server-1": provisioner.prov_ip,
                        "docsis-mta.dhcp-server-2": provisioner.prov_ip,
                        "docsis-mta.provision-server": "0 08:54:43:4F:4D:4C:41:42:53:03:43:4F:4D:00",
                        "docsis-mta.kerberos-realm": "05:42:41:53:49:43:01:31:00",
                        "domain-name-servers": wan.gw,
                        "time-offset": "-25200",
                    },
                },
            }
            if self.mta_cfg.txt:
                config["extra_provisioning"] = {
                    "mta": {
                        "hardware ethernet": config["mta_mac"],
                        "filename": '"' + self.mta_cfg.encoded_fname + '"',
                        "options": {
                            "bootfile-name": '"' + self.mta_cfg.encoded_fname + '"',
                            "dhcp-parameter-request-list": "3, 6, 7, 12, 15, 43, 122",
                            "domain-name": '"sipcenter.com"',
                            "domain-name-servers": wan.gw,
                            "routers": provisioner.mta_gateway,
                            "log-servers": provisioner.prov_ip,
                            "host-name": '"' + config.get_station() + '"',
                        },
                    },
                }
            # No ipv6 for this device, so let's zero out the config so it comes up ipv4 properly
            if "extra_provisioning_v6" not in config:
                config["extra_provisioning_v6"] = {}
            config["extra_provisioning_v6"] = {
                "cm": {
                    "host-identifier option dhcp6.client-id": "00:03:00:01:"
                    + config["cm_mac"],
                    "options": {
                        "docsis.configuration-file": f'"{self.cm_cfg.encoded_fname}"',
                        "dhcp6.name-servers": wan.gwv6,
                    },
                },
                "erouter": {
                    "host-identifier option dhcp6.client-id": "00:03:00:01:"
                    + config["erouter_mac"],
                    "options": {"dhcp6.name-servers": wan.gwv6},
                },
            }

    def flash(self, meta, method="snmp"):
        if method == "snmp":
            self.flash_with_snmp(meta)

    def flash_with_snmp_docsis_comands(self, wan, cm_ip, server_ip, filename, protocol):
        snmp = SNMPv2(wan, cm_ip)
        snmp.snmpset("docsDevSwServer", server_ip, "a")
        snmp.snmpset("docsDevSwFilename", filename, "string")
        snmp.snmpset("docsDevSwServerTransportProtocol", protocol, "integer")
        snmp.snmpset("docsDevSwAdminStatus", "1", "integer")

    def flash_with_snmp(self, image: str):
        if image is None:
            raise Exception("No firware image was provided to flash DUT using snmp")

        self.dev.cmts.clear_cm_reset(self.cm_mac)
        for _ in range(20):
            if self.dev.cmts.is_cm_online(
                ignore_bpi=is_bpi_privacy_disabled(), ignore_partial=True
            ):
                break
            time.sleep(20)

        wan = self.dev.wan
        cm_ip = self.dev.cmts.get_cmip(self.cm_mac)

        protocol = self.swdl_info[self.default_swdl_protocol]["proto"]
        destination = self.swdl_info[self.default_swdl_protocol]["dest"]
        server_ip = wan.get_interface_ipaddr(wan.iface_dut)
        filename = "".join(random.choice(string.ascii_lowercase) for _ in range(10))
        if self.default_swdl_protocol == "http":
            wan.check_output("service lighttpd restart")
            out = wan.check_output("service lighttpd status")
            if "lighttpd is running" not in out:
                logger.warning(
                    colored(
                        "SW download: failed to restart lighttpd on wan device"
                        "\nFalling back to tftp protocol download.",
                        color="yellow",
                        attrs=["bold"],
                    )
                )
                protocol = self.swdl_info["tftp"]["proto"]
                destination = self.swdl_info["tftp"]["dest"]
        # Copying the file to tftpserver
        wan.sendline(f"wget -nc {image} -O {destination}/{filename}")
        wan.expect(["saved"] + ["already there; not retrieving"])
        wan.expect_prompt()

        self.flash_with_snmp_docsis_comands(wan, cm_ip, server_ip, filename, protocol)

    def encode_mta(self):
        self.mta_cfg.encode()

    def encode_cfg(self):
        self.cm_cfg.encode()

    def mta_prov_check(self):
        """To verify it the MTA component of DOCSIS board provisioned successfully."""
        raise NotImplementedError

    def check_sip_endpoints_registration(self):
        """To check if MTA endpoint of DOCSIS board are registered"""
        raise NotImplementedError

    def is_sip_endpoint_idle(self, lines: str = "both") -> bool:
        """To validate the status of the sip endpoint(s) connected
        to the MTA lines 0 and/or 1 are idle.

        :param lines: index value, can be either 0/1/both, defaults to 'both'
        :type lines: Literal["0", "1", "both"], optional
        :raises Exception: In case fails to enter voice mode
        :return: True if idle, else False.
        :rtype: bool
        """
        raise NotImplementedError


class Docsis(DocsisInterface, openwrt_router.OpenWrtRouter):
    """Legacy class used in previous vendors implementations"""

    pass
