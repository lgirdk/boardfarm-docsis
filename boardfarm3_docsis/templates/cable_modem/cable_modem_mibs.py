"""Cable modem mibs template."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class MIBInfo:
    """Dataclass for the MIBs defined either vendors specific or docsis mibs."""

    mib_name: str
    index: int
    type: str
    value: str | int


class CableModemMibs(ABC):
    """Cable modem mibs template."""

    @property
    @abstractmethod
    def vendor_prefix(self) -> str:
        """Vendor prefix.

        :raises NotImplementedError: not implemented in ABC
        """
        msg = "Vendor Prefix string must be defined for the gateway"
        raise NotImplementedError(msg)

    @property
    @abstractmethod
    def sw_method_mib(self) -> str:
        """Software update method mib.

        :raises NotImplementedError: not implemented in ABC
        """
        msg = "SW Method MIB name supported by vendor must be defined for the gateway"
        raise NotImplementedError(msg)

    @property
    @abstractmethod
    def sw_server_address_mib(self) -> str:
        """Software server address mib.

        :raises NotImplementedError: not implemented in ABC
        """
        msg = "SW Server Address MIB name supported by vendor must be defined for the \
        gateway"
        raise NotImplementedError(msg)

    @property
    @abstractmethod
    def sw_model_table_mib(self) -> str:
        """Software modem table mib.

        :raises NotImplementedError: not implemented in ABC
        """
        msg = "SW update table MIB name supported by vendor must be defined for the \
        gateway"
        raise NotImplementedError(msg)

    @property
    @abstractmethod
    def mfg_cvc(self) -> str:
        """Manufacturer CVC details.

        :raises NotImplementedError: not implemented in ABC
        """
        msg = "Manufacturer CVC Details must be defined for the gateway"
        raise NotImplementedError(msg)

    @property
    @abstractmethod
    def hw_model_mib(self) -> str:
        """Manufacturer hardware model details.

        :raises NotImplementedError: not implemented in ABC
        """
        msg = "Manufacturer hardware model must be defined for the gateway"
        raise NotImplementedError(msg)

    @abstractmethod
    def get_sw_update_mibs(  # pylint: disable=too-many-arguments  # noqa: PLR0913
        self,
        model: str,
        server_address: str,
        sw_file_name: str,
        protocol: int,
        admin_status: int,
        address_type: int,
        method: int | None = None,
        index: int = 1,
    ) -> list[MIBInfo]:
        """Return the list of vendor specific mibs required for software update.

        :model: name of the gateway model eg: F3896LG, CH7465LG, etc
        :type model: str
        :param server_address: ip address of the server
        :type server_address: str
        :param sw_file_name: name of the imgae file with extension
        :type sw_file_name: str
        :param protocol: protocol to be used by cm for sw download
            i.e 1 for tftp and 2 for http
        :type protocol: int
        :param admin_status: 1 for upgradeFromMgt, 2 for allowProvisioningUpgrade,
            3 for ignoreProvisioningUpgrade
        :type admin_status: int
        :param address_type: type of ip address i.e 1 for ipv4 and 2 for ipv6
        :type address_type: int
        :param method: 1 for secure and 2 for unsecure download
        :type method: int
        :param index: index of the object for a mib or oid, defaults to 1
        :type index: int
        :raises NotImplementedError: not implemented in ABC
        """
        msg = "Vendor Specific Software Update MIBs must be defined for the gateway"
        raise NotImplementedError(msg)
