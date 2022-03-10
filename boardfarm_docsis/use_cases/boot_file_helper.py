"""Contains the SW update usecases."""
import re

from boardfarm.lib.DeviceManager import get_device_by_name


def add_tlvs(multiline_tlv: str) -> str:
    """Add  tlvs to the boot file in the env_hepler.

    Adds/appends tlvs (as multiline string) at the end
    of the boot file, just before the CmMic comment line

    :param multiline_tlv: a string with embedded newlines with the tlvs to be
                          added
    :type multiline_tlv: str
    :param boot_file: the boot file in multiline string format
    :type boot_file: str

    :return: the bootfile as a multiline string with the added tlvs
    :rtype: str

    :raises ValueError: the string hook was not found in the bootfile

    :return: a copy of the env_helper bootfile with the tlvs added
    :rtype: str
    """
    bootfile: str = get_device_by_name("board").env_helper.get_board_boot_file()

    idx = bootfile.find("/* CmMic")
    if idx < 0:
        raise ValueError("Hook '/* CmMic' not found in boot file")

    comment = "/* SW mibs */"
    return (
        bootfile[: idx - 1] + "\n\t" + comment + "\n\t" + multiline_tlv + bootfile[idx:]
    )


def switch_erotuer_mode(mode: str) -> str:
    """Switch the bootfile erouter config in the env_helper to given mode.

    :param mode: one of "none", "disabled", "ipv4", "ipv6", "dual"
    :type mode: str

    :return: a copy of the env_helper bootfile with the new mode
    :rtype: str

    :raises ValueError: if mode is not valid
    """
    modes = {"disabled": "0", "none": "0", "ipv4": "1", "ipv6": "2", "dual": "3"}

    if mode not in modes:
        raise ValueError(f"Requested initialization mode: {mode} not in {modes}")

    bootfile = get_device_by_name("board").env_helper.get_board_boot_file()

    if mode in {"disabled", "ipv4", "ipv6", "dual"}:
        # simply swap the value in the bootfile
        _from = "InitializationMode((\\s|\t){1,})\\d.*;"
        _to = f"InitializationMode {modes[mode]};"
    elif mode == "none":
        # remove the InitialisationMode
        _from = "VendorSpecific.*\n.*{.*\n.*VendorIdentifier 0x02a613;.*\n.*eRouter.*\n.*{.*\n.*InitializationMode((\\s|\t){1,})\\d.*;.*\n.*}*\n.*}"
        _to = "/* Removed */"

    return re.sub(_from, _to, bootfile)
