"""Use Cases to interact with DOCSIS devices such as CMTS and CM."""
import logging
from ipaddress import IPv4Network, IPv6Network, ip_network
from re import findall as regex_findall
from typing import Optional, Union

from boardfarm.lib.DeviceManager import get_device_by_name
from boardfarm.lib.regexlib import ValidIpv4AddressRegex_Nogroup

from boardfarm_docsis.devices.base_devices.cmts_template import CmtsTemplate

logger = logging.getLogger("bft")


def is_route_present_on_cmts(
    route: Union[IPv4Network, IPv6Network], which_cmts: Optional[CmtsTemplate] = None
) -> bool:
    """Check if routing table of cmts router contains a route.

    perfrom ip route command on quagga router, collet the routes and
    check if route is present in table output.

    .. code-block:: python

        # example usage
        status = is_route_present_on_cmts(
            route=ipaddress.ip_network('192.168.101.0/24')
        )

    :param route: route to be looked up on CMTS
    :type route: Union[IPv4Network, IPv6Network]
    :param which_cmts: CMTS to be used, defaults to None.
        If None is given, it will be automatically selected.
    :type which_cmts: Optional[CmtsTemplate], optional
    :return: True if route is present on CMTS
    :rtype: bool
    """

    if which_cmts is None:
        cmts: CmtsTemplate = get_device_by_name("cmts")
    else:
        cmts = which_cmts

    raw_routes = cmts.ip_route()
    ip_routes = [
        ip_network(_route)
        for _route in regex_findall(
            ValidIpv4AddressRegex_Nogroup + r"\/[\d]{1,2}", raw_routes
        )
    ]
    return True if route in ip_routes else False
