"""Boardfarm DOCSIS CMTS device template."""

from abc import ABC, abstractmethod
from typing import Optional


class CMTS(ABC):
    """Boardfarm DOCSIS CMTS device template."""

    @abstractmethod
    def is_cable_modem_online(
        self,
        mac_address: str,
        ignore_bpi: bool = False,
        ignore_partial: bool = False,
        ignore_cpe: bool = False,
    ) -> bool:
        """Check given cable modem is online on cmts.

        :param mac_address: cable modem mac address
        :param ignore_bpi: ignore BPI. defaults to False.
        :param ignore_partial: ignore partial online. defaults to False.
        :param ignore_cpe: ignore CPE. defaults to False.
        :returns: True when cable is online on cmts, otherwise False
        """
        raise NotImplementedError

    @abstractmethod
    def reset_cable_modem_status(self, mac_address: str) -> None:
        """Rest cable modem status on cmts.

        :param mac_address: mac address of cable modem
        """
        raise NotImplementedError

    @abstractmethod
    def get_cable_modem_ip_address(self, mac_address: str) -> str:
        """Get cable modem IP address on CMTS.

        :param mac_address: cable modem MAC address
        :returns: IP address of the cable modem on CMTS
        """
        raise NotImplementedError

    @abstractmethod
    def get_cmts_ip_bundle(self, gw_ip: Optional[str] = None) -> str:
        """Get CMTS bundle IP.

        Validate if Gateway IP is configured in CMTS and both are in same network.
        The first host address within the network will be assumed to be gateway
        for Mini CMTS

        :param gw_ip: gateway ip address. defaults to None
        :raises ValueError: Failed to get the CMTS bundle IP
        :return: gateway ip if address configured on minicmts else return all ip bundles
        """
        raise NotImplementedError

    @abstractmethod
    def get_ip_routes(self) -> str:
        """Get IP routes from the quagga router.

        :return: ip routes collected from quagga router
        :rtype: str
        """
        raise NotImplementedError

    @abstractmethod
    def clear_cm_reset(self, mac_address: str) -> None:
        """Reset the CM from cmts.

        Usually performed with a cli -clear cable modem <cm_mac> reset command

        :param mac_address: mac address of the CM
        :type mac_address: str
        """
        raise NotImplementedError

    @abstractmethod
    def get_ertr_ipv4(self, mac_address: str) -> Optional[str]:
        """Get erouter ipv4 from CMTS.

        :param mac_address: mac address of the cable modem
        :type mac_address: str
        :return: ipv4 address of erouter else None
        :rtype: Optional[str]
        """
        raise NotImplementedError

    @abstractmethod
    def get_ertr_ipv6(self, mac_address: str) -> Optional[str]:
        """Get erouter ipv6 from CMTS.

        :param mac_address: mac address of the cable modem
        :type mac_address: str
        :return: ipv6 address of erouter else None
        :rtype: Optional[str]
        """
        raise NotImplementedError

    @abstractmethod
    def get_mta_ipv4(self, mac_address: str) -> Optional[str]:
        """Get the MTA IP from CMTS.

        :param mac_address: mac address of the cable modem
        :type mac_address: str
        :return: ipv4 address of mta else None
        :rtype: Optional[str]
        """
        raise NotImplementedError

    @abstractmethod
    def get_downstream_channel_value(self, mac: str) -> str:
        """Get the downstream channel value.

        :param mac: mac address of the cable modem
        :type mac: str
        :return: downstream channel value
        :rtype: str
        """
        raise NotImplementedError

    @abstractmethod
    def get_upstream_channel_value(self, mac: str) -> str:
        """Get the upstream channel value.

        :param mac: mac address of the cable modem
        :type mac: str
        :return: upstream channel value
        :rtype: str
        """
        raise NotImplementedError
