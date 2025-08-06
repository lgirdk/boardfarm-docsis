"""Software update use cases."""

# pylint: disable=too-many-lines

from __future__ import annotations

import logging
from pathlib import Path
from time import sleep
from typing import TYPE_CHECKING, Any, Literal
from urllib.parse import urlparse

from boardfarm3.lib.SNMPv2 import SNMPv2
from boardfarm3.lib.utils import retry_on_exception
from boardfarm3.lib.wrappers import singleton

from boardfarm3_docsis.lib.sw_update_helper import SoftwareUpdateHelper

if TYPE_CHECKING:
    from boardfarm3.templates.cpe.cpe import CPE
    from boardfarm3.templates.wan import WAN

    from boardfarm3_docsis.templates.cable_modem.cable_modem import CableModem
    from boardfarm3_docsis.templates.cmts import CMTS


SoftwareTargetType = Literal["update", "current", "alternative"]

PROTO_DICT: dict[str, dict[str, str]] = {
    "tftp": {"proto": "1", "wan_dir": "/tftpboot"},
    "http": {"proto": "2", "wan_dir": "/var/www/html"},
}

_LOGGER = logging.getLogger(__name__)


@singleton
class _SnmpSwUpdate:  # pylint: disable=too-few-public-methods
    def __init__(self, board: CableModem, wan: WAN, cmts: CMTS) -> None:
        self.snmp = SNMPv2(
            wan,
            cmts.get_cable_modem_ip_address(board.cm_mac),
            board.sw.get_mibs_compiler(),
        )
        self.sw_update = SoftwareUpdateHelper()


def get_current_cm_config(board: CableModem) -> str:
    """Get current cable modem bootfile.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Get current cable modem bootfile.

    :param board: the Cable Modem to be upgraded
    :type board: CableModem
    :return: Cable Modem boot file
    :rtype: str
    """
    # TODO: check whether this is a duplicate use Case
    return board.sw.get_boot_file()


def get_update_image_version(board: CPE) -> str:
    """Return the image version name from env for software update.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Verify DUT's current firmware version is the latest software version.
        - Verify that the DUT is upgraded and operational with the latest firmware

    :param board: the CPE to be upgraded
    :type board: CPE
    :raises ValueError: When failing to get update image version
    :return: image version name for software update uniquely defined for an image
    :rtype: str
    """
    try:
        return board.hw.config["software_update"]["image_version"]
    except KeyError as exception:
        msg = "Failed to get update image version"
        raise ValueError(msg) from exception


def _get_software_filepath(board: CPE, software_target: SoftwareTargetType) -> str:
    """Return the filepath for the given software update target.

    In this lingo there are 3 types of target:
    * current: the build under test
    * update or alternative: the build to upgrade/downgrade to

    The build details are returned from the config object of the board.

    :param board: the CPE to be upgraded
    :type board: CPE
    :param software_target: current or update
    :type software_target: SoftwareTargetType
    :raises ValueError: if the software target has an unexpected value
    :raises ValueError: if the board object does not contain the information
    :return: the relative path on the mirror
    :rtype: str
    """
    board_config = board.hw.config
    try:
        if software_target == "update":
            software_path = board_config["software_update"]["image_uri"]
        elif software_target == "current":
            software_path = board_config["software"]["image_uri"]
        elif software_target == "alternative":
            software_path = board_config["software_alternative"]["image_uri"]
        else:
            # mypy complains that this code is unreachable. fair enough,
            # it is only called from this file with only valid values
            # however, this safety net is left in place
            err_msg = f"Unexpected value '{software_target=}'"  # type: ignore[unreachable]
            raise ValueError(err_msg)
    except KeyError as exception:
        msg = f"Failed to get {software_target} image file name"
        raise ValueError(msg) from exception
    return software_path


def _get_software_file_uri(board: CPE, software_target: SoftwareTargetType) -> str:
    """Return the software file URI.

    The config object of the given board is read and the URI of the specified
    software target is returned, providing the full information on how to
    download the build of choice.

    :param board: the CPE to be upgraded
    :type board: CPE
    :param software_target: current or update
    :type software_target: SoftwareTargetType
    :return: URI of the chosen upgrade type
    :rtype: str
    """
    return board.hw.config.get("mirror") + _get_software_filepath(
        board=board,
        software_target=software_target,
    )


def _ensure_build_is_on_server(
    board: CPE,
    wan: WAN,
    software_target: SoftwareTargetType,
) -> str:
    uri = _get_software_file_uri(board=board, software_target=software_target)
    # Add Management route to mirror
    wan.add_route(destination=urlparse(uri).netloc, gw_interface="eth0")
    try:
        return wan.download_image_to_tftpboot(uri)
    finally:
        wan.delete_route(urlparse(uri).netloc)


def get_update_filename(board: CPE) -> str:
    """Return the image filename of the software to be updated.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Initiate the firmware upgrade from last stable firmware version to latest
        - Initiate Software upgrade on DUT
        - Initiate Software downgrade on DUT
        - Initiate the firmware downgrade from latest version to last stable firmware

    :param board: the CPE to be upgraded
    :type board: CPE
    :return: name of the file for software update along with file extension
    :rtype: str
    """
    return Path(_get_software_filepath(board=board, software_target="update")).name


def get_current_filename(board: CPE) -> str:
    """Return the image filename of the current software.

    :param board: the CPE to be upgraded
    :type board: CPE
    :return: name of the file for current software along with file extension
    :rtype: str
    """
    return Path(_get_software_filepath(board=board, software_target="current")).name


def get_alternative_image_version(board: CPE) -> str:
    """Return the alternative image version name from env for software update.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Get the alternative image version name from env for software update.

    :param board: the CPE to be upgraded
    :type board: CPE
    :raises ValueError: When failed to get alternative update image version
    :return: image version name for software update uniquely defined for an image
    :rtype: str
    """
    try:
        return board.hw.config["software_alternative"]["image_version"]
    except KeyError as exception:
        msg = "Failed to get alternative update image version"
        raise ValueError(msg) from exception


def get_alternative_filename(board: CPE) -> str:
    """Return the alternative image filename of the software to be updated.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Get the alternative image filename of the software to be updated.

    :param board: the CPE to be upgraded
    :type board: CPE
    :return: name of the file for software update along with file extension
    :rtype: str
    """
    return Path(_get_software_filepath(board=board, software_target="alternative")).name


def get_server_address(wan: WAN) -> str:
    """Return the IP address of the image server.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Get the ip address of the image server.

    :param wan: WAN server
    :type wan: WAN
    :return: IP address of the image server
    :rtype: str
    """
    return wan.get_interface_ipv4addr(wan.iface_dut)


def get_gateway_model(board: CPE) -> str:
    """Return the name of the gateway model.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Get the name of the gateway model.

    :param board: the CPE to be upgraded
    :type board: CPE
    :return: name of gateway model, e.g.: F3896LG, CH7465LG, etc
    :rtype: str
    """
    return board.hw.config["type"]


def is_running_updated_version_via_docsis_snmp(
    board: CableModem, wan: WAN, cmts: CMTS
) -> bool:
    """Check whether the current running version via SNMP matches env version.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Verify DUT is running on firmware version prior to image under test via SNMP
        - Verify that the DUT is upgraded with the latest firmware via SNMP
        - Verify that the DUT is downgraded with the old firmware via SNMP

    Current running version fetched via SNMP with DOCSIS MIB and the expected
    updated version provided in env.

    :param board: the Cable Modem to be checked
    :type board: CableModem
    :param wan: WAN server
    :type wan: WAN
    :param cmts: CMTS to which the CM is connected
    :type cmts: CMTS
    :return: true if image_version is a match else False
    :rtype: bool
    """
    update_image_version = get_update_image_version(board)
    return (
        get_docsis_SwCurrentVers(board=board, wan=wan, cmts=cmts)
        == update_image_version
    )


def is_running_alternative_version_via_docsis_snmp(
    board: CableModem, wan: WAN, cmts: CMTS
) -> bool:
    """Check whether the current running version via SNMP matches alternative version.

    Current running version fetched via SNMP with DOCSIS MIB and the expected
    alternative version provided in env

    .. hint:: This Use Case implements statements from the test suite such as:

        - Check whether the current running version via SNMP matches alternative version

    :param board: the Cable Modem to be checked
    :type board: CableModem
    :param wan: WAN server
    :type wan: WAN
    :param cmts: CMTS to which the CM is connected
    :type cmts: CMTS
    :return: True if image_version is a match else False
    :rtype: bool
    """
    alternative_image_version = get_alternative_image_version(board)
    return (
        get_docsis_SwCurrentVers(board=board, wan=wan, cmts=cmts)
        == alternative_image_version
    )


def ensure_update_build_is_on_server(board: CPE, wan: WAN) -> str:
    """Make sure that the build is present on the server.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Make sure that the build is present on the server.

    :param board: the CPE to be upgraded
    :type board: CPE
    :param wan: WAN server
    :type wan: WAN
    :return: name of the image file on the server filesystem
    :rtype: str
    """
    return _ensure_build_is_on_server(board=board, wan=wan, software_target="update")


def ensure_current_build_is_on_server(board: CPE, wan: WAN) -> str:
    """Make sure that the build is present on the server.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Make sure that the build is present on the server.

    :param board: the CPE to be upgraded
    :type board: CPE
    :param wan: WAN server
    :type wan: WAN
    :return: name of the image file on the server filesystem
    :rtype: str
    """
    return _ensure_build_is_on_server(board=board, wan=wan, software_target="current")


def ensure_alternative_build_is_on_server(board: CPE, wan: WAN) -> str:
    """Make sure that the alternative build is present on the server.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Make sure that the alternative build is present on the server.

    :param board: the CPE to be upgraded
    :type board: CPE
    :param wan: WAN server
    :type wan: WAN
    :return: name of the image file on the server filesystem
    :rtype: str
    """
    return _ensure_build_is_on_server(
        board=board, wan=wan, software_target="alternative"
    )


def _get_mib_name(mib: str, vendor_specific: bool, board: CableModem) -> str:
    vendor_prefix = board.sw.mibs.vendor_prefix
    return f"{vendor_prefix}{mib}" if vendor_specific else f"docsDev{mib}"


# pylint: disable-next=invalid-name
def _get_TransportProtocol_mib_name(vendor_specific: bool, board: CableModem) -> str:
    return _get_mib_name("SwServerTransportProtocol", vendor_specific, board=board)


# pylint: disable-next=invalid-name
def _get_SwServerAddressType_mib_name(vendor_specific: bool, board: CableModem) -> str:
    return _get_mib_name("SwServerAddressType", vendor_specific, board=board)


# pylint: disable-next=invalid-name
def _get_SwServerAddress_mib_name(vendor_specific: bool, board: CableModem) -> str:
    return (
        board.sw.mibs.sw_server_address_mib
        if vendor_specific
        else _get_mib_name("SwServerAddress", vendor_specific, board=board)
    )


# pylint: disable-next=invalid-name
def _get_SwFilename_mib_name(vendor_specific: bool, board: CableModem) -> str:
    return _get_mib_name("SwFilename", vendor_specific, board=board)


# pylint: disable-next=invalid-name
def _get_SwAdminStatus_mib_name(vendor_specific: bool, board: CableModem) -> str:
    return _get_mib_name("SwAdminStatus", vendor_specific, board=board)


# pylint: disable-next=invalid-name
def _get_SwCurrentVers_mib_name(vendor_specific: bool, board: CableModem) -> str:
    return _get_mib_name("SwCurrentVers", vendor_specific, board=board)


# pylint: disable-next=invalid-name
def _get_SwOperStatus_mib_name(vendor_specific: bool, board: CableModem) -> str:
    return _get_mib_name("SwOperStatus", vendor_specific, board=board)


# pylint: disable-next=invalid-name
def _get_EventEntry_mib_name(vendor_specific: bool, board: CableModem) -> str:
    return _get_mib_name(mib="EventEntry", vendor_specific=vendor_specific, board=board)


# pylint: disable-next=invalid-name
def _get_EventEntry_securitylevel_oid_name() -> str:
    return "1.3.6.1.2.1.69.1.5.7.1.2"


# pylint: disable-next=invalid-name
def _get_HwModel_mib_name(vendor_specific: bool, mib: str, board: CableModem) -> str:
    return _get_mib_name(mib=mib, vendor_specific=vendor_specific, board=board)


# pylint: disable-next=invalid-name
def set_docsis_SwServerTransportProtocol(
    proto: str, board: CableModem, wan: WAN, cmts: CMTS
) -> None:
    """Set DOCSIS software server transport protocol via SNMP.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Set docsis software server transport protocol via SNMP.

    :param board: the Cable Modem to be upgraded
    :type board: CableModem
    :param wan: WAN server
    :type wan: WAN
    :param cmts: CMTS to which the CM is connected
    :type cmts: CMTS
    :param proto: software update protocol
    :type proto: str
    :raises ValueError: When a wrong protocol name is passed
    """
    if proto not in PROTO_DICT:
        msg = "Wrong protocol name"
        raise ValueError(msg)
    _SnmpSwUpdate(board=board, wan=wan, cmts=cmts).snmp.snmpset(
        _get_TransportProtocol_mib_name(vendor_specific=False, board=board),
        PROTO_DICT[proto]["proto"],
        "i",
    )


# pylint: disable-next=invalid-name
def set_vendor_SwServerTransportProtocol(
    proto: str, board: CableModem, wan: WAN, cmts: CMTS, index: int = 1
) -> None:
    """Set vendor software server transport protocol via SNMP.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Set vendor software server transport protocol via SNMP.

    :param proto: software update protocol
    :type proto: str
    :param board: the Cable Modem to be upgraded
    :type board: CableModem
    :param wan: WAN server
    :type wan: WAN
    :param cmts: CMTS to which the CM is connected
    :type cmts: CMTS
    :param index: index of the object for a mib or oid
        an index value greater than 0 and less than 17 is accepted,
        defaults to 1
    :type index: int
    :raises ValueError: When a wrong protocol name is passed
    """
    if proto not in PROTO_DICT:
        msg = "Wrong protocol name"
        raise ValueError(msg)
    _SnmpSwUpdate(board=board, wan=wan, cmts=cmts).snmp.snmpset(
        _get_TransportProtocol_mib_name(vendor_specific=True, board=board),
        PROTO_DICT[proto]["proto"],
        "i",
        index=index,
    )


# pylint: disable-next=invalid-name
def get_docsis_SwServerTransportProtocol(
    board: CableModem, wan: WAN, cmts: CMTS
) -> str:
    """Get DOCSIS software server transport protocol via SNMP.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Get docsis software server transport protocol via SNMP.

    :param board: the Cable Modem to be upgraded
    :type board: CableModem
    :param wan: WAN server
    :type wan: WAN
    :param cmts: CMTS to which the CM is connected
    :type cmts: CMTS
    :return: docsis software server transport protocol
    :rtype: str
    """
    return _SnmpSwUpdate(board=board, wan=wan, cmts=cmts).snmp.snmpget(
        _get_TransportProtocol_mib_name(
            vendor_specific=False,
            board=board,
        )
    )[0]


# pylint: disable-next=invalid-name
def get_vendor_SwServerTransportProtocol(
    board: CableModem, wan: WAN, cmts: CMTS, index: int = 1
) -> str:
    """Get vendor software server transport protocol via SNMP.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Get vendor software server transport protocol via SNMP.

    :param board: the Cable Modem to be upgraded
    :type board: CableModem
    :param wan: WAN server
    :type wan: WAN
    :param cmts: CMTS to which the CM is connected
    :type cmts: CMTS
    :param index: index of the object for a mib or oid, defaults to 1
    :type index: int
    :return: vendor software server transport protocol
    :rtype: str
    """
    return _SnmpSwUpdate(board=board, wan=wan, cmts=cmts).snmp.snmpget(
        _get_TransportProtocol_mib_name(vendor_specific=True, board=board), index=index
    )[0]


# pylint: disable-next=invalid-name
def set_docsis_SwServerAddressType(
    address_type: int, board: CableModem, wan: WAN, cmts: CMTS
) -> None:
    """Set DOCSIS software server address type via SNMP.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Set docsis software server address type via SNMP.

    :param board: the Cable Modem to be upgraded
    :type board: CableModem
    :param wan: WAN server
    :type wan: WAN
    :param cmts: CMTS to which the CM is connected
    :type cmts: CMTS
    :param address_type: server address type
    :type address_type: int
    """
    _SnmpSwUpdate(board=board, wan=wan, cmts=cmts).snmp.snmpset(
        _get_SwServerAddressType_mib_name(vendor_specific=False, board=board),
        str(address_type),
        "i",
    )


# pylint: disable-next=invalid-name
def set_vendor_SwServerAddressType(
    address_type: int, board: CableModem, wan: WAN, cmts: CMTS, index: int = 1
) -> None:
    """Set vendor software server address type via SNMP.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Set vendor software server address type via SNMP.

    :param board: the Cable Modem to be upgraded
    :type board: CableModem
    :param wan: WAN server
    :type wan: WAN
    :param cmts: CMTS to which the CM is connected
    :type cmts: CMTS
    :param address_type: server address type
    :type address_type: int
    :param index: index of the object for a mib or oid
        an index value greater than 0 and less than 17 is accepted,
        defaults to 1
    :type index: int
    """
    _SnmpSwUpdate(board=board, wan=wan, cmts=cmts).snmp.snmpset(
        _get_SwServerAddressType_mib_name(vendor_specific=True, board=board),
        str(address_type),
        "i",
        index=index,
    )


# pylint: disable-next=invalid-name
def get_docsis_SwServerAddressType(board: CableModem, wan: WAN, cmts: CMTS) -> int:
    """Get DOCSIS software server address type via SNMP.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Get docsis software server address type via SNMP.

    :param board: the Cable Modem to be upgraded
    :type board: CableModem
    :param wan: WAN server
    :type wan: WAN
    :param cmts: CMTS to which the CM is connected
    :type cmts: CMTS
    :return: docsis software server address type
    :rtype: int
    """
    return int(
        _SnmpSwUpdate(board=board, wan=wan, cmts=cmts).snmp.snmpget(
            _get_SwServerAddressType_mib_name(
                vendor_specific=False,
                board=board,
            )
        )[0]
    )


# pylint: disable-next=invalid-name
def get_vendor_SwServerAddressType(
    board: CableModem, wan: WAN, cmts: CMTS, index: int = 1
) -> int:
    """Get vendor software server address type via SNMP.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Get vendor software server address type via SNMP.

    :param board: the Cable Modem to be upgraded
    :type board: CableModem
    :param wan: WAN server
    :type wan: WAN
    :param cmts: CMTS to which the CM is connected
    :type cmts: CMTS
    :param index: index of the object for a mib or oid, defaults to 1
    :type index: int
    :return: vendor software server address type
    :rtype: int
    """
    return int(
        _SnmpSwUpdate(board=board, wan=wan, cmts=cmts).snmp.snmpget(
            _get_SwServerAddressType_mib_name(
                vendor_specific=True,
                board=board,
            ),
            index=index,
        )[0]
    )


# pylint: disable-next=invalid-name
def set_docsis_SwServerAddress(
    addr: str, board: CableModem, wan: WAN, cmts: CMTS
) -> None:
    """Set DOCSIS software server address via SNMP.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Set docsis software server address via SNMP.

    :param board: the Cable Modem to be upgraded
    :type board: CableModem
    :param wan: WAN server
    :type wan: WAN
    :param cmts: CMTS to which the CM is connected
    :type cmts: CMTS
    :param addr: server address type
    :type addr: str
    """
    addr = "0x" + " ".join([format(int(x), "02X") for x in addr.split(".")])
    _SnmpSwUpdate(board=board, wan=wan, cmts=cmts).snmp.snmpset(
        _get_SwServerAddress_mib_name(vendor_specific=False, board=board), addr, "x"
    )


# pylint: disable-next=invalid-name
def set_vendor_SwServerAddress(
    addr: str, board: CableModem, wan: WAN, cmts: CMTS, index: int = 1
) -> None:
    """Set vendor software server address via SNMP.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Set vendor software server address via SNMP.

    :param board: the Cable Modem to be upgraded
    :type board: CableModem
    :param wan: WAN server
    :type wan: WAN
    :param cmts: CMTS to which the CM is connected
    :type cmts: CMTS
    :param addr: server address type
    :type addr: str
    :param index: index of the object for a mib or oid, defaults to 1
    :type index: int
    """
    addr = "0x" + " ".join([format(int(x), "02X") for x in addr.split(".")])
    _SnmpSwUpdate(board=board, wan=wan, cmts=cmts).snmp.snmpset(
        _get_SwServerAddress_mib_name(vendor_specific=True, board=board),
        addr,
        "x",
        index=index,
    )


# pylint: disable-next=invalid-name
def set_vendor_HwModel(
    model: str, board: CableModem, wan: WAN, cmts: CMTS, index: int = 1
) -> None:
    """Set vendor hardware model via SNMP.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Set vendor hardware model via SNMP.

    :param board: the Cable Modem to be upgraded
    :type board: CableModem
    :param wan: WAN server
    :type wan: WAN
    :param cmts: CMTS to which the CM is connected
    :type cmts: CMTS
    :param model: device hardware model collected from board
    :type model: str
    :param index: index of the object for a mib or oid
        an index value greater than 0 and less than 3 is accepted, defaults to 1
    :type index: int
    """
    _SnmpSwUpdate(board=board, wan=wan, cmts=cmts).snmp.snmpset(
        _get_HwModel_mib_name(
            mib=board.sw.mibs.hw_model_mib,
            vendor_specific=True,
            board=board,
        ),
        model,
        "s",
        index=index,
    )


# pylint: disable-next=invalid-name
def get_docsis_SwServerAddress(board: CableModem, wan: WAN, cmts: CMTS) -> str:
    """Get DOCSIS software server address via SNMP.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Verify if the Docsis MIB docsDevSwServerAddress reflect the values set

    :param board: the Cable Modem to be upgraded
    :type board: CableModem
    :param wan: WAN server
    :type wan: WAN
    :param cmts: CMTS to which the CM is connected
    :type cmts: CMTS
    :return: docsis software server address
    :rtype: str
    """
    return _SnmpSwUpdate(board=board, wan=wan, cmts=cmts).snmp.snmpget(
        _get_SwServerAddress_mib_name(vendor_specific=False, board=board)
    )[0]


# pylint: disable-next=invalid-name,too-many-arguments,too-many-locals
def get_vendor_SwServerAddress(
    board: CableModem, wan: WAN, cmts: CMTS, index: int = 1
) -> str:
    """Get vendor software server address via SNMP.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Verify if the vendor specific MIB sagemCmSwServerAddress reflect the value set
        - Verify if the vendor specific MIB cmCbnVendorSwServerAddress has the value set

    :param board: the Cable Modem to be upgraded
    :type board: CableModem
    :param wan: WAN server
    :type wan: WAN
    :param cmts: CMTS to which the CM is connected
    :type cmts: CMTS
    :param index: index of the object for a mib or oid, defaults to 1
    :type index: int
    :return: vendor software server address
    :rtype: str
    """
    return (
        _SnmpSwUpdate(board=board, wan=wan, cmts=cmts)
        .snmp.snmpget(
            _get_SwServerAddress_mib_name(vendor_specific=True, board=board),
            index=index,
        )[0]
        .strip()
    )


# pylint: disable-next=invalid-name
def set_docsis_SwFilename(name: str, board: CableModem, wan: WAN, cmts: CMTS) -> None:
    """Set DOCSIS software filename via SNMP.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Set docsis software filename via SNMP.

    :param board: the Cable Modem to be upgraded
    :type board: CableModem
    :param wan: WAN server
    :type wan: WAN
    :param cmts: CMTS to which the CM is connected
    :type cmts: CMTS
    :param name: software filename
    :type name: str
    """
    _SnmpSwUpdate(board=board, wan=wan, cmts=cmts).snmp.snmpset(
        _get_SwFilename_mib_name(vendor_specific=False, board=board), name, "s"
    )


# pylint: disable-next=invalid-name
def set_vendor_SwFilename(
    name: str, board: CableModem, wan: WAN, cmts: CMTS, index: int = 1
) -> None:
    """Set vendor software filename via SNMP.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Set vendor software filename via SNMP.

    :param board: the Cable Modem to be upgraded
    :type board: CableModem
    :param wan: WAN server
    :type wan: WAN
    :param cmts: CMTS to which the CM is connected
    :type cmts: CMTS
    :param name: software filename
    :type name: str
    :param index: index of the object for a mib or oid
    :type index: int
    """
    _SnmpSwUpdate(board=board, wan=wan, cmts=cmts).snmp.snmpset(
        _get_SwFilename_mib_name(vendor_specific=True, board=board),
        name,
        "s",
        index=index,
    )


# pylint: disable-next=invalid-name
def get_docsis_SwFilename(board: CableModem, wan: WAN, cmts: CMTS) -> str:
    """Get DOCSIS software filename via SNMP.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Verify if the docsis MIB docsDevSwFilename reflects the value set

    :param board: the Cable Modem to be upgraded
    :type board: CableModem
    :param wan: WAN server
    :type wan: WAN
    :param cmts: CMTS to which the CM is connected
    :type cmts: CMTS
    :return: docsis software filename
    :rtype: str
    """
    return _SnmpSwUpdate(board=board, wan=wan, cmts=cmts).snmp.snmpget(
        _get_SwFilename_mib_name(vendor_specific=False, board=board)
    )[0]


# pylint: disable-next=invalid-name
def get_vendor_SwFilename(
    board: CableModem, wan: WAN, cmts: CMTS, index: int = 1
) -> str:
    """Get vendor software filename via SNMP.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Verify if the vendor specific MIB cmCbnVendorSwFilename reflects the value set
        - Verify if the vendor specific MIB sagemCmSwFilename reflects the value set

    :param board: the Cable Modem to be upgraded
    :type board: CableModem
    :param wan: WAN server
    :type wan: WAN
    :param cmts: CMTS to which the CM is connected
    :type cmts: CMTS
    :param index: index of the object for a mib or oid, defaults to 1
    :type index: int
    :return: vendor software filename
    :rtype: str
    """
    return _SnmpSwUpdate(board=board, wan=wan, cmts=cmts).snmp.snmpget(
        _get_SwFilename_mib_name(vendor_specific=True, board=board), index=index
    )[0]


# pylint: disable-next=invalid-name
def set_vendor_SwMethod(board: CableModem, wan: WAN, cmts: CMTS, method: int) -> None:
    """Set vendor software update method via SNMP.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Set vendor software update method via SNMP.

    :param board: the Cable Modem to be upgraded
    :type board: CableModem
    :param wan: WAN server
    :type wan: WAN
    :param cmts: CMTS to which the CM is connected
    :type cmts: CMTS
    :param method: software update method
    :type method: int
    """
    _SnmpSwUpdate(board=board, wan=wan, cmts=cmts).snmp.snmpset(
        board.sw.mibs.sw_method_mib,
        str(method),
        "i",
    )


# pylint: disable-next=invalid-name
def get_vendor_SwMethod(board: CableModem, wan: WAN, cmts: CMTS, index: int = 1) -> int:
    """Get vendor software update method via SNMP.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Verify Secure Software Download is enabled on DUT via SNMP

    :param board: the Cable Modem to be upgraded
    :type board: CableModem
    :param wan: WAN server
    :type wan: WAN
    :param cmts: CMTS to which the CM is connected
    :type cmts: CMTS
    :param index: index of the object for a mib or oid, defaults to 1
    :type index: int
    :return: software update method
    :rtype: int
    """
    return int(
        _SnmpSwUpdate(board=board, wan=wan, cmts=cmts).snmp.snmpget(
            board.sw.mibs.sw_method_mib, index=index
        )[0]
    )


# pylint: disable-next=invalid-name
def set_docsis_SwAdminStatus(val: int, board: CableModem, wan: WAN, cmts: CMTS) -> None:
    """Set DOCSIS software update admin status via SNMP.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Set docsis software update admin status via SNMP.

    :param board: the Cable Modem to be upgraded
    :type board: CableModem
    :param wan: WAN server
    :type wan: WAN
    :param cmts: CMTS to which the CM is connected
    :type cmts: CMTS
    :param val: software update admin status
    :type val: int
    """
    _SnmpSwUpdate(board=board, wan=wan, cmts=cmts).snmp.snmpset(
        _get_SwAdminStatus_mib_name(vendor_specific=False, board=board), str(val), "i"
    )


# pylint: disable-next=invalid-name
def set_vendor_SwAdminStatus(
    board: CableModem, wan: WAN, cmts: CMTS, val: int, index: int = 1
) -> None:
    """Set vendor software update admin status via SNMP.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Set vendor software update admin status via SNMP.

    :param board: the Cable Modem to be upgraded
    :type board: CableModem
    :param wan: WAN server
    :type wan: WAN
    :param cmts: CMTS to which the CM is connected
    :type cmts: CMTS
    :param val: software update admin status
    :type val: int
    :param index: index of the object for a mib or oid
        an index value greater than 0 and less than 17 is accepted,
        defaults to 1
    :type index: int
    """
    _SnmpSwUpdate(board=board, wan=wan, cmts=cmts).snmp.snmpset(
        _get_SwAdminStatus_mib_name(vendor_specific=True, board=board),
        str(val),
        "i",
        index=index,
    )


# pylint: disable-next=invalid-name
def get_docsis_SwAdminStatus(board: CableModem, wan: WAN, cmts: CMTS) -> int:
    """Get DOCSIS software update admin status via SNMP.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Verify if the docsis MIB docsDevSwAdminStatus reflects the value set

    :param board: the Cable Modem to be upgraded
    :type board: CableModem
    :param wan: WAN server
    :type wan: WAN
    :param cmts: CMTS to which the CM is connected
    :type cmts: CMTS
    :return: software update admin status
    :rtype: int
    """
    return int(
        _SnmpSwUpdate(board=board, wan=wan, cmts=cmts).snmp.snmpget(
            _get_SwAdminStatus_mib_name(vendor_specific=False, board=board)
        )[0]
    )


# pylint: disable-next=invalid-name
def get_vendor_SwAdminStatus(
    board: CableModem, wan: WAN, cmts: CMTS, index: int = 1
) -> int:
    """Get vendor software update admin status via SNMP.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Verify if the vendor specific MIB cmCbnVendorSwAdminStatus has the value set
        - Verify if the vendor specific MIB sagemCmSwAdminStatus reflects the value set

    :param board: the Cable Modem to be upgraded
    :type board: CableModem
    :param wan: WAN server
    :type wan: WAN
    :param cmts: CMTS to which the CM is connected
    :type cmts: CMTS
    :param index: index of the object for a mib or oid, defaults to 1
    :type index: int
    :return: software update admin status
    :rtype: int
    """
    return int(
        _SnmpSwUpdate(board=board, wan=wan, cmts=cmts).snmp.snmpget(
            _get_SwAdminStatus_mib_name(vendor_specific=True, board=board), index=index
        )[0]
    )


# pylint: disable-next=invalid-name
def get_docsis_SwCurrentVers(board: CableModem, wan: WAN, cmts: CMTS) -> str:
    """Get DOCSIS software current version via SNMP.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Verify that the DUT is operational with the last stable FW version
        - Verify that the DUT is not upgraded and operational with the last stable FW

    :param board: the Cable Modem to be upgraded
    :type board: CableModem
    :param wan: WAN server
    :type wan: WAN
    :param cmts: CMTS to which the CM is connected
    :type cmts: CMTS
    :return: current software version
    :rtype: str
    """
    return _SnmpSwUpdate(board=board, wan=wan, cmts=cmts).snmp.snmpget(
        _get_SwCurrentVers_mib_name(vendor_specific=False, board=board)
    )[0]


# pylint: disable-next=invalid-name
def get_docsis_OperationStatus(board: CableModem, wan: WAN, cmts: CMTS) -> int:
    """Get DOCSIS operation status via SNMP.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Verify the status of software download via SNMP

    :param board: the Cable Modem to be upgraded
    :type board: CableModem
    :param wan: WAN server
    :type wan: WAN
    :param cmts: CMTS to which the CM is connected
    :type cmts: CMTS
    :return: docsis operation status
    :rtype: int
    """
    return int(
        _SnmpSwUpdate(board=board, wan=wan, cmts=cmts).snmp.snmpget(
            _get_SwOperStatus_mib_name(vendor_specific=False, board=board)
        )[0]
    )


# pylint: disable=too-many-arguments
def wait_for_update_to_complete(  # noqa: PLR0913
    operStatus: int,  # pylint: disable=invalid-name
    retry: int,
    wait: int,
    board: CableModem,
    wan: WAN,
    cmts: CMTS,
) -> bool:
    """Retry snmpget on operStatus and wait for the match with the passed value.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Retries snmpget on operStatus and waits for the match with the passed value.

    :param operStatus: 1 for inProgress, 2 for completeFromProvisioning,
        3 for completeFromMgt, 4 for other
    :type operStatus: int
    :param retry: number retries until the expected operStatus value is returned
    :type retry: int
    :param wait: wait time in seconds after each retry
    :type wait: int
    :param board: the Cable Modem to be upgraded
    :type board: CableModem
    :param wan: WAN server
    :type wan: WAN
    :param cmts: CMTS to which the CM is connected
    :type cmts: CMTS

    :return: true if expected operStatus is fetched after retries else False
    :rtype: bool
    """
    for _ in range(retry):
        if retry_on_exception(get_docsis_OperationStatus, (board, wan, cmts)) != 1:
            _LOGGER.info("Software Update not already In Progress!!!")
        if get_docsis_OperationStatus(board=board, wan=wan, cmts=cmts) == operStatus:
            return True
        sleep(wait)
    return False


# pylint: disable-next=invalid-name
def get_docsis_EventEntry(board: CableModem, wan: WAN, cmts: CMTS) -> tuple[dict, Any]:
    """Return the result of snmpwalk on the docsis event entry mib.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Verify that Software Download successful event message on DUT via SNMP
        - Verify the proper error log on CM

    :param board: the Cable Modem to be upgraded
    :type board: CableModem
    :param wan: WAN server
    :type wan: WAN
    :param cmts: CMTS to which the CM is connected
    :type cmts: CMTS
    :return: docsis event entry
    :rtype: Tuple[Dict, Any]
    """
    return _SnmpSwUpdate(board=board, wan=wan, cmts=cmts).snmp.snmpwalk(
        _get_EventEntry_mib_name(vendor_specific=False, board=board)
    )


def get_vendor_table(
    board: CableModem, wan: WAN, cmts: CMTS, index: int = 1
) -> dict[str, list[str]]:
    """Return the result of snmpwalk on the vendor specific sw download/model table.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Verify that vendor table returns 16 entries via SNMP

    :param board: the Cable Modem to be upgraded
    :type board: CableModem
    :param wan: WAN server
    :type wan: WAN
    :param cmts: CMTS to which the CM is connected
    :type cmts: CMTS
    :param index: index of the object for a mib or oid, defaults to 1
    :type index: int
    :return: sw model vendor tables
    :rtype: Dict[str, List[str]]
    """
    return _SnmpSwUpdate(board=board, wan=wan, cmts=cmts).snmp.snmpwalk(
        board.sw.mibs.sw_model_table_mib, index=index
    )[0]


# pylint: disable=too-many-arguments
def trigger_docsis_snmp_sw_update(  # noqa: PLR0913
    server_address: str,
    sw_filename: str,
    protocol: str,
    admin_status: int,
    address_type: int,
    board: CableModem,
    wan: WAN,
    cmts: CMTS,
) -> None:
    """Trigger the software update by performing snmpset on the DOCSIS specific mibs.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Initiate Software downgrade on DUT via SNMP
        - Trigger the software upgrade on DUT via SNMP

    :param server_address: ip address of the server
    :type server_address: str
    :param sw_filename: name of the image file with extension
    :type sw_filename: str
    :param protocol: protocol to be used by the CM for software download
        i.e 1 for tftp and 2 for http
    :type protocol: str
    :param admin_status: 1 for upgradeFromMgt, 2 for allowProvisioningUpgrade,
        3 for ignoreProvisioningUpgrade
    :type admin_status: int
    :param address_type: type of ip address i.e 1 for ipv4 and 2 for ipv6
    :type address_type: int
    :param board: the Cable Modem to be upgraded
    :type board: CableModem
    :param wan: WAN server
    :type wan: WAN
    :param cmts: CMTS to which the CM is connected
    :type cmts: CMTS
    """
    set_docsis_SwFilename(name=sw_filename, board=board, wan=wan, cmts=cmts)
    set_docsis_SwServerTransportProtocol(
        proto=protocol, board=board, wan=wan, cmts=cmts
    )
    set_docsis_SwServerAddressType(
        address_type=address_type, board=board, wan=wan, cmts=cmts
    )
    set_docsis_SwServerAddress(addr=server_address, board=board, wan=wan, cmts=cmts)
    set_docsis_SwAdminStatus(val=admin_status, board=board, wan=wan, cmts=cmts)
