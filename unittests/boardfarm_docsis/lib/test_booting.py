import os
import sys
from collections import UserList

import pytest

sys.path.insert(0, os.getcwd() + "/unittests/")
import boardfarm
from boardfarm.exceptions import BootFail, CodeError, NoTFTPServer

from boardfarm_docsis.exceptions import VoiceSetupConfigureFailure

sys.path.pop(0)

import boardfarm.lib.voice
import pexpect
from boardfarm.lib.voice import dns_setup_sipserver

import boardfarm_docsis.lib.booting
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

    def voice_enabled(self, *args, **kwargs):
        pass

    def mitm_enabled(self, *args, **kwargs):
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

    def get_dns_dict(self, *args, **kwargs):
        pass

    def get_board_sku(self, *args, **kwargs):
        pass

    def deploy_board_sku_via_dmcli(self, *args, **kwargs):
        pass


class DummyDev:
    name = ""

    def __init__(self):
        self.board = Dummy()
        self.acs_server = Dummy()
        self.board.cm_cfg = None
        self.board.mta_cfg = None
        self.cm_mac = "some mac"
        self.lan_clients = []

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

    def get_dns_dict(self, *args, **kwargs):
        pass

    def __iter__(self):
        return iter([])

    def deploy_board_sku_via_dmcli(self, *args, **kwargs):
        pass

    def configure(self, *args, **kwargs):
        pass

    def kill_asterisk(self, *args, **kwargs):
        assert self.name == "sipcenter", "This method belongs to the sipcenter"

    def start_tftp_server(self, *args, **kwargs):
        assert "wan" in self.name, "This method must be called on the wan objetc"

    def env_config(self, *args, **kwargs):
        assert self.name == "board", "This method belongs to the board obj"

    def stop(self, *args, **kwargs):
        assert self.name == "sipcenter", "This method belongs to the sipcenter obj"

    def reset(self, *args, **kwargs):
        assert self.name == "board", "This method belongs to the board obj"

    def clear_cm_reset(self, *args, **kwargs):
        assert self.name == "cmts", "This method belongs to the cmts obj"

    def get_software(self, *args, **kwargs):
        pass


class device_manager(UserList):
    def __init__(self):
        """Instance initialisation."""
        super().__init__()
        # List of current devices, which we prefer to reuse instead of creating new ones
        self.devices = []


def test_pre_boot_wan_clients_no_tftp(mocker):
    mocker.patch("boardfarm.lib.booting")
    mocker.patch("boardfarm.lib.booting.get_tftp", return_value=(None, []))
    with pytest.raises(NoTFTPServer):
        boardfarm_docsis.lib.booting.pre_boot_wan_clients(Dummy(), Dummy(), Dummy())


def dev_helper():
    devices = device_manager()
    devices.board = DummyDev()
    devices.board.name = "board"
    devices.append(devices.board)
    devices.cmts = DummyDev()
    devices.cmts.name = "cmts"
    devices.wan = DummyDev()
    devices.wan.name = "wan"
    devices.append(devices.wan)
    devices.lan = DummyDev()
    devices.lan.name = "lan"
    devices.append(devices.lan)
    devices.lan2 = DummyDev()
    devices.lan2.name = "lan2"
    devices.append(devices.lan2)
    devices.lan3 = DummyDev()
    devices.lan3.name = "lan3"
    devices.append(devices.lan3)
    devices.sipcenter = DummyDev()
    devices.sipcenter.name = "sipcenter"
    devices.append(devices.sipcenter)
    devices.softphone = DummyDev()
    devices.softphone.name = "softphone"
    devices.append(devices.softphone)
    return devices


def test_pre_boot_wan_clients__2_tftps(mocker):
    mocker.patch("boardfarm.lib.booting")
    mocker.patch(
        "boardfarm.lib.booting.get_tftp",
        return_value=(DummyDev(), [DummyDev(), DummyDev()]),
    )
    devices = dev_helper()

    with pytest.raises(CodeError):
        boardfarm_docsis.lib.booting.pre_boot_wan_clients(Dummy(), Dummy(), devices)


def test_pre_boot_wan_clients__1_tftp(mocker):
    devices = dev_helper()
    mocker.patch("boardfarm.lib.booting")
    mocker.patch(
        "boardfarm.lib.booting.get_tftp", return_value=(devices.wan, [devices.wan])
    )
    boardfarm_docsis.lib.booting.pre_boot_wan_clients(Dummy(), Dummy(), devices)


def test_pre_boot_lan_clients():
    devices = dev_helper()
    boardfarm_docsis.lib.booting.pre_boot_lan_clients(Dummy(), Dummy(), devices)


def test_pre_boot_env__voice_enabled_failed_dns_setup_sipserver(mocker):
    devices = dev_helper()
    env_helper = Dummy()
    mocker.patch.object(env_helper, "voice_enabled", return_value=True, autospec=True)
    mocker.patch(
        "boardfarm.lib.voice.dns_setup_sipserver",
        side_effect=pexpect.TIMEOUT("FakeTimeoutException"),
        autospec=True,
    )
    with pytest.raises(VoiceSetupConfigureFailure):
        boardfarm_docsis.lib.booting.pre_boot_env(Dummy(), env_helper, devices)


def test_pre_boot_env__voice_enabled_failed_voice_devices_configure(mocker):
    devices = dev_helper()
    env_helper = Dummy()
    mocker.patch.object(env_helper, "voice_enabled", return_value=True, autospec=True)
    mocker.patch(
        "boardfarm.lib.voice.voice_devices_configure",
        side_effect=Exception("FakeDeviceConfigurationFailure"),
        autospec=True,
    )
    with pytest.raises(VoiceSetupConfigureFailure):
        boardfarm_docsis.lib.booting.pre_boot_env(Dummy(), env_helper, devices)


def test_pre_boot_env__voice_enabled_provisioning_exception(mocker):
    devices = dev_helper()
    devices.board.tftp_device = "something"
    env_helper = Dummy()
    config = Dummy()
    config.provisioner = "something"
    mocker.patch.object(env_helper, "voice_enabled", return_value=True, autospec=True)
    mocker.patch(
        "boardfarm.lib.booting.provision",
        side_effect=Exception("FakeProvisioningFailure"),
        autospec=True,
    )
    with pytest.raises(Exception):
        boardfarm_docsis.lib.booting.pre_boot_env(config, env_helper, devices)


def test_pre_boot_env__voice_enabled_provisioning_ok(mocker):
    devices = dev_helper()
    devices.board.tftp_device = "something"
    env_helper = Dummy()
    config = Dummy()
    config.provisioner = "something"
    mocker.patch.object(env_helper, "voice_enabled", return_value=True, autospec=True)
    boardfarm_docsis.lib.booting.pre_boot_env(config, env_helper, devices)


def test_boot_board(mocker):
    devices = dev_helper()
    devices.board.tftp_device = "something"
    env_helper = Dummy()
    mocker.patch.object(env_helper, "get_software", return_value=True, autospec=True)
    config = Dummy()
    config.provisioner = "something"
    mocker.patch(
        "boardfarm.lib.booting.boot_image", side_effect=Exception("Flash Failed")
    )
    with pytest.raises(BootFail) as e:
        boardfarm_docsis.lib.booting.boot_board(config, env_helper, devices)
    assert e.typename == "BootFail"
