from boardfarm_docsis.tests.docsis_boot import DocsisBootStub as BF_Test


class reset_tr069_to_defaults(BF_Test):
    """Restart TR069"""

    def runTest(self):
        self.dev.board.restart_tr069(
            self.dev.wan, self.dev.board.get_interface_ipaddr(self.dev.board.wan_iface)
        )
