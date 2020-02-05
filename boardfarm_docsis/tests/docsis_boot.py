from boardfarm.tests import rootfs_boot
from boardfarm.exceptions import BootFail
from boardfarm.lib.common import run_once

class DocsisBootStub(rootfs_boot.RootFSBootTest):
    '''
    Boots a board as usual but with dual-stack-config instead of the board default
    '''

    cfg = None
    ertr_mode = {}

    @run_once
    def runTest(self):
        if self.cfg is None:
            self.skipTest("Do not run stub directly")

        self.dev.board.cm_cfg = self.dev.board.generate_cfg(self.cfg, None, self.ertr_mode)

        # TODO: why is this required? need to fix globally
        self.dev.board.config['cm_cfg'] = self.dev.board.cm_cfg

        try:
            self.boot()
        except Exception as e:
            print("\n\nFailed to Boot")
            print(e)
            raise BootFail

    def recover(self):
        self.dev.board.close()
        super(DocsisBootStub, self).recover()

class DocsisBootFromEnv(DocsisBootStub):
    '''Dynamic boot from ENV json'''

    def runTest(self):
        self.cfg = self.env_helper.get_prov_mode()
        self.ertr_mode = self.env_helper.get_ertr_mode()

        super(DocsisBootFromEnv, self).runTest()

class DocsisBootDualStack(DocsisBootStub):
    '''Normal boot, but with Dual Stack CM cfg specified'''
    cfg = "dual"

class DocsisBootIPv4(DocsisBootStub):
    '''Normal boot, but with IPv4 CM cfg specified'''
    cfg = "ipv4"

class DocsisBootIPv6(DocsisBootStub):
    '''Normal boot, but with IPv6 CM cfg specified'''
    cfg = "ipv6"

class DocsisBootDSLite(DocsisBootStub):
    '''Normal boot, but with DSLite CM cfg specified'''
    cfg = "dslite"

class DocsisBootBridge(DocsisBootStub):
    '''Normal boot, but with bridged CM cfg specified'''
    cfg = "bridge"

class DocsisBootNone(DocsisBootStub):
    '''Normal boot, but with none specified'''
    cfg = "none"

