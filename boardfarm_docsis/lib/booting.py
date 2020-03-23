from boardfarm.exceptions import BootFail
from boardfarm.lib.voice import dns_setup_sipserver, voice_devices_configure
from boardfarm_docsis.exceptions import VoiceSetupConfigureFailure


def boot(self, devices, logged=dict()):
    logged['boot_step'] = "env_ok"

    devices.board.cm_cfg = devices.board.generate_cfg(self.cfg, None,
                                                      self.ertr_mode)
    logged['boot_step'] = "cmcfg_ok"
    devices.board.mta_cfg = devices.board.generate_mta_cfg(self.country)
    logged['boot_step'] = "mtacfg_ok"

    # TODO: why is this required? need to fix globally
    devices.board.config['cm_cfg'] = devices.board.cm_cfg

    if self.voice:
        try:
            sipserver = devices.sipcenter
            sipserver.kill_asterisk()
            dns_setup_sipserver(sipserver, self.config)
            voice_devices_list = [
                sipserver, devices.softphone, devices.lan, devices.lan2
            ]
            voice_devices_configure(voice_devices_list, devices.sipcenter)
        except Exception as e:
            print("\n\nFailed to configure voice setup")
            print(e)
            raise VoiceSetupConfigureFailure
        logged['boot_step'] = "voice_ok"
    else:
        logged['boot_step'] = "voice_skipped"
    try:
        self.boot()
        if self.voice:
            devices.board.wait_for_mta_provisioning()
            logged['boot_step'] = "voice_mta_ok"

    except Exception as e:
        print("\n\nFailed to Boot")
        print(e)
        raise BootFail
