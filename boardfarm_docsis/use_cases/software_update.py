import os
import re
from time import sleep
from typing import Any, Dict, Tuple

from boardfarm.exceptions import CodeError
from boardfarm.lib.common import retry_on_exception
from boardfarm.lib.DeviceManager import get_device_by_name
from boardfarm.lib.SNMPv2 import SNMPv2
from boardfarm.lib.wrappers import singleton
from boardfarm_lgi_shared.lib.ofw.sw_update import OFWSWUpdate


@singleton
class _SnmpSwUpdate:
    def __init__(self):
        self.wan = get_device_by_name("wan")
        self.board = get_device_by_name("board")
        self.cmts = get_device_by_name("cmts")
        self.board_ip = (
            self.cmts.get_cmipv6(self.board.cm_mac)
            if self.board.env_helper.get_prov_mode() in ["dslite", "ipv6"]
            else self.cmts.get_cmip(self.board.cm_mac)
        )
        self.snmp = SNMPv2(self.wan, self.board_ip)
        self.vendor_prefix = self.board.sw.mib.vendor_prefix
        self.proto_dict: Dict[str, Dict[str, str]] = {
            "tftp": {"proto": "1", "wan_dir": "/tftpboot"},
            "http": {"proto": "2", "wan_dir": "/var/www/html"},
        }
        self.ofw_sw_update = OFWSWUpdate()


def get_current_cm_config() -> str:
    helper = _SnmpSwUpdate()
    return helper.board.cm_cfg.txt


def get_update_image_version() -> str:
    """Gets the image version name from env for software update

    :return: returns the image version name for software update uniquely defined for an image
    :rtype: str
    """
    helper = _SnmpSwUpdate()
    return helper.board.env_helper.get_update_image_version()


def get_update_filename() -> str:
    """Gets the image filename of the software to be updated

    :return: returns the name of the file for software update along with file extension
    :rtype: str
    """
    helper = _SnmpSwUpdate()
    return os.path.basename(helper.board.env_helper.get_update_image())


def get_server_address() -> str:
    """Returns the ipaddress of the server

    :return: ip address of the server
    :rtype: str
    """
    helper = _SnmpSwUpdate()
    return helper.wan.get_interface_ipaddr(helper.wan.iface_dut)


def get_gateway_model() -> str:
    """Gets the name of the gateway model

    :return: name of gateway model eg: F3896LG, CH7465LG, etc
    :rtype: str
    """
    helper = _SnmpSwUpdate()
    return helper.board.config["board_type"]


def is_running_updated_version() -> bool:
    """Checks whether the current running version on DUT console matches with the expected updated version provided in env

    :return: true if image_version is a match else False
    :rtype: bool
    """
    helper = _SnmpSwUpdate()
    img = get_update_image_version()
    return helper.board.check_fw_version(img)


def is_running_updated_version_via_vendor_snmp() -> bool:
    """Checks whether the current running version fetched via vendor mib snmp matches with the expected updated version provided in env

    :return: true if image_version is a match else False
    :rtype: bool
    """
    update_image_version = get_update_image_version()
    return get_vendor_SwCurrentVers() == update_image_version


def is_running_updated_version_via_docsis_snmp() -> bool:
    """Checks whether the current running version fetched via docsis mib snmp matches with the expected updated version provided in env

    :return: true if image_version is a match else False
    :rtype: bool
    """
    update_image_version = get_update_image_version()
    return get_docsis_SwCurrentVers() == update_image_version


def generate_bootfile_with_docsis_mibs(
    cfg: str,
    server_address: str,
    sw_file_name: str,
    protocol: str,
    admin_status: int,
    address_type: int,
) -> str:
    """generates the cm config file for software update with docsis mibs for the provided cm configuration
    if value None is passed to any of the parameters then the particular MIB is not added to the cm configuration

    :param cfg: cm configurartion to be updated
    :type cfg: str
    :param server_address: ip address of the server
    :type server_address: str
    :param sw_file_name: name of the imgae file with extension
    :type sw_file_name: str
    :param protocol: protocol to be used by cm for sw download i.e 1 for tftp and 2 for http
    :type protocol: int
    :param address_type: type of ip address i.e 1 for ipv4 and 2 for ipv6
    :type address_type: int
    :param admin_status: 1 for upgradeFromMgt, 2 for allowProvisioningUpgrade, 3 for ignoreProvisioningUpgrade
    :type admin_status: int
    :raises CodeError: Raises code Error exception when an invalid protocol is passed
    :return: the updated cm configuration for software update
    :rtype: str
    """
    helper = _SnmpSwUpdate()
    mibs_string = "\t/* Generic SW Update MIBs */"
    if protocol not in helper.proto_dict:
        raise CodeError("wrong protocol")
    sw_update_mibs = helper.ofw_sw_update.get_sw_update_docsis_mibs(
        server_address,
        sw_file_name,
        helper.proto_dict[protocol]["proto"],
        admin_status,
        address_type,
    )

    for mib in sw_update_mibs:
        if mib.value:
            mib.value = (
                "0x" + "".join([format(int(x), "02X") for x in mib.value.split(".")])
                if mib.type == "HexString"
                else mib.value
            )
            value = f'"{mib.value}"' if mib.type == "String" else mib.value
            mibs_string = f"{mibs_string}\n\tSnmpMibObject {mib.mib_name}.{mib.index} {mib.type} {value};"
            cfg = re.sub(f".*{mib.mib_name}.*\n", "", cfg)

    return re.sub(
        "\t/\\* MFG CVC Data \\*/",
        f"{mibs_string}\n\n\t/* MFG CVC Data */",
        cfg,
        count=1,
    )


def generate_bootfile_with_vendor_details(
    cfg: str,
    model: str,
    server_address: str,
    sw_file_name: str,
    protocol: str,
    admin_status: int,
    address_type: int,
    method: int = None,
    cosigned: bool = False,
) -> str:
    """generates the cm config file for software update with vendor specific mibs, manufacturer CVC details and LG cosigned CVC details for the provided cm configuration
    if value None is passed to any of the parameters then the particular MIB is not added to the cm configuration

    :param cfg: cm configurartion to be updated
    :type cfg: str
    :param model: name of the gateway model eg: F3896LG, CH7465LG, etc
    :type model: str
    :param server_address: ip address of the server
    :type server_address: str
    :param sw_file_name: name of the imgae file with extension
    :type sw_file_name: str
    :param protocol: protocol to be used by cm for sw download i.e 1 for tftp and 2 for http
    :type protocol: int
    :param address_type: type of ip address i.e 1 for ipv4 and 2 for ipv6
    :type address_type: int
    :param admin_status: 1 for upgradeFromMgt, 2 for allowProvisioningUpgrade, 3 for ignoreProvisioningUpgrade
    :type admin_status: int
    :param method: 1 for secure and 2 for unsecure download, defaults to None
    :type method: int, optional
    :param cosigned: cosigned details are added to the configuration only when this value is passed as True, defaults to False
    :type cosigned: bool, optional
    :raises CodeError: Raises code Error exception when an invalid protocol is passed
    :return: the updated cm configuration for software update
    :rtype: str
    """
    helper = _SnmpSwUpdate()
    mfg_cvc_keyword_list = [
        "ManufacturerCVCChain",
        "CVCFragment",
        "SwCvc",
        "TlvCode 81",
        "MfgCVCData",
    ]
    cosign_cvc_keyword_list = ["CoSignerCVCData"]
    mibs_string = "\t/* Vendor Specific SW Update MIBs */"

    for keyword in mfg_cvc_keyword_list:
        cfg = re.sub(f".*{keyword}.*\n", "", cfg)
    if protocol not in helper.proto_dict:
        raise CodeError("wrong protocol")
    sw_update_mibs = helper.board.sw.mib.get_sw_update_mibs(
        model,
        server_address,
        sw_file_name,
        helper.proto_dict[protocol]["proto"],
        admin_status,
        address_type,
        method,
    )

    for mib in sw_update_mibs:
        if mib.value:
            mib.value = (
                "0x" + "".join([format(int(x), "02X") for x in mib.value.split(".")])
                if mib.type == "HexString"
                else mib.value
            )
            value = f'"{mib.value}"' if mib.type == "String" else mib.value
            mibs_string = f"{mibs_string}\n\tSnmpMibObject {mib.mib_name}.{mib.index} {mib.type} {value};"
            cfg = re.sub(f".*{mib.mib_name}.*\n", "", cfg)

    sw_update_string = (
        f"{mibs_string}\n\n\t/* MFG CVC Data */{helper.board.sw.mib.mfg_cvc}\n"
    )
    if cosigned:
        for keyword in cosign_cvc_keyword_list:
            cfg = re.sub(f".*{keyword}.*\n", "", cfg)
        sw_update_string = f"{sw_update_string}\n\t/* Co-signed CVC Data */{helper.ofw_sw_update.get_cosigned_cvc_details}"
    return re.sub("\t/\\* MFG CVC Data \\*/", sw_update_string, cfg, count=1)


def ensure_update_build_is_on_server() -> bool:
    """Makes sure that the build is present on the server

    :return: returns True if the build is present else False
    :rtype: bool
    """
    helper = _SnmpSwUpdate()
    source = helper.board.env_helper.get_update_image()
    build = os.path.basename(source)
    return helper.wan.download_build(build, source)


def _get_mib_name(mib, vendor_specific: bool) -> str:
    helper = _SnmpSwUpdate()
    return f"{helper.vendor_prefix}{mib}" if vendor_specific else f"docsDev{mib}"


def _get_TransportProtocol_mib_name(vendor_specific: bool) -> str:
    return _get_mib_name("SwServerTransportProtocol", vendor_specific)


def _get_SwServerAddressType_mib_name(vendor_specific: bool) -> str:
    return _get_mib_name("SwServerAddressType", vendor_specific)


def _get_SwServerAddress_mib_name(vendor_specific: bool) -> str:
    return _get_mib_name("SwServerAddress", vendor_specific)


def _get_SwFilename_mib_name(vendor_specific: bool) -> str:
    return _get_mib_name("SwFilename", vendor_specific)


def _get_SwAdminStatus_mib_name(vendor_specific: bool) -> str:
    return _get_mib_name("SwAdminStatus", vendor_specific)


def _get_SwCurrentVers_mib_name(vendor_specific: bool) -> str:
    return _get_mib_name("SwCurrentVers", vendor_specific)


def _get_SwOperStatus_mib_name(vendor_specific: bool) -> str:
    return _get_mib_name("SwOperStatus", vendor_specific)


def _get_EventEntry_mib_name(vendor_specific: bool) -> str:
    return _get_mib_name("EventEntry", vendor_specific)


def set_docsis_SwServerTransportProtocol(proto: str) -> None:
    helper = _SnmpSwUpdate()
    if proto not in helper.proto_dict:
        raise CodeError("wrong protocol")
    helper.snmp.snmpset(
        _get_TransportProtocol_mib_name(False),
        helper.proto_dict[proto]["proto"],
        "i",
    )


def set_vendor_SwServerTransportProtocol(proto: str) -> None:
    helper = _SnmpSwUpdate()
    if proto not in helper.proto_dict:
        raise CodeError("wrong protocol")
    helper.snmp.snmpset(
        _get_TransportProtocol_mib_name(True),
        helper.proto_dict[proto]["proto"],
        "i",
        index=1,
    )


def get_docsis_SwServerTransportProtocol() -> str:
    helper = _SnmpSwUpdate()
    return helper.snmp.snmpget(_get_TransportProtocol_mib_name(False))[0]


def get_vendor_SwServerTransportProtocol() -> str:
    helper = _SnmpSwUpdate()
    return helper.snmp.snmpget(_get_TransportProtocol_mib_name(True), index=1)[0]


def set_docsis_SwServerAddressType(type: int) -> None:
    helper = _SnmpSwUpdate()
    helper.snmp.snmpset(_get_SwServerAddressType_mib_name(False), str(type), "i")


def set_vendor_SwServerAddressType(type: int) -> None:
    helper = _SnmpSwUpdate()
    helper.snmp.snmpset(
        _get_SwServerAddressType_mib_name(True), str(type), "i", index=1
    )


def get_docsis_SwServerAddressType() -> int:
    helper = _SnmpSwUpdate()
    return int(helper.snmp.snmpget(_get_SwServerAddressType_mib_name(False))[0])


def get_vendor_SwServerAddressType() -> int:
    helper = _SnmpSwUpdate()
    return int(helper.snmp.snmpget(_get_SwServerAddressType_mib_name(True), index=1)[0])


def set_docsis_SwServerAddress(addr: str) -> None:
    helper = _SnmpSwUpdate()
    addr = "0x" + " ".join([format(int(x), "02X") for x in addr.split(".")])
    helper.snmp.snmpset(_get_SwServerAddress_mib_name(False), f"'{addr}'", "x")


def set_vendor_SwServerAddress(addr: str) -> None:
    helper = _SnmpSwUpdate()
    addr = "0x" + "".join([format(int(x), "02X") for x in addr.split(".")])
    helper.snmp.snmpset(_get_SwServerAddress_mib_name(True), addr, "x", index=1)


def get_docsis_SwServerAddress() -> str:
    helper = _SnmpSwUpdate()
    return helper.snmp.snmpget(_get_SwServerAddress_mib_name(False))[0]


def get_vendor_SwServerAddress() -> str:
    helper = _SnmpSwUpdate()
    return helper.snmp.snmpget(_get_SwServerAddress_mib_name(True), index=1)[0].strip()


def set_docsis_SwFilename(name) -> None:
    helper = _SnmpSwUpdate()
    helper.snmp.snmpset(_get_SwFilename_mib_name(False), name, "s")


def set_vendor_SwFilename(name) -> None:
    helper = _SnmpSwUpdate()
    helper.snmp.snmpset(_get_SwFilename_mib_name(True), name, "s", index=1)


def get_docsis_SwFilename() -> str:
    helper = _SnmpSwUpdate()
    return helper.snmp.snmpget(_get_SwFilename_mib_name(False))[0]


def get_vendor_SwFilename() -> str:
    helper = _SnmpSwUpdate()
    return helper.snmp.snmpget(_get_SwFilename_mib_name(True), index=1)[0]


def set_vendor_SwMethod(method: int) -> None:
    helper = _SnmpSwUpdate()
    helper.snmp.snmpset(helper.board.sw.mib.sw_method_mib, str(method), "i")


def get_vendor_SwMethod() -> int:
    helper = _SnmpSwUpdate()
    return int(helper.snmp.snmpget(helper.board.sw.mib.sw_method_mib)[0])


def set_docsis_SwAdminStatus(val: int) -> None:
    helper = _SnmpSwUpdate()
    helper.snmp.snmpset(_get_SwAdminStatus_mib_name(False), str(val), "i")


def set_vendor_SwAdminStatus(val: int) -> None:
    helper = _SnmpSwUpdate()
    helper.snmp.snmpset(_get_SwAdminStatus_mib_name(True), str(val), "i", index=1)


def get_docsis_SwAdminStatus() -> int:
    helper = _SnmpSwUpdate()
    return int(helper.snmp.snmpget(_get_SwAdminStatus_mib_name(False))[0])


def get_vendor_SwAdminStatus() -> int:
    helper = _SnmpSwUpdate()
    return int(helper.snmp.snmpget(_get_SwAdminStatus_mib_name(True), index=1)[0])


def get_docsis_SwCurrentVers() -> str:
    helper = _SnmpSwUpdate()
    return helper.snmp.snmpget(_get_SwCurrentVers_mib_name(False))[0]


def get_vendor_SwCurrentVers() -> str:
    helper = _SnmpSwUpdate()
    return helper.snmp.snmpget(_get_SwCurrentVers_mib_name(True), index=1)[0]


def get_docsis_OperationStatus() -> int:
    helper = _SnmpSwUpdate()
    return int(helper.snmp.snmpget(_get_SwOperStatus_mib_name(False))[0])


def wait_for_update_to_complete(operStatus: int, retry: int, wait: int) -> bool:
    """Retries snmpget on operStatus and waits for the match with the passed value

    :param operStatus: 1 for inProgress, 2 for completeFromProvisioning, 3 for completeFromMgt, 4 for other
    :type operStatus: int
    :param retry: number retries until the expected operStatus value is returned
    :type retry: int
    :param wait: wait time in seconds after each retry
    :type wait: int
    :return: true if expected operStatus is fetched after retries else False
    :rtype: bool
    """
    for _ in range(retry):
        if retry_on_exception(get_docsis_OperationStatus, ()) != 1:
            CodeError("Software Update not already In Progress!!!")
        if get_docsis_OperationStatus() == operStatus:
            return True
        sleep(wait)
    return False


def get_docsis_EventEntry() -> Tuple[Dict, Any]:
    """returns the result of snmpwalk on the docsis event entry mib

    :return: docsis event entry
    :rtype: Tuple[Dict, Any]
    """
    helper = _SnmpSwUpdate()
    return helper.snmp.snmpwalk(_get_EventEntry_mib_name(False))


def trigger_docsis_snmp_sw_update(
    server_address, sw_filename, protocol, admin_status, address_type
) -> None:
    """triggers the software update by performing snmpset on the docsis specific mibs with the passed values

    :param server_address: ip address of the server
    :type server_address: str
    :param sw_file_name: name of the imgae file with extension
    :type sw_file_name: str
    :param protocol: protocol to be used by cm for sw download i.e 1 for tftp and 2 for http
    :type protocol: int
    :param admin_status: 1 for upgradeFromMgt, 2 for allowProvisioningUpgrade, 3 for ignoreProvisioningUpgrade
    :type admin_status: int
    :param address_type: type of ip address i.e 1 for ipv4 and 2 for ipv6
    :type address_type: int
    """
    set_docsis_SwFilename(sw_filename)
    set_docsis_SwServerTransportProtocol(protocol)
    set_docsis_SwServerAddressType(address_type)
    set_docsis_SwServerAddress(server_address)
    set_docsis_SwAdminStatus(admin_status)


def trigger_vendor_snmp_sw_update(
    server_address, sw_filename, protocol, admin_status, address_type
) -> None:
    """triggers the software update by performing snmpset on the vendor specific mibs with the passed values

    :param server_address: ip address of the server
    :type server_address: str
    :param sw_file_name: name of the imgae file with extension
    :type sw_file_name: str
    :param protocol: protocol to be used by cm for sw download i.e 1 for tftp and 2 for http
    :type protocol: int
    :param admin_status: 1 for upgradeFromMgt, 2 for allowProvisioningUpgrade, 3 for ignoreProvisioningUpgrade
    :type admin_status: int
    :param address_type: type of ip address i.e 1 for ipv4 and 2 for ipv6
    :type address_type: int
    """
    set_vendor_SwFilename(sw_filename)
    set_vendor_SwServerTransportProtocol(protocol)
    set_vendor_SwServerAddressType(address_type)
    set_vendor_SwServerAddress(server_address)
    set_vendor_SwAdminStatus(admin_status)
