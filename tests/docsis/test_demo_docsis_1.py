"""DOCSIS demo test - 1."""

from collections.abc import Iterator

import pytest
from boardfarm3.exceptions import TeardownError
from boardfarm3.lib.device_manager import DeviceManager
from boardfarm3.lib.utils import retry_on_exception
from boardfarm3.templates.wan import WAN
from boardfarm3.use_cases.cpe import get_cpe_provisioning_mode
from pytest_boardfarm3.lib.test_logger import TestLogger
from pytest_boardfarm3.lib.utils import ContextStorage

from boardfarm3_docsis.templates.cable_modem.cable_modem import CableModem
from boardfarm3_docsis.templates.cmts import CMTS
from boardfarm3_docsis.use_cases.connectivity import (
    is_board_online_after_reset,
    power_cycle,
)
from boardfarm3_docsis.use_cases.erouter import (
    get_erouter_addresses,
    get_wan_iface_ip_addresses,
    verify_erouter_ip_address,
)
from boardfarm3_docsis.use_cases.snmp import snmp_walk


@pytest.fixture
def resources(
    bf_context: ContextStorage, bf_logger: TestLogger, device_manager: DeviceManager
) -> Iterator[tuple[CableModem, CMTS, WAN]]:
    """Execute the setup and teardown phases of a test.

    :param bf_context: data struct to store temporary data
    :type bf_context: ContextStorage
    :param bf_logger: boardfarm step logger
    :type bf_logger: TestLogger
    :param device_manager: boardfarm device manager
    :type device_manager: DeviceManager
    :raises TeardownError: If CPE is not online after reboot
    :raises TeardownError: If CPE does not get a WAN IP after reboot
    :yield: devices needed for the test
    :rtype: Iterator[tuple[CableModem, CMTS, WAN]]
    """
    # Test Setup
    # Init some flags used by tests and teardown.
    bf_context.is_reboot_needed = False  # type: ignore[attr-defined]

    # Import devices that will be used by test
    board = device_manager.get_device_by_type(CableModem)  # type:ignore[type-abstract]
    cmts = device_manager.get_device_by_type(CMTS)  # type:ignore[type-abstract]
    wan = device_manager.get_device_by_type(WAN)  # type:ignore[type-abstract]
    mode = get_cpe_provisioning_mode(board)

    # Test setup phase done. Test execution begins
    yield board, cmts, wan

    # Test Teardown
    if bf_context.is_reboot_needed:  # type: ignore[attr-defined]
        bf_logger.log_step(
            "Teardown: Rebooting as the CM was not online after reboot in test case"
        )
        power_cycle()
        if not retry_on_exception(is_board_online_after_reset, (), 5, 15):
            msg = "Board did not come online during teardown!"
            raise TeardownError(msg)
        if not verify_erouter_ip_address(mode=mode, board=board, retry=9):
            msg = "Erouter failed to get an IP after reboot in teardown"
            raise TeardownError(msg)


# Define the test bed requirements as a Pytest mark.
@pytest.mark.env_req(
    {
        "environment_def": {
            "board": {
                "eRouter_Provisioning_mode": ["ipv4"],
                "model": ["TG2492LG", "CH7465LG", "TG3492LG", "F3896LG"],
            }
        }
    }
)
def test_demo_docsis_1(
    resources: tuple[CableModem, CMTS, WAN],  # pylint: disable=redefined-outer-name
    bf_logger: TestLogger,
    bf_context: ContextStorage,
) -> None:
    """IPv4 mode: CM Provisioning is successful.

    Validate if a pre-provisioned CPE in IPv4 mode, on reboot:
    - ranges and bonds to DOCSIS US and DS channels
    - US/DS on CMTS matches the SNMP output of docsIfUpChannelId/docsIfUpChannelId mib.
    - does not acquire an IPv6 address on the data interface

    :param resources: devices required for the test
    :type resources: tuple[CableModem, CMTS, WAN]
    :param bf_logger: boardfarm test logger
    :type bf_logger: TestLogger
    :param bf_context: data struct to store temporary data
    :type bf_context: ContextStorage
    """
    board, cmts, wan = resources

    bf_logger.log_step("Step 1: Reboot the DUT and verify Provisioning")
    board.sw.reset()
    bf_context.is_reboot_needed = True  # type: ignore[attr-defined]
    assert is_board_online_after_reset(), "DUT not online after reboot"
    bf_context.is_reboot_needed = False  # type: ignore[attr-defined]

    bf_logger.log_step(
        "Step 2: Verify the downstream and upstream bonding status of DUT at CMTS."
    )
    us_ds_chls = cmts.get_cm_channel_values(
        board.sw.get_interface_mac_addr(board.hw.wan_iface)
    )
    assert us_ds_chls, "Failed to fetch the DS and US bonding status"

    bf_logger.log_step("Step 3: Check if the eCM acquire the IP address")
    assert get_wan_iface_ip_addresses(board, 3), "eCM didn't acquire IP address"

    bf_logger.log_step(
        "Step 4: Do SNMP Walk 'docsIfUpChannelId' Mib object on DUT and verify DUT "
        "returns all US channel identities."
    )
    walk_us_chl_id = snmp_walk("docsIfUpChannelId", wan=wan, board=board, cmts=cmts)
    us_length = len(us_ds_chls["US"].replace("(", ",").replace(")", "").split(","))
    assert us_length == len(walk_us_chl_id[0]), (
        "US channels mismatch between CM and CMTS"
    )

    bf_logger.log_step(
        "Step 5: Do SNMP Walk 'docsIfDownChannelId' Mib object on DUT and verify DUT "
        "returns all DS channel identities."
    )
    walk_ds_chl_id = snmp_walk("docsIfDownChannelId", wan=wan, board=board, cmts=cmts)
    ds_length = len(us_ds_chls["DS"].replace("(", ",").replace(")", "").split(","))
    assert ds_length == len(walk_ds_chl_id[0]), (
        "DS channels mismatch between CM and CMTS"
    )

    bf_logger.log_step("Step 6: check if eRouter acquires the correct IP address")
    ip_addresses = get_erouter_addresses(retry_count=2, board=board)
    assert ip_addresses.ipv4, "eRouter does not have ipv4 address in ipv4 mode"
    assert not ip_addresses.ipv6, "eRouter has ipv6 address in ipv4 mode"
