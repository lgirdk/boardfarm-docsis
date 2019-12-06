import time
import pexpect

from boardfarm.devices import openwrt_router
from boardfarm.lib.network_helper import valid_ipv4, valid_ipv6

# TODO: probably the wrong parent
class Docsis(openwrt_router.OpenWrtRouter):
    """Docsis class used to perform generic operations
    """
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
        """
        Name: cmStatus
        Purpose: Use snmp mib to get cm status.
        Input: wan, wan_ip, board, status_string
        Output: return snmp string
        Value list (INTEGER: \d+)
            1: other(1)
            2: notReady(2)
            3: notSynchronized(3)
            4: phySynchronized(4)
            5: usParametersAcquired(5)
            6: rangingComplete(6)
            7: ipComplete(7)
            8: todEstablished(8)
            9: securityEstablished(9)
            10: paramTransferComplete(10)
            11: registrationComplete(11)
            12: operational(12)
            13: accessDenied(13)
        """
        status=['Timeout: No Response from', '(INTEGER: \d+)']
        for not_used in range(100):
            # TODO: wan ip could change after reboot?
            wan.sendline("snmpget -v 2c -t 2 -r 10 -c public %s %s.2" %(wan_ip, self.mib["docsIf3CmStatusValue"]) )
            i=wan.expect(status)
            match=wan.match.group() if i==1 or i==0 else None
            wan.expect(wan.prompt)

            # wait up to 100 * 5 seconds for board to come online
            # ideally this was board. but that's not passed in here for now
            wan.expect(pexpect.TIMEOUT, timeout=1)
            self.arm.expect(pexpect.TIMEOUT, timeout=4)
            if match==status_string:
                return match

            # this can be a lot longer than 5 minutes so let's touch each pass
            self.touch()
        return False

    def tr069_connected(self):
        """This method validates if the TR069 client is running on CM

        :raises Exception: to be implemented
        """
        assert False, "Code to detect if tr069 client is running, to be implemented"

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
        mta_ipv6 = False # Not in spec

        # this is not cm config mode, it's erouter prov mode
        cm_configmode = self.cm_cfg.cm_configmode

        # we need to fetch the CM config mode from CMTS, skippin wan0 validation for the time being.

        if cm_configmode == 'bridge':
            # TODO
            pass
        if cm_configmode == 'ipv4':
            erouter_ipv4 = True
        if cm_configmode == 'dslite':
            erouter_ipv6 = True
        if cm_configmode == 'dual-stack':
            erouter_ipv4 = True
            erouter_ipv6 = True

        failure = "should not see this message"
        while (time.time() - start_time < time_for_provisioning):
            try:
                if wan_ipv4:
                    failure="wan ipv4 failed"
                    valid_ipv4(self.get_interface_ipaddr(self.wan_iface))
                if wan_ipv6:
                    failure="wan ipv6 failed"
                    valid_ipv6(self.get_interface_ip6addr(self.wan_iface))

                if hasattr(self, 'erouter_iface'):
                    if erouter_ipv4:
                        failure="erouter ipv4 failed"
                        valid_ipv4(self.get_interface_ipaddr(self.erouter_iface))
                    if erouter_ipv6:
                        failure="erouter ipv6 failed"
                        valid_ipv6(self.get_interface_ip6addr(self.erouter_iface))

                if hasattr(self, 'mta_iface'):
                    if mta_ipv4:
                        failure="mta ipv4 failed"
                        valid_ipv4(self.get_interface_ipaddr(self.mta_iface))
                    if mta_ipv6:
                        failure="mta ipv6 failed"
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
        raise Exception("Not implemented! should be implemented to return the cm model name")
