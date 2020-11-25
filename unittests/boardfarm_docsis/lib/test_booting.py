import os
import sys

import pytest

sys.path.insert(0, os.getcwd() + "/unittests/")
import boardfarm
from boardfarm.exceptions import BootFail

sys.path.pop(0)

from boardfarm_docsis.lib.booting import boot


class Dummy:
    cfg = None
    config = {}

    def SPV(self, *args, **kwargs):
        pass

    def get_prov_mode(self, *args, **kwargs):
        pass

    def get_ertr_mode(self, *args, **kwargs):
        pass

    def get_country(self, *args, **kwargs):
        pass

    def get_tr069_provisioning(self, *args, **kwargs):
        pass

    def generate_cfg(self, *args, **kwargs):
        pass

    def generate_mta_cfg(self, *args, **kwargs):
        pass

    def sipserver(self, *args, **kwargs):
        pass

    def voice_enabled(self, *args, **kwargs):
        pass

    def get_software(self, *args, **kwargs):
        pass

    def enable_logs(self, *args, **kwargs):
        pass

    def wait_for_mta_provisioning(self, *args, **kwargs):
        pass

    def get_cpeid(self, *args, **kwargs):
        pass

    def factory_reset(self, *args, **kwargs):
        pass

    def get_mta_config(self, *args, **kwargs):
        pass

    def get_emta_config_template(self, *args, **kwargs):
        pass


class DummyDev:
    def __init__(self):
        self.board = Dummy()
        self.acs_server = Dummy()
        self.board.cm_cfg = None
        self.board.mta_cfg = None

    def get_prov_mode(self, *args, **kwargs):
        pass

    def get_ertr_mode(self, *args, **kwargs):
        pass

    def get_country(self, *args, **kwargs):
        pass

    def get_tr069_provisioning(self, *args, **kwargs):
        pass

    def get_mta_config(self, *args, **kwargs):
        pass

    def get_emta_config_template(self, *args, **kwargs):
        pass


@pytest.mark.parametrize(
    "provision, sw_output, exp_out",
    [
        ([{"SPV": [{"dummy_param": "dummy_val"}]}], {"factory_reset": True}, None),
        ([{"SPV": [{"dummy_param": "dummy_val"}]}], {"factory_reset": False}, None),
    ],
)
def test_boot(mocker, provision, sw_output, exp_out):

    mocker.patch("boardfarm.lib.booting")
    config = Dummy()
    env_helper = Dummy()
    mocker.patch.object(env_helper, "get_prov_mode", return_value="dual", autospec=True)
    mocker.patch.object(
        env_helper, "get_ertr_mode", return_value={"max_config": False}, autospec=True
    )
    mocker.patch.object(env_helper, "get_country", return_value="NL", autospec=True)
    mocker.patch.object(
        env_helper, "get_tr069_provisioning", return_value=provision, autospec=True
    )
    mocker.patch.object(env_helper, "voice_enabled", return_value=False, autospec=True)
    mocker.patch.object(
        env_helper, "get_software", return_value=sw_output, autospec=True
    )
    mocker.patch.object(
        env_helper, "get_mta_config", return_value=provision, autospec=True
    )
    mocker.patch.object(
        env_helper, "get_emta_config_template", return_value="CH-Compal", autospec=True
    )

    devices = DummyDev()
    mocker.patch.object(devices.board, "generate_cfg", return_value=None, autospec=True)
    mocker.patch.object(
        devices.board, "generate_mta_cfg", return_value=None, autospec=True
    )
    mocker.patch.object(devices.board, "sipserver")
    mocker.patch.object(devices.board, "enable_logs", return_value=None, autospec=True)
    mocker.patch.object(
        devices.board, "wait_for_mta_provisioning", return_value=None, autospec=True
    )
    mocker.patch.object(devices.board, "get_cpeid", return_value=None, autospec=True)
    mocker.patch.object(
        devices.board, "factory_reset", return_value=False, autospec=True
    )
    if "True" in str(sw_output):
        val = boot(config, env_helper, devices, logged=None)
        assert val == exp_out
    else:
        with pytest.raises(BootFail):
            boot(config, env_helper, devices, logged=None)
