from boardfarm.exceptions import BootFail
from boardfarm_docsis.exceptions import VoiceSetupConfigureFailure
from boardfarm.lib.voice import voice_devices_configure, dns_setup_sipserver


def boot(self):
    self.logged['boot_step'] = "env_ok"

    self.dev.board.cm_cfg = self.dev.board.generate_cfg(
        self.cfg, None, self.ertr_mode)
    self.logged['boot_step'] = "cmcfg_ok"
    self.dev.board.mta_cfg = self.dev.board.generate_mta_cfg(self.country)
    self.logged['boot_step'] = "mtacfg_ok"

    # TODO: why is this required? need to fix globally
    self.dev.board.config['cm_cfg'] = self.dev.board.cm_cfg

    if self.voice:
        try:
            sipserver = self.dev.sipcenter
            sipserver.kill_asterisk()
            dns_setup_sipserver(sipserver, self.config)
            voice_devices_list = [
                sipserver, self.dev.softphone, self.dev.lan, self.dev.lan2
            ]
            voice_devices_configure(voice_devices_list, self.dev.sipcenter)
        except Exception as e:
            print("\n\nFailed to configure voice setup")
            print(e)
            raise VoiceSetupConfigureFailure
        self.logged['boot_step'] = "voice_ok"
    else:
        self.logged['boot_step'] = "voice_skipped"
    try:
        self.boot()
        if self.voice:
            self.dev.board.wait_for_mta_provisioning()
            self.logged['boot_step'] = "voice_mta_ok"

    except Exception as e:
        print("\n\nFailed to Boot")
        print(e)
        raise BootFail