"""Boardfarm DOCSIS cable modem base device."""

import time
from abc import abstractmethod
from typing import Dict, List

from boardfarm import hookimpl
from boardfarm.devices.base_devices.boardfarm_device import BoardfarmDevice
from boardfarm.exceptions import (
    DeviceBootFailure,
    DeviceRequirementError,
    EnvConfigError,
)
from boardfarm.lib.device_manager import DeviceManager
from boardfarm.lib.mibs_compiler import MibsCompiler
from boardfarm.templates.wan import WAN

from boardfarm_docsis.lib.docsis_encoder import DocsisConfigEncoder
from boardfarm_docsis.templates.cable_modem import CableModem
from boardfarm_docsis.templates.cmts import CMTS
from boardfarm_docsis.templates.provisioner import Provisioner


class DocsisCableModem(BoardfarmDevice, CableModem):
    """Boardfarm DOCSIS cable modem base device."""

    @property
    def mac_address(self) -> str:
        """Get cable modem MAC address.

        :returns: cable modem mac address
        """
        return self._config.get("cm_mac")

    @hookimpl
    def validate_device_requirements(self, device_manager: DeviceManager) -> None:
        """Boardfarm hook implementation to validate cable modem requirements.

        :param device_manager: device manager
        """
        if not (
            device_manager.get_devices_by_type(CMTS)
            and device_manager.get_devices_by_type(Provisioner)
            and device_manager.get_devices_by_type(WAN)
        ):
            raise DeviceRequirementError(
                f"{self.device_name} device requires wan, cmts and provisioner"
                " for booting"
            )
        if self._cmdline_args.ldap_credentials is None:
            raise DeviceRequirementError(
                f"{self.device_name} requires --ldap-credentials argument"
            )

    def _wait_until_cable_modem_is_online_on_cmts(self, cmts: CMTS) -> None:
        """Wait until cable modem is online on cmts.

        :param cmts: cmts device instance
        :raises DeviceBootFailure: when cable modem is not online within timeout
        """
        is_online = False
        timeout = 300
        while timeout > 0:
            if cmts.is_cable_modem_online(self.mac_address):
                is_online = True
                break
            time.sleep(15)
            timeout -= 15
        if not is_online:
            raise DeviceBootFailure(
                f"{self.mac_address} - Cable modem is not online on CMTS"
            )

    @abstractmethod
    def _get_device_mibs_path(self) -> List[str]:
        """Get device mibs directory paths.

        :returns: mibs directory paths
        """
        raise NotImplementedError

    def _provision_cable_modem(
        self, provisioner: Provisioner, tftp_device: WAN
    ) -> None:
        """Provision this cable modem on provisioner.

        :param provisioner: provisioner device
        :param tftp_device: tftp device
        """
        cm_config_path = DocsisConfigEncoder().encode_cm_config(
            self._config.get("boot_file"), self._get_device_mibs_path()
        )
        tftp_device.copy_local_file_to_tftpboot(str(cm_config_path))
        provisioner.provision_cable_modem(
            self.mac_address,
            cm_config_path.name,
            tftp_device.get_eth_interface_ipv4_address(),
            tftp_device.get_eth_interface_ipv6_address(),
        )
        cm_config_path.unlink()

    def get_provision_mode(self) -> str:
        """Get cable modem provision mode from boot file.

        :returns: cable modem provision mode
        :raises EnvConfigError: when failed to find provision mode
        """
        boot_file = self._config.get("boot_file")
        modes = ["disabled", "ipv4", "ipv6", "dual"]
        for index, provision_mode in enumerate(modes):
            if f"InitializationMode {index}" in boot_file:
                return provision_mode
        raise EnvConfigError("Unable to find cable modem provision mode")

    def _get_cable_modem_image_uri(self) -> str:
        """Get cable modem image URI.

        :returns: cable modem image URI
        """
        software_details: Dict = self._config.get("software")
        return self._config.get("mirror") + software_details.get("image_uri")

    @staticmethod
    def _get_docsis_snmp_flashing_mibs(
        image_name: str, tftp_ip_addr: str
    ) -> List[Dict]:
        """Get DOCSIS SNMP cable modem flashing MIBs.

        :param image_name: cable modem image name
        :param tftp_ip_addr: tftp server ip address
        :returns: docsis cable modem flashing snmp MIBs
        """
        snmp_commands = [
            {"mib": "docsDevSwServer", "dtype": "a", "value": tftp_ip_addr},
            {"mib": "docsDevSwFilename", "dtype": "s", "value": f'"{image_name}"'},
            {"mib": "docsDevSwServerTransportProtocol", "dtype": "i", "value": "2"},
            {"mib": "docsDevSwAdminStatus", "dtype": "i", "value": "1"},
        ]
        return snmp_commands

    def _flash_cable_modem_using_docsis_snmp_mibs(
        self, cm_wan_ip: str, tftp_device: WAN, docsis_snmp_mibs: List[Dict]
    ) -> None:
        """Flash cable modem using DOCSIS snmp commands.

        :param cm_wan_ip: cable modem wan ip address
        :param provisioner: provisioner device
        :param docsis_snmp_mibs: docsis snmp MIBs list
        :raises DeviceBootFailure: On SNMP command execution failure
        """
        mib_compiler = MibsCompiler(self._get_device_mibs_path())
        for snmp_mib in docsis_snmp_mibs:
            oid = mib_compiler.get_mib_oid(snmp_mib.get("mib"))
            snmp_command = (
                f"snmpset -On -v 2c -c private -t 10 {cm_wan_ip} {oid}.0 "
                f"{snmp_mib.get('dtype')} {snmp_mib.get('value')}"
            )
            result = tftp_device.execute_snmp_command(snmp_command)
            if f": {snmp_mib.get('value')}" not in result:
                raise DeviceBootFailure("Failed to flash cable modem via SNMP.")
