"""Software update helper."""

from __future__ import annotations

from boardfarm3_docsis.templates.cable_modem.cable_modem_mibs import MIBInfo


# pylint: disable=too-few-public-methods
class SoftwareUpdateHelper:
    """Software update utility."""

    # pylint: disable=too-many-arguments
    def get_sw_update_docsis_mibs(  # noqa: PLR0913
        self,
        server_address: str,
        sw_file_name: str,
        protocol: int,
        admin_status: int,
        address_type: int,
        index: int = 0,
    ) -> list[MIBInfo]:
        """Return the list of docsis specific mibs required for software update.

        :param server_address: ip address of the server
        :type server_address: str
        :param sw_file_name: name of the imgae file with extension
        :type sw_file_name: str
        :param protocol: protocol to be used by cm for sw download
            i.e 1 for tftp and 2 for http
        :type protocol: int
        :param address_type: type of ip address i.e 1 for ipv4 and 2 for ipv6
        :type address_type: int
        :param admin_status: 1 for upgradeFromMgt, 2 for allowProvisioningUpgrade,
            3 for ignoreProvisioningUpgrade
        :type admin_status: int
        :param index: index of the object for a mib or oid, defaults to 0
        :type index: int
        :return: the docsis specific mibs with values passed as parameters
        :rtype: List[MIBInfo]
        """
        return [
            MIBInfo("docsDevSwAdminStatus", index, "Integer", admin_status),
            MIBInfo("docsDevSwServerAddressType", index, "Integer", address_type),
            MIBInfo("docsDevSwServerAddress", index, "HexString", server_address),
            MIBInfo("docsDevSwFilename", index, "String", sw_file_name),
            MIBInfo("docsDevSwServerTransportProtocol", index, "Integer", protocol),
        ]
