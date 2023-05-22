"""Boardfarm DOCSIS provisioner device template."""

from abc import ABC, abstractmethod

# pylint: disable=too-few-public-methods


class Provisioner(ABC):
    """Boardfarm DOCSIS provisioner device template."""

    @abstractmethod
    def provision_cable_modem(  # noqa: PLR0913
        self,
        cm_mac: str,
        cm_bootfile: str,
        mta_bootfile: str,
        tftp_ipv4_addr: str,
        tftp_ipv6_addr: str,
    ) -> None:
        """Provision given cable modem.

        :param cm_mac: cable modem mac address
        :type cm_mac: str
        :param cm_bootfile: cable modem boot file path
        :type cm_bootfile: str
        :param mta_bootfile: mta boot file path
        :type mta_bootfile: str
        :param tftp_ipv4_addr: tftp server ipv4 address
        :type tftp_ipv4_addr: str
        :param tftp_ipv6_addr: tftp server ipv6 address
        :type tftp_ipv6_addr: str
        """
        raise NotImplementedError
