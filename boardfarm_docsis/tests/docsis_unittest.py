import pytest
from boardfarm.lib.SnmpHelper import snmp_v2
from boardfarm.tests import rootfs_boot


@pytest.mark.selftest
class selftest_test_cmts_functions(rootfs_boot.RootFSBootTest):
    def test_main(self):
        """
        This function is to test the cmts functions moved to boardfarm-docsis/devices/base_cmts.py.
        Input : None (self -- cmts object).
        Output : None (checks the cmts methods and prints the output).
        """
        cmts = self.dev.cmts
        board = self.dev.board
        ip_provisioning_mode = cmts.check_docsis_mac_ip_provisioning_mode(
            cmts.mac_domain
        )
        print(f"The ip provisioning mode on given mac domain is {ip_provisioning_mode}")
        cmts.wait_for_ready()
        is_cm_bridged = cmts.is_cm_bridged(board.config["cm_mac"])
        print(f"The status of cm bridged is {is_cm_bridged}")
        ertr_ipv4 = cmts.get_ertr_ipv4(board.config["cm_mac"])
        print(f"The erouter Ipv4 address is {ertr_ipv4}")
        ertr_ipv6 = cmts.get_ertr_ipv6(board.config["cm_mac"])
        print(f"The erouter Ipv6 address is {ertr_ipv6}")


class selftest_snmpv2(rootfs_boot.RootFSBootTest):
    def test_main(self):
        board = self.dev.board
        wan = self.dev.wan
        mib_list = ["docsDevSwServer", "docsDevSwFilename"]
        ip = board.get_interface_ipaddr(board.wan_iface)
        for mib in mib_list:
            try:
                value_1 = snmp_v2(wan, ip, mib)
                print(f"snmpget on mib: {mib}\nvalue: {value_1}")

                # In case of SNMP set, script first performs a get, loads the mib details and then performs a set.
                value_2 = snmp_v2(wan, ip, mib, value=value_1 + "error")
                print(f"snmpset on mib: {mib}\nvalue: {value_2}")

            except Exception as e:
                print(e)
            finally:
                value_2 = snmp_v2(wan, ip, mib, value=value_1)
                print(f"snmpset on mib: {mib}\nvalue: {value_2}")


class selftest_check_online(rootfs_boot.RootFSBootTest):
    """This test should not throw ANY exceptions (This is for the Arris cmts
    class way of connecting)"""

    def test_main(self):
        v = self.dev.cmts.check_online(self.dev.board.get_cm_mac_addr())
        if v is True:
            print("CM is online")
        else:
            print(f"cmts.check_online returned: {v}")
        # no need to verify, we just don't want exceptions
