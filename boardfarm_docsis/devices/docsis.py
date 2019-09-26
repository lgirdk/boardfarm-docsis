import openwrt_router

import pexpect


# TODO: probably the wrong parent
class Docsis(openwrt_router.OpenWrtRouter):

    def get_cmStatus(self, wan, wan_ip, status_string=None):
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
        assert False, "Code to detect if tr069 clienti is running is not implemented"
