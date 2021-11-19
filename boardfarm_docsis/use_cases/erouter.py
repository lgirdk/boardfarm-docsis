import ipaddress
import logging
from typing import Callable, List, Optional

from boardfarm.exceptions import BftIfaceNoIpV6Addr, PexpectErrorTimeout
from boardfarm.lib.common import retry_on_exception
from boardfarm.lib.DeviceManager import get_device_by_name
from boardfarm.use_cases.networking import IPAddresses
from termcolor import colored

logger = logging.getLogger("bft")


def _get_erouter_ip(
    get_ip_method: Callable, board_interface: List[str], retry_count: int
) -> Optional[str]:
    """Utility to get ip address based on get_ip_method

    :param get_ip_method: function to be be called to get ip
    :type get_ip_method: Callable
    :param board_interface: board erouter interface
    :type board_interface: list[str]
    :param retry_count: number of retries on failure to get ip
    :type retry_count: int
    :return: None if no ip found, ip string otherwise.
    :rtype: Optional[str]
    """
    ip_addr = None
    try:
        ip_addr = retry_on_exception(
            get_ip_method,
            board_interface,
            retry_count,
        )
    except (PexpectErrorTimeout, BftIfaceNoIpV6Addr):
        msg = "\n\nFailed to get ip address"
        logger.warning(colored(msg, color="yellow", attrs=["bold"]))
    if ip_addr:
        ipaddress.ip_address(ip_addr)
    return ip_addr


def get_erouter_addresses(retry_count: int) -> IPAddresses:
    """Get erouter ip addresses ipv4, ipv6

    :param retry_count: number of retries to get ips
    :type retry_count: int
    :return: erouter ip addresses data class
    :rtype ErouterIPs
    """
    board = get_device_by_name("board")

    # get ipv4 address if assigned to erouter
    ipv4 = _get_erouter_ip(
        board.get_interface_ipaddr, [board.erouter_iface], retry_count
    )

    # get ipv6 address if assigned to erouter
    ipv6 = _get_erouter_ip(
        board.get_interface_ip6addr, [board.erouter_iface], retry_count
    )

    return IPAddresses(ipv4=ipv4, ipv6=ipv6)
