import logging
import time
import traceback
import warnings

import boardfarm.lib.booting
import boardfarm.lib.voice
import pexpect
from boardfarm.devices.debian_lan import DebianLAN
from boardfarm.exceptions import (
    BootFail,
    CodeError,
    DeviceDoesNotExistError,
    NoTFTPServer,
)
from boardfarm.library import check_devices
from termcolor import colored

from boardfarm_docsis.exceptions import VoiceSetupConfigureFailure
from boardfarm_docsis.lib.dns_helper import dns_acs_config

logger = logging.getLogger("bft")


def activate_mitm(devices, env_helper):
    # TODO: Deploy mitm containers before mitm activation.
    # Now we assume that container is already deployed manually
    try:
        devices.mitm.start_capture(env_helper.get_mitm_devices())
    except AttributeError:
        raise CodeError("No MITM device found in device manager")
    except KeyError as e:
        raise CodeError(str(e))


def pre_boot_wan_clients(config, env_helper, devices):
    tftp_device, tftp_servers = boardfarm.lib.booting.get_tftp(config)
    if not tftp_servers:
        logger.error(colored("No tftp server found", color="red", attrs=["bold"]))
        # currrently we must have at least 1 tftp server configured
        raise NoTFTPServer
    if len(tftp_servers) > 1:
        msg = f"Found more than 1 tftp server: {tftp_servers}, using {tftp_device.name}"
        logger.error(colored(msg, color="red", attrs=["bold"]))
        raise CodeError(msg)

    # should we run configure for all the wan devices? or just wan?
    for x in devices:
        # if isinstance(x, DebianWAN): # does not work for mitm
        if "wan" in x.name:
            logger.info(f"Configuring {x.name}")
            x.configure(config=config)
    # if more than 1 tftp server should we start them all?
    # currently starting the 1 being used
    logger.info(f"Starting FTP server on {tftp_device}")
    tftp_device.start_tftp_server()
    devices.board.tftp_device = tftp_device


def pre_boot_lan_clients(config, env_helper, devices):
    for x in devices:
        if isinstance(x, DebianLAN):
            logger.info(f"Configuring {x.name}")
            x.configure()


def pre_boot_wlan_clients(config, env_helper, devices):
    pass


def pre_boot_board(config, env_helper, devices):
    pass


def pre_boot_env(config, env_helper, devices):
    # this should take care of provisioner/tr069/voice/etc
    # depending on what the env_helperd has configured

    if env_helper.mitm_enabled() and not hasattr(devices, "mitm"):
        raise DeviceDoesNotExistError("No mitm device (requested by environment)")

    devices.board.env_config()

    # to get recahbale and unreachable ips for ACS DNS
    dns_acs_config(devices, env_helper.get_dns_dict())

    if env_helper.voice_enabled():
        # could this be moved inside boardfar.lib.voice.voice_devices_configure?
        # and here only invoke
        # voice_devices_configure(voice_devices_list, devices.sipcenter)?
        try:
            sipserver = devices.sipcenter
            sipserver.stop()
            boardfarm.lib.voice.dns_setup_sipserver(sipserver, config)
            sipserver.kill_asterisk()
            boardfarm.lib.voice.dns_setup_sipserver(sipserver, config)
            voice_devices_list = [
                sipserver,
                devices.softphone,
                devices.lan,
                devices.lan2,
            ]
            boardfarm.lib.voice.voice_devices_configure(
                voice_devices_list, devices.sipcenter
            )
        except Exception as e:
            logger.error("\n\nFailed to configure voice setup")
            logger.error(e)
            raise VoiceSetupConfigureFailure
    prov = getattr(config, "provisioner", None)
    if prov:
        logger.info("Provisioning board")
        boardfarm.lib.booting.provision(
            devices.board, prov, devices.wan, devices.board.tftp_device
        )
    else:
        # should this be an error?
        logger.error(
            colored(
                "No provisioner found! Board provisioned skipped",
                color="yellow",
                attrs=["bold"],
            )
        )


pre_boot_actions = {
    "wan_clients": pre_boot_wan_clients,
    "lan_clients": pre_boot_lan_clients,
    "wlan_clients": pre_boot_wlan_clients,
    "board": pre_boot_board,
    "environment": pre_boot_env,
}


def boot_board(config, env_helper, devices):
    try:
        devices.board.reset()
        if env_helper.get_software():
            boardfarm.lib.booting.boot_image(
                config,
                env_helper,
                devices.board,
                devices.lan,
                devices.wan,
                devices.board.tftp_device,
            )
        # store the timestamp, for uptime check later (in case the board
        # crashes on boot)
        devices.board.__reset__timestamp = time.time()
        devices.cmts.clear_cm_reset(devices.board.cm_mac)
        time.sleep(20)
    except Exception as e:
        logger.critical(colored("\n\nFailed to Boot", color="red", attrs=["bold"]))
        logger.error(e)
        raise BootFail


boot_actions = {
    "board": boot_board,
}


def post_boot_board(config, env_helper, devices):
    for _ in range(50):
        if devices.cmts.is_cm_online(ignore_partial=True):
            break
        else:
            # show the arm prompt as it is a log in itself
            devices.board.arm.expect(pexpect.TIMEOUT, timeout=0.5)
            time.sleep(15)
    else:
        msg = "\n\nFailed to Boot: board not online on CMTS"
        logger.critical(msg)
        raise BootFail(msg)
    devices.board.login_atom_root()
    devices.board.login_arm_root()
    devices.board.set_printk()
    board_uptime = devices.board.get_seconds_uptime()
    logger.info(f"Time up: {board_uptime}")
    if hasattr(devices.board, "__reset__timestamp"):
        time_elapsed = time.time() - devices.board.__reset__timestamp
        logger.info(f"Time since reboot: {time_elapsed}")
        if time_elapsed < board_uptime:
            raise BootFail("Error: board did not reset!")
        if (time_elapsed - board_uptime) > 30:
            logger.warning(
                colored(
                    "Board may have rebooted multiple times after flashing process",
                    color="yellow",
                    attrs=["bold"],
                )
            )

    devices.board.check_valid_docsis_ip_networking(strict=False)


def post_boot_wan_clients(config, env_helper, devices):
    pass


def post_boot_lan_clients(config, env_helper, devices):
    for i, v in enumerate(devices.board.dev.lan_clients):
        if getattr(env_helper, "has_lan_advertise_identity", None):
            if env_helper.has_lan_advertise_identity(i):
                v.configure_dhclient((["125", True],))
            else:
                v.configure_dhclient((["125", False],))
    if devices.board.routing and config.setup_device_networking:
        for x in devices:
            if isinstance(x, DebianLAN):  # should this use devices.lan_clients?
                logger.info(f"Starting LAN client on {x.name}")
                for n in range(3):
                    try:
                        x.configure_docker_iface()
                        if (
                            env_helper.get_prov_mode() == "ipv6"
                            and not devices.board.cm_cfg.dslite
                        ):
                            x.start_ipv6_lan_client(wan_gw=devices.wan.gw)
                        else:
                            if env_helper.get_prov_mode() == "dual":
                                x.start_ipv6_lan_client(wan_gw=devices.wan.gw)

                            x.start_ipv4_lan_client(wan_gw=devices.wan.gw)
                        x.configure_proxy_pkgs()
                        break
                    except Exception as e:
                        logger.warning(e)
                        logger.error(
                            colored(
                                f"Failed to start lan client on '{x.name}' device, attempt #{n}",
                                color="red",
                                attrs=["bold"],
                            )
                        )
                        time.sleep(10)
                else:
                    msg = f"Failed to start lan client on {x.name}"
                    logger.warning(colored(msg, color="yellow", attrs=["bold"]))
                    # do not fail the boot with raise BootFail(msg)
                    # reason: the board config may be such that the
                    # clients are not getting an ip (see LLCs)


def post_boot_wlan_clients(config, env_helper, devices):
    pass


def post_boot_env(config, env_helper, devices):
    sku = env_helper.get_board_sku()
    if sku:
        if not devices.board.deploy_board_sku_via_dmcli(sku):
            raise BootFail("Failed to set the SKU via dmcli")

    if env_helper.mitm_enabled():
        activate_mitm(devices, env_helper)
    if env_helper.voice_enabled():
        devices.board.enable_logs(component="pacm")
        devices.board.wait_for_mta_provisioning()
        devices.board.enable_logs(component="voice")
    cfg = env_helper.get_prov_mode()
    tr069check = cfg not in ["disabled", "bridge", "none"]
    tr069provision = env_helper.get_tr069_provisioning()
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
    # should this be here?
    if hasattr(devices.board, "guiPassword"):
        if not devices.board.trigger_dmcli_cmd(
            operation="setvalues",
            param="Device.Users.User.3.X_CISCO_COM_Password",
            value_for_set=devices.board.gui_password,
        ):
            raise BootFail("Failed to set the GUI password via dmcli")


post_boot_actions = {
    "board": post_boot_board,
    "wan_clients": post_boot_wan_clients,
    "lan_clients": post_boot_lan_clients,
    "wlan_clients": post_boot_wlan_clients,
    "environment": post_boot_env,
}


def run_actions(actions_dict, actions_name, *args, **kwargs):
    logger.info(colored(f"{actions_name} ACTIONS", color="green", attrs=["bold"]))
    for key, func in actions_dict.items():
        try:
            logger.info(colored(f"Action {key} start", color="green", attrs=["bold"]))
            func(*args, **kwargs)
            logger.info(
                colored(f"Action {key} completed", color="green", attrs=["bold"])
            )
        except Exception as e:
            msg = f"Failed at: {actions_name}: {key} with exception {e}"
            logger.error(colored(msg, color="red", attrs=["bold"]))
            raise e
    logger.info(colored(f"{actions_name} COMPLETED", color="green", attrs=["bold"]))


def boot(config, env_helper, devices, logged=None, actions_list=None):
    if not actions_list:
        actions_list = ["pre", "boot", "post"]
    try:
        if "pre" in actions_list:
            run_actions(pre_boot_actions, "PRE-BOOT", config, env_helper, devices)
        if "boot" in actions_list:
            run_actions(boot_actions, "BOOT", config, env_helper, devices)
        if "post" in actions_list:
            run_actions(post_boot_actions, "POST-BOOT", config, env_helper, devices)
    except Exception:
        traceback.print_exc()
        check_devices(devices)
        raise
