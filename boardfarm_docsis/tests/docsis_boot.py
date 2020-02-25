from boardfarm.tests import rootfs_boot
from boardfarm.exceptions import BootFail
from boardfarm.lib.common import run_once
from boardfarm.lib.voice import voice_devices_configure, dns_setup_sipserver
from boardfarm_docsis.exceptions import VoiceSetupConfigureFailure

class DocsisBootStub(rootfs_boot.RootFSBootTest):
    '''
    Boots a board as usual but with dual-stack-config instead of the board default
    '''

    cfg = None
    ertr_mode = {}
    country = 'NL' #default
    voice = False

    @run_once
    def runTest(self):
        if self.cfg is None:
            self.skipTest("Do not run stub directly")

        self.dev.board.cm_cfg = self.dev.board.generate_cfg(self.cfg, None, self.ertr_mode)
        self.dev.board.mta_cfg = self.dev.board.generate_mta_cfg(self.country)

        # TODO: why is this required? need to fix globally
        self.dev.board.config['cm_cfg'] = self.dev.board.cm_cfg

        if self.voice:
            try:
                sipserver = self.dev.sipcenter
                sipserver.kill_asterisk()
                dns_setup_sipserver(sipserver, self.config)
                voice_devices_list = [sipserver, self.dev.softphone, self.dev.lan, self.dev.lan2]
                voice_devices_configure(voice_devices_list, self.dev.sipcenter)
            except Exception as e:
                print("\n\nFailed to configure voice setup")
                print(e)
                raise VoiceSetupConfigureFailure
        try:
            self.boot()
            if self.voice:
                self.dev.board.wait_for_mta_provisioning()

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
        self.country = self.env_helper.get_country()
        self.voice = False #To be acquired from env Json once the Json schema is decided
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

