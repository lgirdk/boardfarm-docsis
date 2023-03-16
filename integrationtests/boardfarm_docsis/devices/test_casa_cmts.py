#!/usr/bin/env python
import re

import pytest
from boardfarm.lib.regexlib import ValidIpv4AddressRegex

from boardfarm_docsis.devices.casa_cmts import CasaCMTS

out_str_zero_ip = """show cable modem 342c.c454.2ed2
    MAC Address    IP Address      US         DS       MAC         Prim RxPwr Timing Num  BPI
                                   Intf       Intf     Status      Sid  (dB)  Offset CPEs Enb
    342c.c454.2ed2 0.0.0.0         0/2.0/0    3/0/0    offline     0    0.0   0      0    no
    online cm 0 ; offline cm 1 ; ranging cm 0
"""
out_str_valid_ip = """show cable modem 342c.c454.2ed2
    MAC Address    IP Address      US         DS       MAC         Prim RxPwr Timing Num  BPI
                                   Intf       Intf     Status      Sid  (dB)  Offset CPEs Enb
    342c.c454.2ed2 10.15.1.78      0/2.0/0    3/0/0    offline     0    0.0   0      0    no
    online cm 1 ; offline cm 0 ; ranging cm 0
"""
out_str_no_ip = """show cable modem 342c.c454.2ed2
    MAC Address    IP Address      US         DS       MAC         Prim RxPwr Timing Num  BPI
                                   Intf       Intf     Status      Sid  (dB)  Offset CPEs Enb
    342c.c454.2ed2                 0/2.0/0    3/0/0    offline     0    0.0   0      0    no
    online cm 0 ; offline cm 1 ; ranging cm 0
"""


# this could be moved elsewhere as it tests the base class... but for
# the moment....
@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("52:54:00:7d:3b:39", "5254.007d.3b39"),
        ("80:CE:62:1A:52:9C", "80ce.621a.529c"),
        ("ff:ff:ff:ff:ff:ff", "ffff.ffff.ffff"),
        ("11:11:11:11:11:11", "1111.1111.1111"),
    ],
)
def test_get_cm_mac_cmts_format_pass(mocker, test_input, expected):
    """Tests the mac address conversion function"""
    self = mocker.Mock()
    assert CasaCMTS.get_cm_mac_cmts_format(self, test_input) == expected


@pytest.mark.parametrize(
    "cmts_ouput, cmmac,expected_ip",
    [
        (out_str_zero_ip, "342c.c454.2ed2", "None"),
        (out_str_valid_ip, "342c.c454.2ed2", "10.15.1.78"),
        (out_str_no_ip, "342c.c454.2ed2", "None"),
    ],
)
def test_get_cmip(mocker, cmts_ouput, cmmac, expected_ip):
    """Tests different casa output scenarios"""

    def _scan_output(cmmac, cmts_ouput_str):
        return re.search(cmmac + r"\s+(" + ValidIpv4AddressRegex + "+)", cmts_ouput_str)

    mocker.patch.object(CasaCMTS, "__init__", return_value=None, autospec=True)
    mocker.patch.object(CasaCMTS, "sendline", autospec=True)
    mocker.patch.object(CasaCMTS, "expect", autospec=True)
    casa = CasaCMTS()
    casa.match = _scan_output(cmmac, cmts_ouput)
    assert casa.get_cmip(cmmac) == expected_ip
