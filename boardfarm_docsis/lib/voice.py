import datetime
import re

import pexpect
from boardfarm.lib.SnmpHelper import get_mib_oid, snmp_v2
from boardfarm_lgi.tests.lib.lgi_lib import mibstring2dict


def get_tone_time(tones_file, out, tone):
    """"To verify dial tone based on country after off hook or call

    :param tones_file: tones_file with all tone metrics
    :type tones_file: dict
    :param out: basic_call output
    :type out: string
    :param tone: name of the tone,defaults to dial_tone. Could take values
    like ring_tone,busy_tone etc.
    :type tone: string
    :rval: timediff
    :rtype: int
    """
    compansation = tones_file[tone]["compansation"]
    signal_num = tones_file[tone]["signal_num"]
    assert re.search(r"TONE gain compansation\s" + str(compansation), out), "No tone"
    time_start = re.findall(
        r"([Mon|Tue|Wed|Thu|Fri|Sat|Sun].*)\[ERROR\].*Started Signal\["
        + str(signal_num)
        + r"\]",
        out,
    )[0]
    time_stop = re.findall(
        r"([Mon|Tue|Wed|Thu|Fri|Sat|Sun].*)\[ERROR\].*Stopping Signal\["
        + str(signal_num)
        + r"\]",
        out,
    )[-1]
    date_time_obj_start = datetime.datetime.strptime(
        time_start, "%a %b %d %H:%M:%S %Y "
    )
    date_time_obj_stop = datetime.datetime.strptime(time_stop, "%a %b %d %H:%M:%S %Y ")
    time_diff = date_time_obj_stop - date_time_obj_start
    return time_diff.total_seconds()


def check_peer_registration(board, num_list, sipserver):
    """
    Method to validate the peer registration status.
    :param board: The board object
    :type board: string
    :param num_list: The users corresponding to MTA Lines
    :type num_list: list
    :param sipserver: The sipserver object
    :type sipserver: string
    :return: True if both the users in sip server are registered
    :rtype: Boolean
    """
    mta_ip = board.get_interface_ipaddr(board.mta_iface)
    return_list = [
        True if sipserver.peer_reg_status(user, mta_ip) == "Registered" else False
        for user in num_list
    ]

    return all(return_list)


def fetch_mta_interfaces(wan, mta_ip):
    """
    To fetch the mta interfaces using snmpwalk on the Mib 'ifDescr'.
    :param wan: The wan object
    :type wan: boardfarm.devices.DebianBox_AFTR
    :param mta_ip: The mta_ip
    :type mta_list: string
    :return: list containing the mta int indexes
    :rtype: list
    """
    snmp_output = snmp_v2(
        wan,
        mta_ip,
        "ifEntry",
        index=2,
        walk_cmd="awk /{}/".format(get_mib_oid("ifDescr")),
    )
    out_dict = mibstring2dict(snmp_output, "ifDescr")
    index_list = []
    for k, v in out_dict.items():
        if v == "Voice Over Cable Interface":
            index_list.append(int(k.split(".")[-1]))
    return index_list


def cleanup_voice_prompt(self, devices):
    """This method to cleanup container's (LAN/LAN2 and softphone) prompt
    :param self: self for container object
    :param devices: lan or softphone
    :type device: list of container Object
    :return: boolean value based on result_result list
    :rtype: Boolean
    """
    result = []
    for dev in devices:
        for _ in range(2):
            dev.sendline()
            idx = dev.expect([pexpect.TIMEOUT, ">>>"] + dev.prompt, timeout=5)
            if idx == 0:
                dev.sendcontol("c")
                dev.expect(dev.prompt, timeout=5)
            elif idx == 1:
                if dev in [self.dev.lan, self.dev.lan2]:
                    dev.sendline("set.close()")
                    dev.sendline("exit()")
                    dev.expect(dev.prompt, timeout=5)
                else:
                    dev.sendline("q")
                    dev.expect(dev.prompt, timeout=5)
            else:
                result.append(True)
                break
        else:
            result.append(False)
    return all(result)
