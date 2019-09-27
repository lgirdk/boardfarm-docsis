import rootfs_boot
from boardfarm.devices import board
class selftest_test_cmts_functions(rootfs_boot.RootFSBootTest):
    def runTest(self):
            '''
            This function is to test the cmts functions moved to boardfarm-docsis/devices/base_cmts.py.
            Input : None (self -- cmts object).
            Output : None (checks the cmts methods and prints the output).
            '''
            from boardfarm.devices import cmts
            ip_provisioning_mode=cmts.check_docsis_mac_ip_provisioning_mode(cmts.mac_domain)
            print("The ip provisioning mode on given mac domain is %s" % ip_provisioning_mode)
            cmts.wait_for_ready()
            is_cm_bridged=cmts.is_cm_bridged(board.config["cm_mac"])
            print("The status of cm bridged is %s" % is_cm_bridged)
            ertr_ipv4=cmts.get_ertr_ipv4(board.config["cm_mac"])
            print("The erouter Ipv4 address is %s" % ertr_ipv4)
            ertr_ipv6=cmts.get_ertr_ipv6(board.config["cm_mac"])
            print("The erouter Ipv6 address is %s" % ertr_ipv6)
