class ProvisionHelper:
    """Provision related use cases"""

    def __init__(self, devices):
        self.dev = devices

    def provision_board(self):
        if hasattr(self.dev.board, "hw") and hasattr(self.dev.board, "sw"):
            cm_cfg, mta_cfg = self.dev.board.reprovision(self.dev.provisioner)
            for cfg in [cm_cfg, mta_cfg]:
                self._push_to_tftp_server(cfg, self.dev.wan)
            self.dev.provisioner.provision_board(self.dev.board.config)
        else:
            self.dev.board.reprovision(self.dev.provisioner)

    def _push_to_tftp_server(self, cfg, server):
        server.copy_file_to_server(cfg)
