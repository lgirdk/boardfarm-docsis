"""Unit tests for booting module in boardfarm docsis."""

import os
import sys
from collections import UserList
from typing import Any, Iterator

import pytest

sys.path.insert(0, os.getcwd() + "/unittests/")
from boardfarm.exceptions import BootFail, CodeError, NoTFTPServer

sys.path.pop(0)
import boardfarm_docsis.lib.booting


class Dummy:
    cfg = None
    config = {}

    def SPV(self, *args, **kwargs) -> None:
        pass

    def get_prov_mode(self, *args, **kwargs) -> None:
        pass

    def get_ertr_mode(self, *args, **kwargs) -> None:
        pass

    def get_country(self, *args, **kwargs) -> None:
        pass

    def get_tr069_provisioning(self, *args, **kwargs) -> None:
        pass

    def generate_cfg(self, *args, **kwargs) -> None:
        pass

    def generate_mta_cfg(self, *args, **kwargs) -> None:
        pass

    def voice_enabled(self, *args, **kwargs) -> None:
        pass

    def mitm_enabled(self, *args, **kwargs) -> None:
        pass

    def get_software(self, *args, **kwargs) -> None:
        pass

    def enable_logs(self, *args, **kwargs) -> None:
        pass

    def wait_for_mta_provisioning(self, *args, **kwargs) -> None:
        pass

    def get_cpeid(self, *args, **kwargs) -> None:
        pass

    def factory_reset(self, *args, **kwargs) -> None:
        pass

    def get_mta_config(self, *args, **kwargs) -> None:
        pass

    def get_emta_config_template(self, *args, **kwargs) -> None:
        pass

    def get_dns_dict(self, *args, **kwargs) -> None:
        pass

    def get_board_sku(self, *args, **kwargs) -> None:
        pass

    def deploy_board_sku_via_dmcli(self, *args, **kwargs) -> None:
        pass


class DummyDev:
    name = ""

    def __init__(self) -> None:
        self.board = Dummy()
        self.acs_server = Dummy()
        self.board.cm_cfg = None
        self.board.mta_cfg = None
        self.cm_mac = "some mac"
        self.lan_clients = []

    def get_prov_mode(self, *args, **kwargs) -> None:
        pass

    def get_ertr_mode(self, *args, **kwargs) -> None:
        pass

    def get_country(self, *args, **kwargs) -> None:
        pass

    def get_tr069_provisioning(self, *args, **kwargs) -> None:
        pass

    def get_mta_config(self, *args, **kwargs) -> None:
        pass

    def get_emta_config_template(self, *args, **kwargs) -> None:
        pass

    def get_dns_dict(self, *args, **kwargs) -> None:
        pass

    def __iter__(self) -> Iterator[Any]:
        return iter([])

    def deploy_board_sku_via_dmcli(self, *args, **kwargs) -> None:
        pass

    def configure(self, *args, **kwargs) -> None:
        pass

    def kill_asterisk(self, *args, **kwargs) -> None:
        assert self.name == "sipcenter", "This method belongs to the sipcenter"

    def start_tftp_server(self, *args, **kwargs) -> None:
        assert "wan" in self.name, "This method must be called on the wan object"

    def env_config(self, *args, **kwargs) -> None:
        assert self.name == "board", "This method belongs to the board obj"

    def stop(self, *args, **kwargs) -> None:
        assert self.name == "sipcenter", "This method belongs to the sipcenter obj"

    def reset(self, *args, **kwargs) -> None:
        assert self.name == "board", "This method belongs to the board obj"

    def clear_cm_reset(self, *args, **kwargs) -> None:
        assert self.name == "cmts", "This method belongs to the cmts obj"

    def get_software(self, *args, **kwargs) -> None:
        pass

    def flash(self, *args, **kwargs) -> None:
        pass


class device_manager(UserList):
    def __init__(self) -> None:
        """Instance initialisation."""
        super().__init__()
        # List of current devices, which we prefer to reuse instead of creating new ones
        self.devices: list[Dummy] = []


def test_pre_boot_wan_clients_no_tftp(mocker) -> None:
    mocker.patch("boardfarm.lib.booting.get_tftp", return_value=(None, []))
    devices = dev_helper()
    with pytest.raises(NoTFTPServer):
        boardfarm_docsis.lib.booting.pre_boot_wan_clients(Dummy(), Dummy(), devices)


def dev_helper() -> device_manager:
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


def test_pre_boot_wan_clients_2_tftps(mocker) -> None:
    mocker.patch(
        "boardfarm.lib.booting.get_tftp",
        return_value=(DummyDev(), [DummyDev(), DummyDev()]),
    )
    devices = dev_helper()
    with pytest.raises(CodeError):
        boardfarm_docsis.lib.booting.pre_boot_wan_clients(Dummy(), Dummy(), devices)


def test_pre_boot_wan_clients_1_tftp(mocker) -> None:
    devices = dev_helper()
    mocker.patch(
        "boardfarm.lib.booting.get_tftp", return_value=(devices.wan, [devices.wan])
    )
    boardfarm_docsis.lib.booting.pre_boot_wan_clients(Dummy(), Dummy(), devices)


def test_pre_boot_lan_clients() -> None:
    devices = dev_helper()
    devices.lan_clients = []
    boardfarm_docsis.lib.booting.pre_boot_lan_clients(Dummy(), Dummy(), devices)


def test_boot_board(mocker) -> None:
    devices = dev_helper()
    devices.board.tftp_device = "something"
    env_helper = Dummy()
    mocker.patch.object(env_helper, "get_software", return_value=True, autospec=True)
    config = Dummy()
    config.provisioner = "something"
    mocker.patch.object(devices.board, "flash", side_effect=Exception("Flash Failed"))
    with pytest.raises(BootFail) as e:
        boardfarm_docsis.lib.booting.boot_board(config, env_helper, devices)
    assert e.typename == "BootFail"
