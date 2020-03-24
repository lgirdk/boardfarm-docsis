import warnings

import boardfarm_docsis.lib.booting
from boardfarm.lib.common import run_once
from boardfarm.tests import rootfs_boot
from boardfarm_docsis.exceptions import BftProvEnvMismatch
from debtcollector import deprecate, removals

warnings.simplefilter("always", UserWarning)


class DocsisBootStub(rootfs_boot.RootFSBootTest):
    '''
    Boots a board as usual but with dual-stack-config instead of the board default
    '''

    cfg = None
    ertr_mode = {}
    country = 'NL'  #default
    voice = False

    def __init__(self, *args, **kw):
        # check DocsisBoottype and Enviornment config
        self.check_bootmode()

        super(DocsisBootStub, self).__init__(*args, **kw)

    def check_bootmode(self):
        if not isinstance(self, DocsisBootFromEnv):
            deprecate(
                "Warning!",
                message=
                "Use DocisisBootFromEnv to boot with MAX config, and set BFT_ARGS to the required environment.",
                category=UserWarning)

    @run_once
    def runTest(self):
        if not self.env_helper.env_check(self.env_req):
            raise BftProvEnvMismatch()
        if self.__class__.__name__ == "DocsisBootStub":
            self.skipTest("Do not run stub directly")
        boardfarm_docsis.lib.booting.boot(self, self.config, self.env_helper,
                                          self.dev, self.logged)

    @removals.remove(removal_version="> 1.1.1", category=UserWarning)
    def recover(self):
        pass


class DocsisBootFromEnv(DocsisBootStub):
    '''Dynamic boot from ENV json'''

    env_req = {}

    def runTest(self):
        super(DocsisBootFromEnv, self).runTest()


class DocsisBootDualStack(DocsisBootStub):
    '''Normal boot, but with Dual Stack CM cfg specified'''

    env_req = {
        "environment_def": {
            "board": {
                "eRouter_Provisioning_mode": "dual"
            }
        }
    }
    cfg = "dual"


class DocsisBootIPv4(DocsisBootStub):
    '''Normal boot, but with IPv4 CM cfg specified'''

    env_req = {
        "environment_def": {
            "board": {
                "eRouter_Provisioning_mode": "ipv4"
            }
        }
    }
    cfg = "ipv4"


class DocsisBootIPv6(DocsisBootStub):
    '''Normal boot, but with IPv6 CM cfg specified'''

    env_req = {
        "environment_def": {
            "board": {
                "eRouter_Provisioning_mode": "ipv6"
            }
        }
    }
    cfg = "ipv6"


class DocsisBootDSLite(DocsisBootStub):
    '''Normal boot, but with DSLite CM cfg specified'''

    env_req = {
        "environment_def": {
            "board": {
                "eRouter_Provisioning_mode": "dslite"
            }
        }
    }
    cfg = "dslite"


class DocsisBootBridge(DocsisBootStub):
    '''Normal boot, but with bridged CM cfg specified'''

    env_req = {
        "environment_def": {
            "board": {
                "eRouter_Provisioning_mode": "bridge"
            }
        }
    }
    cfg = "bridge"


class DocsisBootNone(DocsisBootStub):
    '''Normal boot, but with none specified'''

    env_req = {
        "environment_def": {
            "board": {
                "eRouter_Provisioning_mode": "none"
            }
        }
    }
    cfg = "none"
