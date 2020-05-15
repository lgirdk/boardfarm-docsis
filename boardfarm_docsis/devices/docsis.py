import time

import pexpect
from boardfarm.devices import openwrt_router
from boardfarm.exceptions import CodeError
from boardfarm.lib.DeviceManager import device_type
from boardfarm.lib.network_helper import valid_ipv4, valid_ipv6


# TODO: probably the wrong parent
class Docsis(openwrt_router.OpenWrtRouter):
    """Docsis class used to perform generic operations
    """
    # The possible configurations for the CM
    cm_mgmt_config_modes = {"dual", "ipv4", "ipv6"}

    # The possible configurations for the eRouter
    disabled = {
        "bridge", "disabled"
    }  # this will add an erouter initialisation (TLV 202) set to  0
    erouter_config_modes = cm_mgmt_config_modes | disabled | {
        "dslite", "none"
    }  # "none" will NOT add any eRouter initialisation to the config file

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
                    cmts.mac_domain)
        except AttributeError:
            print("Failed on get_cm_mgmt_cfg: has_cmts no set")
            pass
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
        status = ['Timeout: No Response from', r'(INTEGER: \d+)']
        for not_used in range(100):
            # TODO: wan ip could change after reboot?
            wan.sendline("snmpget -v 2c -t 2 -r 10 -c public %s %s.2" %
                         (wan_ip, self.mib["docsIf3CmStatusValue"]))
            i = wan.expect(status)
            match = wan.match.group() if i == 1 or i == 0 else None
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
        assert False, "Code to detect if tr069 client is running, to be implemented"

    def check_valid_docsis_ip_networking(self,
                                         strict=True,
                                         time_for_provisioning=240):
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

        if cm_configmode in ['bridge', 'disabled']:
            # TODO
            pass
        if cm_configmode == 'ipv4':
            erouter_ipv4 = True
        if cm_configmode in ['dslite', 'ipv6']:
            erouter_ipv6 = True
        if cm_configmode == 'dual-stack':
            erouter_ipv4 = True
            erouter_ipv6 = True

        failure = "should not see this message"
        while (time.time() - start_time < time_for_provisioning):
            try:
                if wan_ipv4:
                    failure = "wan ipv4 failed"
                    valid_ipv4(self.get_interface_ipaddr(self.wan_iface))
                if wan_ipv6:
                    failure = "wan ipv6 failed"
                    valid_ipv6(self.get_interface_ip6addr(self.wan_iface))

                if hasattr(self, 'erouter_iface'):
                    if erouter_ipv4:
                        failure = "erouter ipv4 failed"
                        valid_ipv4(
                            self.get_interface_ipaddr(self.erouter_iface))
                    if erouter_ipv6:
                        failure = "erouter ipv6 failed"
                        valid_ipv6(
                            self.get_interface_ip6addr(self.erouter_iface))

                if hasattr(self, 'mta_iface'):
                    if mta_ipv4:
                        failure = "mta ipv4 failed"
                        valid_ipv4(self.get_interface_ipaddr(self.mta_iface))
                    if mta_ipv6:
                        failure = "mta ipv6 failed"
                        valid_ipv6(self.get_interface_ip6addr(self.mta_iface))

                # if we get this far, we have all IPs and can exit while loop
                break
            except KeyboardInterrupt:
                raise
            except:
                if time.time() - start_time > time_for_provisioning:
                    if strict:
                        assert False, "Failed to provision docsis device properly = " + failure
                    else:
                        print("WARN: failed to provision board entirely")

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
