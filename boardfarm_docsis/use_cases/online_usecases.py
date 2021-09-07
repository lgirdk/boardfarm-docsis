import logging
import time

from boardfarm.lib.DeviceManager import get_device_by_name
from termcolor import colored

logger = logging.getLogger("bft")


def is_board_online_after_reset() -> bool:
    """Check board online after reset

    :return: True if board is online else false
    :rtype: bool
    """
    board = get_device_by_name("board")
    cmts = get_device_by_name("cmts")

    for _ in range(180):
        if cmts.is_cm_online(ignore_partial=True) is False:
            board.touch()
            time.sleep(15)
            continue
        if board.finalize_boot():
            break
        board.wait_for_reboot(timeout=900)
        logger.info("######Rebooting######")
        cmts.clear_cm_reset(board.cm_mac)
        time.sleep(20)

    else:
        msg = "\n\nFailed to Boot: board not online on CMTS"
        logger.warning(colored(msg, color="yellow", attrs=["bold"]))
        return False

    return True