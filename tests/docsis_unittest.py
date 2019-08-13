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
    2. waits for cmts interface to be up and in service
    3. checks if a cm is bridged
    4. gets the erouter ipv4 address 
    5. gets the erouter ipv6 address
    '''
    def runTest(self):
            from devices import cmts
            mac_domain=cmts.get_cm_mac_domain(board.config["cm_mac"])
            ip_provisioning_mode=cmts.check_docsis_mac_ip_provisioning_mode(cmts.mac_domain)
            print ("The ip provisioning mode on given mac domain is %s" % ip_provisioning_mode)
            cmts.wait_for_ready()
            is_cm_bridged=cmts.is_cm_bridged(board.config["cm_mac"])
            print ("The status of cm bridged is %s" % is_cm_bridged)
            ertr_ipv4=cmts.get_ertr_ipv4(board.config["cm_mac"])
            print ("The erouter Ipv4 address is %s" % ertr_ipv4)
            ertr_ipv6=cmts.get_ertr_ipv6(board.config["cm_mac"])
            print ("The erouter Ipv6 address is %s" % ertr_ipv6)
