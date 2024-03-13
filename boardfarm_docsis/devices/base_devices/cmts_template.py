import abc
import re
import time
from datetime import datetime
from typing import Dict, List, Optional

import boardfarm.devices.connection_decider as conn_dec
from boardfarm.exceptions import CodeError, PexpectErrorTimeout
from boardfarm.lib import DeviceManager
from boardfarm.lib.bft_pexpect_helper import bft_pexpect_helper as PexpectHelper
from boardfarm.lib.signature_checker import __MetaSignatureChecker
from netaddr import EUI, mac_cisco


class CmtsTemplate(
    PexpectHelper, metaclass=__MetaSignatureChecker
):  # pylint:disable=invalid-metaclass
    """CMTS template class.
    Contains basic list of APIs to be able to connect to CMTS
    and to check if DUT is online.
    All methods, marked with @abc.abstractmethod annotation have to be implemented in derived
    class with the same signatures as in template.
    """

    log = ""
    log_calls = ""

    @property
    @abc.abstractmethod
    def model(self):
        """This attribute is used by boardfarm to select the class to be used
        to create the object that allows the test fixutes to access the CMTS.
        This property shall be a value that matches the "type"
        attribute of CMTS entry in the inventory file.
        """

    @property
    @abc.abstractmethod
    def prompt(self):
        """This attribute is used by boardfarm to understand how does device's prompt look like.
        E.g. for CASA3200 CMTS this class atribute may be:
        prompt = [
            "CASA-C3200>",
            "CASA-C3200#",
            r"CASA-C3200\\(.*\\)#",
        ]
        Should be a list.
        May containg regexs.
        """

    @abc.abstractmethod
    def __init__(self, *args, **kwargs) -> None:
        """Initialize CMTS parameters.
        Config data dictionary will be unpacked and passed to init as kwargs.
        You can use kwargs in a following way:
            self.username = kwargs.get("username", "DEFAULT_USERNAME")
            self.password = kwargs.get("password", "DEFAULT_PASSWORD")
        Be sure to add
            self.spawn_device(**kwargs)
            self.connect()
        at the end in order to properly initialize device prompt on init step
        """
        mgr = kwargs.get("mgr", None)
        if mgr:
            board = mgr.by_type(DeviceManager.device_type.DUT)
            self.board_wan_mac = EUI(board.cm_mac, dialect=mac_cisco)
            self.board_mta_mac = EUI(int(self.board_wan_mac) + 1, dialect=mac_cisco)

        def spawn_device(self, **kwargs):
            """Spawns a console device based on the class type specified in
            the paramter device_type. Currently the communication with the console
            occurs via the pexpect module."""
            self.connection = conn_dec.connection(self.conn_type, device=self, **kwargs)

    @abc.abstractmethod
    def connect(self) -> None:
        """Connect to CMTS & initialize prompt.
        Here you can run initial commands in order to land on specific prompt
        and/or initialize system
        E.g. enter username/password, set stuff in config or disable pagination"""
        # Use this at the beginning to initialize connection pipe
        self.connection.connect()

    @abc.abstractmethod
    def check_online(self, cm_mac: str) -> bool:
        """Return true if cm_mac modem is online.
        Criteria of 'online' should be defined for concrete CMTS"""

    @abc.abstractmethod
    def logout(self) -> None:
        """Logout of the CMTS"""

    @abc.abstractmethod
    def DUT_chnl_lock(self, cm_mac: str) -> List[int]:
        """Return amount of upstream / downstream channels that modem is bonded to
        :param cm_mac: cable modem mac address
        :return: [upstream_channels_count, downstream_channels_count]
        """

    @abc.abstractmethod
    def clear_offline(self, cm_mac: str) -> None:
        """Clear the CM entry from cmts which is offline -clear cable modem <cm_mac> delete
        :param cm_mac: mac address of the CM
        :type cm_mac: str
        """

    @abc.abstractmethod
    def clear_cm_reset(self, cm_mac: str) -> None:
        """Reset the CM from cmts using cli -clear cable modem <cm_mac> reset
        :param cm_mac: mac address of the CM
        :type cm_mac: str
        """

    @abc.abstractmethod
    def get_cmip(self, cm_mac: str) -> Optional[str]:
        """API to get modem IPv4 address
        :param cm_mac: cable modem mac address
        :return: CM ip in case CM is online, None otherwise
        """

    @abc.abstractmethod
    def get_cmipv6(self, cm_mac: str) -> Optional[str]:
        """PI to get modem IPv6 address
        :param cm_mac: cable modem mac address
        :return: CM ip in case CM is online, None otherwise
        """

    @abc.abstractmethod
    def check_partial_service(self, cm_mac: str) -> bool:
        """Check the CM status from CMTS
        Function checks the show cable modem and returns True if p-online
        :param cm_mac: cm mac
        :type cm_mac: str
        :return: True if modem is in partial service, False otherwise
        :rtype: bool
        """

    @abc.abstractmethod
    def get_cmts_ip_bundle(
        self, cm_mac: Optional[str] = None, gw_ip: Optional[str] = None
    ) -> str:
        """Get CMTS bundle IP, Validate if Gateway IP is configured in CMTS and both are in same network
        The first host address within the network will be assumed to be gateway for Mini CMTS
        :param cm_mac: cm mac
        :type cm_mac: str
        :param gw_ip: gateway ip
        :type gw_ip: str
        :raises assertion error: ERROR: Failed to get the CMTS bundle IP
        :return: gateway ip if address configured on mini cmts else return all ip bundles
        :rtype: str
        """

    @abc.abstractmethod
    def get_qos_parameter(self, cm_mac: str) -> Dict[str, List[dict]]:
        """To get the qos related parameters of CM
        Example output format : {'DS':  [{'Sfid': '1' ..},
                                         {'Sfid': '2' ..}
                                 'US': [{{'Sfid': '1' ..},
                                  'Maximum Burst': '128000',
                                  'IP ToS Overwrite [AND-msk, OR-mask]':
                                  ['0x00', '0x00'], ...},
                                  {'Sfid': '1' ..}}
        The units for measuring are
        1) Maximum Sustained rate, Minimum Reserved rate -- bits/sec
        2) Maximum Burst, Minimum Packet Size, Maximum Concatenated Burst,
            Bytes received, Packet dropped -- bytes
        3) Admitted Qos Timeout, Active QoS Timeout -- seconds
        4) Current Throughput -- [bits/sec, packets/sec]
        :param cm_mac: mac address of the cable modem
        :type cm_mac: string
        :return: containing the qos related parameters.
        :rtype: dictionary
        """

    @abc.abstractmethod
    def get_mtaip(self, cm_mac: str, mta_mac: str = None) -> Optional[str]:
        """Get the MTA IP from CMTS
        :param cm_mac: mac address of the CM
        :type cm_mac: string
        :param mta_mac: mta mac address
        :type mta_mac: string
        :return: MTA ip address or "None" if ip not found
        :rtype: string
        """

    @abc.abstractmethod
    def get_ertr_ipv4(self, mac: str, offset: int = 2) -> Optional[str]:
        """Get erouter ipv4 from CMTS
        :param mac: mac address of the cable modem
        :type mac: string
        :param offset: eRouter mac address offset, defaults to 2
        :type offset: int
        :return: returns ipv4 address of erouter else None
        :rtype: string, None
        """

    @abc.abstractmethod
    def get_ertr_ipv6(self, mac: str, offset: int = 2) -> Optional[str]:
        """Get erouter ipv4 from CMTS
        :param mac: mac address of the cable modem
        :type mac: string
        :param offset: eRouter mac address offset, defaults to 2
        :return: returns ipv4 address of erouter else None
        :rtype: string, None
        """

    @abc.abstractmethod
    def is_cm_bridged(self, mac: str, offset: int = 2) -> bool:
        """Check if the modem is in bridge mode
        :param mac: Mac address of the modem,
        :param offset: eRouter mac address offset, defaults to 2
        :return: True if the modem is bridged mode else False.
        :rtype: boolean
        """

    ######################################################
    # Util methods. Not abstract, can and should be reused
    ######################################################
    def get_cm_mac_cmts_format(self, mac):
        """to convert mac adress to the format that to be used on cmts
        :param mac: mac address of CM in foramt XX:XX:XX:XX:XX:XX or XX-XX-XX-XX-XX-XX
        :type mac: string
        :return:  the cm_mac in cmts format xxxx.xxxx.xxxx (lowercase)
        :rtype: string
        """
        if mac is None:
            return None
        mac = EUI(mac)
        mac.dialect = mac_cisco
        return str(mac)

    def wait_for_cm_online(
        self,
        ignore_bpi=False,
        ignore_partial=False,
        ignore_cpe=False,
        time_to_sleep=10,
        iterations=50,
    ):
        """Waits for a CM to come online in an iterate-check-sleep loop. A CM
        is online when the its status is OPERATIONAL.
        The total timeout is 200s ca. (10s * 20 iterations). An ideal timeout
        for a CM to come online should be around 90s max, but currently this is
        not the case in our setup.
        :param ignore_bpi: (optional) considers the CM online even when BPI is disabled
        :type ignore_bpi: bool
        :param ignore_partial: (optional) considers the CM online even when CM is oin
        :type ignore_partial: bool
        :param ignore_cpe: (optional) considers tje CM online even when LAN<->WAN forwarding is disabled
        :type ignore_cpe: bool
        :param :
        :raises Execption: boardfarm.exception.CodeError on online failure
        """
        for _ in range(iterations):
            if self.dev.cmts.is_cm_online(ignore_bpi, ignore_partial, ignore_cpe):
                return
            self.dev.board.touch()
            time.sleep(time_to_sleep)
        raise CodeError(f"CM {self.board_wan_mac} is not online!!")

    def get_current_time(self, fmt="%Y-%m-%dT%H:%M:%S%z") -> str:
        """Returns the current time on the CMTS
        the derived class only needs to set the "current_time_cmd" and
        "dateformat" strings (both specific to the cmts vendor) amd then call
        super.
        :return: the current time as a string formatted as "YYYY-MM-DD hh:mm:ss"
        :raises ValueError: if the conversion failed for whatever reason
        :raises CodeError: if there is no timestamp
        """
        if not self.current_time_cmd or not self.dateformat:
            raise NotImplementedError
        output = self.check_output(self.current_time_cmd)
        if output != "":
            return datetime.strptime(output, self.dateformat).strftime(fmt)
        else:
            raise CodeError("Failed to get CMTS current time")

    def ping(
        self,
        ping_ip: str,
        ping_count: int = 4,
        timeout: int = 4,
    ) -> bool:
        """Ping the device from cmts
        :param ping_ip: device ip which needs to be pinged.
        :param ping_count: optional. Number of ping packets.
        :param timeout: optional, seconds. Timeout for each packet.
        :return: True if all ping packets passed else False
        """

        timeout = (
            timeout * 1000
        )  # Convert timeout from seconds to milliseconds for backward compatibility
        command_timeout = (ping_count * timeout) / 1000 + 5  # Seconds
        output = self.check_output(
            f"ping {ping_ip} timeout {timeout} pktnum {ping_count}",
            timeout=command_timeout,
        )
        match = re.search(
            f"{ping_count} packets transmitted, {ping_count} packets received", output
        )
        return bool(match)

    # this is only suppose to run with instance methods
    @classmethod
    def connect_and_run(cls, func):
        def wrapper(*args, **kwargs):
            instance = args[0]
            exc_to_raise = None
            # to ensure we don't connect/disconnect in case of nested
            # API calls
            check = [func.__name__, instance.connlock][bool(instance.connlock)]
            if check == func.__name__:
                instance.connect()
                instance.connlock = check
            try:
                output = func(*args, **kwargs)
            except (PexpectErrorTimeout, IndexError, KeyError) as e:
                exc_to_raise = e
            if func.__name__ == instance.connlock:
                instance.logout()
                instance.connlock = None
                instance.pid = None
            if exc_to_raise:
                raise exc_to_raise
            return output

        return wrapper

    def tcpdump_capture(
        self,
        fname: str,
        interface: str = "any",
        additional_args: Optional[str] = None,
    ) -> None:
        """Capture packets from specified interface

        Packet capture using tcpdump utility at a specified interface.

        :param fname: name of the file where packet captures will be stored
        :type fname: str
        :param interface: name of the interface, defaults to "all"
        :type interface: str, optional
        :param additional_args: argument arguments to tcpdump executable, defaults to None
        :type additional_args: Optional[str], optional
        :yield: process id of tcpdump process
        :rtype: None
        """
        raise NotImplementedError("CMTS does not support tcpdump command")

    def remove_file_from_router(self, filename: str):
        """Delete a file from the router given the file name

        :param filename: name of file to remove
        :type filename: str
        """
        raise NotImplementedError("CMTS remove file from router is not implemented")

    def tcpdump_read_pcap(
        self,
        fname: str,
        additional_args: Optional[str] = None,
        timeout: int = 30,
        rm_pcap: bool = False,
    ) -> str:
        """Read packet captures using tcpdump from a device given the file name

        :param fname: name of file to read from
        :type fname: str
        :param additional_args: filter to apply on packet display, defaults to None
        :type additional_args: Optional[str], optional
        :param timeout: time for tcpdump read command to complete, defaults to 30
        :type timeout: int, optional
        :param rm_pcap: if True remove packet capture file after read, defaults to False
        :type rm_pcap: bool, optional
        :return: console output from the command execution
        :rtype: str
        """
        raise NotImplementedError("CMTS does not support tcpdump command")

    def tshark_read_pcap(
        self,
        fname: str,
        additional_args: Optional[str] = None,
        timeout: int = 30,
        rm_pcap: bool = False,
    ) -> str:
        """Read packet captures from an existing file

        :param fname: name of the file in which captures are saved
        :type fname: str
        :param additional_args: additional arguments for tshark command to display filtered output, defaults to None
        :type additional_args: Optional[str], optional
        :param timeout: time out for tshark command to be executed, defaults to 30
        :type timeout: int, optional
        :param rm_pcap: If True remove the packet capture file after reading it, defaults to False
        :type rm_pcap: bool, optional
        :return: return tshark read command console output
        :rtype: str
        """
        raise NotImplementedError("CMTS does not support tshark command")

    @abc.abstractmethod
    def ip_route(self) -> str:
        """Execute ip router command and parse the output."""
