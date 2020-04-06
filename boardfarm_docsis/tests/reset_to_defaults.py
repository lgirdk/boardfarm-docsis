from boardfarm.exceptions import BootFail
from boardfarm.lib.common import retry_on_exception
from boardfarm_docsis.tests.docsis_boot import DocsisBootStub as BF_Test


class reset_board_to_defaults(BF_Test):
    """Factory reset via ARM console command, wait for boot
    and CM to become operational"""
    def runTest(self):
        try:
            self.dev.board.reset_defaults_via_os(self)
            self.eRouter_ip = retry_on_exception(
                self.dev.board.get_interface_ipaddr,
                (self.dev.board.erouter_iface, ),
                retries=5)
            self.dev.board.restart_tr069(
                self.dev.wan,
                self.dev.board.get_interface_ipaddr(self.dev.board.wan_iface))
        except Exception:
            raise BootFail("BootFail : Failed to Factory Reset")
