"""Use Cases to handle getting the CPE online."""

from __future__ import annotations

import logging
import time
from typing import TYPE_CHECKING

from boardfarm3.exceptions import UseCaseFailure
from boardfarm3.lib.device_manager import get_device_manager
from boardfarm3.lib.utils import retry_on_exception
from boardfarm3.templates.cpe import CPE
from boardfarm3.templates.wan import WAN
from boardfarm3.use_cases.device_getters import device_getter
from boardfarm3.use_cases.networking import http_get
from termcolor import colored

from boardfarm3_docsis.templates.cable_modem import CableModem
from boardfarm3_docsis.templates.cmts import CMTS
from boardfarm3_docsis.use_cases.erouter import get_erouter_addresses

if TYPE_CHECKING:
    from boardfarm3.lib.custom_typing.cpe import CPEInterfaces, HostInterfaces
    from boardfarm3.templates.aftr import AFTR
    from boardfarm3.templates.lan import LAN
    from boardfarm3.templates.wlan import WLAN


_LOGGER = logging.getLogger(__name__)


def wait_for_board_boot_start(board: CPE | None = None) -> None:
    """Wait for the board boot to start.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Verify that DUT comes online.

    The usage if this directly in the test would be depecrated in favour of
    power_cycle() as it would handle both board turn OFF and ON
    and wait for board boot to start

    :param board: the board object, defaults to None
    :type board: CPE | None, optional
    """
    if board is None:
        board = get_device_manager().get_device_by_type(CPE)  # type: ignore[type-abstract]
    board.hw.wait_for_hw_boot()


def power_cycle(board: CPE | None = None) -> None:
    """Power cycle the board.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Perform a reboot on the CPE
        - Reboot the DUT
        - Do power cycle of DUT

    Turn OFF and turn ON the board and wait for the boot to start
    This method is preferred to wait_for_board_boot_start as the power cycle
    and wait for the board boot is handled in this use case

    :param board: the board object, defaults to None
    :type board: CPE | None, optional
    """
    if board is None:
        board = get_device_manager().get_device_by_type(CPE)  # type: ignore[type-abstract]
    board.hw.power_cycle()
    wait_for_board_boot_start(board=board)


def is_board_online_after_reset() -> bool:
    """Check board online after reset.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Verify CPE comes online after the factory reset
        - Verify DUT comes back online

    :return: True if board is online else false
    :rtype: bool
    """
    # TODO: rework
    board = None
    termination_sys: CMTS = None
    cpe = get_device_manager().get_device_by_type(CPE)  # type: ignore[type-abstract]
    if hasattr(cpe, "cm_mac"):
        board = get_device_manager().get_device_by_type(
            CableModem,  # type: ignore[type-abstract]
        )
        termination_sys = get_device_manager().get_device_by_type(
            CMTS,  # type: ignore[type-abstract]
        )
        termination_sys.reset_cable_modem_status(mac_address=board.hw.mac_address)

    for _ in range(180):
        if termination_sys:
            if not termination_sys.is_cable_modem_online(
                mac_address=board.cm_mac,
                ignore_partial=True,
            ):
                time.sleep(15)
                continue
        elif not cpe.sw.is_online():
            time.sleep(15)
            continue

        if cpe.sw.finalize_boot():
            break
        _LOGGER.info("######Rebooting######")
        if termination_sys:
            termination_sys.clear_cm_reset(board.cm_mac)
        time.sleep(20)

    else:
        msg = "\n\nFailed to Boot: board not online on CMTS"
        _LOGGER.warning(colored(msg, color="yellow", attrs=["bold"]))
        return False
    applist = cpe.config.get("install_applications", [])
    if applist:
        wan_server = get_device_manager().get_device_by_type(
            WAN,  # type: ignore[type-abstract]
        )
        if hasattr(cpe.sw, "login_to_linux_consoles"):
            retry_on_exception(cpe.sw.login_to_linux_consoles, (), 3, 20)
        cpe.sw.install_app_via_wan(wan_server, applist)  # type: ignore [attr-defined]

    return True


def has_ipv6_tunnel_interface_address(board: CPE | None = None) -> bool:
    """Check for the tunnel interface on DUT console.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Check for the tunnel interface on DUT console.

    :param board: the board object, defaults to None
    :type board: CPE | None, optional
    :return: True if tunnel interface is present else False
    :rtype: bool
    """
    if board is None:
        board = get_device_manager().get_device_by_type(CPE)  # type: ignore[type-abstract]
    try:
        iptunv6 = board.sw.get_interface_ipv6addr(board.sw.aftr_iface)
        return bool(iptunv6)
    except ValueError as exc:
        _LOGGER.warning(
            colored(
                f"Interface check failed.\nReason: {exc}",
                color="yellow",
                attrs=["bold"],
            ),
        )
        return False


def is_wan_accessible_on_client(
    who_access: LAN,
    port: int,
    is_ipv6: bool = False,
    wan: WAN | None = None,
) -> bool:
    """Ping the WAN IP address max with 2 retries from the lan/wifi client.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Check that the connected LAN client is able to access the internet
        - Verify LAN Client is able to reach the internet

    :param who_access: name of the client who wants to ping wan side
    :type who_access: LAN
    :param port: port to which to perform the curl on wan client
    :type port: int
    :param is_ipv6: whether to ping ipv4 or ipv6 address for wan
    :type is_ipv6: bool
    :param wan: WAN client to be pinged
    :type wan: WAN | None
    :return: True if ping returns a success
    :rtype: bool
    """
    if wan is None:
        wan = device_getter(WAN)  # type: ignore[type-abstract]
    ip_addr = (
        wan.get_eth_interface_ipv4_address()
        if not is_ipv6
        else f"[{wan.get_eth_interface_ipv6_address()}]"
    )
    return bool(http_get(who_access, f"{ip_addr}:{port}"))


def get_interface_status(
    device: LAN | WAN | CPE,  # TODO: missing wifi
    interface: CPEInterfaces | HostInterfaces,
) -> bool:
    """Return the status of the Linux interface.

    If the interface link is up or down on the device.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Check that the [] interface is up

    :param device: device class object
    :type device: LAN | WAN | CPE
    :param interface: enum for possible values for interfaces definition
    :type interface: CPEInterfaces | HostInterfaces | PONCPEInterface
    :raises UseCaseFailure: when device doesn't have attribute mapped in enum
    :return: True if interface is up else False
    :rtype: bool
    """
    try:
        if isinstance(device, CPE):
            # TODO: check interfaces on SW component
            return bool(device.sw.is_link_up(getattr(device.sw, interface.value)))
        return bool(device.is_link_up(getattr(device, interface.value)))
    except AttributeError as exc:
        msg = f"{device} object does not have {interface.value} as its instance"
        raise UseCaseFailure(msg) from exc


def reset_board_via_cmts(board: CPE, cmts: CMTS) -> None:
    """Reset the board via CMTS.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Reset the board via CMTS.

    :param board: cpe device instance
    :type board: CPE
    :param cmts: cmts device instance
    :type cmts: CMTS
    """
    cmts.clear_cm_reset(board.hw.mac_address)


def get_subnet_mask(device: LAN | WAN | WLAN, interface: str) -> str:
    """Get the subnet mask of the interface.

    :param device: device instance
    :type device: LAN | WAN | WLAN
    :param interface: name of the inerface
    :type interface: str
    :return: subnet mask of the interface
    :rtype: str
    """
    return device.get_interface_mask(interface)


def get_interface_mtu_size(device: CPE | LAN | WAN | WLAN, interface: str) -> int:
    """Return the MTU size of the interface in bytes.

    :param device: device instance
    :type device: CPE | LAN | WAN | WLAN
    :param interface: name of the interface
    :type interface: str
    :return: MTU size of the interface in bytes
    :rtype: int
    """
    if isinstance(device, CPE):
        return device.sw.get_interface_mtu_size(interface)
    return device.get_interface_mtu_size(interface)


def enable_tunnel_iface(
    aftr: AFTR, board: CPE | None = None, wan: WAN | None = None
) -> None:
    """Enable tunnel iface by configuring AFTR post mode switch.

    .. hint:: This use case to be used:

        - When modem reprovisioning is done with ipv6 mode.

        Note: not to be used if board is booted with ipv6 mode.

    :param aftr: AFTR device instance
    :type aftr: AFTR
    :param board: cpe device instance, defaults to None
    :type board: CPE, optional
    :param wan: WAN client, defaults to None
    :type wan: WAN, optional
    """
    if board is None:
        board = get_device_manager().get_device_by_type(
            CPE  # type: ignore[type-abstract]
        )
    if wan is None:
        wan = get_device_manager().get_device_by_type(
            WAN,  # type: ignore[type-abstract]
        )
    erouter_ips = get_erouter_addresses(board=board, retry_count=1)
    if erouter_ips.ipv6 and not erouter_ips.ipv4:
        aftr.configure_aftr(wan=wan)
        aftr.restart_aftr_process(wan=wan)
