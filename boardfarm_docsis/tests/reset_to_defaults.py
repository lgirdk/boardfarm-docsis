from boardfarm.exceptions import BootFail

from boardfarm_docsis.tests.docsis_boot import DocsisBootStub as BF_Test


class reset_board_to_defaults(BF_Test):
    """Factory reset via ARM console command, wait for boot
    and CM to become operational"""

    env_req = {}

    def runTest(self):
        try:
            self.dev.board.reset_defaults_via_os(self)
            self.dev.board.check_valid_docsis_ip_networking(
                strict=False, time_for_provisioning=60
            )
            if self.env_helper.get_prov_mode() not in ["bridge", "disabled"]:
                self.dev.board.restart_tr069(
                    self.dev.wan,
                    self.dev.board.get_interface_ipaddr(self.dev.board.wan_iface),
                )
        except Exception:
            raise BootFail("BootFail : Failed to Factory Reset")
