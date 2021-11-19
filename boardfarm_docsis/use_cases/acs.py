import logging

import pexpect
from boardfarm.exceptions import PexpectErrorTimeout, TR069FaultCode
from boardfarm.lib.common import retry
from boardfarm.lib.DeviceManager import get_device_by_name
from termcolor import colored

logger = logging.getLogger("bft")


def is_dut_online_on_acs() -> bool:
    """Checks if the DUT is online on acs.

    :return: True if devices is registered with acs and GPV
    is successful for Device.DeviceInfo.SoftwareVersion else false
    :rtype: bool
    """
    board = get_device_by_name("board")
    acs_server = get_device_by_name("acs_server")
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
            return bool(acs_server.GPV("Device.DeviceInfo.SoftwareVersion"))
        except TR069FaultCode as err:
            msg = f"\n\nFailed to get DeviceInfo.SoftwareVersion due to {err} retrying"
            logger.error(colored(msg, color="red", attrs=["bold"]))
    return False
