import logging
import time

from boardfarm.lib.DeviceManager import get_device_by_name
from termcolor import colored

logger = logging.getLogger("bft")


def wait_for_board_boot_start():
    board = get_device_by_name("board")
    board.wait_for_boot()


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
    board.post_boot_init()
    board.post_boot_env()

    logger.warning(
        colored(
            "This must be removed once OFW-2175 is fixed",
            color="yellow",
            attrs=["bold"],
        )
    )
    if board.env_helper.get_prov_mode().lower() in ["dslite", "ipv6"]:
        for _ in range(45):
            if has_ipv6_tunnel_interface_address():
                break
            time.sleep(20)
        else:
            msg = f"\n\nFailed to fetch {board.aftr_iface} interface in IPV6 mode even after 15 min of successful reboot"
            logger.warning(colored(msg, color="yellow", attrs=["bold"]))
            return False
    return True


def has_ipv6_tunnel_interface_address() -> bool:
    """Check for the tunnel interface on DUT console

    :return: True if tunnel interface is present else False
    :rtype: bool
    """
    board = get_device_by_name("board")
    try:
        iptunv6 = board.get_interface_ip6addr(board.aftr_iface)
        return True if iptunv6 else False
    except Exception as e:
        logger.warning(
            colored(
                f"Interface check failed.\nReason: {e}", color="yellow", attrs=["bold"]
            )
        )
        return False
