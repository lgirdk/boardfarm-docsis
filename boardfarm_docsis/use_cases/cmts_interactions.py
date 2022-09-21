"""Use case implementations for CMTS interactions.

CMTS interactions involve:

    - Reading DOCSIS RF parameters
    - Reading CM TLV and service flow configuration
"""

import re

from boardfarm.lib.DeviceManager import device_type, get_device_manager


def is_bpi_privacy_disabled() -> bool:
    """Fetch the GlobalPrivacy TLV value in CM config file.

    Return True if GlobalPrivacyEnable inside config file is set to Integer 0.
    By default, BPI privacy is enabled in CM config file.

    This use case will be used for scenarios where BPI+ encyption is not used.
    i.e. Multicast

    :return: True if BPI is disabled.
    :rtype: bool
    """
    device_mgr = get_device_manager()
    board = device_mgr.get_device_by_type(device_type.DUT)
    return bool(
        re.search(r"GlobalPrivacyEnable\s*0;", board.env_helper.get_board_boot_file())
    )
