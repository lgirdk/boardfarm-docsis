"""Boardfarm DOCSIS provisioner device template."""

from abc import ABC, abstractmethod
from functools import cached_property

from boardfarm3.lib.boardfarm_pexpect import BoardfarmPexpect
from boardfarm3.lib.networking import IptablesFirewall

# pylint: disable=too-few-public-methods


class Provisioner(ABC):
    """Boardfarm DOCSIS provisioner device template."""

    @property
    @abstractmethod
    def console(self) -> BoardfarmPexpect:
        """Returns Provisioner console.

        :return: console
        :rtype: BoardfarmPexpect
        """
        raise NotImplementedError

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

    @property
    @abstractmethod
    def firewall(self) -> IptablesFirewall:
        """Returns Firewall utility instance.

        :return: firewall component instance with console object
        :rtype: IptablesFirewall
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def iface_dut(self) -> str:
        """Name of the interface that is connected to DUT."""
        raise NotImplementedError
