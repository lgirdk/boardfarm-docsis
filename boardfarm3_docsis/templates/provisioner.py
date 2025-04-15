"""Boardfarm DOCSIS provisioner device template."""

from abc import abstractmethod
from functools import cached_property

from boardfarm3.templates.provisioner import Provisioner as BaseProvisioner

# pylint: disable=too-few-public-methods


class Provisioner(BaseProvisioner):
    """Boardfarm DOCSIS provisioner device template."""

    @cached_property
    @abstractmethod
    def ipv4_addr(self) -> str:
        """Return the IPv4 address on IFACE facing DUT.

        :return: IPv4 address in string format.
        :rtype: str
        """
        raise NotImplementedError

    @cached_property
    @abstractmethod
    def ipv6_addr(self) -> str:
        """Return the IPv6 address on IFACE facing DUT.

        :return: IPv6 address in string format.
        :rtype: str
        """
        raise NotImplementedError

    @abstractmethod
    def provision_cable_modem(
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
