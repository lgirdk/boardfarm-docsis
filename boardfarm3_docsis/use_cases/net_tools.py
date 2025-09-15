"""Network utility helper use cases."""

from typing import Any

from boardfarm3.lib.device_manager import get_device_manager
from pandas import DataFrame

from boardfarm3_docsis.templates.cable_modem import CableModem


class NwUtility:
    """OneFW network utility."""

    @staticmethod
    def netstat_listening_ports(
        device_type: type[CableModem],
        opts: str = "-nlp",
        extra_opts: str = "",
    ) -> DataFrame:
        """Get all listening ports.

        :param device_type: type of the device
        :type device_type: Type[CableModem]
        :param opts: command line options
        :type opts: str
        :param extra_opts: extra command line options
        :type extra_opts: str
        :return: parsed netstat output
        :rtype: DataFrame
        """
        return (
            get_device_manager()
            .get_device_by_type(device_type)
            .sw.nw_utility.netstat(opts, extra_opts)
        )

    @staticmethod
    def netstat_all_udp(
        device_type: type[CableModem],
        opts: str = "-nlp",
        extra_opts: str = "",
    ) -> DataFrame:
        """Get all udp ports.

        :param device_type: type of the device
        :type device_type: Type[CableModem]
        :param opts: command line options
        :type opts: str
        :param extra_opts: extra command line options
        :type extra_opts: str
        :return: parsed netstat output
        :rtype: DataFrame
        """
        return (
            get_device_manager()
            .get_device_by_type(device_type)
            .sw.nw_utility.netstat(opts, extra_opts)
        )

    @staticmethod
    def netstat_all_tcp(
        device_type: type[CableModem],
        opts: str = "-nlp",
        extra_opts: str = "",
    ) -> DataFrame:
        """Get all UDP ports.

        :param device_type: type of the device
        :type device_type: Type[CableModem]
        :param opts: command line options
        :type opts: str
        :param extra_opts: extra command line options
        :type extra_opts: str
        :return: parsed netstat output
        :rtype: DataFrame
        """
        return (
            get_device_manager()
            .get_device_by_type(device_type)
            .sw.nw_utility.netstat(opts, extra_opts)
        )


class Firewall:
    """Linux iptables network firewall."""

    @staticmethod
    def iptables_list(
        device_type: type[CableModem],
        opts: str = "",
        extra_opts: str = "-nvL --line-number",
    ) -> dict[str, list[dict]]:
        """Return iptables rules as dictionary.

        :param device_type: type of the device
        :type device_type: Type[CableModem]
        :param opts: command line arguments for iptables command
        :type opts: str
        :param extra_opts: extra command line arguments for iptables command
        :type extra_opts: str
        :return: iptables rules dictionary
        :rtype: dict[str, list[dict]]
        """
        return (
            get_device_manager()
            .get_device_by_type(device_type)
            .sw.firewall.get_iptables_list(opts, extra_opts)
        )

    @staticmethod
    def is_table_empty(
        device_type: type[CableModem],
        opts: str = "",
        extra_opts: str = "-nvL --line-number",
    ) -> bool:
        """Return True if iptables is empty.

        :param device_type: type of the device
        :type device_type: Type[CableModem]
        :param opts: command line arguments for iptables command
        :type opts: str
        :param extra_opts: extra command line arguments for iptables command
        :type extra_opts: str
        :return: True if iptables is empty, False otherwise
        :rtype: bool
        """
        return (
            get_device_manager()
            .get_device_by_type(device_type)
            .sw.firewall.is_iptable_empty(opts, extra_opts)
        )

    @staticmethod
    def ip6tables_list(
        device_type: type[CableModem],
        opts: str = "",
        extra_opts: str = "-nvL --line-number",
    ) -> dict[str, list[dict]]:
        """Return ip6tables rules as dictionary.

        :param device_type: type of the device
        :type device_type: Type[CableModem]
        :param opts: command line arguments for ip6tables command
        :type opts: str
        :param extra_opts: extra command line arguments for ip6tables command
        :type extra_opts: str
        :return: ip6tables rules dictionary
        :rtype: dict[str, list[dict]]
        """
        return (
            get_device_manager()
            .get_device_by_type(device_type)
            .sw.firewall.get_ip6tables_list(opts, extra_opts)
        )

    @staticmethod
    def is_6table_empty(
        device_type: type[CableModem],
        opts: str = "",
        extra_opts: str = "-nvL --line-number",
    ) -> bool:
        """Return True if ip6tables is empty.

        :param device_type: type of the device
        :type device_type: Type[CableModem]
        :param opts: command line arguments for ip6tables command
        :type opts: str
        :param extra_opts: extra command line arguments for ip6tables command
        :type extra_opts: str
        :return: True if ip6tables is empty, False otherwise
        :rtype: bool
        """
        return (
            get_device_manager()
            .get_device_by_type(device_type)
            .sw.firewall.is_ip6table_empty(opts, extra_opts)
        )

    @staticmethod
    def add_drop_rule_iptables(
        device_type: type[CableModem],
        option: str,
        valid_ip: str,
    ) -> None:
        """Add drop rule to iptables.

        :param device_type: type of the device
        :type device_type: Type[CableModem]
        :param option: iptables command line options, set -s for source
            and -d for destination
        :type option: str
        :param valid_ip: ip to be blocked from device
        :type valid_ip: str
        """
        get_device_manager().get_device_by_type(
            device_type,
        ).sw.firewall.add_drop_rule_iptables(option, valid_ip)

    @staticmethod
    def add_drop_rule_ip6tables(
        device_type: type[CableModem],
        option: str,
        valid_ip: str,
    ) -> None:
        """Add drop rule to ip6tables.

        :param device_type: type of the device
        :type device_type: Type[CableModem]
        :param option: ip6tables command line options
        :type option: str
        :param valid_ip: ip to be blocked from device
        :type valid_ip: str
        """
        get_device_manager().get_device_by_type(
            device_type,
        ).sw.firewall.add_drop_rule_ip6tables(option, valid_ip)

    @staticmethod
    def del_drop_rule_iptables(
        device_type: type[CableModem],
        option: str,
        valid_ip: str,
    ) -> None:
        """Delete drop rule from iptables.

        :param device_type: type of the device
        :type device_type: Type[CableModem]
        :param option: iptables command line options, set -s for source
            and -d for destination
        :type option: str
        :param valid_ip: ip to be unblocked
        :type valid_ip: str
        """
        get_device_manager().get_device_by_type(
            device_type,
        ).sw.firewall.del_drop_rule_iptables(option, valid_ip)

    @staticmethod
    def del_drop_rule_ip6tables(
        device_type: type[CableModem],
        option: str,
        valid_ip: str,
    ) -> None:
        """Delete drop rule from ip6tables.

        :param device_type: type of the device
        :type device_type: Type[CableModem]
        :param option: ip6tables command line options
        :type option: str
        :param valid_ip: ip to be unblocked
        :type valid_ip: str
        """
        get_device_manager().get_device_by_type(
            device_type,
        ).sw.firewall.del_drop_rule_ip6tables(option, valid_ip)


class DNS:
    """DNS use cases."""

    @staticmethod
    def nslookup_A_record(  # pylint: disable=invalid-name
        device_type: type[CableModem],
        domain_name: str,
        opts: str = "-q=A",
        extra_opts: str = "",
    ) -> dict[str, Any]:
        """Perform nslookup for A records and return the parsed results.

        :param device_type: type of the device
        :type device_type: Type[CableModem]
        :param domain_name: domain name to perform nslookup on
        :type domain_name: str
        :param opts: nslookup command line options
        :type opts: str
        :param extra_opts: nslookup additional command line options
        :type extra_opts: str
        :return: parsed nslookup results as dictionary
        :rtype: dict[str, Any]
        """
        return (
            get_device_manager()
            .get_device_by_type(device_type)
            .sw.dns.nslookup.nslookup(domain_name, opts, extra_opts)
        )

    @staticmethod
    def nslookup_AAAA_record(  # pylint: disable=invalid-name
        device_type: type[CableModem],
        domain_name: str,
        opts: str = "-q=AAAA",
        extra_opts: str = "",
    ) -> dict[str, Any]:
        """Perform nslookup for AAAA records and return the parsed results.

        :param device_type: type of the device
        :type device_type: Type[CableModem]
        :param domain_name: domain name to perform nslookup on
        :type domain_name: str
        :param opts: nslookup command line options
        :type opts: str
        :param extra_opts: nslookup additional command line options
        :type extra_opts: str
        :return: parsed nslookup results as dictionary
        :rtype: dict[str, Any]
        """
        return (
            get_device_manager()
            .get_device_by_type(device_type)
            .sw.dns.nslookup.nslookup(domain_name, opts, extra_opts)
        )

    @staticmethod
    def get_dns_record(
        device_type: type[CableModem],
        domain_name: str,
    ) -> dict[str, Any]:
        """Perform nslookup and return the parsed results.

        :param device_type: type of the device
        :type device_type: Type[CableModem]
        :param domain_name: domain name to perform nslookup on
        :type domain_name: str
        :return: parsed nslookup results as dictionary
        :rtype: dict[str, Any]
        """
        return (
            get_device_manager()
            .get_device_by_type(device_type)
            .sw.dns.nslookup.nslookup(domain_name)
        )
