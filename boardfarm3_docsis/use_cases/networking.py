"""Boardfarm docsis networking use cases."""

from __future__ import annotations

import json
import os
import re
from contextlib import contextmanager
from ipaddress import IPv4Address
from ipaddress import ip_address as ip_address_factory
from typing import TYPE_CHECKING, TypeAlias

from boardfarm3.exceptions import UseCaseFailure
from boardfarm3.lib.dataclass.packets import ICMPPacketData, IPAddresses
from boardfarm3.lib.networking import (
    IptablesFirewall,
    start_tcpdump,
    stop_tcpdump,
    tcpdump_read,
)
from boardfarm3.templates.acs import ACS
from boardfarm3.templates.cpe import CPE
from boardfarm3.templates.lan import LAN
from boardfarm3.templates.provisioner import Provisioner
from boardfarm3.templates.wan import WAN

from boardfarm3_docsis.templates.provisioner import Provisioner as DocsisProvisioner

if TYPE_CHECKING:
    from collections.abc import Generator

    from boardfarm3.templates.sip_server import SIPServer
    from boardfarm3.templates.wlan import WLAN

    from boardfarm3_docsis.templates.cable_modem import CableModem
    from boardfarm3_docsis.templates.cmts import CMTS


DeviceWithFwType: TypeAlias = LAN | WAN | ACS | CPE
ProvisionerType: TypeAlias = Provisioner | DocsisProvisioner


# pylint: disable=too-many-lines
def __get_dev_s_firewall(
    device: DeviceWithFwType | ProvisionerType,
) -> IptablesFirewall:
    return device.sw.firewall if isinstance(device, CPE) else device.firewall


def get_traceroute_from_board(
    host_ip: str,
    board: CableModem,
    version: str = "",
    options: str = "",
) -> str:
    """Run the ``traceroute`` on board console.

    Returns the route packets take to a network host.

    :param host_ip: IP address of the host
    :type host_ip: str
    :param board: CableModem device instance
    :type board: CableModem
    :param version: version of the traceroute command, defaults to ""
    :type version: str
    :param options: additional options in the command, defaults to ""
    :type options: str
    :return: return the entire route to the host IP from linux device
    :rtype: str
    """
    return board.sw.nw_utility.traceroute_host(host_ip, version, options)


def parse_icmp_trace(
    device: LAN | WAN | CMTS,
    fname: str,
    args: str = "-Y icmp -T fields -e ip.src -e ip.dst -e icmp.type",
    timeout: int = 30,
) -> list[ICMPPacketData] | list[str]:
    """Read and filter out the ICMP packets from the pcap file with fields.

    Source, Destinationa and Code of Query Type

    .. hint:: This Use Case implements statements from the test suite such as:

        - For the Upstream communication from LAN client to WAN side verify that static
          IP address and WAN server IP is used

    :param device: object of the device class where tcpdump is captured
    :type device: LAN | WAN | CMTS
    :param fname: name of the captured pcap file
    :type fname: str
    :param args: arguments to be used for the filter,
        defaults to "-Y icmp -T fields -e ip.src -e ip.dst -e icmp.type"
    :type args: str
    :param timeout: pexpect timeout for the command in seconds, defaults to 30
    :type timeout: int
    :return: sequence of ICMP packets filtered from captured pcap file
    :rtype: list[ICMPPacketData] | list[str]
    :raises UseCaseFailure: ICMP packets not found
    """
    out = (
        device.tshark_read_pcap(fname, args, timeout=timeout)
        .split("This could be dangerous.")[-1]
        .splitlines()[1:]
    )
    output: list[ICMPPacketData] = []
    if args == "-Y icmp -T fields -e ip.src -e ip.dst -e icmp.type":
        for line in out:
            try:
                (src, dst, query_code) = line.split("\t")
            except ValueError as exception:
                msg = "ICMP packets not found"
                raise UseCaseFailure(msg) from exception

            output.append(
                ICMPPacketData(
                    int(query_code),
                    (
                        IPAddresses(
                            ip_address_factory(src),  # type: ignore[arg-type]
                            None,
                            None,
                        )
                        if isinstance(ip_address_factory(src), IPv4Address)
                        else IPAddresses(
                            None,
                            ip_address_factory(src),  # type: ignore[arg-type]
                            None,
                        )
                    ),
                    (
                        IPAddresses(
                            ip_address_factory(dst),  # type: ignore[arg-type]
                            None,
                            None,
                        )
                        if isinstance(ip_address_factory(dst), IPv4Address)
                        else IPAddresses(
                            None,
                            ip_address_factory(dst),  # type: ignore[arg-type]
                            None,
                        )
                    ),
                ),
            )
        return output
    return out


def block_ipv4_traffic(
    device: DeviceWithFwType | ProvisionerType, destination: str
) -> None:
    """Block the traffic to and from the destination address.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Make sure ACS IPv4 address is not reachable

    :param device: device class object
    :type device: device template such as ,
        LAN | WAN | ACS | Provisioner
    :param destination: destination IP or the corresponding domain name to be blocked
    :type destination: str
    """
    device_s_fwall = __get_dev_s_firewall(device)
    device_s_fwall.add_drop_rule_iptables("-s", destination)
    device_s_fwall.add_drop_rule_iptables("-d", destination)


def block_ipv6_traffic(
    device: DeviceWithFwType | ProvisionerType, destination: str
) -> None:
    """Block the traffic to and from the destination address.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Make sure ACS IPv6 address is not reachable

    :param device: device class object
    :type device: device template such as ,
        LAN | WAN | ACS | Provisioner
    :param destination: destination IP or the corresponding domain name to be blocked
    :type destination: str
    """
    device_s_fwall = __get_dev_s_firewall(device)
    device_s_fwall.add_drop_rule_ip6tables("-s", destination)
    device_s_fwall.add_drop_rule_ip6tables("-d", destination)


def unblock_ipv4_traffic(
    device: DeviceWithFwType | ProvisionerType, destination: str
) -> None:
    """Unblock the traffic to and from the destination address on a device.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Unblock the traffic to and from the destination address on a device.

    :param device: device class object
    :type device: device template such as ,
        LAN | WAN | ACS | Provisioner
    :param destination: destination IP or the corresponding domain name to be unblocked
    :type destination: str
    """
    device_s_fwall = __get_dev_s_firewall(device)
    device_s_fwall.del_drop_rule_iptables("-s", destination)
    device_s_fwall.del_drop_rule_iptables("-d", destination)


def unblock_ipv6_traffic(
    device: DeviceWithFwType | ProvisionerType, destination: str
) -> None:
    """Unblock the traffic to and from the destination address.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Unblock the traffic to and from the destination address on a device.

    :param device: device class object
    :type device: device template such as ,
        LAN | WAN | ACS | Provisioner
    :param destination: destination IP or the corresponding domain name to be unblocked
    :type destination: str
    """
    device_s_fwall = __get_dev_s_firewall(device)
    device_s_fwall.del_drop_rule_ip6tables("-s", destination)
    device_s_fwall.del_drop_rule_ip6tables("-d", destination)


def copy_pcap_to_artifacts(
    source_file: str,
    device: LAN | WAN | WLAN | ACS | Provisioner | SIPServer | CMTS,
    execution_status: bool,
    destination: str | None = None,
) -> None:
    """Copy the pcap file to the artifacts.

    This method will remove the pcap file from the server if the execution status of
    the test is True else file will be copied to the destination folder meaning that
    the test is failed.

    :param source_file: file name of the packet capture
    :type source_file: str
    :param device: source device where the capture is done
    :type device: LAN | WAN | WLAN | ACS | Provisioner | SIPServer | CMTS
    :param execution_status: True if the test pass, False otherwise
    :type execution_status: bool
    :param destination: destination path, defaults to None
    :type destination: str | None
    :raises ValueError: when the invalid file is provided
    """
    if ".pcap" not in source_file:
        err_msg = f"Invalid file name provided {source_file}"
        raise ValueError(err_msg)
    if not execution_status:
        destination = (
            os.path.realpath("results") if destination is None else destination
        )
        device.scp_device_file_to_local(
            local_path=destination,
            source_path=source_file,
        )
    device.delete_file(source_file)


@contextmanager
def tcpdump(
    device: LAN | WAN | WLAN | ACS | Provisioner | CMTS,
    fname: str,
    interface: str,
    filters: dict[str, str] | None,
    additional_filters: str | None = "",
) -> Generator[str]:
    """Contextmanager to perform tcpdump on the provided device such as LAN, WAN etc.

    Start ``tcpdump`` on the device console and kill it outside its scope.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Start packet capture on []

    :param device: the device on which tcpdump to be performed
    :type device: LAN | WAN | WLAN | ACS | Provisioner | CMTS
    :param fname: the filename or the complete path of the resource
    :type fname: str
    :param interface: interface name on which the tcp traffic will listen to
    :type interface: str
    :param filters: filters as key value pair(eg: {"-v": "", "-c": "4"})
    :type filters: Optional[dict[str, str]]
    :param additional_filters: additional filters
    :type additional_filters: Optional[str]
    :yield: Yields the process id of the tcp capture started
    :rtype: Generator[str, None, None]
    """
    pid: str = ""
    try:
        pid = start_tcpdump(
            console=device.console,
            interface=interface,
            output_file=fname,
            filters=filters,
            port=None,
            additional_filters=additional_filters,
        )
        yield pid
    finally:
        stop_tcpdump(device.console, process_id=pid)


def read_tcpdump_from_device(  # pylint: disable=too-many-arguments  # noqa: PLR0913
    device: LAN | WAN | WLAN | ACS | Provisioner | CMTS,
    fname: str,
    protocol: str = "",
    opts: str = "",
    rm_pcap: bool = True,
    timeout: int = 30,
) -> str:
    """Read the tcpdump packets from device and delete the capture file afterwards.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Verify from the packet capture...

    :param device: the device from which tcpdump to be read from
    :type device: LAN | WAN | WLAN | ACS | Provisioner | CMTS
    :param fname: filename or the complete path of the pcap file
    :type fname: str
    :param protocol: protocol to filter, defaults to ""
    :type protocol: str
    :param opts: command line options for reading pcap, defaults to ""
    :type opts: str
    :param rm_pcap: remove pcap file, defaults to True
    :type rm_pcap: bool
    :param timeout: timeout for reading the tcpdump output
    :type timeout: int
    :return: Output of tcpdump read command
    :rtype: str
    """
    return tcpdump_read(
        console=device.console,
        capture_file=fname,
        protocol=protocol,
        opts=opts,
        rm_pcap=rm_pcap,
        timeout=timeout,
    )


def upload_pcap_to_wan(
    device: CMTS,
    host: WAN,
    src_path: str,
    dest_path: str,
) -> None:
    """Copy pcap file from FRR router to WAN.

    Since tshark should not be installed on router,
    we copy the file to WAN container to parse packets.

    :param device: source device where the capture is done
    :type device: CMTS
    :param host: The remote host instance.
    :type host: WAN
    :type src_path: str
    :param dest_path: destination path
    :type dest_path: str
    """
    device.copy_file_to_wan(host, src_path, dest_path)


def parse_pcap_via_tshark(
    device: LAN | WAN | CMTS | Provisioner | SIPServer,
    fname: str,
    args: str = "",
    timeout: int = 60,
    limit_paket_count: int | None = None,
) -> list[dict]:
    """Read and filter out the packets from the pcap file with fields.

    Source, Destinationa and Code of Query Type

    .. hint:: This Use Case implements statements from the test suite such as:

        - Analyze the packets and check that...

    :param device: object of the device class where tcpdump is captured
    :type device: LAN | WAN | CMTS | Provisioner
    :param fname: name of the captured pcap file
    :type fname: str
    :param args: arguments to be used for the filter,
        defaults to no filter
    :type args: str
    :param timeout: timeout for reading the packets, defaults to 60
    :type timeout: int
    :param limit_paket_count: limits the number of packet to parse from,
        defaults to None
    :type limit_paket_count: int | None
    :return: sequence of packets filtered from captured pcap file
    :rtype: list[dict]
    """
    additional_args = "-T json"
    _temp_file = "/tmp/temp_filtered_file.pcap"  # noqa: S108

    if limit_paket_count:
        additional_args = f"-c {limit_paket_count} " + additional_args
        matched = re.search(r"(?:^|\s)(-Y\s+.+?)(?=\s-\w|\s*$)", args)
        _display_filter_y = matched.group(1) if matched else None
        if _display_filter_y:
            filter_args = f"{_display_filter_y} -w {_temp_file}"
            # it ceates a new file that has only the filterd entries
            device.tshark_read_pcap(fname, filter_args, timeout=timeout)
            additional_args = f"{additional_args} {args.replace(_display_filter_y, '')}"
            res = (
                device.tshark_read_pcap(
                    _temp_file, additional_args, timeout=timeout, rm_pcap=True
                )
                .split("This could be dangerous.")[-1]
                .strip("'")
            )
            return json.loads(res)

    if args:
        additional_args += " " + args
    res = (
        device.tshark_read_pcap(fname, additional_args, timeout=timeout)
        .split("This could be dangerous.")[-1]
        .strip("'")
    )
    return json.loads(res)


def stop_cm_agent(board: CableModem) -> None:
    """Kill CM agent process running on DUT.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Stop the CM agent process on DUT

    :param board: CableModem device instance
    :type board: CableModem
    """
    board.sw.stop_cm_agent()


def parse_tunnel_packets(
    device: LAN | WAN | WLAN, fname: str, additional_args: str = "", timeout: int = 30
) -> list[tuple[str, ...]]:
    """Use case to parse packet capture for tunnel static IP service.

    Parse packets with encapsulated info

    .. hint:: This Use Case implements statements from the test suite such as:

        - Access Internet from Ethernet LAN client and verify that,

            -Internet traffic from Ethernet LAN client is bridged
                with L2GRE tunnel interface.
            -Internet traffic from Ethernet LAN client is sent via
                L2GRE tunnel interface.
                ...


    :param device: object of the device class where tcpdump is captured
    :type device: LAN | WAN | CMTS
    :param fname: name of the captured pcap file
    :type fname: str
    :param additional_args: any additional arguments to be used for the filter
    :type additional_args: str
    :param timeout: pexpect timeout for the command in seconds, defaults to 30
    :type timeout: int
    :return: list of parsed IP packets
    :rtype: list[tuple[str, ...]]
    """
    args = "-Y icmp -Y eth "
    fields = "-T fields -e ip.src -e eth.src -e ip.dst -e eth.dst"

    out = (
        device.tshark_read_pcap(fname, args + fields + additional_args, timeout=timeout)
        .split("This could be dangerous.")[-1]
        .splitlines()[1:]
    )
    return [tuple(line.strip().split("\t")) for line in out]
