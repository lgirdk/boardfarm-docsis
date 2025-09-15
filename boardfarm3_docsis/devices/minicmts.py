"""Boardfarm DOCSIS MiniCMTS device module."""

from __future__ import annotations

import logging
import re
from io import StringIO
from ipaddress import IPv4Address, IPv6Address, ip_interface
from time import sleep
from typing import TYPE_CHECKING

import netaddr
import pandas as pd
import pexpect
from boardfarm3 import hookimpl
from boardfarm3.devices.base_devices.boardfarm_device import BoardfarmDevice
from boardfarm3.exceptions import (
    BoardfarmException,
    ConfigurationFailure,
    DeviceConnectionError,
    DeviceNotFound,
    SCPConnectionError,
)
from boardfarm3.lib.connection_factory import connection_factory
from boardfarm3.lib.connections.connect_and_run import connect_and_run
from boardfarm3.lib.connections.local_cmd import LocalCmd
from boardfarm3.lib.networking import scp
from boardfarm3.lib.networking import start_tcpdump as start_dump
from boardfarm3.lib.networking import stop_tcpdump as stop_dump
from boardfarm3.lib.shell_prompt import DEFAULT_BASH_SHELL_PROMPT_PATTERN
from boardfarm3.lib.utils import get_nth_mac_address
from pexpect.exceptions import ExceptionPexpect

from boardfarm3_docsis.templates.cmts import CMTS

if TYPE_CHECKING:
    from argparse import Namespace

    from boardfarm3.lib.boardfarm_pexpect import BoardfarmPexpect
    from boardfarm3.templates.wan import WAN

_LOGGER = logging.getLogger(__name__)


# pylint: disable=duplicate-code,too-many-public-methods
class MiniCMTS(BoardfarmDevice, CMTS):
    """Boardfarm DOCSIS MiniCMTS device."""

    def __init__(self, config: dict, cmdline_args: Namespace) -> None:
        """Initialize boardfarm DOCSIS MiniCMTS.

        :param config: device configuration
        :param cmdline_args: command line arguments
        """
        super().__init__(config, cmdline_args)
        self._console: BoardfarmPexpect = None
        self._rtr_console: BoardfarmPexpect = None
        self._shell_prompt = ["Topvision(.*)>", "Topvision(.*)#"]
        self._router_shell_prompt = [DEFAULT_BASH_SHELL_PROMPT_PATTERN]

    def _additional_shell_setup(self) -> None:
        """Additional shell initialization steps."""
        self._console.login_to_server(password=self._config.get("password", "admin"))
        self._console.execute_command("enable")
        # Change terminal length to inf in order to avoid pagination
        self._console.execute_command("terminal length 0")
        # Increase connection timeout until better solution
        self._console.execute_command("config terminal")
        self._console.execute_command("line vty")
        self._console.execute_command("exec-timeout 60")
        self._console.execute_command("end")

    def _connect_to_console(self) -> None:
        self._console = connection_factory(
            self._config.get("connection_type"),
            f"{self.device_name}.console",
            username=self._config.get("username", "admin"),
            password=self._config.get("password", "admin"),
            ip_addr=self._config.get("ipaddr"),
            port=self._config.get("port", "22"),
            shell_prompt=self._shell_prompt,
            save_console_logs=self._cmdline_args.save_console_logs,
        )
        self._additional_shell_setup()

    def _connect_to_rtr_console(self) -> None:
        """Create FRR router connection."""
        self._rtr_console = connection_factory(
            connection_type=self._config.get("connection_type"),
            connection_name="FRR_router",
            username=self._config.get("router_username", "root"),
            password=self._config.get("router_password", "bigfoot1"),
            ip_addr=self._config.get("router_ipaddr", ""),
            port=self._config.get("router_port", ""),
            shell_prompt=self._router_shell_prompt,
        )
        self._rtr_console.login_to_server()

    async def _connect_to_rtr_console_async(self) -> None:
        """Create FRR router connection."""
        self._rtr_console = connection_factory(
            connection_type=self._config.get("connection_type"),
            connection_name="FRR_router",
            username=self._config.get("router_username", "root"),
            password=self._config.get("router_password", "bigfoot1"),
            ip_addr=self._config.get("router_ipaddr", ""),
            port=self._config.get("router_port", ""),
            shell_prompt=self._router_shell_prompt,
        )
        await self._rtr_console.login_to_server_async()

    @hookimpl
    def boardfarm_server_boot(self) -> None:
        """Boot MiniCMTS device."""
        _LOGGER.info("Booting %s(%s) device", self.device_name, self.device_type)
        self._connect_to_rtr_console()

    @hookimpl
    def boardfarm_skip_boot(self) -> None:
        """Boot MiniCMTS device."""
        _LOGGER.info(
            "Initializing %s(%s) device with skip-boot option",
            self.device_name,
            self.device_type,
        )
        self._connect_to_rtr_console()

    @hookimpl
    async def boardfarm_skip_boot_async(self) -> None:
        """Boot MiniCMTS device using the asyncio libs."""
        _LOGGER.info(
            "Initializing %s(%s) device with skip-boot option",
            self.device_name,
            self.device_type,
        )
        await self._connect_to_rtr_console_async()

    @hookimpl
    def boardfarm_shutdown_device(self) -> None:
        """Close all the connection to MiniCMTS."""
        _LOGGER.info("Shutdown %s(%s) device", self.device_name, self.device_type)
        if self._rtr_console is not None:
            self._rtr_console.close()
            self._rtr_console = None
        if self._console is not None:
            self._console.close()
            self._console = None

    @connect_and_run
    def _get_cable_modem_table_data(
        self, mac_address: str, column_name: str
    ) -> str | None:
        """Get given cable modem information on CMTS.

        :param mac_address: cable modem mac address
        :type mac_address: str
        :param column_name: cable modem data column name
        :type column_name: str
        :returns: cable modem column data, None if not available
        :rtype: str
        """
        mac_address = self._convert_mac_address(mac_address)
        output = self._console.execute_command("show cable modem")
        columns = [
            "MAC_ADDRESS",
            "IP_ADDRESS",
            "I/F",
            "MAC_STATE",
            "PRIMARY_SID",
            "RXPWR(dBmV)",
            "TIMING_OFFSET",
            "NUMBER_CPE",
            "BPI_ENABLED",
            "ONLINE_TIME",
        ]
        csv = pd.read_csv(
            StringIO(output),
            skiprows=2,
            skipfooter=1,
            names=columns,
            header=None,
            sep=r"\s+",
            engine="python",
            index_col="MAC_ADDRESS",
            dtype=None,
        )
        return (
            str(csv.loc[mac_address][column_name]) if mac_address in csv.index else None
        )  # pylint: disable=no-member # known issue

    @connect_and_run
    def _get_cable_modem_cpe_table_data(self, cpe_mac: str) -> pd.DataFrame:
        """Return cable modem cpe table data of cpe with given mac.

        :param cpe_mac: mac address of the cpe
        :type cpe_mac: str
        :return: cable modem cpe table data of cpe
        :rtype: pd.DataFrame
        """
        columns = [
            "CPE_MAC",
            "CMC_INDEX",
            "CM_MAC",
            "CPE_IP_ADDRESS",
            "DUAL_IP",
            "CPE_TYPE",
            "LEASE_TIME",
            "LEARNED",
        ]
        cpe_mac = self._convert_mac_address(cpe_mac)
        output = self._console.execute_command(f"show cable modem {cpe_mac} cpe")
        return pd.read_csv(
            StringIO(output),
            skiprows=1,
            skipfooter=6,
            names=columns,
            header=None,
            sep=r"\s+",
            engine="python",
            index_col="CPE_MAC",
            dtype=None,
        )

    def _get_cable_modem_status(self, mac_address: str) -> str:
        """Get given cable modem status on cmts.

        :param mac_address: cable modem mac address
        :returns: cable modem status, None on unknown status
        """
        return self._get_cable_modem_table_data(mac_address, "MAC_STATE")

    @staticmethod
    def _convert_mac_address(mac_address: str) -> str:
        """Convert mac address to cmts format.

        :param mac_address: mac address
        :returns: mac address in cmts format
        """
        return str(netaddr.EUI(mac_address, dialect=netaddr.mac_cisco))

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
        status = self._get_cable_modem_status(mac_address)
        is_modem_online = False
        if status is None:
            _LOGGER.info("Cable modem status is unknown")
        elif "offline" in status:
            _LOGGER.info("Cable modem is %s", status)
        elif "init" in status:
            _LOGGER.info("Cable modem is initializing: %s", status)
        elif "online" not in status:
            _LOGGER.info("Cable modem in unknown state: %s", status)
        elif not ignore_bpi and re.search(r"online\(p(t|k)", status) is None:
            _LOGGER.info("Cable modem in BPI is disabled: %s", status)
        elif not ignore_partial and re.search(r"p-online", status) is not None:
            _LOGGER.info("Cable modem in partial service: %s", status)
        elif not ignore_cpe and re.search(r"online\(d", status) is not None:
            _LOGGER.info("Cable modem is prohibited from forwarding data: %s", status)
        else:
            _LOGGER.info("Cable modem is online: %s", status)
            is_modem_online = True
        return is_modem_online

    @connect_and_run
    def reset_cable_modem_status(self, mac_address: str) -> None:
        """Reset given cable modem status on cmts.

        :param mac_address: mac address of the cable modem
        :raises ConfigurationFailure: when failed to reset cable modem status
        """
        self._console.execute_command(f"clear cable modem {mac_address} reset")
        status = self._get_cable_modem_status(mac_address)
        if status != "offline":
            err_msg = "Cable modem is not offline after reset"
            raise ConfigurationFailure(err_msg)

    def get_cable_modem_ip_address(self, mac_address: str) -> str:
        """Get cable modem IP address on CMTS.

        :param mac_address: cable modem MAC address
        :returns: IP address of the cable modem on CMTS
        :raises DeviceNotFound: when given cable modem is not found on CMTS
        """
        ip_address = self._get_cable_modem_table_data(mac_address, "IP_ADDRESS")
        if ip_address is None:
            err_msg = f"Unable to find {mac_address} cable modem on CMTS."
            raise DeviceNotFound(err_msg)
        return ip_address.strip().replace("*", "")

    @connect_and_run
    def get_cmts_ip_bundle(self, gw_ip: str | None = None) -> str:
        """Get CMTS bundle IP.

        Validate if Gateway IP is configured in CMTS and both are in same network.
        The first host address within the network will be assumed to be gateway
        for Mini CMTS

        :param gw_ip: gateway ip address. defaults to None
        :raises ValueError: Failed to get the CMTS bundle IP
        :return: gateway ip if address configured on minicmts else return all ip bundles
        """
        output = self._console.execute_command(
            'show running-config | include "ip address"',
        )
        if gw_ip is None:
            return output
        for line in output.splitlines():
            addr, mask = line.split()[2:-1]
            cmts_ip = ip_interface(f"{addr}/{mask}")
            if gw_ip == str(next(cmts_ip.network.hosts())):  # type: ignore[arg-type]
                return gw_ip
        err_msg = "Failed to get the CMTS bundle IP"
        raise ValueError(err_msg)

    def get_ip_routes(self) -> list[str]:
        """Get IP routes from the quagga router.

        :return: ip routes collected from quagga router
        :rtype: list[str]
        """
        self._rtr_console.sudo_sendline("ip route")
        self._rtr_console.expect(self._router_shell_prompt, timeout=10)
        output = self._rtr_console.before.splitlines()
        return output[1:]

    # TODO: replace this method with reset_cable_modem_status
    def clear_cm_reset(self, mac_address: str) -> None:
        """Reset the CM from cmts.

        Uses cli command:
            clear cable modem <mac_address> reset

        :param mac_address: mac address of the CM
        :type mac_address: str
        """
        self.reset_cable_modem_status(mac_address)

    def _get_cpe_ip_address(
        self,
        mac_address: str,
        offset: int,
        is_ipv6: bool,
    ) -> str | None:
        cpe_table = self._get_cable_modem_cpe_table_data(mac_address)
        ip_type = IPv6Address if is_ipv6 else IPv4Address
        mac = self._convert_mac_address(get_nth_mac_address(mac_address, offset))
        for cpe_mac, cpe_details in cpe_table.iterrows():
            if cpe_mac != mac:
                continue
            try:
                return str(ip_type(cpe_details["CPE_IP_ADDRESS"]))
            except ValueError:
                pass
        return None

    def get_ertr_ipv4(self, mac_address: str) -> str | None:
        """Get erouter ipv4 from CMTS.

        :param mac_address: mac address of the cable modem
        :type mac_address: str
        :return: ipv4 address of erouter else None
        :rtype: Optional[str]
        """
        return self._get_cpe_ip_address(mac_address, offset=2, is_ipv6=False)

    def get_ertr_ipv6(self, mac_address: str) -> str | None:
        """Get erouter ipv6 from CMTS.

        :param mac_address: mac address of the cable modem
        :type mac_address: str
        :return: ipv6 address of erouter else None
        :rtype: Optional[str]
        """
        return self._get_cpe_ip_address(mac_address, offset=2, is_ipv6=True)

    def get_mta_ipv4(self, mac_address: str) -> str | None:
        """Get the MTA ipv4 from CMTS.

        :param mac_address: mac address of the cable modem
        :type mac_address: str
        :return: ipv4 address of mta else None
        :rtype: Optional[str]
        """
        # Note: currently MTA on PacketCable 1.0 only supports IPv4
        return self._get_cpe_ip_address(mac_address, offset=1, is_ipv6=False)

    @connect_and_run
    def _get_cm_docsis_provisioned_version(self, mac_address: str) -> float:
        """Get the docsis version of cable modem.

        :param mac_address: mac address of the cable modem
        :type mac_address: str
        :return: Docsis version of the cm
        :rtype: float
        :raises ValueError: Failed to get the docsis version
        """
        mac_address = self._convert_mac_address(mac_address)
        output = self._console.execute_command(
            f"show cable modem {mac_address} docsis version",
        )
        result = re.search(r"DOCSISv(\d\.\d)", output)
        if result is None:
            err_msg = "Failed to get the Docsis Version"
            raise ValueError(err_msg)
        return float(result.group(1))

    @connect_and_run
    def _get_cm_channel_bonding_detail(self, mac_address: str) -> dict[str, str]:
        """Get the primary channel values.

        :param mac_address: mac address of the cable modem
        :type mac_address: str
        :return: upstream and downstream channel values
        :rtype: dict[str, str]
        :raises ValueError: Failed to get Upstream & Downstream channel values
        """
        mac_address = self._convert_mac_address(mac_address)
        result = re.search(
            r"(\d+\([\d\,]+\))\s+(\d+\([\d\,]+\))",
            self._console.execute_command(
                f"show cable modem {mac_address} primary-channel",
            ),
        )
        if result is None:
            # TODO: no idea why 2 below, clarify
            err_msg = f"Failed to get Upstream & Downstream values:\n {result}"
            raise ValueError(err_msg)
        return dict(zip(["US", "DS"], (result.group(1), result.group(2))))

    def get_interactive_consoles(self) -> dict[str, BoardfarmPexpect]:
        """Get the interactive console from the CMTS.

        :return: The interactive console of the CMTS
        :rtype: dict[str, BoardfarmPexpect]
        :raises conn_exception: In case interact session fails
        """
        conn_exception: DeviceConnectionError = None
        for _ in range(3):
            try:
                if self.is_console_connected():
                    self.disconnect_console()
                self.connect_console()
                break
            except DeviceConnectionError as exc:
                conn_exception = exc
                self._console = None
                sleep(15)
        else:
            raise conn_exception

        return {"console": self._console}

    def get_downstream_channel_value(self, mac: str) -> str:
        """Get the downstream channel value.

        :param mac: mac address of the cable modem
        :type mac: str
        :return: downstream channel value
        :rtype: str
        """
        return re.search(
            r"'DS': \'((\d{1,2}))\(",
            str(self._get_cm_channel_bonding_detail(mac)),
        )[1]

    def get_upstream_channel_value(self, mac: str) -> str:
        """Get the upstream channel value.

        :param mac: mac address of the cable modem
        :type mac: str
        :return: upstream channel value
        :rtype: str
        """
        return re.search(
            r"'US': \'((\d{1,2}))\(",
            str(self._get_cm_channel_bonding_detail(mac)),
        )[1]

    def get_cm_channel_values(self, mac: str) -> dict[str, str]:
        """Get the cm channel values.

        :param mac: mac address of the cable modem
        :type mac: str
        :return: cm channel values
        :rtype: dict[str, str]
        """
        return self._get_cm_channel_bonding_detail(mac)

    def connect_console(self) -> None:
        """Connect to the console."""
        self._connect_to_console()

    def is_console_connected(self) -> bool:
        """Get status of the connection.

        :return: True or False
        :rtype: bool
        """
        return self._console and not self._console.closed

    def disconnect_console(self) -> None:
        """Disconnect from the console."""
        if self._console.closed:
            return
        try:
            self._console.close()
        except ExceptionPexpect:
            # TODO: at times the network lab seems glitchy, just
            # consider the connection as closed.
            _LOGGER.exception(
                "Received anexception on closing cmts console!! Leaking the connection",
            )
            self._console.closed = True

    @property
    def console(self) -> BoardfarmPexpect:
        """Returns FRR router console.

        Since CMTS does not support tcpdump, mini cmts router is required for tcpdump,
         this console is used in use cases for operations such as tcpdump capture.

        :return: console
        :rtype: BoardfarmPexpect
        """
        return self._rtr_console

    def scp_device_file_to_local(self, local_path: str, source_path: str) -> None:
        """Copy a local file from a server using SCP.

        :param local_path: local file path
        :param source_path: source path
        """
        source_path = (
            f"{self._config.get('router_username', 'root')}@"
            f"{self._config.get('router_ipaddr')}:{source_path}"
        )
        self._scp_local_files(source=source_path, destination=local_path)

    def _scp_local_files(self, source: str, destination: str) -> None:
        """Perform file copy on local console using SCP.

        :param source: source file path
        :param destination: destination file path
        :raises SCPConnectionError: when SCP command return non-zero exit code
        """
        args = [
            f"-P {self._config.get('router_port')}",
            "-o StrictHostKeyChecking=no",
            "-o UserKnownHostsFile=/dev/null",
            "-o ServerAliveInterval=60",
            "-o ServerAliveCountMax=5",
            source,
            destination,
        ]
        session = LocalCmd(
            f"{self.device_name}.scp",
            "scp",
            save_console_logs="",
            args=args,
            # TODO: why do we need to pass shell prompt?
            shell_prompt=self._router_shell_prompt,
        )
        session.setwinsize(24, 80)
        match_index = session.expect(
            [" password:", "\\d+%", pexpect.TIMEOUT, pexpect.EOF],
            timeout=20,
        )
        if match_index in (2, 3):
            msg = f"Failed to perform SCP from {source} to {destination}"
            raise SCPConnectionError(
                msg,
            )
        if match_index == 0:
            session.sendline(self._config.get("router_password"))
        session.expect(pexpect.EOF, timeout=90)
        if session.wait() != 0:
            msg = f"Failed to SCP file from {source} to {destination}"
            raise SCPConnectionError(
                msg,
            )

    def tshark_read_pcap(
        self,
        fname: str,
        additional_args: str | None = None,
        timeout: int = 30,
        rm_pcap: bool = False,
    ) -> str:
        """Read packet captures from an existing file.

        :param fname: name of the file in which captures are saved
        :param additional_args: additional arguments for tshark command
        :param timeout: timeout for tshark command to be executed, defaults to 30
        :param rm_pcap: If True remove the packet capture file after reading it
        :return: return tshark read command console output
        :raises  FileNotFoundError: when file is not found
        :raises BoardfarmException: when invalid filters are added
        """
        output = self._run_command_with_args(
            "tshark -r",
            fname,
            additional_args,
            timeout,
        )

        if f'The file "{fname}" doesn\'t exist' in output:
            msg = f"pcap file not found {fname} on device {self.device_name}"
            raise FileNotFoundError(
                msg,
            )
        if "was unexpected in this context" in output:
            msg = (
                "Invalid filters for tshark read, review "
                f"additional_args={additional_args}"
            )
            raise BoardfarmException(
                msg,
            )
        if rm_pcap:
            self.console.sudo_sendline(f"rm {fname}")
            self.console.expect(self._router_shell_prompt)
        return output

    def _run_command_with_args(
        self,
        command: str,
        fname: str,
        additional_args: str | None,
        timeout: int,
    ) -> str:
        """Run command with given arguments and return the output.

        :param command: command to run
        :param fname: name of the file in which captures are saved
        :param additional_args:  additional arguments to run command
        :param timeout: timout for the command
        :return: return read command console output
        """
        read_command = f"{command} {fname} "
        if additional_args:
            read_command += additional_args
        self.console.sudo_sendline(read_command)
        self.console.expect(self._router_shell_prompt, timeout=timeout)
        return self.console.before

    def delete_file(self, filename: str) -> None:
        """Delete the file from the device.

        :param filename: name of the file with absolute path
        :type filename: str
        """
        self.console.execute_command(f"rm {filename}")

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
        scp(
            self.console,
            # TODO: private members should not be used, BOARDFARM-5040
            host._config.get("ipaddr"),  # type: ignore[attr-defined] # noqa: SLF001 pylint: disable=W0212
            host._config.get("port"),  # type: ignore[attr-defined] # noqa: SLF001 pylint: disable=W0212
            host._username,  # type: ignore[attr-defined] # noqa: SLF001 pylint: disable=W0212
            host._password,  # type: ignore[attr-defined] # noqa: SLF001 pylint: disable=W0212
            src_path,
            dest_path,
            "upload",
        )

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
        return start_dump(
            console=self._rtr_console,
            interface=interface,
            output_file=output_file,
            filters=filters,
            port=port,
            additional_filters=additional_filters,
        )

    def stop_tcpdump(self, process_id: str) -> None:
        """Stop tcpdump capture.

        :param process_id: tcpdump process id
        :type process_id: str
        """
        stop_dump(self._rtr_console, process_id=process_id)


if __name__ == "__main__":
    # stubbed instantation of the device
    # this would throw a linting issue in case the device does not follow the template
    from argparse import Namespace

    MiniCMTS(config={}, cmdline_args=Namespace())
