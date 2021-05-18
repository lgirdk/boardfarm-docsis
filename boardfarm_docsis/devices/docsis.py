import logging
import re
import time

import pexpect
from boardfarm.devices import openwrt_router
from boardfarm.exceptions import CodeError
from boardfarm.lib import SnmpHelper
from boardfarm.lib.DeviceManager import device_type
from boardfarm.lib.network_helper import valid_ipv4, valid_ipv6
from boardfarm.lib.SNMPv2 import SNMPv2
from netaddr import EUI, mac_unix_expanded

from boardfarm_docsis.lib.docsis import cm_cfg as cm_cfg_cls
from boardfarm_docsis.lib.docsis import docsis_encoder

logger = logging.getLogger("bft")


# TODO: probably the wrong parent
class DocsisInterface:
    """Docsis class used to perform generic operations"""

    cm_cfg = None

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

    def tr069_connected(self):
        """This method validates if the TR069 client is running on CM

        :raises Exception: to be implemented
        """
        raise AssertionError(
            "Code to detect if tr069 client is running, to be implemented"
        )

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

    reprovisionFirstRun = True

    def reprovision(self, provisioner, cm_cfg=None, mta_cfg=None, erouter_cfg=None):
        """Provision the board with config file
        :param provisioner: provisioner device
        :param cm_cfg: cable modem config, defaults to None
        :type cm_cfg: string, optional
        :param mta_cfg: MTA config, defaults to None
        :type mta_cfg: string, optional
        :param erouter_cfg: erouter config, defaults to None
        :type erouter_cfg: string, optional
        """
        if cm_cfg is None:
            cm_cfg = self.env_helper.get_board_boot_file()

        # if mta_cfg is None:
        #    # to check where to get the mta config from

        if type(cm_cfg) is str:
            self.cm_cfg = cm_cfg_cls(cfg_file=cm_cfg)

        self.update_config()

        provisioner.tftp_device = self.dev.board.tftp_dev

        docsis_encoder.copy_cmts_provisioning_files(self.config, self.tftp_dev, self)
        if self.reprovisionFirstRun:
            self.reprovisionFirstRun = False
            provisioner.provision_board(self.config)
        else:
            provisioner.reprovision_board(self.config)

    def update_config(self):
        """Get the mac address of CM, MTA and erouter, add extra provisioning to the config"""
        config = self.config
        cm_cfg = self.cm_cfg
        if cm_cfg is None:
            cm_cfg = self.env_helper.get_board_boot_file()
            self.cm_cfg = cm_cfg_cls(cfg_file=cm_cfg)
        mta_cfg = None
        # TODO: use EUI to parse cm_mac
        if "cm_mac" not in config:
            print("MAC addresses not in config, some provisioning might not work!")
            return

        if "mta_mac" not in config:
            from netaddr import EUI, mac_unix_expanded

            mac = EUI(config["cm_mac"])
            config["mta_mac"] = "%s" % EUI(int(mac) + 1, dialect=mac_unix_expanded)

        if "erouter_mac" not in config:
            from netaddr import EUI, mac_unix_expanded

            mac = EUI(config["cm_mac"])
            config["erouter_mac"] = "%s" % EUI(int(mac) + 2, dialect=mac_unix_expanded)

        config["tftp_cfg_files"] = [cm_cfg, mta_cfg]

        if hasattr(self.dev, "provisioner") and hasattr(
            self.dev.provisioner, "prov_ip"
        ):
            wan = self.dev.wan
            provisioner = self.dev.provisioner

            config["extra_provisioning"] = {
                "mta": {
                    "hardware ethernet": config["mta_mac"],
                    "filename": '"' + "mta-config-d41d8cd98f.bin" '"',
                    "options": {
                        "bootfile-name": '"' + "mta-config-d41d8cd98f.bin" '"',
                        "dhcp-parameter-request-list": "3, 6, 7, 12, 15, 43, 122",
                        "domain-name": '"sipcenter.com"',
                        "domain-name-servers": wan.gw,
                        "routers": provisioner.mta_gateway,
                        "log-servers": provisioner.prov_ip,
                        "host-name": '"' + config.get_station() + '"',
                    },
                },
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
            # No ipv6 for this device, so let's zero out the config so it comes up ipv4 properly
            if "extra_provisioning_v6" not in config:
                config["extra_provisioning_v6"] = {}
            config["extra_provisioning_v6"] = {
                "cm": {
                    "host-identifier option dhcp6.client-id": "00:03:00:01:"
                    + config["cm_mac"],
                    "options": {
                        "docsis.configuration-file": '"%s"' % self.cm_cfg.encoded_fname,
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

    def flash_with_snmp(self, image: str):
        if image is None:
            raise Exception("No firware image was provided to flash DUT using snmp")

        wan = self.dev.wan
        cm_ip = self.dev.cmts.get_cmip(self.cm_mac)
        snmp = SNMPv2(wan, cm_ip)

        protocol = "1"  # Default protocol to tftp
        server_ip = wan.get_interface_ipaddr(wan.iface_dut)
        filename = re.search("LG-RDK.*", image).group()
        # Copying the file to tftpserver
        wan.sendline("wget -nc {} -O /tftpboot/{}".format(image, filename))
        wan.expect(["saved"] + ["already there; not retrieving"])
        wan.expect_prompt()

        self.dev.cmts.clear_cm_reset(self.cm_mac)
        for _ in range(20):
            if self.dev.cmts.is_cm_online(ignore_partial=True):
                break
            time.sleep(20)

        wan.sendline(
            f"snmpset -v 2c -c private {cm_ip} .1.3.6.1.4.1.1038.28.1.1.5.0 i 2"
        )  # noqa: E501
        wan.expect_prompt()

        snmp.snmpset("docsDevSwServer", server_ip, "a")

        snmp.snmpset("docsDevSwFilename", filename, "string")

        snmp.snmpset("docsDevSwServerTransportProtocol", protocol, "integer")

        status = "1"
        snmp.snmpset("docsDevSwAdminStatus", status, "integer")


class Docsis(DocsisInterface, openwrt_router.OpenWrtRouter):
    pass
