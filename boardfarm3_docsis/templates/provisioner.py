"""Boardfarm DOCSIS provisioner device template."""

from abc import ABC, abstractmethod

# pylint: disable=too-few-public-methods


class Provisioner(ABC):
    """Boardfarm DOCSIS provisioner device template."""

    @abstractmethod
    def provision_cable_modem(
        self, cm_mac: str, cm_bootfile: str, tftp_ipv4_addr: str, tftp_ipv6_addr: str
    ) -> None:
        """Provision given cable modem.

        :param cm_mac: cable modem mac address
        :param cm_bootfile: cable modem boot file path
        :param tftp_ipv4_addr: tftp server ipv4 address
        :param tftp_ipv6_addr: tftp server ipv6 address
        """
        raise NotImplementedError
