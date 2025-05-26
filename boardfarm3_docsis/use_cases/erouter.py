"""eRouter use cases."""

from __future__ import annotations

import ipaddress
import logging
from ipaddress import IPv4Address, IPv6Address
from typing import TYPE_CHECKING, Callable

from boardfarm3.lib.dataclass.interface import IPAddresses
from boardfarm3.lib.utils import retry_on_exception
from pexpect import TIMEOUT

if TYPE_CHECKING:
    from boardfarm3.templates.cpe import CPE

_LOGGER = logging.getLogger(__name__)


def _get_ip_from_board(
    get_ip_method: Callable,
    board_interface: list[str],
    retry_count: int,
) -> IPv4Address | IPv6Address | None:
    """Get IP address based on get_ip_method.

    :param get_ip_method: function to be be called to get IP
    :type get_ip_method: Callable
    :param board_interface: board eRouter interface
    :type board_interface: list[str]
    :param retry_count: number of retries on failure to get IP
    :type retry_count: int
    :return: None if no IPv4 or IPv6 found, IP string otherwise.
    :rtype: IPv4Address | IPv6Address | None
    """
    ip_addr = None
    try:
        ip_addr = retry_on_exception(
            get_ip_method,
            board_interface,
            retry_count,
        )
    except (TIMEOUT, ValueError):
        _LOGGER.warning("Failed to get IP address")
    if ip_addr:
        return ipaddress.ip_address(ip_addr)
    return ip_addr


def get_erouter_addresses(retry_count: int, board: CPE) -> IPAddresses:
    """Get erouter IPv4, IPv6 addresses.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Check if eRouter gets an IP address.
        - Check if the eRouter WAN Interface acquires IPv4 and IPv6 address

    :param retry_count: number of retries to get IPs
    :type retry_count: int
    :param board: CPE device instance
    :type board: CPE
    :return: erouter IP addresses data class
    :rtype: IPAddresses
    """
    return _get_ip_addresses(board, [board.sw.erouter_iface], retry_count)


def _get_ip_addresses(board: CPE, interfaces: list[str], retry: int = 1) -> IPAddresses:
    """Get the IP addresses of given list of interface names.

    :param board: CPE device instance
    :type board: CPE
    :param interfaces: list of the interfaces
    :type interfaces: list[str]
    :param retry: number of retry, defaults to 1
    :type retry: int
    :return: IP addresses of the interfaces
    :rtype: IPAddresses
    """
    # get IPv4 address
    ipv4 = _get_ip_from_board(board.sw.get_interface_ipv4addr, interfaces, retry)

    # get IPv6 address
    ipv6 = _get_ip_from_board(board.sw.get_interface_ipv6addr, interfaces, retry)

    # get link_local IPv6 address
    link_local_ipv6 = _get_ip_from_board(
        board.sw.get_interface_link_local_ipv6_addr,
        interfaces,
        retry,
    )

    return IPAddresses(
        ipv4=ipv4,  # type: ignore[arg-type]
        ipv6=ipv6,  # type: ignore[arg-type]
        link_local_ipv6=link_local_ipv6,  # type: ignore[arg-type]
    )


def verify_erouter_ip_address(mode: str, board: CPE, retry: int = 1) -> bool:
    """Verify the eRouter interface has the correct IP addresses for the specified mode.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Verify eRouter gets an IP address.
        - Check if the eRouter WAN Interface acquires IPv4 and/or IPv6 address

    :param mode: mode could be IPv4, IPv6/DSLite, Dual, disabled/bridge/modem
    :type mode: str
    :param board: CPE device instance
    :type board: CPE
    :param retry: number of retries in order to fetch the erouter IP, defaults to 1
    :type retry: int
    :return: True if the eRouter has correct IPv4/IPv6 address based on the mode passed
    :rtype: bool
    """
    erouter_ips = get_erouter_addresses(board=board, retry_count=retry)
    ipv4, ipv6, local_ipv6 = (
        erouter_ips.ipv4,
        erouter_ips.ipv6,
        erouter_ips.link_local_ipv6,
    )
    if board.hw.config["type"] in ["TG2492LG", "CH7465LG"] and mode not in [
        "ipv4",
        "ipv6",
        "dual",
        "dslite",
    ]:
        return bool(not local_ipv6 and not ipv4 and not ipv6)

    return bool(
        (mode == "ipv4" and ipv4 and not ipv6)
        or (mode == "ipv6" and ipv6 and local_ipv6 and not ipv4)
        or (mode == "dual" and ipv4 and ipv6)
        or (mode in {"ipv6", "dslite"} and ipv6 and local_ipv6 and not ipv4)
        or (
            mode not in ("ipv4", "ipv6", "dual", "dslite")
            and local_ipv6
            and not ipv4
            and not ipv6
        )
    )


def get_board_lan_ip_address(board: CPE, retry_count: int) -> IPAddresses:
    """Get the board's LAN IP addresses.

    :param board: instance of CPE
    :type board: CPE
    :param retry_count: number of retries
    :type retry_count: int
    :return: IPAddress of LAN interface
    :rtype: IPAddresses
    """
    return _get_ip_addresses(board, [board.sw.lan_iface], retry_count)


def get_wan_iface_ip_addresses(board: CPE, retry_count: int) -> IPAddresses:
    """Get the management interface IP addresses.

    :param board: CPE device instance
    :type board: CPE
    :param retry_count: number of retries
    :type retry_count: int
    :return: IP addresses of management interface
    :rtype: IPAddresses
    """
    return _get_ip_addresses(board, [board.hw.wan_iface], retry_count)


def get_mta_iface_ip_addresses(board: CPE, retry_count: int) -> IPAddresses:
    """Get the voice interface IP addresses.

    :param board: CPE device instance
    :type board: CPE
    :param retry_count: number of retries
    :type retry_count: int
    :return: IP addresses of voice interface
    :rtype: IPAddresses
    """
    return _get_ip_addresses(board, [board.hw.mta_iface], retry_count)


def get_erouter_iface_ipv6_address(board: CPE) -> IPv6Address:
    """Get eRouter interface IPv6 address.

    :param board: CPE device instance
    :type board: CPE
    :return: IPv6 address of eRouter interface
    :rtype: IPv6Address
    """
    return _get_ip_addresses(board, [board.sw.erouter_iface]).ipv6


def get_board_guest_ip_address(board: CPE, retry_count: int) -> IPAddresses:
    """Get the board's Guest IP addresses.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Verify that the guest interface acquires an IPv4/IPv6 address.

    :param board: instance of CPE
    :type board: CPE
    :param retry_count: number of retries
    :type retry_count: int
    :return: IPAddress of guest interface
    :rtype: IPAddresses
    """
    return _get_ip_addresses(board, [board.sw.guest_iface], retry_count)
