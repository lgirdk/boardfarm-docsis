import inspect
from typing import Optional

from boardfarm.lib.DeviceManager import device_manager


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
