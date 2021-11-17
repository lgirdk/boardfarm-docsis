import inspect
from typing import Optional

from boardfarm.exceptions import CodeError
from boardfarm.lib.DeviceManager import device_manager, get_device_by_name


def provision_board():
    dev = device_manager()
    if hasattr(dev.board, "hw") and hasattr(dev.board, "sw"):
        cm_cfg, mta_cfg = dev.board.hw.reprovision(dev.provisioner)
        for cfg in [cm_cfg, mta_cfg]:
            _push_to_tftp_server(cfg, dev.wan)
        dev.provisioner.provision_board(dev.board.config)
    else:
        dev.board.reprovision(dev.provisioner)


def provision_board_boot_file(
    cm_boot_file: Optional[str] = None,
    mta_boot_file: Optional[str] = None,
):
    dev = device_manager()
    if not cm_boot_file and dev.board.env_helper.has_board_boot_file():
        cm_boot_file = dev.board.env_helper.get_board_boot_file()
    if not mta_boot_file and dev.board.env_helper.has_board_boot_file_mta():
        mta_boot_file = dev.board.env_helper.get_board_boot_file_mta()

    if inspect.isclass(dev.board.cm_cfg):
        dev.board.env_config(cm_boot_file, mta_boot_file, dev.board.mibs_path)
    else:
        dev.board.hw.cm_cfg.load_from_string(cm_str_txt=cm_boot_file)
        dev.board.hw.cm_cfg.init_copy(dev.board.hw.cm_cfg)
    provision_board()


def _push_to_tftp_server(cfg, server):
    server.copy_file_to_server(cfg)


def _get_board_boot_logs(timeout: int) -> str:
    """Gets the console log for the boot process.

    :param timeout: time value to collect the logs for
    :type timeout: int
    :return: Console Logs
    :rtype: str
    """
    board = get_device_by_name("board")
    return board.get_board_logs(timeout)


def _verify_cm_config_downloaded(boot_logs: str) -> bool:
    """Verify if the CM config download is successful

    :param boot_logs: The console logs collected post reboot
    :type boot_logs: str
    :return: True if CM config download is successful else false
    :rtype: bool
    """
    board = get_device_by_name("board")
    return all(
        [
            message in boot_logs
            for message in board.provisioning_messages["verify_cm_cfg_file_download"]
        ]
    )


def _verify_emta_config_downloaded(boot_logs: str) -> bool:
    """Verify if the MTA config download is successful

    :param boot_logs: The console logs collected post reboot
    :type boot_logs: str
    :return: True if MTA config download is successful else false
    :rtype: bool
    """
    board = get_device_by_name("board")
    return board.provisioning_messages["verify_emta_cfg_file_download"] in boot_logs


def _verify_emta_config_applied(boot_logs: str) -> bool:
    """Verify if the MTA config is applied successfully

    :param boot_logs: The console logs collected post reboot
    :type boot_logs: str
    :return: True if MTA config is applied successfully else false
    :rtype: bool
    """
    board = get_device_by_name("board")
    return board.provisioning_messages["verify_emta_config_apply"] in boot_logs


def _verify_emta_provisioning(boot_logs: str) -> bool:
    """Verify if the MTA provisioning is successful

    :param boot_logs: The console logs collected post reboot
    :type boot_logs: str
    :return: True if MTA provisioning is successful else false
    :rtype: bool
    """
    board = get_device_by_name("board")
    return board.provisioning_messages["verify_emta_provisioning"] in boot_logs


def verify_boot_stages_and_provisioning(timeout: int) -> bool:
    """Collect the boot logs and validate the boot stages and provisioning

    :param timeout: time value to collect the logs for
    :type timeout: int
    :return: True if boot stages are verified and provisioning is successful else false
    :rtype: bool
    """
    board = get_device_by_name("board")
    try:
        board.hw.wait_for_hw_boot()
    except Exception:
        raise CodeError("Board Reboot not performed")
    log = _get_board_boot_logs(timeout)
    return all(
        [
            _verify_cm_config_downloaded(log),
            _verify_emta_config_downloaded(log),
            _verify_emta_config_applied(log),
            _verify_emta_provisioning(log),
        ]
    )
