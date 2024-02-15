"""Boardfarm DOCSIS MiniCMTS device module."""

from __future__ import annotations

import logging
import re
from io import StringIO
from ipaddress import IPv4Address, IPv6Address, ip_interface
from typing import TYPE_CHECKING

import netaddr
import pandas as pd
from boardfarm3 import hookimpl
from boardfarm3.devices.base_devices.boardfarm_device import BoardfarmDevice
from boardfarm3.exceptions import ConfigurationFailure, DeviceNotFound
from boardfarm3.lib.connection_factory import connection_factory
from boardfarm3.lib.utils import get_nth_mac_address

from boardfarm3_docsis.templates.cmts import CMTS

if TYPE_CHECKING:
    from argparse import Namespace

    from boardfarm3.lib.boardfarm_pexpect import BoardfarmPexpect

_LOGGER = logging.getLogger(__name__)


class MiniCMTS(BoardfarmDevice, CMTS):
    """Boardfarm DOCSIS MiniCMTS device."""

    def __init__(self, config: dict, cmdline_args: Namespace) -> None:
        """Initialize boardfarm DOCSIS MiniCMTS.

        :param config: device configuration
        :param cmdline_args: command line arguments
        """
        super().__init__(config, cmdline_args)
        self._console: BoardfarmPexpect = None
        self._shell_prompt = ["Topvision(.*)>", "Topvision(.*)#"]

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

    async def _additional_shell_setup_async(self) -> None:
        """Additional shell initialization steps."""
        await self._console.login_to_server_async(
            password=self._config.get("password", "admin"),
        )
        await self._console.execute_command_async("enable")
        # Change terminal length to inf in order to avoid pagination
        await self._console.execute_command_async("terminal length 0")
        # Increase connection timeout until better solution
        await self._console.execute_command_async("config terminal")
        await self._console.execute_command_async("line vty")
        await self._console.execute_command_async("exec-timeout 60")
        await self._console.execute_command_async("end")

    async def _connect_to_console_async(self) -> None:
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
        await self._additional_shell_setup_async()

    @hookimpl
    def boardfarm_server_boot(self) -> None:
        """Boot MiniCMTS device."""
        _LOGGER.info("Booting %s(%s) device", self.device_name, self.device_type)
        self._connect_to_console()

    @hookimpl
    def boardfarm_skip_boot(self) -> None:
        """Boot MiniCMTS device."""
        _LOGGER.info(
            "Initializing %s(%s) device with skip-boot option",
            self.device_name,
            self.device_type,
        )
        self._connect_to_console()

    @hookimpl
    async def boardfarm_skip_boot_async(self) -> None:
        """Boot MiniCMTS device using the asyncio libs."""
        _LOGGER.info(
            "Initializing %s(%s) device with skip-boot option",
            self.device_name,
            self.device_type,
        )
        await self._connect_to_console_async()

    @hookimpl
    def boardfarm_shutdown_device(self) -> None:
        """Close all the connection to MiniCMTS."""
        _LOGGER.info("Shutdown %s(%s) device", self.device_name, self.device_type)
        if self._console is not None:
            self._console.close()
            self._console = None

    def _get_cable_modem_table_data(self, mac_address: str, column_name: str) -> str:
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
            delim_whitespace=True,
            engine="python",
            index_col="MAC_ADDRESS",
            dtype=None,
        )
        return (
            csv.loc[mac_address][column_name] if mac_address in csv.index else None
        )  # pylint: disable=no-member # known issue

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
            delim_whitespace=True,
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
        elif not ignore_bpi and re.search(r"online\(p(t|k)", status) is not None:
            _LOGGER.info("Cable modem in BPI is disabled: %s", status)
        elif not ignore_partial and re.search(r"p-online", status):
            _LOGGER.info("Cable modem in partial service: %s", status)
        elif not ignore_cpe and re.search(r"online\(d", status):
            _LOGGER.info("Cable modem is prohibited from forwarding data: %s", status)
        else:
            _LOGGER.info("Cable modem is online: %s", status)
            is_modem_online = True
        return is_modem_online

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
            if gw_ip == str(next(cmts_ip.network.hosts())):
                return gw_ip
        err_msg = "Failed to get the CMTS bundle IP"
        raise ValueError(err_msg)

    def get_ip_routes(self) -> str:
        """Get IP routes from the quagga router.

        :return: ip routes collected from quagga router
        :rtype: str
        """
        return "None"

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
        """
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
