"""RIPv2 usecase library All usecases are independent of the device."""

from dataclasses import dataclass
from datetime import datetime
from ipaddress import IPv4Address, ip_interface
from typing import List, Optional, Union

from boardfarm.exceptions import CodeError
from boardfarm.use_cases.descriptors import LanClients, WanClients

from boardfarm_docsis.devices.topvision_cmts import MiniCMTS


@dataclass
class RIPv2PacketData:
    """Class to hold RIP packet details for usecase."""

    source: IPv4Address
    destination: IPv4Address
    ip_address: List[IPv4Address]
    subnet: List[ip_interface]
    frame_time: Optional[datetime] = None


def parse_rip_trace(
    dev: Union[LanClients, WanClients, MiniCMTS],
    fname: str,
    frame_time: bool,
    rm_pcap: bool,
) -> List[RIPv2PacketData]:
    """Read and filter rip packets from the captured file.

    The Routing Information Protocol is one of a family of IP Routing
    protocols.RIP is a simple vector routing protocol.
    This usecase parses rip protocol packets.

    Usage:
    .. highlight:: python
    ..code-block:: python

    cmts_packet_cap = read_rip_trace(
            device= LanClient,
            fname="some_capture.pcap",
            frame_time=False,
            rm_pcap=False)

    :param dev: device where captures were taken, LanClient, WanClient, WifiLan, MiniCmts
    :type dev: Devices
    :param fname: PCAP file to be read
    :type fname: str
    :param frame_time: If True stores timestap value in RIPv2PacketData else stores None
    :type fname: boolean
    :param rm_pcap: if True remove the pcap file after reading else keeps the file.
    :type fname: boolean
    :return: list of rip packets as [(frame, src ip, dst ip, rip contact, rip msg:media_attribute:connection:info, time)]
    :rtype: List[RIPv2PacketData]
    """

    output = []
    time_field = "-e frame.time_epoch" if frame_time else ""
    fields = (
        f" -Y rip -T fields -e ip.src -e ip.dst -e rip.ip -e rip.netmask {time_field}"
    )
    filter_str = fields
    raw_rip_packets = dev.tshark_read_pcap(
        fname=fname,
        additional_args=filter_str,
        rm_pcap=rm_pcap,
    )
    rip_packets = raw_rip_packets.split("This could be dangerous.\r\n")[-1]
    if not rip_packets:
        raise CodeError(
            f"No trace found in pcap file {fname} with filters: {filter_str}"
        )

    ftime = None
    for packet in rip_packets.splitlines():
        packet_fields = packet.split("\t")
        try:
            (
                src,
                dst,
                advertised_ips,
                netmask,
            ) = packet_fields[:4]

            if frame_time:
                ftime = datetime.fromtimestamp(float(packet_fields[-1]))

        except (IndexError, ValueError):
            raise CodeError(f"No RIPv2 trace found in pcap file {fname}")

        if advertised_ips:
            output.append(
                RIPv2PacketData(
                    source=IPv4Address(src),
                    destination=IPv4Address(dst),
                    ip_address=[IPv4Address(ip) for ip in advertised_ips.split(",")],
                    subnet=[ip_interface(mask) for mask in netmask.split(",")],
                    frame_time=ftime,
                )
            )
    return output
