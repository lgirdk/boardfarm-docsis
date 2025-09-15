"""TR-069 Use cases."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

import pexpect
from boardfarm3.exceptions import TR069FaultCode, UseCaseFailure
from boardfarm3.lib.utils import retry
from debtcollector import moves
from termcolor import colored

from boardfarm3_docsis.use_cases.connectivity import (
    is_board_online_after_reset,
    wait_for_board_boot_start,
)

if TYPE_CHECKING:
    from boardfarm3.templates.acs import ACS
    from boardfarm3.templates.cpe import CPE


_LOGGER = logging.getLogger(__name__)


def _check_devices(acs: ACS | None, board: CPE | None) -> None:
    """Check that devices passed to the Use Case are not None.

    This behaviour is not tolerated anymore in boardfarm v3.

    :param acs: the ACS to be used in the Use Case
    :type acs: ACS | None
    :param board: the ACS to be used in the Use Case
    :type board: CPE | None
    :raises ValueError: when ACS or Board are None
    """
    err_msg = "Board and ACS objects must be passed explicitely."
    if board is None or acs is None:
        raise ValueError(err_msg)


@dataclass
class AddObjectResponse:
    """Store output of TR-069 AddObject RPC.

    :raises UseCaseFailure: in case of parsing errors
    """

    response: list[dict[str, str]]
    object_name: str

    @property
    def instance_number(self) -> int:
        """Store the Instance Number of the newly created Object.

        Once created, a Parameter or sub-object within this Object can be later
        referenced by using this Instance Number Identifier (defined in Section A.2.2.1)
        in the Path Name. The Instance Number assigned by the CPE is arbitrary.

        Note the fact that Instance Numbers are arbitrary means that they
        do not  define a useful Object ordering, e.g. the ACS cannot assume
        that a newly created Object will have a higher Instance Number than
        its existing sibling Objects.

        :return: instance number
        :rtype: int
        """
        return self._instance_number

    def __post_init__(self) -> None:
        """Parse response.

        :raises UseCaseFailure: in case of parsing issues.
        """
        if self.object_name in str(self.response):
            self._instance_number = int(
                self.response[0]["key"][len(self.object_name) :].split(".")[0],
            )
        else:
            msg = f"AddObject Response could not be parsed. Response: {self.response}"
            raise UseCaseFailure(msg)


def is_dut_online_on_acs(
    acs: ACS | None = None,
    board: CPE | None = None,
) -> bool:
    """Check if the DUT is online on ACS.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Verify the DUT registration status on the ACS
        - Make sure that DUT is registered on the ACS.

    :param acs: ACS server that will perform GPV
    :type acs: ACS | None
    :param board: CPE on which to perform TR-069 method
    :type board: CPE | None
    :return: True if devices is registered with ACS and GPV
        is successful for Device.DeviceInfo.SoftwareVersion, else False
    :rtype: bool
    """
    _check_devices(acs=acs, board=board)
    try:
        # FIXME: retry uses *args, that normally passes the arguments'      # noqa: FIX001 # pylint: disable=fixme
        # names here it seems that we are passing the arguments' values
        # instead for the time being this is ignored.
        acs_status: bool = retry(board.sw.is_tr069_connected, 3)
    except pexpect.TIMEOUT:
        acs_status = False
        msg = "Pexpect timeout, While checking DUT online status on ACS"
        _LOGGER.exception(msg)
    if not acs_status:
        msg = "\n\n DUT is not registered on ACS"
        _LOGGER.error(colored(msg, color="red", attrs=["bold"]))
        return acs_status
    # TR069 Agent takes about 6-8 mins after the board comes online
    # and hence added loop for 2 times (GPV call has a timeout of 5 mins)
    for _ in range(2):
        try:
            return bool(GPV("Device.DeviceInfo.SoftwareVersion", acs, board))
        except TR069FaultCode as err:  # noqa: PERF203
            msg = f"\n\nFailed to get DeviceInfo.SoftwareVersion due to {err}, retrying"
            _LOGGER.exception(colored(msg, color="red", attrs=["bold"]))
    return False


def get_parameter_values(
    params: str | list[str],
    acs: ACS | None = None,
    board: CPE | None = None,
) -> list[dict[str, Any]]:
    """Perform TR-069 RPC call GetParameterValues.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Execute GetParameterValues RPC by providing param name
        - Perform GPV on parameter
        - using GPV via ACS

    Usage:

    .. code-block:: python

        GPV(params=["param1", "param2"])

    :param params: List of parameters
    :type params: str | list[str]
    :param acs: ACS server that will perform GPV
    :type acs: ACS | None
    :param board: CPE on which to perform TR-069 method
    :type board: CPE | None
    :return: List of dict of Param,Value pairs
    :rtype: List[RPCOutput]
    """
    _check_devices(acs=acs, board=board)
    return acs.GPV(params, cpe_id=board.sw.tr69_cpe_id)


GPV = moves.moved_function(get_parameter_values, "GPV", __name__)


def set_parameter_values(
    params: list[dict[str, Any]],
    acs: ACS | None = None,
    board: CPE | None = None,
) -> int:
    """Perform TR-069 RPC call SetParameterValues.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Perform SetParameterValues RPC by providing parameter
        - Execute SPV RPC by providing parameter name
        - Execute SPV from ACS

    Usage:

    .. code-block:: python

        SPV(params=[{"param1": "value1"}, {"param2": 123}])

    :param params: Dict or list of Dict[parameters, values]
    :type params: list[dict[str, Any]]
    :param acs: ACS server that will perform GPV
    :type acs: ACS | None
    :param board: CPE on which to perform TR-069 method
    :type board: CPE | None
    :return: List of dict of Param,Value pairs
    :rtype: int
    """
    _check_devices(acs=acs, board=board)
    return acs.SPV(params, cpe_id=board.sw.tr69_cpe_id)


SPV = moves.moved_function(set_parameter_values, "SPV", __name__)


def set_parameter_attributes(  # noqa: PLR0913
    param: list[dict[str, str]] | dict[str, str],
    notification_change: bool,
    access_change: bool,
    access_list: list,
    acs: ACS | None = None,
    board: CPE | None = None,
) -> None:
    """Perform TR-069 RPC call SetParameterValues.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Execute SetParameterAttributes RPC
        - Execute SPA RPC by providing ParameterName
        - Perform SPA on

    Example usage:

    .. code-block:: python

        SPA([{"Device.WiFi.SSID.1.SSID": "1"}], True, False, [])

    :param param: parameter as key of dictionary and notification as its value
    :type param: list[dict[str, str]] | dict[str, str]
    :param notification_change: If true, the value of Notification replaces the
        current notification setting for this Parameter or group of Parameters.
        If false, no change is made to the notification setting
    :type notification_change: bool
    :param access_change: If true, the value of AccessList replaces the current
        access list for this Parameter or group of Parameters.
        If false, no change is made to the access list.
    :type access_change: bool
    :param access_list: Array of zero or more entities for which write access
        to the specified Parameter(s) is granted
    :type access_list: list
    :param acs: ACS server that will perform GPV
    :type acs: ACS | None
    :param board: CPE on which to perform TR-069 method
    :type board: CPE | None
    """
    _check_devices(acs=acs, board=board)
    acs.SPA(
        param,
        access_param=access_change,
        access_list=access_list,
        notification_param=notification_change,
        cpe_id=board.sw.tr69_cpe_id,
    )


SPA = moves.moved_function(set_parameter_attributes, "SPA", __name__)


def get_parameter_attributes(
    param: str,
    acs: ACS | None = None,
    board: CPE | None = None,
) -> list[dict[str, Any]]:  # pylint: disable=invalid-name
    """Perform TR-069 RPC call GetParameterAttributes.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Execute GetParameterAttributes RPC
        - Execute GPA RPC
        - Execute GPA on param

    :param param: name of the parameter
    :type param: str
    :param acs: ACS server that will perform GPV
    :type acs: ACS | None
    :param board: CPE on which to perform TR-069 method
    :type board: CPE | None
    :return: list of dictionary with keys Name, AccessList, Notification
        indicating the attributes of the parameter
    :rtype: list[dict[str, Any]]
    """
    _check_devices(acs=acs, board=board)
    return acs.GPA(param, cpe_id=board.sw.tr69_cpe_id)


GPA = moves.moved_function(get_parameter_attributes, "GPA", __name__)


def add_object(
    object_name: str,
    parameter_key: str | None = None,
    acs: ACS | None = None,
    board: CPE | None = None,
) -> AddObjectResponse:
    """Perform TR-069 RPC call AddObject.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Execute AddObject RPC by providing parameter name
        - Add the [] entry by Add object from ACS
        - Add new instance to [] by Add object from ACS

    Usage:

    .. code-block:: python

        out = add_object(object_name)
        instance_number = out.instance_number
        response = out.response

    :param object_name: Name of the object to be added
    :type object_name: str
    :param parameter_key: The optional string value to set the ParameterKey.
    :type parameter_key: str | None
    :param acs: ACS server that will perform GPV
    :type acs: ACS | None
    :param board: CPE on which to perform TR-069 method
    :type board: CPE | None
    :return: AddObjectResponse with values response & instance_number
    :rtype: AddObjectResponse
    """
    _check_devices(acs=acs, board=board)
    if parameter_key:
        return AddObjectResponse(
            acs.AddObject(
                object_name,
                param_key=parameter_key,
                cpe_id=board.sw.tr69_cpe_id,
            ),
            object_name,
        )
    return AddObjectResponse(
        acs.AddObject(object_name, cpe_id=board.sw.tr69_cpe_id),
        object_name,
    )


def del_object(
    object_name: str,
    parameter_key: str | None = None,
    acs: ACS | None = None,
    board: CPE | None = None,
) -> int:
    """Perform TR-069 RPC call DeleteObject.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Delete the [] entry using Delete Object RPC from ACS
        - Login to ACS and delete
        - Execute DeleteObject RPC from ACS

    Usage:

    .. code-block:: python

        del_object(object_name)

    :param object_name: Name of the object to be added
    :type object_name: str
    :param parameter_key: The optional string value to set the ParameterKey.
    :type parameter_key: str | None
    :param acs: ACS server that will perform GPV
    :type acs: ACS | None
    :param board: CPE on which to perform TR-069 method
    :type board: CPE | None
    :return: delete object response value
    :rtype: int
    """
    _check_devices(acs=acs, board=board)
    if parameter_key:
        result = acs.DelObject(
            object_name,
            param_key=parameter_key,
            cpe_id=board.sw.tr69_cpe_id,
        )
    else:
        result = acs.DelObject(object_name, cpe_id=board.sw.tr69_cpe_id)
    return int(result[0]["value"])


def factory_reset(acs: ACS | None = None, board: CPE | None = None) -> None:
    """Perform TR-069 FactoryReset RPC call and guarantee the board is back online.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Factory Reset the DUT
        - Perform factory reset on the CPE

    Usage:

    .. code-block:: python

        factory_reset()

    :param acs: ACS server that will perform GPV
    :type acs: ACS | None
    :param board: CPE on which to perform TR-069 method
    :type board: CPE | None
    :raises UseCaseFailure: in case of board not online after reset
    """
    _check_devices(acs=acs, board=board)
    acs.FactoryReset(cpe_id=board.sw.tr69_cpe_id)
    wait_for_board_boot_start()
    status = is_board_online_after_reset()
    if not status:
        msg = "Board not Online after Factory Reset through ACS"
        raise UseCaseFailure(msg)


def get_parameter_names(
    param_path: str,
    next_level: bool,
    acs: ACS | None = None,
    board: CPE | None = None,
    timeout: int = 120,
) -> list[dict[str, Any]]:
    """Perform TR-069 RPC call GetParametersName.

    .. hint:: This Use Case implements statements from the test suite such as:

        - GPN of []
        - GetParameterNames RPC

    :param param_path: name of the parameter
    :type param_path: str
    :param next_level: If false, the response MUST contain the Parameter or
        Object whose name exactly matches the ParameterPath argument
    :type next_level: bool
    :param acs: ACS server that will perform GPV
    :type acs: ACS | None
    :param board: CPE on which to perform TR-069 method
    :type board: CPE | None
    :param timeout: Timeout for the GPN RPC call, defaults to 120
    :type timeout: int
    :return: list of dictionary with key, type and value
    :rtype: list[dict[str, Any]]
    """
    _check_devices(acs=acs, board=board)
    return acs.GPN(
        param=param_path,
        next_level=next_level,
        cpe_id=board.sw.tr69_cpe_id,
        timeout=timeout,
    )


GPN = moves.moved_function(get_parameter_names, "GPN", __name__)


def reboot(
    command_key: str,
    acs: ACS | None = None,
    board: CPE | None = None,
) -> None:  # pylint: disable=invalid-name
    """Perform TR-069 RPC call Reboot.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Perform reboot on DUT
        - Reboot the DUT
        - Execute Reboot RPC from ACS

    :param command_key: The string to return in the CommandKey element of the
        InformStruct when the CPE reboots and calls the Inform method.
    :type command_key: str
    :param acs: ACS server that will perform GPV
    :type acs: ACS | None
    :param board: CPE on which to perform TR-069 method
    :type board: CPE | None
    :raises UseCaseFailure: in case of board not online after reset
    """
    _check_devices(acs=acs, board=board)
    acs.Reboot(CommandKey=command_key, cpe_id=board.sw.tr69_cpe_id)
    wait_for_board_boot_start()
    status = is_board_online_after_reset()
    if not status:
        msg = "Board not Online after Reboot through ACS"
        raise UseCaseFailure(msg)


# Reboot
Reboot = moves.moved_function(reboot, "Reboot", __name__)


def schedule_inform(
    delay_seconds: int,
    command_key: str,
    acs: ACS | None = None,
    board: CPE | None = None,
) -> None:
    """Perform TR-069 RPC call ScheduleInform.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Execute ScheduleInform RPC from ACS

    :param delay_seconds: The number of seconds from the time this method is called
        to the time the CPE is requested to initiate a one-time Inform method call
    :type delay_seconds: int
    :param command_key: The string to return in the CommandKey element of the
        InformStruct when the CPE calls the Inform method.
    :type command_key: str
    :param acs: ACS server that will perform GPV
    :type acs: ACS | None
    :param board: CPE on which to perform TR-069 method
    :type board: CPE | None
    """
    _check_devices(acs=acs, board=board)
    acs.ScheduleInform(
        CommandKey=command_key,
        DelaySeconds=delay_seconds,
        cpe_id=board.sw.tr69_cpe_id,
    )


ScheduleInform = moves.moved_function(schedule_inform, "ScheduleInform", __name__)


def get_rpc_methods(
    acs: ACS | None = None,
    board: CPE | None = None,
) -> list[str]:
    """Perform TR-069 RPC call GetRPCMethods.

    :param acs: ACS server that will perform GPV
    :type acs: ACS | None
    :param board: CPE on which to perform TR-069 method
    :type board: CPE | None
    :return: list of all the RPC methods
    :rtype: List[str]
    """
    _check_devices(acs=acs, board=board)
    return acs.GetRPCMethods(cpe_id=board.sw.tr69_cpe_id)[0]["value"].split(" ")


GetRPCMethods = moves.moved_function(get_rpc_methods, "GetRPCMethods", __name__)


def download(  # pylint: disable=too-many-arguments  # noqa: PLR0913
    url: str,
    filetype: str,
    targetfilename: str,
    filesize: int,
    username: str,
    password: str,
    commandkey: str,
    delayseconds: int,
    successurl: str,
    failureurl: str,
    acs: ACS | None = None,
    board: CPE | None = None,
) -> list[dict[str, Any]]:
    """Perform TR-069 RPC call Download.

    This method is used by the ACS to cause the CPE to download a specified file
    from the designated location.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Execute Download RPC via ACS


    :param url: specifies the source file location. HTTP and HTTPS transports
        MUST be supported
    :type url: str
    :param filetype: An integer followed by a space followed by the file type
        description. Only the following values are currently defined for the
        FileType argument:
        1. Firmware Upgrade Image
        2. Web Content
        3. Vendor Configuration File
        4. Tone File
        5. Ringer File
        6. Stored Firmware Image
    :type filetype: str
    :param targetfilename: The name of the file to be used on the target file system.
    :type targetfilename: str
    :param filesize: The size of the file to be downloaded in bytes
    :type filesize: int
    :param username: Username to be used by the CPE to authenticate with the file server
    :type username: str
    :param password: Password to be used by the CPE to authenticate with the file server
    :type password: str
    :param commandkey: The string the CPE uses to refer to a particular download
    :type commandkey: str
    :param delayseconds: This argument has different meanings for Unicast and
        Multicast downloads
    :type delayseconds: int
    :param successurl: this argument contains the URL, the CPE should redirect
        the user's browser to if the download completes successfully
    :type successurl: str
    :param failureurl: this argument contains the URL, the CPE should redirect
        the user's browser to if the download completes unsuccessfully
    :type failureurl: str
    :param acs: ACS server that will perform GPV
    :type acs: ACS | None
    :param board: CPE on which to perform TR-069 method
    :type board: CPE | None
    :return: Return the list of Dictionary containing the keys Status,StartTime
        and CompleteTime
    :rtype: list[dict[str, Any]]
    """
    _check_devices(acs=acs, board=board)
    return acs.Download(
        url,
        filetype,
        targetfilename,
        filesize,
        username,
        password,
        commandkey,
        delayseconds,
        successurl,
        failureurl,
        cpe_id=board.sw.tr69_cpe_id,
    )


Download = moves.moved_function(download, "Download", __name__)


def get_ccsptr069_pid(board: CPE) -> int | None:
    """Return the CcspTr069PaSsp process id.

    :param board: The CPE device instance
    :type board: CPE
    :return: The pid of CcspTr069PaSsp process
    :rtype: int | None
    """
    return next(
        (
            command["pid"]
            for command in board.sw.get_running_processes()
            if isinstance(command, dict) and command["cmd"] == "CcspTr069PaSsp"
        ),
        None,
    )


def restart_tr069_agent(board: CPE) -> None:
    """Restart the TR-069 agent by killing the process based on the PID.

    :param board: CPE device instance
    :type board: CPE
    :raises ValueError: when the CcspTr069PaSsp is not alive
    """
    if (pid := get_ccsptr069_pid(board)) is None:
        msg = "CcspTr069PaSsp process is not alive"
        raise ValueError(msg)
    # killing the process restarts the Tr069 agent after 300s
    board.sw.kill_process_immediately(pid)
