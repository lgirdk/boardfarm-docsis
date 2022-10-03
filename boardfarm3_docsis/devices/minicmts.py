"""Boardfarm DOCSIS MiniCMTS device module."""

import logging
import re
from argparse import Namespace
from io import StringIO
from ipaddress import IPv4Address, IPv6Address, ip_interface
from typing import Optional

import netaddr
import pandas as pd
from boardfarm3 import hookimpl
from boardfarm3.devices.base_devices import LinuxDevice
from boardfarm3.exceptions import ConfigurationFailure, DeviceNotFound

from boardfarm3_docsis.templates.cmts import CMTS

_LOGGER = logging.getLogger(__name__)


class MiniCMTS(LinuxDevice, CMTS):
    """Boardfarm DOCSIS MiniCMTS device."""

    def __init__(self, config: dict, cmdline_args: Namespace) -> None:
        """Initialize boardfarm DOCSIS MiniCMTS.

        :param config: device configuration
        :param cmdline_args: command line arguments
        """
        super().__init__(config, cmdline_args)
        self._shell_prompt = ["Topvision(.*)>", "Topvision(.*)#"]

    def _connect(self) -> None:
        """Establish connection to the device via SSH."""
        if self._console is None:
            super()._connect()
            self._additional_shell_setup()

    def _additional_shell_setup(self) -> None:
        """Additional shell initialization steps."""
        self._console.execute_command("enable")
        # Change terminal length to inf in order to avoid pagination
        self._console.execute_command("terminal length 0")
        # Increase connection timeout until better solution
        self._console.execute_command("config terminal")
        self._console.execute_command("line vty")
        self._console.execute_command("exec-timeout 60")
        self._console.execute_command("end")

    @hookimpl
    def boardfarm_server_boot(self) -> None:
        """Boot MiniCMTS device."""
        _LOGGER.info("Booting %s(%s) device", self.device_name, self.device_type)
        self._connect()

    @hookimpl
    def boardfarm_shutdown_device(self) -> None:
        """Close all the connection to MiniCMTS."""
        _LOGGER.info("Shutdown %s(%s) device", self.device_name, self.device_type)
        self._disconnect()

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

    def _get_cable_modem_cpe_table_data(self, mac: str) -> pd.DataFrame:
        """Return scm cpe dataframe.

        :param mac: mac address of the CM
        :type mac: str
        :return: dataframe
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
        output = self._console.execute_command(f"show cable modem {mac} cpe")
        csv = pd.read_csv(
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
        return csv

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
        mac_address = mac_address.replace(":", "").lower()
        return ".".join(re.findall("[0-9a-z]{4}", mac_address))

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
        elif not ignore_bpi and not re.search(r"online\(p(t|k)", status):
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
            raise ConfigurationFailure("Cable modem is not offline after reset")

    def get_cable_modem_ip_address(self, mac_address: str) -> str:
        """Get cable modem IP address on CMTS.

        :param mac_address: cable modem MAC address
        :returns: IP address of the cable modem on CMTS
        :raises DeviceNotFound: when given cable modem is not found on CMTS
        """
        ip_address = self._get_cable_modem_table_data(mac_address, "IP_ADDRESS")
        if ip_address is None:
            raise DeviceNotFound(f"Unable to find {mac_address} cable modem on CMTS.")
        return ip_address.strip().replace("*", "")

    def get_cmts_ip_bundle(self, gw_ip: Optional[str] = None) -> str:
        """Get CMTS bundle IP.

        Validate if Gateway IP is configured in CMTS and both are in same network.
        The first host address within the network will be assumed to be gateway
        for Mini CMTS

        :param gw_ip: gateway ip address. defaults to None
        :raises ValueError: Failed to get the CMTS bundle IP
        :return: gateway ip if address configured on minicmts else return all ip bundles
        """
        output = self._console.execute_command(
            'show running-config | include "ip address"'
        )
        if gw_ip is None:
            return output
        for line in output.splitlines():
            addr, mask = line.split()[2:-1]
            cmts_ip = ip_interface(addr + "/" + mask)
            if gw_ip == str(next(cmts_ip.network.hosts())):
                return gw_ip
        raise ValueError("Failed to get the CMTS bundle IP")

    def get_ip_routes(self) -> str:
        """Get IP routes from the quagga router.

        :return: ip routes collected from quagga router
        :rtype: str
        """
        return "None"

    def clear_cm_reset(self, mac_address: str) -> None:
        """Reset the CM from cmts.

        Uses cli command:
            clear cable modem <mac_address> reset

        :param mac_address: mac address of the CM
        :type mac_address: str
        """
        self._console.execute_command(f"clear cable modem {mac_address} reset")

    def _get_cpe_ip(
        self, mac_address: netaddr.EUI, offset: int, ipv6: bool
    ) -> Optional[str]:
        cpe_table = self._get_cable_modem_cpe_table_data(mac_address)
        ip_type = IPv6Address if ipv6 else IPv4Address
        ertr_mac = netaddr.EUI(int(mac_address) + offset)
        ertr_mac.dialect = netaddr.mac_cisco

        for cpe_mac, cpe_details in cpe_table.iterrows():
            if cpe_mac != ertr_mac:
                continue
            try:
                return str(ip_type(cpe_details["CPE_IP_ADDRESS"]))
            except ValueError:
                pass
        return None

    def get_ertr_ipv4(self, mac_address: str) -> Optional[str]:
        """Get erouter ipv4 from CMTS.

        :param mac_address: mac address of the cable modem
        :type mac_address: str
        :return: returns ipv4 address of erouter else None
        :rtype: string, None
        """
        return self._get_cpe_ip(
            mac_address=netaddr.EUI(mac_address, dialect=netaddr.mac_cisco),
            offset=2,
            ipv6=False,
        )

    def get_ertr_ipv6(self, mac_address: str) -> Optional[str]:
        """Get erouter ipv6 from CMTS.

        :param mac_address: mac address of the cable modem
        :type mac_address: str
        :return: returns ipv6 address of erouter else None
        :rtype: string, None
        """
        return self._get_cpe_ip(
            mac_address=netaddr.EUI(mac_address, dialect=netaddr.mac_cisco),
            offset=2,
            ipv6=True,
        )
