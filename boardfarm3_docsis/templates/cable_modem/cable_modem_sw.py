"""Cable modem software template."""

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from boardfarm3.templates.cpe import CPESW

if TYPE_CHECKING:
    from boardfarm3.lib.mibs_compiler import MibsCompiler
    from boardfarm3.lib.networking import DNS
    from boardfarm3.templates.wan import WAN

    from boardfarm3_docsis.templates.cable_modem.cable_modem_mibs import CableModemMibs
    from boardfarm3_docsis.templates.cmts import CMTS
    from boardfarm3_docsis.templates.provisioner import Provisioner


class CableModemSW(CPESW):
    """Cable modem software template."""

    @property
    @abstractmethod
    def dns(self) -> DNS:
        """DNS component of cpe software."""
        raise NotImplementedError

    @property
    @abstractmethod
    def provisioning_messages(self) -> dict[str, str]:
        """Provisioning messages for verification."""
        raise NotImplementedError

    @property
    @abstractmethod
    def mibs(self) -> CableModemMibs:
        """Device specific SNMP mibs details."""
        raise NotImplementedError

    @abstractmethod
    def flash_via_snmp(self, image_uri: str, tftp_device: WAN, cmts: CMTS) -> None:
        """Flash cable modem via snmp.

        :param image_uri: image uri
        :param tftp_device: tftp device instance
        :param cmts: cmts device instance
        """
        raise NotImplementedError

    @abstractmethod
    def provision_cable_modem(
        self,
        provisioner: Provisioner,
        tftp_device: WAN,
        boot_file: str = "",
        boot_file_mta: str = "",
    ) -> None:
        """Provision this cable modem on given provisioner.

        :param provisioner: provisioner device
        :type provisioner: Provisioner
        :param tftp_device: tftp device
        :type tftp_device: WAN
        :param boot_file: cable modem boot file
        :type boot_file: str
        :param boot_file_mta: mta boot file
        :type boot_file_mta: str
        """
        raise NotImplementedError

    @abstractmethod
    def get_boot_file(self) -> str:
        """Return cable modem bootfile.

        :return: cable modem bootfile
        :rtype: str
        """
        raise NotImplementedError

    @abstractmethod
    def get_mta_boot_file(self) -> str:
        """Return cable modem mta bootfile.

        :return: cable modem mta bootfile
        :rtype: str
        """
        raise NotImplementedError

    @abstractmethod
    def get_mibs_compiler(self) -> MibsCompiler:
        """Return mibs compiler instance.

        :return: mibs compiler instance
        :rtype: Type[MibsCompiler]
        """
        raise NotImplementedError

    @abstractmethod
    def login_to_linux_consoles(self) -> None:
        """Login to the cable modem linux consoles."""
        raise NotImplementedError

    @abstractmethod
    def get_golden_ds_freq_list(self) -> list[str]:
        """Return the golden frequency list.

        :return: golden frequency list
        :rtype: list[str]
        """
        raise NotImplementedError

    @abstractmethod
    def verify_cm_cfg_file_read_log(self, logs: str | None) -> bool:
        """Verify the cable modem configuration file log.

        :param logs: boot logs from console
        :type logs: Union[str, None]
        :return: True if the log is present,False otherwise
        :rtype: bool
        """
        raise NotImplementedError

    @abstractmethod
    def get_gateway_provision_log(self) -> str | None:
        """Fetch the Gateway Provision log from the board.

        :return: gateway provision logs
        :rtype: Union[str, None]
        """
        raise NotImplementedError

    @abstractmethod
    def stop_cm_agent(self) -> None:
        """Kill CM agent process running on DUT."""
        raise NotImplementedError
