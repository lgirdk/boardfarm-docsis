import boardfarm.lib.booting
from boardfarm.exceptions import BootFail, NoTFTPServer
from boardfarm.lib.voice import dns_setup_sipserver, voice_devices_configure
from boardfarm_docsis.exceptions import VoiceSetupConfigureFailure


def boot(config, env_helper, devices, logged=dict()):
    cfg = env_helper.get_prov_mode()
    ertr_mode = env_helper.get_ertr_mode()
    country = env_helper.get_country()
    voice = env_helper.voice_enabled()
    tr069check = cfg not in ["disabled", "bridge", "none"]

    logged['boot_step'] = "env_ok"

    devices.board.cm_cfg = devices.board.generate_cfg(cfg, None, ertr_mode)
    logged['boot_step'] = "cmcfg_ok"
    devices.board.mta_cfg = devices.board.generate_mta_cfg(country)
    logged['boot_step'] = "mtacfg_ok"

    # TODO: why is this required? need to fix globally
    devices.board.config['cm_cfg'] = devices.board.cm_cfg

    devices.board.enable_time_display()

    if voice:
        try:
            sipserver = devices.sipcenter
            sipserver.kill_asterisk()
            dns_setup_sipserver(sipserver, config)
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
        boardfarm.lib.booting.boot(config,
                                   env_helper,
                                   devices,
                                   reflash=True,
                                   logged=logged)
        if voice:
            devices.board.wait_for_mta_provisioning()
            logged['boot_step'] = "voice_mta_ok"

        if tr069check:
            devices.board.restart_tr069(
                devices.wan,
                devices.board.get_interface_ipaddr(devices.board.wan_iface))
            logged['boot_step'] = "acs_connection_ok"
    except NoTFTPServer as e:
        raise e
    except Exception as e:
        print("\n\nFailed to Boot")
        print(e)
        raise BootFail
