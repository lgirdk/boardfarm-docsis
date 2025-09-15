"""Boardfarm DOCSIS CMTS device template."""

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from boardfarm3.templates.line_termination import LTS

if TYPE_CHECKING:
    from boardfarm3.lib.boardfarm_pexpect import BoardfarmPexpect
    from boardfarm3.templates.wan import WAN


class CMTS(LTS):
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
    def get_cmts_ip_bundle(self, gw_ip: str | None = None) -> str:
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
    def get_ip_routes(self) -> list[str]:
        """Get IP routes from the quagga router.

        :return: ip routes collected from quagga router
        :rtype: list[str]
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
    def get_ertr_ipv4(self, mac_address: str) -> str | None:
        """Get erouter ipv4 from CMTS.

        :param mac_address: mac address of the cable modem
        :type mac_address: str
        :return: ipv4 address of erouter else None
        :rtype: Optional[str]
        """
        raise NotImplementedError

    @abstractmethod
    def get_ertr_ipv6(self, mac_address: str) -> str | None:
        """Get erouter ipv6 from CMTS.

        :param mac_address: mac address of the cable modem
        :type mac_address: str
        :return: ipv6 address of erouter else None
        :rtype: Optional[str]
        """
        raise NotImplementedError

    @abstractmethod
    def get_mta_ipv4(self, mac_address: str) -> str | None:
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

    @abstractmethod
    def get_cm_channel_values(self, mac: str) -> dict[str, str]:
        """Get the cm channel values.

        :param mac: mac address of the cable modem
        :type mac: str
        :return: cm channel values
        :rtype: dict[str, str]
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def console(self) -> BoardfarmPexpect:
        """Returns CMTS console.

        :return: console
        :rtype: BoardfarmPexpect
        """
        raise NotImplementedError

    @abstractmethod
    def scp_device_file_to_local(self, local_path: str, source_path: str) -> None:
        """Copy a local file from a server using SCP.

        :param local_path: local file path
        :param source_path: source path
        """
        raise NotImplementedError

    @abstractmethod
    def delete_file(self, filename: str) -> None:
        """Delete the file from the device.

        :param filename: name of the file with absolute path
        :type filename: str
        """
        raise NotImplementedError

    @abstractmethod
    def copy_file_to_wan(
        self,
        host: WAN,
        src_path: str,
        dest_path: str,
    ) -> None:
        """Copy file from FRR router to WAN container.

        :param host: the remote host instance
        :type host: WAN
        :param src_path: source file path
        :type src_path: str
        :param dest_path: destination path
        :type dest_path: str
        """
        raise NotImplementedError

    @abstractmethod
    def start_tcpdump(
        self,
        interface: str,
        port: str | None,
        output_file: str = "pkt_capture.pcap",
        filters: dict | None = None,
        additional_filters: str | None = "",
    ) -> str:
        """Start tcpdump capture on given interface.

        :param interface: inteface name where packets to be captured
        :type interface: str
        :param port: port number, can be a range of ports(eg: 443 or 433-443)
        :type port: str
        :param output_file: pcap file name, Defaults: pkt_capture.pcap
        :type output_file: str
        :param filters: filters as key value pair(eg: {"-v": "", "-c": "4"})
        :type filters: Optional[Dict]
        :param additional_filters: additional filters
        :type additional_filters: Optional[str]
        :return: console ouput and tcpdump process id
        :rtype: str
        """
        raise NotImplementedError

    @abstractmethod
    def stop_tcpdump(self, process_id: str) -> None:
        """Stop tcpdump capture.

        :param process_id: tcpdump process id
        :type process_id: str
        """
        raise NotImplementedError
