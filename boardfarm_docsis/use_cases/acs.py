"""ACS Use cases."""
import logging
from typing import Any, Dict, List, TypedDict, Union

import pexpect
from boardfarm.exceptions import PexpectErrorTimeout, TR069FaultCode
from boardfarm.lib.common import retry
from boardfarm.lib.DeviceManager import get_device_by_name
from termcolor import colored

logger = logging.getLogger("bft")


class RPCOutput(TypedDict):
    """Output of TR069 RPC operation on a paramter.

    Resultant is a dictionary with keys specified as attribute of this class.
    """

    key: str
    type: str
    value: Any


def is_dut_online_on_acs() -> bool:
    """To check if the DUT is online on acs.

    :return: True if devices is registered with acs and GPV
        is successful for Device.DeviceInfo.SoftwareVersion else false
    :rtype: bool
    """
    board = get_device_by_name("board")
    try:
        acs_status = retry(board.tr069_connected, 3, [False])
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


def GPV(params: Union[str, List[str]]) -> List[RPCOutput]:
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


def SPV(params: List[Dict[str, Any]]) -> List[RPCOutput]:
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
