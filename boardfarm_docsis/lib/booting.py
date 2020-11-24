import time
import warnings

import boardfarm.lib.booting
from boardfarm.exceptions import BootFail, CodeError, NoTFTPServer
from boardfarm.lib.voice import dns_setup_sipserver, voice_devices_configure
from boardfarm.library import check_devices

from boardfarm_docsis.exceptions import VoiceSetupConfigureFailure


def activate_mitm(devices, env_helper, logged):
    # TODO: Deploy mitm containers before mitm activation.
    # Now we assume that container is already deployed manually
    try:
        devices.mitm.start_capture(env_helper.get_mitm_devices())
    except AttributeError:
        raise CodeError("No MITM device found in device manager")
    except KeyError as e:
        raise CodeError(str(e))
    logged["boot_step"] = "mitm_ok"


def boot(config, env_helper, devices, logged=None):
    cfg = env_helper.get_prov_mode()
    ertr_mode = env_helper.get_ertr_mode()
    country = env_helper.get_country()
    voice = env_helper.voice_enabled()
    mitm_present = env_helper.mitm_enabled()
    tr069check = cfg not in ["disabled", "bridge", "none"]
    tr069provision = env_helper.get_tr069_provisioning()
    mta_mibs = env_helper.get_mta_config()
    config_template = env_helper.get_emta_config_template()

    if logged is None:
        logged = dict()

    logged["boot_step"] = "env_ok"
    gui_password = None

    # the following if should not be here
    sw = env_helper.get_software()
    if sw.get("image_uri", None) and "rdkb" in sw["image_uri"]:
        ertr_mode.update({"max_config": False})
        ertr_mode.update({"favour_tlvs": True})
        ertr_mode.update({"rdkb": True})
        devices.board.lan_iface = "brlan0"
        devices.board._build_arm_ifaces_list(lan_i=devices.board.lan_iface)
        devices.board.tr069_agent = "CcspTr069PaSsp"
        devices.board.unsupported_objects = [
            "Device.IP.Diagnostics.DownloadDiagnostics."
        ]
        # Remove "# " from arm prompts
        if "# " in devices.board.arm.prompt:
            devices.board.arm.prompt.remove("# ")
        gui_password = "password"

    devices.board.cm_cfg = devices.board.generate_cfg(cfg, None, ertr_mode)
    logged["boot_step"] = "cmcfg_ok"

    if config_template:
        # TODO: Yet to implement country specific emta config file from template
        warnings.warn(
            "Currently framework only supports country NL, Hence booting with NL specific MTA config file"
        )
    devices.board.mta_cfg = devices.board.generate_mta_cfg(
        country, snmp_mib_obj=mta_mibs
    )
    logged["boot_step"] = "mtacfg_ok"

    # TODO: why is this required? need to fix globally
    devices.board.config["cm_cfg"] = devices.board.cm_cfg

    if voice:
        try:
            sipserver = devices.sipcenter
            sipserver.kill_asterisk()
            dns_setup_sipserver(sipserver, config)
            voice_devices_list = [
                sipserver,
                devices.softphone,
                devices.lan,
                devices.lan2,
            ]
            voice_devices_configure(voice_devices_list, devices.sipcenter)
        except Exception as e:
            print("\n\nFailed to configure voice setup")
            print(e)
            raise VoiceSetupConfigureFailure
        logged["boot_step"] = "voice_ok"
    else:
        logged["boot_step"] = "voice_skipped"

    check_devs = True
    try:
        boardfarm.lib.booting.boot(
            config,
            env_helper,
            devices,
            reflash=True,
            logged=logged,
            flashing_image=False,
        )
        devices.board.enable_logs(component="pacm")

        if mitm_present:
            activate_mitm(devices, env_helper, logged)

        if voice:
            devices.board.wait_for_mta_provisioning()
            logged["boot_step"] = "voice_mta_ok"
            devices.board.enable_logs(component="voice")

        if tr069check:
            for _ in range(20):
                try:
                    devices.board.get_cpeid()
                    break
                except Exception as e:
                    print(e)
                    warnings.warn("Failed to connect to ACS, retrying")
                    time.sleep(10)
            else:
                raise BootFail("Failed to connect to ACS")

            if tr069provision:
                reset_val = env_helper.get_software().get("factory_reset", False)
                if reset_val:
                    for i in tr069provision:
                        for acs_api in i:
                            API_func = getattr(devices.acs_server, acs_api)
                            for param in i[acs_api]:
                                API_func(param)
                else:
                    raise BootFail(
                        "Factory reset has to performed for tr069 provisioning. Env json with factory reset true should be used."
                    )
        if gui_password:
            if not devices.board.trigger_dmcli_cmd(
                operation="setvalues",
                param="Device.Users.User.3.X_CISCO_COM_Password",
                value_for_set=gui_password,
            ):
                raise BootFail("Failed to set the GUI password via dmcli")

        check_devs = False
    except NoTFTPServer as e:
        raise e
    except Exception as e:
        print("\n\nFailed to Boot")
        print(e)
        raise BootFail
    finally:
        if check_devs:
            check_devices(devices)
