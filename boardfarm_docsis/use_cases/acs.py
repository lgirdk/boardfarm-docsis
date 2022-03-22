"""ACS Use cases."""
import logging
from typing import Any, Dict, List, Union

import pexpect
from boardfarm.exceptions import PexpectErrorTimeout, TR069FaultCode, UseCaseFailure
from boardfarm.lib.common import retry
from boardfarm.lib.DeviceManager import get_device_by_name
from termcolor import colored

from boardfarm_docsis.use_cases.descriptors import AddObjectResponse
from boardfarm_docsis.use_cases.online_usecases import (
    is_board_online_after_reset,
    wait_for_board_boot_start,
)

logger = logging.getLogger("bft")


def is_dut_online_on_acs() -> bool:
    """To check if the DUT is online on acs.

    :return: True if devices is registered with acs and GPV
        is successful for Device.DeviceInfo.SoftwareVersion else false
    :rtype: bool
    """
    board = get_device_by_name("board")
    try:
        acs_status = retry(board.sw.tr069_connected, 3, [False])
    except PexpectErrorTimeout:
        acs_status = False
        msg = "\n\n Pexpect timeout, While checking DUT online status on ACS"
        logger.error(colored(msg, color="red", attrs=["bold"]))

    if not acs_status:
        msg = "\n\n DUT is not registered on acs"
        logger.error(colored(msg, color="red", attrs=["bold"]))
        return bool(acs_status)

    # TR069 Agent takes about 6-8 mins after the board comes online
    # and hence added loop for 2 times(GPV Call has a timeout of 5 mins)
    for _ in range(2):
        board.expect(pexpect.TIMEOUT, timeout=60)
        try:
            return bool(GPV("Device.DeviceInfo.SoftwareVersion"))
        except TR069FaultCode as err:
            msg = f"\n\nFailed to get DeviceInfo.SoftwareVersion due to {err} retrying"
            logger.error(colored(msg, color="red", attrs=["bold"]))
    return False


def GPV(params: Union[str, List[str]]) -> List[Dict[str, Any]]:
    """Perform TR069 RPC call GetParameterValues.

    Usage:
    ..code-block:: python

        GPV(params=["param1", "param2"])

    :param params: List of parameters
    :type params: Union[str, List[str]]
    :raises TR069FaultCode: incase GPV operation fails
    :return: List of dict of Param,Value pairs
    :rtype: List[RPCOutput]
    """
    acs_server = get_device_by_name("acs_server")
    return acs_server.GPV(params)


def SPV(params: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Perform TR069 RPC call SetParameterValues.

    Usage:
    ..code-block:: python

        SPV(params=[{"param1":"value1"}, {"param2":123}])

    :param params: Dict or list of Dict[parameters, values]
    :type params: Union[Dict[str, Any], List[Dict[str, Any]]]
    :raises TR069FaultCode: incase SPV operation fails
    :return: List of dict of Param,Value pairs
    :rtype: List[RPCOutput]
    """
    acs_server = get_device_by_name("acs_server")
    return acs_server.SPV(params)


def SPA(
    param: Union[List[Dict[str, str]], Dict[str, str]],
    notification_change: bool,
    access_change: bool,
    access_list: list,
) -> None:
    """Perform TR069 RPC call SetParameterValues.
    Example usage : SPA([{'Device.WiFi.SSID.1.SSID':'1'}], True, False, [])

    :param param: parameter as key of dictionary and notification as its value
    :type param: List of Dictionary or Dictionary
    :param notification_change: If true, the value of Notification replaces the current notification setting for this Parameter or group of Parameters. If false, no change is made to the notification setting
    :type notification_change: bool
    :param access_change: If true, the value of AccessList replaces the current access list for this Parameter or group of Parameters. If false, no change is made to the access list
    :type access_change: bool
    :param access_list: Array of zero or more entities for which write access to the specified Parameter(s) is granted
    :type access_list: list
    :raises TR069FaultCode: incase SPA operation fails
    :raises HTTPError: in case of HTTP error code is recieved in response
    """
    acs = get_device_by_name("acs_server")
    acs.SPA(param, access_change, access_list, notification_change)


def GPA(param: str) -> List[Dict[str, Any]]:
    """Perform TR069 RPC call GetParameterAttributes.

    :param param: name of the parameter
    :type param: str
    :raises TR069FaultCode: incase GPA operation fails
    :raises HTTPError: in case of HTTP error code is recieved in response
    :return: list of dictionary with keys Name, AccessList, Notification indicating the attributes of the parameter
    :rtype: List[Dict[str, Any]]
    """
    acs = get_device_by_name("acs_server")
    return acs.GPA(param)


def add_object(object_name: str) -> AddObjectResponse:
    """Perform TR069 RPC call AddObject
    Usage:
    ..code-block:: python
        out = add_object(object_name)
        instance_number = out.instance_number
        response = out.response
    :param object_name: Name of the object to be added
    :type object_name: str
    :raises TR069FaultCode: incase AddObject operation fails
    :raises UseCaseFailure: incase AddObjectResponseParser fails
    :return: AddObjectResponse with values response & instance_number
    :rtype: object
    """
    acs_server = get_device_by_name("acs_server")
    return AddObjectResponse(acs_server.AddObject(object_name), object_name)


def del_object(object_name: str) -> int:
    """Perform TR069 RPC call DeleteObject.
    Usage:
    ..code-block:: python
        del_object(object_name)
    :param object_name: Name of the object to be added
    :type object_name: str
    :raises TR069FaultCode: incase DelObject operation fails
    :return: int
    :rtype: status
    """
    acs_server = get_device_by_name("acs_server")
    result = acs_server.DelObject(object_name)
    return int(result[0]["value"])


def factory_reset() -> None:
    """Perform TR-069 FactoryReset RPC call and guarantee the board is back online.

    Usage:
    ..code-block:: python
        factory_reset()
    :raises TR069FaultCode: in case Factory Reset operation fails with fault code
    :raises HTTPError: in case Factory Reset operation fails with HTTP error code
    :raises: UseCaseFailure: in case the board is not back online
    """
    acs = get_device_by_name("acs_server")
    acs.FactoryReset()
    wait_for_board_boot_start()
    status = is_board_online_after_reset()
    if not status:
        raise UseCaseFailure("Board not Online after Factory Reset through ACS")
