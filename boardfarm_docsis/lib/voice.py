import datetime
import re


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
    compansation = tones_file[tone]['compansation']
    signal_num = tones_file[tone]['signal_num']
    assert re.search(r"TONE gain compansation\s"+str(compansation), out), \
    "No tone"
    time_start = re.findall(
        r"([Mon|Tue|Wed|Thu|Fri|Sat|Sun].*)\[ERROR\].*Started Signal\[" +
        str(signal_num) + r"\]", out)[0]
    time_stop = re.findall(
        r"([Mon|Tue|Wed|Thu|Fri|Sat|Sun].*)\[ERROR\].*Stopping Signal\[" +
        str(signal_num) + r"\]", out)[-1]
    date_time_obj_start = datetime.datetime.strptime(time_start,
                                                     '%a %b %d %H:%M:%S %Y ')
    date_time_obj_stop = datetime.datetime.strptime(time_stop,
                                                    '%a %b %d %H:%M:%S %Y ')
    time_diff = date_time_obj_stop - date_time_obj_start
    return time_diff.total_seconds()


def check_peer_registration(board, num_list, sipserver):
    '''
    Method to validate the peer registration status.
    :param board: The board object
    :type board: string
    :param num_list: The users corresponding to MTA Lines
    :type num_list: list
    :param sipserver: The sipserver object
    :type sipserver: string
    :return: True if both the users in sip server are registered
    :rtype: Boolean
    '''
    mta_ip = board.get_interface_ipaddr(board.mta_iface)
    return_list = [
        True
        if sipserver.peer_reg_status(user, mta_ip) == "Registered" else False
        for user in num_list
    ]

    return all(return_list)
