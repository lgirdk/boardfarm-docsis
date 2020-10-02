#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from boardfarm_docsis.devices.arris_cmts import ArrisCMTS

is_cm_online_offline = """Jul  2 15:33:36


"""

is_cm_online_DhcpV4Done = """
Jul  2 15:42:54


15/15-1/6       CM 342c.c454.2f0b (COMPAL_CH7465) D1.0 State=DhcpV4Done D1.0/atdma PrimSID=14023 FiberNode= FN2
Cable-Mac= 2,  mCMsg = 1   mDSsg = 1   mUSsg = 1, RCS=0x00000010 TCS=0x00000007
Timing Offset=23296    Rec Power= 2.00 dBmV Proto-Throttle=Normal
Uptime=  0 days  0:00:35 IPv4=10.11.0.49      cfg=dual-stack-dyn.cfg  FreqRng=STD
LB Policy=0  LB Group=0    Filter-Group CM-Down:0   CM-Up:0
Privacy=Initializing
em1x1Enable=Disabled  em1x1Operational=No  em1x1TotalDuration=   0 days 00:00:00
MDF Capability= N/A                  MDF Mode= N/A
u/d     SFID    SID State Sched    Tmin       Tmax     DFrms   DBytes    CRC    HCS  Slot/Channels
u    2083995  14023 Activ BE          0          0         9     1780      0      0    1/6
d    2083996  *4670 Activ             0          0         8     2872                 15/15
L2VPN per CM: (Disabled)
Current CPE=0, IPv4 Addr=0, IPv6 Addr=0          Max CPE=32, IPv4 Addr=0, IPv6 Addr=0
"""

is_cm_online_online_d = """Jul  2 15:33:36


15/15-1/6       CM 342c.c454.2f0b (COMPAL_CH7465) D3.0 State=Online-d   D1.1/atdma PrimSID=14336 FiberNode= FN2
Cable-Mac= 2,  mCMsg = 1   mDSsg = 1   mUSsg = 1  RCP_ID= 0x0010001018  RCC_Stat= 1023, RCS=0x0100000d TCS=0x0100000d
Timing Offset=23040    Rec Power= 1.75 dBmV Proto-Throttle=Normal dsPartialServMask=0x00000000 usPartialServMask=0x00000000
Uptime=  0 days  0:02:36 IPv4=10.11.0.49      cfg=dual-stack-dyn.cfg  FreqRng=EXT
LB Policy=4  LB Group=25167872    Filter-Group CM-Down:0   CM-Up:0
Privacy=Ready  Ver=BPI Plus  Authorized    DES56 Primary SAId=14336  Seq=1
em1x1Enable=Disabled  em1x1Operational=No  em1x1TotalDuration=   0 days 00:00:00
MDF Capability= GMAC Promiscuous(2)  MDF Mode= MDF Enabled(1)
u/d     SFID    SID State Sched    Tmin       Tmax     DFrms   DBytes    CRC    HCS  Slot/Channels
uB   2083945  14336 Activ BE          0          0         0        0      0      0    1/0-7
dB   2083946  *5150 Activ             0          0         0        0                 15/0-23
L2VPN per CM: (Disabled)
Current CPE=0, IPv4 Addr=0, IPv6 Addr=0          Max CPE=16, IPv4 Addr=32, IPv6 Addr=64
"""

is_cm_online_online_d_without_encr = """Jul  2 15:33:36


15/15-1/6       CM 342c.c454.2f0b (COMPAL_CH7465) D3.0 State=Online-d   D1.1/atdma PrimSID=14336 FiberNode= FN2
Cable-Mac= 2,  mCMsg = 1   mDSsg = 1   mUSsg = 1  RCP_ID= 0x0010001018  RCC_Stat= 1023, RCS=0x0100000d TCS=0x0100000d
Timing Offset=23040    Rec Power= 1.75 dBmV Proto-Throttle=Normal dsPartialServMask=0x00000000 usPartialServMask=0x00000000
Uptime=  0 days  0:02:36 IPv4=10.11.0.49      cfg=dual-stack-dyn.cfg  FreqRng=EXT
LB Policy=4  LB Group=25167872    Filter-Group CM-Down:0   CM-Up:0
Privacy=Disabled
em1x1Enable=Disabled  em1x1Operational=No  em1x1TotalDuration=   0 days 00:00:00
MDF Capability= GMAC Promiscuous(2)  MDF Mode= MDF Enabled(1)
u/d     SFID    SID State Sched    Tmin       Tmax     DFrms   DBytes    CRC    HCS  Slot/Channels
uB   2083945  14336 Activ BE          0          0         0        0      0      0    1/0-7
dB   2083946  *5150 Activ             0          0         0        0                 15/0-23
L2VPN per CM: (Disabled)
Current CPE=0, IPv4 Addr=0, IPv6 Addr=0          Max CPE=16, IPv4 Addr=32, IPv6 Addr=64
"""

is_cm_online_online_without_encr = """Jul  2 15:44:24


15/15-1/6       CM 342c.c454.2f0b (COMPAL_CH7465) D3.0 State=Operational D1.1/atdma PrimSID=14023 FiberNode= FN2
Cable-Mac= 2,  mCMsg = 1   mDSsg = 1   mUSsg = 1  RCP_ID= 0x0010001018  RCC_Stat= 8, RCS=0x0100000d TCS=0x0100000d
Timing Offset=23296    Rec Power= 1.75 dBmV Proto-Throttle=Normal dsPartialServMask=0x00000000 usPartialServMask=0x00000000
Uptime=  0 days  0:02:05 IPv4=10.11.0.49      cfg=dual-stack-dyn.cfg  FreqRng=EXT
LB Policy=4  LB Group=25167872    Filter-Group CM-Down:0   CM-Up:0
Privacy=Disabled
em1x1Enable=Disabled  em1x1Operational=No  em1x1TotalDuration=   0 days 00:00:00
MDF Capability= GMAC Promiscuous(2)  MDF Mode= MDF Enabled(1)
u/d     SFID    SID State Sched    Tmin       Tmax     DFrms   DBytes    CRC    HCS  Slot/Channels
uB   2083995  14023 Activ BE          0          0        26     7001      0      0    1/0-7
dB   2083996  *4670 Activ             0          0        18     4641                 15/0-23
L2VPN per CM: (Disabled)
Current CPE=2, IPv4 Addr=2, IPv6 Addr=2          Max CPE=16, IPv4 Addr=32, IPv6 Addr=64
 CPE(MTA)  342c.c454.2f0c Filter-Group:Up=0 Down=0 Proto-Throttle=Normal IPv4=10.12.0.31
 CPE       342c.c454.2f0d Filter-Group:Up=0 Down=0 Proto-Throttle=Normal IPv6=fe80::362c:c4ff:fe54:2f0d
+CPE       342c.c454.2f0d IPv6=2002:0:c4:2::e:c1
+CPE       342c.c454.2f0d IPv4=10.13.0.20
"""

is_cm_online_online_with_encr = """Jul  2 15:44:24


15/15-1/6       CM 342c.c454.2f0b (COMPAL_CH7465) D3.0 State=Operational D1.1/atdma PrimSID=14023 FiberNode= FN2
Cable-Mac= 2,  mCMsg = 1   mDSsg = 1   mUSsg = 1  RCP_ID= 0x0010001018  RCC_Stat= 8, RCS=0x0100000d TCS=0x0100000d
Timing Offset=23296    Rec Power= 1.75 dBmV Proto-Throttle=Normal dsPartialServMask=0x00000000 usPartialServMask=0x00000000
Uptime=  0 days  0:02:05 IPv4=10.11.0.49      cfg=dual-stack-dyn.cfg  FreqRng=EXT
LB Policy=4  LB Group=25167872    Filter-Group CM-Down:0   CM-Up:0
Privacy=Ready  Ver=BPI Plus  Authorized    DES56 Primary SAId=14023  Seq=1
em1x1Enable=Disabled  em1x1Operational=No  em1x1TotalDuration=   0 days 00:00:00
MDF Capability= GMAC Promiscuous(2)  MDF Mode= MDF Enabled(1)
u/d     SFID    SID State Sched    Tmin       Tmax     DFrms   DBytes    CRC    HCS  Slot/Channels
uB   2083995  14023 Activ BE          0          0        26     7001      0      0    1/0-7
dB   2083996  *4670 Activ             0          0        18     4641                 15/0-23
L2VPN per CM: (Disabled)
Current CPE=2, IPv4 Addr=2, IPv6 Addr=2          Max CPE=16, IPv4 Addr=32, IPv6 Addr=64
 CPE(MTA)  342c.c454.2f0c Filter-Group:Up=0 Down=0 Proto-Throttle=Normal IPv4=10.12.0.31
 CPE       342c.c454.2f0d Filter-Group:Up=0 Down=0 Proto-Throttle=Normal IPv6=fe80::362c:c4ff:fe54:2f0d
+CPE       342c.c454.2f0d IPv6=2002:0:c4:2::e:c1
+CPE       342c.c454.2f0d IPv4=10.13.0.20
"""

is_cm_online_online_impaired = """Jul  2 18:14:09


15/15-1/6       CM 342c.c454.2f0b (COMPAL_CH7465) D3.0 State=Operational D1.1/atdma PrimSID=12369 FiberNode= FN2
Cable-Mac= 2,  mCMsg = 1   mDSsg = 1   mUSsg = 1  RCP_ID= 0x0010001018  RCC_Stat= 9, RCS=0x0100000d TCS=0x0100000d
Timing Offset=22272    Rec Power= 1.75 dBmV Proto-Throttle=Normal dsPartialServMask=0x00000000 usPartialServMask=0x00000000
Uptime=  0 days  1:03:05 IPv4=10.11.0.49      cfg=cm-config-d41d8cd98f.cfg  FreqRng=EXT
LB Policy=4  LB Group=25167872    Filter-Group CM-Down:0   CM-Up:0
Privacy=Ready  Ver=BPI Plus  Authorized    DES56 Primary SAId=12369  Seq=1
em1x1Enable=Disabled  em1x1Operational=No  em1x1TotalDuration=   0 days 00:00:00
MDF Capability= GMAC Promiscuous(2)  MDF Mode= MDF Enabled(1)
u/d     SFID    SID State Sched    Tmin       Tmax     DFrms   DBytes    CRC    HCS  Slot/Channels
uB   2084201  12369 Activ BE          0  300000000         2      416      0      0    1/0-7 (impaired: 1/7)
dB   2084202   *802 Activ             0 1000000000         2      274                 15/0-23
uB   2084203  13359 Activ BE      12000          0         0        0      0      0    1/0-7 (impaired: 1/7)
uB   2084204  14825 Activ BE          0    4096000         0        0      0      0    1/0-7 (impaired: 1/7)
dB   2084205  *4374 Activ         12000          0         0        0                 15/0-23
dB   2084206  *4493 Activ             0   10240000         0        0                 15/0-23
L2VPN per CM: (Disabled)
Current CPE=1, IPv4 Addr=1, IPv6 Addr=2          Max CPE=16, IPv4 Addr=32, IPv6 Addr=64
 CPE       342c.c454.2f0d Filter-Group:Up=0 Down=0 Proto-Throttle=Normal IPv6=fe80::362c:c4ff:fe54:2f0d
+CPE       342c.c454.2f0d IPv6=2002:0:c4:2::e:c1
+CPE       342c.c454.2f0d IPv4=10.13.0.20
"""

combinations = [
    (False, False, False),
    (False, False, True),
    (False, True, False),
    (False, True, True),
    (True, False, False),
    (True, False, True),
    (True, True, False),
    (True, True, True),
]


@pytest.mark.parametrize(
    "cmts_ouput, params_combination, partial, result",
    [
        (is_cm_online_offline, combinations[0], 0, False),
        (is_cm_online_DhcpV4Done, combinations[0], 0, False),
        (is_cm_online_online_d_without_encr, combinations[0], 0, False),
        (is_cm_online_online_d, combinations[0], 0, False),
        (is_cm_online_online_without_encr, combinations[0], 0, False),
        (is_cm_online_online_with_encr, combinations[0], 0, True),
        (is_cm_online_offline, combinations[0], 1, False),
        (is_cm_online_DhcpV4Done, combinations[0], 1, False),
        (is_cm_online_online_d_without_encr, combinations[0], 1, False),
        (is_cm_online_online_d, combinations[0], 1, False),
        (is_cm_online_online_without_encr, combinations[0], 1, False),
        (is_cm_online_online_with_encr, combinations[0], 1, False),
        (is_cm_online_offline, combinations[1], 0, False),
        (is_cm_online_DhcpV4Done, combinations[1], 0, False),
        (is_cm_online_online_d_without_encr, combinations[1], 0, False),
        (is_cm_online_online_d, combinations[1], 0, True),
        (is_cm_online_online_without_encr, combinations[1], 0, False),
        (is_cm_online_online_with_encr, combinations[1], 0, True),
        (is_cm_online_offline, combinations[1], 1, False),
        (is_cm_online_DhcpV4Done, combinations[1], 1, False),
        (is_cm_online_online_d_without_encr, combinations[1], 1, False),
        (is_cm_online_online_d, combinations[1], 1, False),
        (is_cm_online_online_without_encr, combinations[1], 1, False),
        (is_cm_online_online_with_encr, combinations[1], 1, False),
        (is_cm_online_offline, combinations[2], 0, False),
        (is_cm_online_DhcpV4Done, combinations[2], 0, False),
        (is_cm_online_online_d_without_encr, combinations[2], 0, False),
        (is_cm_online_online_d, combinations[2], 0, False),
        (is_cm_online_online_without_encr, combinations[2], 0, False),
        (is_cm_online_online_with_encr, combinations[2], 0, True),
        (is_cm_online_offline, combinations[2], 1, False),
        (is_cm_online_DhcpV4Done, combinations[2], 1, False),
        (is_cm_online_online_d_without_encr, combinations[2], 1, False),
        (is_cm_online_online_d, combinations[2], 1, False),
        (is_cm_online_online_without_encr, combinations[2], 1, False),
        (is_cm_online_online_with_encr, combinations[2], 1, True),
        (is_cm_online_offline, combinations[3], 0, False),
        (is_cm_online_DhcpV4Done, combinations[3], 0, False),
        (is_cm_online_online_d_without_encr, combinations[3], 0, False),
        (is_cm_online_online_d, combinations[3], 0, True),
        (is_cm_online_online_without_encr, combinations[3], 0, False),
        (is_cm_online_online_with_encr, combinations[3], 0, True),
        (is_cm_online_offline, combinations[3], 1, False),
        (is_cm_online_DhcpV4Done, combinations[3], 1, False),
        (is_cm_online_online_d_without_encr, combinations[3], 1, False),
        (is_cm_online_online_d, combinations[3], 1, True),
        (is_cm_online_online_without_encr, combinations[3], 1, False),
        (is_cm_online_online_with_encr, combinations[3], 1, True),
        (is_cm_online_offline, combinations[4], 0, False),
        (is_cm_online_DhcpV4Done, combinations[4], 0, False),
        (is_cm_online_online_d_without_encr, combinations[4], 0, False),
        (is_cm_online_online_d, combinations[4], 0, False),
        (is_cm_online_online_without_encr, combinations[4], 0, True),
        (is_cm_online_online_with_encr, combinations[4], 0, True),
        (is_cm_online_offline, combinations[4], 1, False),
        (is_cm_online_DhcpV4Done, combinations[4], 1, False),
        (is_cm_online_online_d_without_encr, combinations[4], 1, False),
        (is_cm_online_online_d, combinations[4], 1, False),
        (is_cm_online_online_without_encr, combinations[4], 1, False),
        (is_cm_online_online_with_encr, combinations[4], 1, False),
        (is_cm_online_offline, combinations[5], 0, False),
        (is_cm_online_DhcpV4Done, combinations[5], 0, False),
        (is_cm_online_online_d_without_encr, combinations[5], 0, True),
        (is_cm_online_online_d, combinations[5], 0, True),
        (is_cm_online_online_without_encr, combinations[5], 0, True),
        (is_cm_online_online_with_encr, combinations[5], 0, True),
        (is_cm_online_offline, combinations[5], 1, False),
        (is_cm_online_DhcpV4Done, combinations[5], 1, False),
        (is_cm_online_online_d_without_encr, combinations[5], 1, False),
        (is_cm_online_online_d, combinations[5], 1, False),
        (is_cm_online_online_without_encr, combinations[5], 1, False),
        (is_cm_online_online_with_encr, combinations[5], 1, False),
        (is_cm_online_offline, combinations[6], 0, False),
        (is_cm_online_DhcpV4Done, combinations[6], 0, False),
        (is_cm_online_online_d_without_encr, combinations[6], 0, False),
        (is_cm_online_online_d, combinations[6], 0, False),
        (is_cm_online_online_without_encr, combinations[6], 0, True),
        (is_cm_online_online_with_encr, combinations[6], 0, True),
        (is_cm_online_offline, combinations[6], 1, False),
        (is_cm_online_DhcpV4Done, combinations[6], 1, False),
        (is_cm_online_online_d_without_encr, combinations[6], 1, False),
        (is_cm_online_online_d, combinations[6], 1, False),
        (is_cm_online_online_without_encr, combinations[6], 1, True),
        (is_cm_online_online_with_encr, combinations[6], 1, True),
        (is_cm_online_offline, combinations[7], 0, False),
        (is_cm_online_DhcpV4Done, combinations[7], 0, False),
        (is_cm_online_online_d_without_encr, combinations[7], 0, True),
        (is_cm_online_online_d, combinations[7], 0, True),
        (is_cm_online_online_without_encr, combinations[7], 0, True),
        (is_cm_online_online_with_encr, combinations[7], 0, True),
        (is_cm_online_offline, combinations[7], 1, False),
        (is_cm_online_DhcpV4Done, combinations[7], 1, False),
        (is_cm_online_online_d_without_encr, combinations[7], 1, True),
        (is_cm_online_online_d, combinations[7], 1, True),
        (is_cm_online_online_without_encr, combinations[7], 1, True),
        (is_cm_online_online_with_encr, combinations[7], 1, True),
    ],
)
def test_is_cm_online(mocker, cmts_ouput, params_combination, partial, result):
    mocker.patch.object(ArrisCMTS, "__init__", return_value=None, autospec=True)
    mocker.patch.object(ArrisCMTS, "sendline", autospec=True)
    mocker.patch.object(
        ArrisCMTS, "check_output", return_value=cmts_ouput, autospec=True
    )
    mocker.patch.object(ArrisCMTS, "expect", autospec=True)
    mocker.patch.object(
        ArrisCMTS, "_check_PartialService", return_value=partial, autospec=True
    )
    arris = ArrisCMTS()
    assert arris._is_cm_online(*params_combination) == result
