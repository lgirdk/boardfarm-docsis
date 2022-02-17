"""mini cmts use cases library."""
import ipaddress
import logging
from re import findall as regex_findall

from boardfarm.lib.DeviceManager import get_device_by_name
from boardfarm.lib.regexlib import ValidIpv4AddressRegex_Nogroup

logger = logging.getLogger("bft")


def is_route_present_on_cmts(route: ipaddress.ip_network) -> bool:
    """Check if routing table of cmts router contains a route.

    perfrom ip route command on quagga router, collet the routes and
    check if route is present in table output.
    .. highlight:: python
    ..code-block:: python

        status = is_route_present_on_cmts(
            route=ipaddress.ip_network('192.168.101.0/24')
            )

    :return: True if route is present on cmts else false
    :rtype: bool
    """
    cmts = get_device_by_name("cmts")
    raw_routes = cmts.ip_route()
    ip_routes = [
        ipaddress.ip_network(_route)
        for _route in regex_findall(
            ValidIpv4AddressRegex_Nogroup + r"\/[\d]{1,2}", raw_routes
        )
    ]
    return True if route in ip_routes else False
