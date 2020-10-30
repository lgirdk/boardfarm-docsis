#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

import pytest
from boardfarm.exceptions import CodeError

from boardfarm_docsis.devices.topvision_cmts import MiniCMTS

ok_date1 = """System time: 1970-01-08 19:49:00 Thu
Timezone: GMT+00:00"""

wrong_date = """System time: 2020-10-0 13:17:42 Fri
Timezone: GMT+00:00"""

wrong_time = """System time: 2020-10-30 :17:42 Fri
Timezone: GMT+00:00"""

ok_date2 = """System time: 2020-10-29 10:26:07 Thu
Timezone: GMT+00:00"""

ok_date3 = """System time: 2020-02-04 14:00:00 Tue
Timezone: GMT+00:00"""

no_date = ""


# NOTE: here the behaviour differs slightly from the other
# cmts' as here there is no ValueError. The pattern mathching
# used in the implementation generates CodeError
@pytest.mark.parametrize(
    "cmts_output, result, raises",
    [
        (ok_date1, "1970-01-08T19:49:00", None),
        (wrong_date, "", CodeError),
        (wrong_time, "", CodeError),
        (ok_date2, "2020-10-29T10:26:07", None),
        (ok_date3, "2020-02-04T14:00:00", None),
        (no_date, "", CodeError),
    ],
)
def test_get_current_time(mocker, cmts_output, result, raises):
    mocker.patch.object(MiniCMTS, "__init__", return_value=None, autospec=True)
    mocker.patch.object(
        MiniCMTS, "check_output", return_value=cmts_output, autospec=True
    )
    cmts = MiniCMTS()
    if raises:
        with pytest.raises(raises) as e:
            cmts._get_current_time()
    else:
        assert cmts._get_current_time() == result
