"""Boardfarm DOCSIS CMTS device template."""

from abc import ABC, abstractmethod


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
