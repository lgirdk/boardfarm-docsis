"""
Utils file for functions that are used in booting process.
Created in order to keep booting.py implementation as clean as possible
"""
import logging
from random import choice
from typing import Union

from boardfarm.devices.debian_lan import DebianLAN
from boardfarm.devices.debian_wifi import DebianWifi
from boardfarm.exceptions import CodeError
from boardfarm.lib.common import ip_pool_to_list
from boardfarm_lgi_shared.lib.ofw.networking import (
    get_cpe_ipv4_pool,
    get_defualt_gw_and_netmask,
)
from termcolor import colored

logger = logging.getLogger("bft")


def activate_mitm(devices, mitm_devices: list) -> None:
    """Method tries to activate MITM for all devices specified in
    env.json["environment_def"]["mitm"] section

    :param devices: device manager
    :param env_helper: env.json wrapper
    :raises AttributeError: In case MITM device (container) is not found in device manager
    """
    # We assume that mitm container is already deployed manually
    try:
        devices.mitm.start_capture(mitm_devices)
    except AttributeError:
        logger.error("No MITM device found in device manager")
        raise AttributeError("No MITM device found in device manager")
    except KeyError as e:
        logger.error(str(e))
        raise KeyError(str(e))


def register_fxs_details(fxs_devices, board):
    # this raises an exception, will clear this later.
    try:
        board.mta_prov_check()
        mta_ip = board.get_interface_ipaddr(board.mta_iface)
    except Exception:
        print(colored("MTA is not provisioned properly!!", color="red", attrs=["bold"]))
    for fxs in fxs_devices:
        try:
            _, fxs.tcid = board.get_fxs_details(fxs.fxs_port)
            fxs.gw = mta_ip
        except CodeError as e:
            raise CodeError(f"FXS registration failure.\nReason:{e}")


def set_static_ip_and_default_gw(client: Union[DebianLAN, DebianWifi]) -> None:
    """set static ip and defauly gw based primary lan/wlan interface

    :param cliet: lan/wlan client for which we need to set static ip
    :type cliet: Union[DebianLAN, DebianWifi]
    """
    ip_pool = get_cpe_ipv4_pool()
    ip_address = choice(ip_pool_to_list(*ip_pool))
    default_gw, netmask = get_defualt_gw_and_netmask()
    client.set_static_ip(client.iface_dut, ip_address, netmask)
    client.set_default_gw(default_gw, client.iface_dut)
