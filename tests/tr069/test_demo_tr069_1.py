"""TR069 Demo test case - 1."""

import pytest
from boardfarm3.exceptions import TR069FaultCode
from boardfarm3.lib.device_manager import DeviceManager
from boardfarm3.templates.acs import ACS
from boardfarm3.templates.cpe import CPE
from pytest_boardfarm3.lib import TestLogger

from boardfarm3_docsis.use_cases.tr069 import set_parameter_values


@pytest.mark.env_req(
    {
        "environment_def": {
            "board": {
                "eRouter_Provisioning_mode": ["ipv4"],
            },
            "tr-069": {},
        }
    }
)
@pytest.mark.parametrize(
    ("param", "example_value"),
    [
        (
            "Device.RootDataModelVersion",
            "2.4",
        ),
        (
            "Device.InterfaceStackNumberOfEntries",
            "4",
        ),
        (
            "Device.DeviceInfo.DeviceCategory",
            "DOCSIS_Gateway",
        ),
        (
            "Device.DeviceInfo.ManufacturerOUI",
            "5C353B",
        ),
        (
            "Device.DeviceInfo.Description",
            "DOCSIS 3.0 Cable Modem Gateway Device",
        ),
        (
            "Device.DeviceInfo.SerialNumber",
            "AC:22:05:EE:F8:C0",
        ),
        (
            "Device.DeviceInfo.HardwareVersion",
            "5.01",
        ),
        (
            "Device.DeviceInfo.AdditionalHardwareVersion",
            "5.01",
        ),
        (
            "Device.DeviceInfo.UpTime",
            "236856",
        ),
        (
            "Device.DeviceInfo.FirstUseDate",
            "2021-04-09T11:36:10",
        ),
    ],
)
def test_demo_tr069_1(
    param: str,
    example_value: str,
    bf_logger: TestLogger,
    device_manager: DeviceManager,
) -> None:
    """SPV on read-only parameter <Param> should report fault code.

    Purpose of this test case is to verify that when an attempt is made to
    set a read-only TR-181 data model parameter <Param> with a valid value
    by using SetParameterValues RPC then DUT should return fault response with
    appropriate fault code.

    :param param: TR069 param
    :type param: str
    :param example_value: TR069 value
    :type example_value: str
    :param bf_logger: boardfarm test logger
    :type bf_logger: TestLogger
    :param device_manager: boardfarm device manager
    :type device_manager: DeviceManager
    """
    board = device_manager.get_device_by_type(CPE)  # type:ignore[type-abstract]
    acs = device_manager.get_device_by_type(ACS)  # type:ignore[type-abstract]

    bf_logger.log_step(
        "Step 2: Execute SetParameterValues RPC by providing parameter"
        f"name as {param} and value as any valid value of datatype"
    )
    with pytest.raises(TR069FaultCode) as exc:
        set_parameter_values([{param: example_value}], acs, board)
    assert exc.value.faultdict["spv_fault"][0]["FaultCode"] == "9008", (
        "Unexpected fault code"
    )
    check_str = "Attempt to set a non-writable parameter"
    assert exc.value.faultdict["spv_fault"][0]["FaultString"] == check_str, (
        "Unexpected fault string"
    )
