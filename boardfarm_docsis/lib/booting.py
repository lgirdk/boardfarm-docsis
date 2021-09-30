import logging
import time
import traceback
import warnings

import boardfarm.lib.booting
import boardfarm.lib.voice
from boardfarm.devices.debian_lan import DebianLAN
from boardfarm.exceptions import (
    BootFail,
    CodeError,
    DeviceDoesNotExistError,
    NoTFTPServer,
)
from boardfarm.library import check_devices
from packaging.version import Version
from termcolor import colored

from boardfarm_docsis.devices.base_devices.board import DocsisCPE
from boardfarm_docsis.lib.booting_utils import (
    activate_mitm,
    check_and_connect_to_wifi,
    register_fxs_details,
)
from boardfarm_docsis.lib.dns_helper import dns_acs_config
from boardfarm_docsis.use_cases.provision_helper import provision_board

logger = logging.getLogger("bft")


def pre_boot_wan_clients(config, env_helper, devices):
    if env_helper.get_dns_dict():
        # to get reachable and unreachable ips for ACS DNS
        devices.wan.auth_dns = True
        dns_acs_config(devices, env_helper.get_dns_dict())

    tftp_device, tftp_servers = boardfarm.lib.booting.get_tftp(config)
    if not tftp_servers:
        logger.error(colored("No tftp server found", color="red", attrs=["bold"]))
        # currently we must have at least 1 tftp server configured
        raise NoTFTPServer
    if len(tftp_servers) > 1:
        msg = f"Found more than 1 tftp server: {tftp_servers}, using {tftp_device.name}"
        logger.error(colored(msg, color="red", attrs=["bold"]))
        raise CodeError(msg)

    # should we run configure for all the wan devices? or just wan?
    for x in devices:
        # if isinstance(x, DebianWAN): # does not work for mitm
        if hasattr(x, "name") and "wan" in x.name:
            logger.info(f"Configuring {x.name}")
            x.configure(config=config)
    # if more than 1 tftp server should we start them all?
    # currently starting the 1 being used
    logger.info(f"Starting TFTP server on {tftp_device.name}")
    tftp_device.start_tftp_server()
    devices.board.tftp_device = tftp_device


def pre_boot_lan_clients(config, env_helper, devices):
    for x in devices.lan_clients:
        if isinstance(x, DebianLAN):
            logger.info(f"Configuring {x.name}")
            x.configure()


def pre_boot_wlan_clients(config, env_helper, devices):
    for x in getattr(devices, "wlan_clients", []):
        logger.info(f"Configuring {x.name}")
        x.configure()


def pre_boot_board(config, env_helper, devices):
    env_cwmp_v = env_helper.get_cwmp_version()
    if env_cwmp_v:
        assert Version(env_cwmp_v) == Version(
            devices.board.cwmp_version()
        ), f"CWMP version mismatch, Expected version {env_cwmp_v}"


def pre_boot_env(config, env_helper, devices):
    # this should take care of provisioner/tr069/voice/etc
    # depending on what the env_helperd has configured
    if env_helper.mitm_enabled() and not hasattr(devices, "mitm"):
        raise DeviceDoesNotExistError("No mitm device (requested by environment)")

    cm_boot_file = None
    mta_boot_file = None
    if env_helper.has_board_boot_file():
        cm_boot_file = env_helper.get_board_boot_file()
    if env_helper.has_board_boot_file_mta():
        mta_boot_file = env_helper.get_board_boot_file_mta()
    devices.board.env_config(cm_boot_file, mta_boot_file, devices.board.mibs_path)

    if env_helper.voice_enabled():
        dev_list = [
            devices.sipcenter,
            devices.softphone,
        ] + getattr(devices, "FXS", [devices.lan, devices.lan2])
        if env_helper.get_external_voip():
            dev_list.append(devices.softphone2)
        boardfarm.lib.voice.voice_configure(
            dev_list,
            devices.sipcenter,
            config,
        )

    prov = getattr(config, "provisioner", None)
    if prov:
        if env_helper.vendor_encap_opts(ip_proto="ipv4"):
            devices.provisioner.vendor_opts_acsv4_url = True
        if env_helper.vendor_encap_opts(ip_proto="ipv6"):
            devices.provisioner.vendor_opts_acsv6_url = True
        logger.info("Provisioning board")
        provision_board()
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
    "wan_clients_pre_boot": pre_boot_wan_clients,
    "lan_clients_pre_boot": pre_boot_lan_clients,
    "wlan_clients_pre_boot": pre_boot_wlan_clients,
    "board_pre_boot": pre_boot_board,
    "environment_pre_boot": pre_boot_env,
}


def boot_board(config, env_helper, devices):
    try:
        devices.board.reset()
        if env_helper.get_software():
            devices.board.flash(env_helper)
            # store the timestamp, for uptime check later (in case the board
            # crashes on boot)
            devices.board.__reset__timestamp = time.time()
            devices.cmts.clear_cm_reset(devices.board.cm_mac)
            time.sleep(20)
    except Exception as e:
        logger.critical(colored("\n\nFailed to Boot", color="red", attrs=["bold"]))
        logger.error(e)
        raise BootFail


boot_actions = {"board_boot": boot_board}


def post_boot_board(config, env_helper, devices):

    for _ in range(180):
        if devices.cmts.is_cm_online(ignore_partial=True) is False:
            # show the arm prompt as it is a log in itself
            devices.board.touch()
            time.sleep(15)
            continue
        if devices.board.finalize_boot():
            break
        else:
            devices.board.wait_for_reboot(timeout=900)
            logger.info("######Rebooting######")
            devices.cmts.clear_cm_reset(devices.board.cm_mac)
            time.sleep(20)

    else:
        msg = "\n\nFailed to Boot: board not online on CMTS"
        logger.critical(msg)
        raise BootFail(msg)
    devices.board.post_boot_init()
    board_uptime = devices.board.get_seconds_uptime()
    logger.info(f"Time up: {board_uptime}")
    if hasattr(devices.board, "__reset__timestamp"):
        time_elapsed = time.time() - devices.board.__reset__timestamp
        logger.info(f"Time since reboot: {time_elapsed}")
        if time_elapsed < board_uptime:
            # TODO: the following should be an exception and not
            # just a print!!!!
            logger.warning("Error: possibly the board did not reset!")
        if (time_elapsed - board_uptime) > 60:
            logger.warning(
                colored(
                    "Board may have rebooted multiple times after flashing process",
                    color="yellow",
                    attrs=["bold"],
                )
            )
    if isinstance(devices.board, DocsisCPE):
        pass  # maybe new method to be added
    else:
        # the old way for legacy
        devices.board.check_valid_docsis_ip_networking(strict=False)


def post_boot_wan_clients(config, env_helper, devices):
    pass


def post_boot_lan_clients(config, env_helper, devices):
    for i, v in enumerate(devices.board.dev.lan_clients):
        if getattr(env_helper, "has_lan_advertise_identity", None):
            for option in ["125", "17"]:
                if env_helper.has_lan_advertise_identity(i):
                    v.configure_dhclient(([option, True],))
                else:
                    v.configure_dhclient(([option, False],))
    if devices.board.routing and config.setup_device_networking:
        for x in devices.board.dev.lan_clients:
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
    wifi_clients = env_helper.wifi_clients()
    if wifi_clients:

        # Register all wifi clients in wifi manager
        for client in wifi_clients:
            devices.wlan_clients.register(client)

        # Start to connect all clients after registartions done:
        for client in wifi_clients:
            check_and_connect_to_wifi(devices, client)

        logger.info(colored("\nWlan clients:", color="green"))
        devices.wlan_clients.registered_clients_summary()


def post_boot_env(config, env_helper, devices):
    if env_helper.mitm_enabled():
        activate_mitm(devices, env_helper.get_mitm_devices())

    eMTA_iface_status = env_helper.get_emta_interface_status()
    if eMTA_iface_status:
        devices.board.set_eMTA_interface(devices.board.mta_iface, eMTA_iface_status)
    if env_helper.voice_enabled() and eMTA_iface_status != "down":
        devices.board.wait_for_mta_provisioning()
        register_fxs_details(getattr(devices, "FXS", []), devices.board)

    cfg = env_helper.get_prov_mode()
    tr069check = cfg not in ["disabled", "bridge", "none"]
    tr069provision = env_helper.get_tr069_provisioning()
    if tr069check:
        for _ in range(20):
            try:
                devices.board.get_cpeid()
                break
            except Exception as e:
                logger.error(e)
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
    if hasattr(devices.board, "post_boot_env"):
        devices.board.post_boot_env()


post_boot_actions = {
    "board_post_boot": post_boot_board,
    "wan_clients_post_boot": post_boot_wan_clients,
    "lan_clients_post_boot": post_boot_lan_clients,
    "environment_post_boot": post_boot_env,
    "wlan_clients_connection": post_boot_wlan_clients,
}


def run_actions(actions_dict, actions_name, *args, **kwargs):
    logger.info(colored(f"{actions_name} ACTIONS", color="green", attrs=["bold"]))
    for key, func in actions_dict.items():
        try:
            logger.info(colored(f"Action {key} start", color="green", attrs=["bold"]))
            start_time = time.time()
            func(*args, **kwargs)
            logger.info(
                colored(
                    f"\nAction {key} completed. Took {int(time.time() - start_time)} seconds to complete.",
                    color="green",
                    attrs=["bold"],
                )
            )
        except Exception as e:
            msg = f"\nFailed at: {actions_name}: {key} after {int(time.time() - start_time)} seconds with exception {e}"
            logger.error(colored(msg, color="red", attrs=["bold"]))
            raise e
    logger.info(colored(f"{actions_name} COMPLETED", color="green", attrs=["bold"]))


def boot(config, env_helper, devices, logged=None, actions_list=None):
    start_time = time.time()
    if not actions_list:
        actions_list = ["pre", "boot", "post"]
    try:
        if "pre" in actions_list:
            run_actions(pre_boot_actions, "PRE-BOOT", config, env_helper, devices)
        if "boot" in actions_list:
            run_actions(boot_actions, "BOOT", config, env_helper, devices)
        if "post" in actions_list:
            run_actions(post_boot_actions, "POST-BOOT", config, env_helper, devices)
        logger.info(
            colored(
                f"Boot completed in {int(time.time() - start_time)} seconds.",
                color="green",
                attrs=["bold"],
            )
        )
    except Exception:
        traceback.print_exc()
        check_devices(devices)
        logger.info(
            colored(
                f"Boot failed after {int(time.time() - start_time)} seconds.",
                color="red",
                attrs=["bold"],
            )
        )
        raise
