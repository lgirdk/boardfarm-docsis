#!/usr/bin/env python
import pytest
from boardfarm.exceptions import CodeError

from boardfarm_docsis.devices.arris_cmts import ArrisCMTS


@pytest.mark.parametrize(
    "cmts_output, result, raises",
    [
        ("2020 October 30 12:08:27", "2020-10-30T12:08:27", None),
        ("2020 October  12:08:27", "", ValueError),
        ("2020 October 32 12:08:27", "", ValueError),
        ("2020 October 29 16:08:27", "2020-10-29T16:08:27", None),
        ("Tue Feb 04 14:00:00 UTC 2020", "2020-02-04T14:00:00", ValueError),
        ("", "", CodeError),
    ],
)
def test_get_current_time(mocker, cmts_output, result, raises):
    mocker.patch.object(ArrisCMTS, "__init__", return_value=None, autospec=True)
    mocker.patch.object(
        ArrisCMTS, "check_output", return_value=cmts_output, autospec=True
    )
    arris = ArrisCMTS()
    if raises:
        with pytest.raises(raises) as e:
            arris.get_current_time()
    else:
        assert arris.get_current_time() == result
