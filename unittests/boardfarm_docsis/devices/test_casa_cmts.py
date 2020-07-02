#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

import pytest
from boardfarm.lib.regexlib import ValidIpv4AddressRegex
from boardfarm_docsis.devices.casa_cmts import CasaCMTS

out_str_zero_ip = '''show cable modem 342c.c454.2ed2
    MAC Address    IP Address      US         DS       MAC         Prim RxPwr Timing Num  BPI
                                   Intf       Intf     Status      Sid  (dB)  Offset CPEs Enb
    342c.c454.2ed2 0.0.0.0         0/2.0/0    3/0/0    offline     0    0.0   0      0    no
    online cm 0 ; offline cm 1 ; ranging cm 0
'''

out_str_valid_ip = '''show cable modem 342c.c454.2ed2
    MAC Address    IP Address      US         DS       MAC         Prim RxPwr Timing Num  BPI
                                   Intf       Intf     Status      Sid  (dB)  Offset CPEs Enb
    342c.c454.2ed2 10.15.1.78      0/2.0/0    3/0/0    offline     0    0.0   0      0    no
    online cm 1 ; offline cm 0 ; ranging cm 0
'''

out_str_no_ip = '''show cable modem 342c.c454.2ed2
    MAC Address    IP Address      US         DS       MAC         Prim RxPwr Timing Num  BPI
                                   Intf       Intf     Status      Sid  (dB)  Offset CPEs Enb
    342c.c454.2ed2                 0/2.0/0    3/0/0    offline     0    0.0   0      0    no
    online cm 0 ; offline cm 1 ; ranging cm 0
'''


# this could be moved elsewhere as it tests the base class... but for
# the moment....
@pytest.mark.parametrize("test_input,expected",
                         [("52:54:00:7d:3b:39", "5254.007d.3b39"),
                          ("80:CE:62:1A:52:9C", "80ce.621a.529c"),
                          ("ff:ff:ff:ff:ff:ff", "ffff.ffff.ffff"),
                          ("11:11:11:11:11:11", "1111.1111.1111")])
def test_get_cm_mac_cmts_format_pass(mocker, test_input, expected):
    """Tests the mac address conversion function"""
    self = mocker.Mock()
    assert CasaCMTS.get_cm_mac_cmts_format(self, test_input) == expected


@pytest.mark.parametrize("cmts_ouput, cmmac,expected_ip",
                         [(out_str_zero_ip, "342c.c454.2ed2", "None"),
                          (out_str_valid_ip, "342c.c454.2ed2", "10.15.1.78"),
                          (out_str_no_ip, "342c.c454.2ed2", 'None')])
def test_get_cmip(mocker, cmts_ouput, cmmac, expected_ip):
    """Tests different casa output scenarios"""
    def _scan_output(cmmac, cmts_ouput_str):
        return re.search(cmmac + r'\s+(' + ValidIpv4AddressRegex + '+)',
                         cmts_ouput_str)

    mocker.patch.object(CasaCMTS, '__init__', return_value=None, autospec=True)
    mocker.patch.object(CasaCMTS, 'sendline', autospec=True)
    mocker.patch.object(CasaCMTS, 'expect', autospec=True)
    casa = CasaCMTS()
    casa.match = _scan_output(cmmac, cmts_ouput)
    assert casa.get_cmip(cmmac) == expected_ip


# Testset for the method CASA is_cm_online
is_cm_online_offline = '''MAC Address    IP Address      US         DS       MAC         Prim RxPwr Timing Num  BPI
                               Intf       Intf     Status      Sid  (dB)  Offset CPEs Enb
6802.b802.ca84 0.0.0.0         1/1.1/0    5/0/0    offline     0    0.0   0      0    no
online cm 0 ; offline cm 1 ; ranging cm 0
'''

is_cm_online_online = '''MAC Address    IP Address      US         DS       MAC         Prim RxPwr Timing Num  BPI
                               Intf       Intf     Status      Sid  (dB)  Offset CPEs Enb
6802.b802.c43c 10.15.78.167    1/1.1/0*   5/0/0*   online      7432 0.0   1335   3    no
               2001:730:1f:60b::c:98
online cm 1 ; offline cm 0 ; ranging cm 0
'''

is_cm_online_online_d = '''MAC Address    IP Address      US         DS       MAC         Prim RxPwr Timing Num  BPI
                               Intf       Intf     Status      Sid  (dB)  Offset CPEs Enb
6802.b802.c43c 10.15.78.167    1/1.1/0*   5/0/0*   online(d)  7432 0.0   1335   3    yes
               2001:730:1f:60b::c:98
online cm 1 ; offline cm 0 ; ranging cm 0
'''

is_cm_online_online_pkd = '''MAC Address    IP Address      US         DS       MAC         Prim RxPwr Timing Num  BPI
                               Intf       Intf     Status      Sid  (dB)  Offset CPEs Enb
6802.b802.c43c 10.15.78.167    1/1.1/0*   5/0/0*   online(pkd) 7432 0.0   1335   3    yes
               2001:730:1f:60b::c:98
online cm 1 ; offline cm 0 ; ranging cm 0
'''

is_cm_online_online_pt = '''MAC Address    IP Address      US         DS       MAC         Prim RxPwr Timing Num  BPI
                               Intf       Intf     Status      Sid  (dB)  Offset CPEs Enb
6802.b802.c43c 10.15.78.167    1/1.1/0*   5/0/0*   online(pt)  7432 0.0   1335   3    yes
               2001:730:1f:60b::c:98
online cm 1 ; offline cm 0 ; ranging cm 0
'''

is_cm_online_online_ptd = '''MAC Address    IP Address      US         DS       MAC         Prim RxPwr Timing Num  BPI
                               Intf       Intf     Status      Sid  (dB)  Offset CPEs Enb
6802.b802.c43c 10.15.78.167    1/1.1/0*   5/0/0*   online(ptd) 7432 0.0   1335   3    yes
               2001:730:1f:60b::c:98
online cm 1 ; offline cm 0 ; ranging cm 0
'''

is_cm_online_online_pk = '''MAC Address    IP Address      US         DS       MAC         Prim RxPwr Timing Num  BPI
                               Intf       Intf     Status      Sid  (dB)  Offset CPEs Enb
6802.b802.c43c 10.15.78.167    1/1.1/0*   5/0/0*   online(pk)  7432 0.0   1335   3    yes
               2001:730:1f:60b::c:98
online cm 1 ; offline cm 0 ; ranging cm 0
'''

combinations = [(False, False, False), (False, False, True),
                (False, True, False), (False, True, True),
                (True, False, False), (True, False, True), (True, True, False),
                (True, True, True)]


@pytest.mark.parametrize("cmts_ouput, params_combination, partial, result",
                         [(is_cm_online_offline, combinations[0], 0, False),
                          (is_cm_online_online, combinations[0], 0, False),
                          (is_cm_online_online_d, combinations[0], 0, False),
                          (is_cm_online_online_pkd, combinations[0], 0, False),
                          (is_cm_online_online_pt, combinations[0], 0, True),
                          (is_cm_online_online_ptd, combinations[0], 0, False),
                          (is_cm_online_online_pk, combinations[0], 0, True),
                          (is_cm_online_offline, combinations[0], 1, False),
                          (is_cm_online_online, combinations[0], 1, False),
                          (is_cm_online_online_d, combinations[0], 1, False),
                          (is_cm_online_online_pkd, combinations[0], 1, False),
                          (is_cm_online_online_pt, combinations[0], 1, False),
                          (is_cm_online_online_ptd, combinations[0], 1, False),
                          (is_cm_online_online_pk, combinations[0], 1, False),
                          (is_cm_online_offline, combinations[1], 0, False),
                          (is_cm_online_online, combinations[1], 0, False),
                          (is_cm_online_online_d, combinations[1], 0, False),
                          (is_cm_online_online_pkd, combinations[1], 0, True),
                          (is_cm_online_online_pt, combinations[1], 0, True),
                          (is_cm_online_online_ptd, combinations[1], 0, True),
                          (is_cm_online_online_pk, combinations[1], 0, True),
                          (is_cm_online_offline, combinations[1], 1, False),
                          (is_cm_online_online, combinations[1], 1, False),
                          (is_cm_online_online_d, combinations[1], 1, False),
                          (is_cm_online_online_pkd, combinations[1], 1, False),
                          (is_cm_online_online_pt, combinations[1], 1, False),
                          (is_cm_online_online_ptd, combinations[1], 1, False),
                          (is_cm_online_online_pk, combinations[1], 1, False),
                          (is_cm_online_offline, combinations[2], 0, False),
                          (is_cm_online_online, combinations[2], 0, False),
                          (is_cm_online_online_d, combinations[2], 0, False),
                          (is_cm_online_online_pkd, combinations[2], 0, False),
                          (is_cm_online_online_pt, combinations[2], 0, True),
                          (is_cm_online_online_ptd, combinations[2], 0, False),
                          (is_cm_online_online_pk, combinations[2], 0, True),
                          (is_cm_online_offline, combinations[2], 1, False),
                          (is_cm_online_online, combinations[2], 1, False),
                          (is_cm_online_online_d, combinations[2], 1, False),
                          (is_cm_online_online_pkd, combinations[2], 1, False),
                          (is_cm_online_online_pt, combinations[2], 1, True),
                          (is_cm_online_online_ptd, combinations[2], 1, False),
                          (is_cm_online_online_pk, combinations[2], 1, True),
                          (is_cm_online_offline, combinations[3], 0, False),
                          (is_cm_online_online, combinations[3], 0, False),
                          (is_cm_online_online_d, combinations[3], 0, False),
                          (is_cm_online_online_pkd, combinations[3], 0, True),
                          (is_cm_online_online_pt, combinations[3], 0, True),
                          (is_cm_online_online_ptd, combinations[3], 0, True),
                          (is_cm_online_online_pk, combinations[3], 0, True),
                          (is_cm_online_offline, combinations[3], 1, False),
                          (is_cm_online_online, combinations[3], 1, False),
                          (is_cm_online_online_d, combinations[3], 1, False),
                          (is_cm_online_online_pkd, combinations[3], 1, True),
                          (is_cm_online_online_pt, combinations[3], 1, True),
                          (is_cm_online_online_ptd, combinations[3], 1, True),
                          (is_cm_online_online_pk, combinations[3], 1, True),
                          (is_cm_online_offline, combinations[4], 0, False),
                          (is_cm_online_online, combinations[4], 0, True),
                          (is_cm_online_online_d, combinations[4], 0, False),
                          (is_cm_online_online_pkd, combinations[4], 0, False),
                          (is_cm_online_online_pt, combinations[4], 0, True),
                          (is_cm_online_online_ptd, combinations[4], 0, False),
                          (is_cm_online_online_pk, combinations[4], 0, True),
                          (is_cm_online_offline, combinations[4], 1, False),
                          (is_cm_online_online, combinations[4], 1, False),
                          (is_cm_online_online_d, combinations[4], 1, False),
                          (is_cm_online_online_pkd, combinations[4], 1, False),
                          (is_cm_online_online_pt, combinations[4], 1, False),
                          (is_cm_online_online_ptd, combinations[4], 1, False),
                          (is_cm_online_online_pk, combinations[4], 1, False),
                          (is_cm_online_offline, combinations[5], 0, False),
                          (is_cm_online_online, combinations[5], 0, True),
                          (is_cm_online_online_d, combinations[5], 0, True),
                          (is_cm_online_online_pkd, combinations[5], 0, True),
                          (is_cm_online_online_pt, combinations[5], 0, True),
                          (is_cm_online_online_ptd, combinations[5], 0, True),
                          (is_cm_online_online_pk, combinations[5], 0, True),
                          (is_cm_online_offline, combinations[5], 1, False),
                          (is_cm_online_online, combinations[5], 1, False),
                          (is_cm_online_online_d, combinations[5], 1, False),
                          (is_cm_online_online_pkd, combinations[5], 1, False),
                          (is_cm_online_online_pt, combinations[5], 1, False),
                          (is_cm_online_online_ptd, combinations[5], 1, False),
                          (is_cm_online_online_pk, combinations[5], 1, False),
                          (is_cm_online_offline, combinations[6], 0, False),
                          (is_cm_online_online, combinations[6], 0, True),
                          (is_cm_online_online_d, combinations[6], 0, False),
                          (is_cm_online_online_pkd, combinations[6], 0, False),
                          (is_cm_online_online_pt, combinations[6], 0, True),
                          (is_cm_online_online_ptd, combinations[6], 0, False),
                          (is_cm_online_online_pk, combinations[6], 0, True),
                          (is_cm_online_offline, combinations[6], 1, False),
                          (is_cm_online_online, combinations[6], 1, True),
                          (is_cm_online_online_d, combinations[6], 1, False),
                          (is_cm_online_online_pkd, combinations[6], 1, False),
                          (is_cm_online_online_pt, combinations[6], 1, True),
                          (is_cm_online_online_ptd, combinations[6], 1, False),
                          (is_cm_online_online_pk, combinations[6], 1, True),
                          (is_cm_online_offline, combinations[7], 0, False),
                          (is_cm_online_online, combinations[7], 0, True),
                          (is_cm_online_online_d, combinations[7], 0, True),
                          (is_cm_online_online_pkd, combinations[7], 0, True),
                          (is_cm_online_online_pt, combinations[7], 0, True),
                          (is_cm_online_online_ptd, combinations[7], 0, True),
                          (is_cm_online_online_pk, combinations[7], 0, True),
                          (is_cm_online_offline, combinations[7], 1, False),
                          (is_cm_online_online, combinations[7], 1, True),
                          (is_cm_online_online_d, combinations[7], 1, True),
                          (is_cm_online_online_pkd, combinations[7], 1, True),
                          (is_cm_online_online_pt, combinations[7], 1, True),
                          (is_cm_online_online_ptd, combinations[7], 1, True),
                          (is_cm_online_online_pk, combinations[7], 1, True)])
def test_is_cm_online(mocker, cmts_ouput, params_combination, partial, result):
    mocker.patch.object(CasaCMTS, '__init__', return_value=None, autospec=True)
    mocker.patch.object(CasaCMTS, 'sendline', autospec=True)
    mocker.patch.object(CasaCMTS,
                        'check_output',
                        return_value=cmts_ouput,
                        autospec=True)
    mocker.patch.object(CasaCMTS, 'expect', autospec=True)
    mocker.patch.object(CasaCMTS,
                        'check_PartialService',
                        return_value=partial,
                        autospec=True)
    casa = CasaCMTS()
    assert casa.is_cm_online(*params_combination) == result
