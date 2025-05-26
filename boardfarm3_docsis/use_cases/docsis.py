"""Use Cases to interact with DOCSIS devices such as CMTS and CM."""

from __future__ import annotations

import re
from ipaddress import IPv4Network, IPv6Network, ip_network
from re import findall as regex_findall
from typing import TYPE_CHECKING

from boardfarm3.exceptions import DeviceBootFailure
from boardfarm3.lib.regexlib import ValidIpv4AddressRegex_Nogroup
from debtcollector import removals

from boardfarm3_docsis.use_cases.connectivity import is_board_online_after_reset

if TYPE_CHECKING:
    from boardfarm3.templates.wan import WAN

    from boardfarm3_docsis.templates.cable_modem import CableModem
    from boardfarm3_docsis.templates.cmts import CMTS
    from boardfarm3_docsis.templates.provisioner import Provisioner


def is_route_present_on_cmts(
    route: IPv4Network | IPv6Network,
    cmts: CMTS,
) -> bool:
    """Check if routing table of CMTS router contains a route.

    Perfrom ``ip route`` command on a router, collect the routes and
    check if route is present in table output.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Verify that the CMTS learns route
        - Make sure that the packets can be captured between CPE and CMTS

    .. code-block:: python

        # example usage
        status = is_route_present_on_cmts(
            route=ipaddress.ip_network("192.168.101.0/24"),
        )

    :param route: route to be looked up on CMTS
    :type route: IPv4Network | IPv6Network
    :param cmts: CMTS to be used
    :type cmts: CMTS
    :return: True if route is present on CMTS
    :rtype: bool
    """
    raw_routes = cmts.get_ip_routes()
    routes = "\n".join(raw_routes)
    ip_routes = [
        ip_network(_route)
        for _route in regex_findall(
            ValidIpv4AddressRegex_Nogroup + r"\/[\d]{1,2}",
            routes,
        )
    ]
    return route in ip_routes


def get_downstream_bonded_channel(board: CableModem, cmts: CMTS) -> str:
    """Get the Downstream bonded channel value from the CMTS.

    .. code-block:: python

        # example output
        "9"

    :param board: Cable Modem device instance
    :type board: CableModem
    :param cmts: CMTS device instance
    :type cmts: CMTS
    :return: Downstream bonded channel value
    :rtype: str
    """
    return cmts.get_downstream_channel_value(board.hw.mac_address)


def get_upstream_bonded_channel(board: CableModem, cmts: CMTS) -> str:
    """Get the upstream bonded channel value from the CMTS.

    .. code-block:: python

        # example output
        "8"

    :param board: Cable Modem device instance
    :type board: CableModem
    :param cmts: CMTS device instance
    :type cmts: CMTS
    :return: Upstream bonded channel value
    :rtype: str
    """
    return cmts.get_upstream_channel_value(board.hw.mac_address)


def get_cable_modem_channels(board: CableModem, cmts: CMTS) -> dict[str, str]:
    """Get the CM channel values from the CMTS.

    .. code-block:: python

        # example output
        {
            "US": "1(2,3,4,5,6,7,8)",
            "DS": "9(1,2,3,4,5,6,7,8,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24)",
        }


    :param board: Cable Modem device instance
    :type board: CableModem
    :param cmts: CMTS device instance
    :type cmts: CMTS
    :return: Cable Modem channel values
    :rtype: dict[str, str]
    """
    return cmts.get_cm_channel_values(board.hw.mac_address)


def get_ds_frequecy_list(board: CableModem) -> list[str]:
    """Return the frequency list of CableModem.

    Get the Downstream frequency list from the CableModem device.

    .. code-block:: python

        # example output:
        [
            "137000000",
            "242000000",
            "274000000",
            "300000000",
            "305000000",
            "306750000",
            "330250000",
            "330750000",
            "331000000",
            "370750000",
            "338000000",
            "338750000",
            "339000000",
            "402000000",
            "402750000",
            "410000000",
            "418000000",
            "426000000",
            "434000000",
            "442000000",
            "450000000",
            "458000000",
            "466000000",
            "474000000",
            "482000000",
            "490000000",
            "498000000",
            "578000000",
            "586750000",
            "594000000",
            "618000000",
            "634000000",
            "666000000",
            "730000000",
            "754000000",
            "778000000",
            "786000000",
            "810000000",
            "826000000",
            "842000000",
        ]

    :param board: CableModem device instance
    :type board: CableModem
    :return: frequency list of CPE
    :rtype: list[str]
    """
    return board.sw.get_golden_ds_freq_list()


def is_bpi_privacy_disabled(board: CableModem) -> bool:
    """Fetch the GlobalPrivacy TLV value in CM config file.

    Return True if GlobalPrivacyEnable inside config file is set to Integer 0.
    By default, BPI privacy is enabled in CM config file.

    This use case will be used for scenarios where BPI+ encyption is not used.
    i.e. Multicast

    :param board: CableModem device instance, defaults to None
    :type board: CableModem
    :raises ValueError: when the board object is None
    :raises ValueError: when the bootfile is an empty string
    :return: True if BPI is disabled.
    :rtype: bool
    """
    if board is None:
        err_msg = "The board object is None; it must be explicitely passed."
        raise ValueError(err_msg)

    boot_file = board.sw.get_boot_file()
    if boot_file == "":
        err_msg = "Bootfile content cannot be empty."
        raise ValueError(err_msg)
    return bool(regex_findall(r"GlobalPrivacyEnable\s*0;", boot_file))


@removals.remove()
def provision_cable_modem(
    board: CableModem,
    provisioner: Provisioner,
    wan: WAN,
    cm_boot_file: str | None = None,
    emta_boot_file: str | None = None,
) -> None:
    """Provision the Cable Modem.

    With this function, the CM and eMTA boot files can be None.
    This function is deprecated; prefer to use provision_docsis_board()
    instead. That ensures that we are explicit, rather than implicit.

    :param board: the CM to be provisioned
    :type board: CableModem
    :param provisioner: the Provisioner
    :type provisioner: Provisioner
    :param wan: the TFTP device
    :type wan: WAN
    :param cm_boot_file: content of the CM boot file, defaults to None
    :type cm_boot_file: str | None
    :param emta_boot_file: content of the eMTA boot file, defaults to None
    :type emta_boot_file: str | None
    """
    board.sw.provision_cable_modem(
        provisioner=provisioner,
        tftp_device=wan,
        boot_file=cm_boot_file,
        boot_file_mta=emta_boot_file,
    )


@removals.remove()
def provision_board_w_boot_files(
    board: CableModem,
    provisioner: Provisioner,
    tftp: WAN,
    cm_boot_file: str | None = None,
    mta_boot_file: str | None = None,
) -> None:
    """Provision Cable Modem with given boot files.

    This Use Case is deprecated in favour of `provision_docsis_board_and_reboot_it()`.
    Said Use Case forces us to be more explicit.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Initialize DUT using boot file with below parameters

    :param board: the Cable Modem to be provisioned
    :type board: CableModem
    :param provisioner: the Provisioner
    :type provisioner: Provisioner
    :param tftp: the TFTP device
    :type tftp: WAN
    :param cm_boot_file: Cable Modem boot file, defaults to None
    :param cm_boot_file: str | None
    :param mta_boot_file: MTA boot file, defaults to None
    :param mta_boot_file: str | None
    """
    _cm_boot_file, _mta_boot_file = _override_boot_files(
        board=board,
        cm_boot_file=cm_boot_file,
        mta_boot_file=mta_boot_file,
    )
    provision_cable_modem(
        board=board,
        provisioner=provisioner,
        wan=tftp,
        cm_boot_file=_cm_boot_file,
        emta_boot_file=_mta_boot_file,
    )
    # TODO: discuss with Michele, should we use Use Cases for the next two lines?
    # BOARDFARM-5034
    board.sw.reset()
    board.sw.wait_for_boot()


def _get_board_boot_logs(timeout: int, board: CableModem) -> str:
    """Get the console log for the boot process.

    :param timeout: time value to collect the logs for
    :type timeout: int
    :param board: Cable Modem device instance
    :type board: CableModem
    :return: console logs for given timeout
    :rtype: str
    """
    return board.sw.get_board_logs(timeout)


def _verify_cm_config_downloaded(boot_logs: str, board: CableModem) -> bool:
    """Verify if the CM config download is successful.

    :param boot_logs: The console logs collected post reboot
    :type boot_logs: str
    :param board: Cable Modem device instance
    :type board: CableModem
    :return: True if CM config download is successful else False
    :rtype: bool
    :raises DeviceBootFailure: if board is not online
    """
    if is_board_online_after_reset():
        if logs := board.sw.get_gateway_provision_log():
            return board.sw.verify_cm_cfg_file_read_log(logs)
        return board.sw.verify_cm_cfg_file_read_log(boot_logs)
    err_msg = "Board not online"
    raise DeviceBootFailure(err_msg)


def _verify_emta_config_downloaded(boot_logs: str, board: CableModem) -> bool:
    """Verify if the MTA config file download is successful.

    :param boot_logs: The console logs collected post reboot
    :type boot_logs: str
    :param board: Cable Modem device instance
    :type board: CableModem
    :return: True if MTA config download is successful else False
    :rtype: bool
    """
    return board.sw.provisioning_messages["verify_emta_cfg_file_download"] in boot_logs


def _verify_emta_config_applied(boot_logs: str, board: CableModem) -> bool:
    """Verify if the MTA config is applied successfully.

    :param boot_logs: The console logs collected post reboot
    :type boot_logs: str
    :param board: Cable Modem device instance
    :type board: CableModem
    :return: True if MTA config is applied successfully else False
    :rtype: bool
    """
    return board.sw.provisioning_messages["verify_emta_config_apply"] in boot_logs


def _verify_emta_provisioning(boot_logs: str, board: CableModem) -> bool:
    """Verify if the MTA provisioning is successful.

    :param boot_logs: The console logs collected post reboot
    :type boot_logs: str
    :param board: Cable Modem device instance
    :type board: CableModem
    :return: True if MTA provisioning is successful else False
    :rtype: bool
    """
    return board.sw.provisioning_messages["verify_emta_provisioning"] in boot_logs


def are_boot_logs_successful(timeout: int, board: CableModem) -> bool:
    """Collect the boot logs and validate the boot stages and provisioning.

    :param timeout: time value to collect the logs for
    :type timeout: int
    :param board: Cable Modem device instance
    :type board: CableModem
    :return: True if boot stages are verified and provisioning is successful else False
    :rtype: bool
    """
    log = _get_board_boot_logs(timeout, board=board)
    return all(
        [
            _verify_cm_config_downloaded(log, board=board),
            _verify_emta_config_downloaded(log, board=board),
            _verify_emta_config_applied(log, board=board),
            _verify_emta_provisioning(log, board=board),
        ],
    )


def _get_boot_file(board: CableModem) -> str:
    return board.sw.get_boot_file()


def add_tlvs_to_bootfile(
    multiline_tlv: str, config_file: str | None, board: CableModem
) -> str:
    """Add TLVs to the boot file in the env_hepler.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Add  TLVs to the boot file in the env_hepler.

    Adds/appends TLVs (as multiline string) at the end of the boot file, just before
        the CmMic comment line

    :param multiline_tlv: a string with embedded newlines with the TLVs to be added
    :type multiline_tlv: str
    :param config_file: updated config file
    :type config_file: str | None
    :param board: Cable Modem device instance
    :type board: CableModem
    :raises ValueError: if the string hook was not found in the bootfile
    :return: a copy of the env_helper bootfile with the TLVs added
    :rtype: str
    """
    bootfile = config_file if config_file else _get_boot_file(board=board)
    idx = bootfile.find("/* CmMic")
    if idx < 0:
        msg = "Hook '/* CmMic' not found in boot file"
        raise ValueError(msg)

    comment = "/* SW mibs */"
    return (
        bootfile[: idx - 1] + "\n\t" + comment + "\n\t" + multiline_tlv + bootfile[idx:]
    )


def get_vendor_id_from_cm_bootfile(board: CableModem) -> str:
    """Fetch the vendor identifier hexadecimal value from CM bootfile.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Fetch the vendor identifier hexadecimal value from CM bootfile.

    :param board: Cable Modem device instance
    :type board: CableModem
    :return: hexadecimal value of vendor identifier
    :rtype: str
    """
    return re.search("VendorIdentifier 0x([A-Za-z0-9]*);", _get_boot_file(board=board))[
        1
    ]


# pylint: disable-next=too-many-locals
def update_erouter_mode(
    mode: str, board: CableModem, bootfile: str | None = None
) -> str:
    """Switch the bootfile eRouter config in the env_helper to given mode.

    If the mode has to be switched multiple times then the bootfile param to be used.
    bootfile param should be the current eRouter config and not the one in
    env_helper.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Switch to modem mode using config file
        - Switch the provisioning mode via config file
        - Switch back to IPv4 provisioning mode using config file


    :param mode: one of "none", "disabled", "ipv4", "ipv6", "dual"
    :type mode: str
    :param board: Cable Modem device instance
    :type board: CableModem
    :param bootfile: config file to be used before updating mode
    :type bootfile: str
    :raises ValueError: if mode is not valid
    :return: a copy of the env_helper bootfile with the new mode
    :rtype: str
    """
    modes = {"disabled": "0", "none": "0", "ipv4": "1", "ipv6": "2", "dual": "3"}

    if mode not in modes:
        msg = f"Requested initialization mode: {mode} not in {modes}"
        raise ValueError(msg)
    if not bootfile:
        bootfile = _get_boot_file(board=board)
    vendor_id = get_vendor_id_from_cm_bootfile(board=board)

    if "InitializationMode 1" in bootfile:
        # add the LLCfilters
        pattern = r"SnmpMibObject\sdocsDevFilterLLCStatus+\.2\s\w+\s\d;\s.*"
        _new_llc_index = (
            "SnmpMibObject docsDevFilterLLCIfIndex.3 Integer 0 ; /* all interfaces */"
            "SnmpMibObject docsDevFilterLLCProtocolType.3 Integer 1; /* ethertype */"
            "SnmpMibObject docsDevFilterLLCProtocol.3 Integer 34525 ; /* ipv6 */"
            "SnmpMibObject docsDevFilterLLCStatus.3 Integer 4; /* createAndGo */"
        )
        _from_llc = re.findall(pattern, bootfile)
        _to_llc = str(_from_llc[0]) + _new_llc_index
        bootfile = re.sub(re.escape(_from_llc[0]), _to_llc, bootfile)
    if mode in {"ipv4", "ipv6", "dual"} and "TR69 Management Server" not in bootfile:
        tr69_param = (
            f"/* TR69 Management Server */\n\tVendorSpecific\n\t{{\n\t\t"
            f"VendorIdentifier 0x{vendor_id};\n\t\teRouter\n\t\t{{\n\t\t\t"
            f"TR69ManagementServer\n\t\t\t{{\n\t\t\t\tEnableCWMP 1;\n\t\t\t\t"
            f'URL "http://acs_server.boardfarm.com:9675"'
            f";\n\t\t\t\tACSOverride 1;"
            f"\n\t\t\t}}\n\t\t}}\n\t}}\n\n\t/* MFG CVC Data */"
        )
        pattern = r".*MFG CVC Data.*"
        bootfile = re.sub(pattern, tr69_param, bootfile)
    if mode == "ipv6":
        ipv6_params_to_add = (
            f"VendorSpecific\n\t{{\n\t\tVendorIdentifier "
            f"0x{vendor_id};\n\t\teRouter\n\t\t{{\n\t\t\tGenericTLV TlvCode 12"
            f' TlvString "Device.DSLite.Enable|boolean|true"'
            f";\n\t\t\tGenericTLV TlvCode 12 TlvString "
            f'"Device.DSLite.InterfaceSetting.1.Enable|boolean|true";\n\t\t\t'
            f"GenericTLV TlvCode 12 TlvString "
            f'"Device.DSLite.InterfaceSetting.1.X_LGI-COM_MssClampingEnable|'
            f'boolean|true";\n\t\t\tGenericTLV TlvCode 12 TlvString '
            f'"Device.DSLite.InterfaceSetting.1.X_LGI-COM_Tcpmss|unsigned|1420"'
            f";\n\t\t}}\n\t}}\n\n\t/* MFG CVC Data */"
        )
        pattern = r".*MFG CVC Data.*"
        bootfile = re.sub(pattern, ipv6_params_to_add, bootfile)
    if mode in {"disabled", "ipv4", "ipv6", "dual"}:
        # simply swap the value in the bootfile
        _from = "InitializationMode((\\s|\t){1,})\\d.*;"
        _to = f"InitializationMode {modes[mode]};"
        if mode == "disabled":
            # remove TR69 management server section
            _tr69_from = r"TR69 Management Server (.+)((?:\n.+)+)\n\n.* Plume"
            _tr69_to = "Plume"
            bootfile = re.sub(_tr69_from, _tr69_to, bootfile)
    elif mode == "none":
        # remove the InitialisationMode
        _from = (
            "VendorSpecific.*\n.*{.*\n.*VendorIdentifier"
            rf" 0x{vendor_id};.*\n.*eRouter.*\n.*{{.*\n.*InitializationMode("
            r"(\\s|\t){1,})\\d.*;.*\n.*}}*\n.*}}"
        )
        _to = "/* Removed */"
    else:
        msg = f"Unexpected value: {mode=}"
        raise ValueError(msg)
    return re.sub(_from, _to, bootfile)


def _override_boot_files(
    board: CableModem,
    cm_boot_file: str | None = None,
    mta_boot_file: str | None = None,
) -> tuple[str, str]:
    """Ensure that CM and eMTA boot files are not None.

    These configuration files are read from the board object, in case of None.

    This method is a small helper, that, once `override_boot_files()` is removed,
    could be put in its caller function.

    :param board: the Cable Modem to be provisioned
    :type board: CableModem
    :param cm_boot_file: Cable Modem config, defaults to None
    :type cm_boot_file: str | None, optional
    :param mta_boot_file: eMTA config, defaults to None
    :type mta_boot_file: str | None, optional
    :return: the two configuration files in string format
    :rtype: tuple[str, str]
    """
    if cm_boot_file is None:
        cm_boot_file = board.sw.get_boot_file()
    if mta_boot_file is None:
        mta_boot_file = board.sw.get_mta_boot_file()

    return cm_boot_file, mta_boot_file


@removals.remove()
def override_boot_files(
    board: CableModem,
    cm_boot_file: str | None = None,
    mta_boot_file: str | None = None,
) -> tuple[str, str]:
    """Configure the boot file.

    This method implements what in Boardfarm v2 was `configure_boot_file()`, but
    does not update the objects' configuration anymore.
    In Boardfarm v2, the CPE object needed update before a call to the provisioning
    Use Cases was made.
    As such, it is deprecated in favour of passing the files explicitly to the
    appropriate Use Case.

    In Boardfarm v3 the user should choose `between provision_docsis_board()` and
    `provision_docsis_board_and_reboot_it()`

    :param board: the Cable Modem to be provisioned
    :type board: CableModem
    :param cm_boot_file: Cable Modem config, defaults to None
    :type cm_boot_file: str | None, optional
    :param mta_boot_file: eMTA config, defaults to None
    :type mta_boot_file: str | None, optional
    :return: the two configuration files in string format
    :rtype: tuple[str, str]
    """
    return _override_boot_files(board, cm_boot_file, mta_boot_file)


def provision_docsis_board(
    board: CableModem,
    provisioner: Provisioner,
    wan: WAN,
    cm_boot_file: str,
    emta_boot_file: str,
) -> None:
    """Provision the Cable Modem with the given CM and eMTA boot files.

    :param board: the Cable Modem to be provisioned
    :type board: CableModem
    :param provisioner: DOCSIS provisioner
    :type provisioner: Provisioner
    :param wan: TFTP server
    :type wan: WAN
    :param cm_boot_file: Cable Modem config
    :type cm_boot_file: str
    :param emta_boot_file: eMTA config
    :type emta_boot_file: str
    """
    board.sw.provision_cable_modem(
        provisioner=provisioner,
        tftp_device=wan,
        boot_file=cm_boot_file,
        boot_file_mta=emta_boot_file,
    )


def provision_docsis_board_and_reboot_it(
    board: CableModem,
    provisioner: Provisioner,
    wan: WAN,
    cm_boot_file: str,
    emta_boot_file: str,
) -> None:
    """Provision the Cable Modem with the given bootfiles and reboot it.

    This Use Case performs a CPE-triggered software reboot.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Initialize DUT using boot file with below parameters

    :param board: the Cable Modem to be provisioned
    :type board: CableModem
    :param provisioner: DOCSIS provisioner
    :type provisioner: Provisioner
    :param wan: TFTP server
    :type wan: WAN
    :param cm_boot_file: Cable Modem config
    :type cm_boot_file: str
    :param emta_boot_file: eMTA config
    :type emta_boot_file: str
    """
    provision_docsis_board(
        board=board,
        provisioner=provisioner,
        wan=wan,
        cm_boot_file=cm_boot_file,
        emta_boot_file=emta_boot_file,
    )
    board.sw.reset()
    board.sw.wait_for_boot()
