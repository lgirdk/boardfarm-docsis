from boardfarm.tests import rootfs_boot
from boardfarm.devices import board
from boardfarm.exceptions import BootFail
from boardfarm.lib.common import run_once

class DocsisBootStub(rootfs_boot.RootFSBootTest):
    '''
    Boots a board as usual but with dual-stack-config instead of the board default
    '''

    cfg = None

    @run_once
    def runTest(self):
        if self.cfg is None:
            self.skipTest("Do not run stub directly")

        board.cm_cfg = board.generate_cfg(self.cfg)

        # TODO: why is this required? need to fix globally
        board.config['cm_cfg'] = board.cm_cfg

        try:
            self.boot()
        except Exception as e:
            print("\n\nFailed to Boot")
            print(e)
            raise BootFail

    def recover(self):
        board.close()
        super(DocsisBootStub, self).recover()

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

