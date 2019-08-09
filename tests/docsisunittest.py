import rootfs_boot
from devices import board
'''
    This file can be used to add unit tests that
    tests/validate the behavior of new/modified
    components.
'''
class selftest_test_cmts_functions(rootfs_boot.RootFSBootTest):
    '''
    tests the cmts functions moved to boardfarm-docsis/devices/base_cmts.py as of now testing the method check_docsis_mac_ip_provisioning_mode
    1. gets the mac domain from cmts and checks the ip provisioning mode on the mac domain
    '''
    def runTest(self):
        try:
            from devices import cmts
        except Exception as e:
            print (e)
        else:
            mac_domain=cmts.get_cm_mac_domain(board.config["cm_mac"])
            ip_provisioning_mode=cmts.check_docsis_mac_ip_provisioning_mode(cmts.mac_domain)
            print ("The ip provisioning mode on given mac domain is %s" % ip_provisioning_mode)
