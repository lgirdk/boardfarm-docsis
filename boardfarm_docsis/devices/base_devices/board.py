import logging
import traceback
from collections import OrderedDict
from pathlib import Path
from typing import Optional

import debtcollector
from boardfarm.devices import get_device_mapping_class
from boardfarm.devices.base import BaseDevice
from boardfarm.devices.base_devices.board import BaseBoard
from boardfarm.devices.base_devices.board_templates import BoardHWTemplate
from boardfarm.exceptions import CodeError
from netaddr import EUI, mac_unix_expanded
from termcolor import colored

from boardfarm_docsis.devices.base_devices.mta_template import MTATemplate
from boardfarm_docsis.devices.docsis import DocsisInterface
from boardfarm_docsis.lib.env_helper import DocsisEnvHelper

logger = logging.getLogger("bft")


def __calc_mac(cm_mac: str, offset: int, d=mac_unix_expanded):
    return EUI(int(EUI(cm_mac)) + offset, dialect=d)


def get_mta_mac(cm_mac: str):
    return __calc_mac(cm_mac, 1)


def get_erouter_mac(cm_mac: str):
    return __calc_mac(cm_mac, 2)


class DocsisCPEHw(DocsisInterface):
    mac = {"cm": "", "mta": "", "ertr": "", "wifi2.4": "", "wifi5": ""}
    sr_no = None
    power = None  # port + credentials. Does it need to Power class object...?
    conn_type = None

    def _meta_flash(self, img):
        """Flash with image."""
        try:
            self.dev.board.dev.cmts.clear_cm_reset(self.dev.board.hw.mac["cm"])
            self.dev.board.dev.cmts.wait_for_cm_online(ignore_partial=True)
            self.dev.board.hw.flash_meta(
                img, self.dev.wan, self.dev.lan, check_version=True
            )
            return True
        except Exception as e:
            traceback.print_exc()
            logger.error(
                colored(
                    f"Failed to flash meta image: {img}",
                    color="red",
                    attrs=["bold"],
                )
            )
            logger.error(f"{e}")
            return False

    def _factory_reset(self, img):
        """Reset using factory_reset method."""
        try:
            self.dev.board.hw.factory_reset()
            return True
        except Exception as e:
            traceback.print_exc()
            logger.error(
                colored(
                    "Failed to perform reset using factory reset method",
                    color="red",
                    attrs=["bold"],
                )
            )
            logger.error(f"{e}")
            return False

    def _flash_docsis_image(self, config, env_helper, board, lan, wan, tftp_device):
        """Given an environment spec and a board attempts to flash the HW following
        the strategy defined in the environment. The flashing process includes
        breaking into the bootloader if needed, getting the image (from a webserver
        or local file system) copying it to a tftp server on the lan side of the
        device

        Current strategies are:

        atom: flashes the atom image from bootloader
        arm: flashes the arm image from the bootloader
        combined: flashes a combined (atom+arm) image from the bootloader
        comdined_meta: TBD (not from bootloader)
        """

        def _perform_flash(boot_sequence):
            """Perform Flash booting."""
            board.hw.reset()
            for i in boot_sequence:
                for strategy, img in i.items():
                    if strategy != "pre_flash_factory_reset":
                        if strategy in [
                            "factory_reset",
                            "meta_build",
                        ]:
                            board.hw.wait_for_linux()
                        else:
                            board.hw.wait_for_boot()

                    board.hw.setup_uboot_network(tftp_device.gw)
                    result = self.methods[strategy](img)

                    if strategy in [
                        "pre_flash_factory_reset",
                        "factory_reset",
                        "meta_build",
                    ]:
                        if not result:
                            board.hw.reset()
                            raise Exception(
                                colored(
                                    f"Failed to perform '{strategy}' boot sequence",
                                    color="red",
                                    attrs=["bold"],
                                )
                            )
                    else:
                        board.hw.boot_linux()

        def _check_override(strategy, img):
            """Check for Overriding image value."""
            if getattr(config, strategy.upper(), None):
                # this is the override
                debtcollector.deprecate(
                    "Warning!!! cmd line arg has been passed."
                    "Overriding image value for {}".format(strategy),
                    removal_version="> 1.1.1",
                    category=UserWarning,
                )

                return getattr(config, strategy.upper())
            return img

        boot_sequence = []
        stage = OrderedDict()
        stage[1] = OrderedDict()
        stage[2] = OrderedDict()
        d = env_helper.get_dependent_software()
        if d:
            fr = d.get("factory_reset", False)
            if fr:
                stage[1]["factory_reset"] = fr
            strategy = d.get("flash_strategy")
            img = _check_override(strategy, d.get("image_uri"))
            stage[1][strategy] = img

        d = env_helper.get_software()
        if d:
            if "load_image" in d:
                strategy = "meta_build"
                img = _check_override(strategy, d.get("load_image"))
            else:
                strategy = d.get("flash_strategy")
                img = _check_override(strategy, d.get("image_uri"))

            if stage[1]:
                assert (
                    strategy != "meta_build"
                ), "meta_build strategy needs to run alone!!!"

            pbfr = d.get("pre_flash_factory_reset", False)
            if pbfr:
                stage[2]["pre_flash_factory_reset"] = pbfr
            if stage[1].get(strategy, None) != img:
                stage[2][strategy] = img
            fr = d.get("factory_reset", False)
            if fr:
                stage[2]["factory_reset"] = fr

        for k, v in stage[1].items():
            boot_sequence.append({k: v})
        for k, v in stage[2].items():
            boot_sequence.append({k: v})

        if boot_sequence:
            _perform_flash(boot_sequence)

    def __init__(self, *args, **kwargs):
        self.methods = {
            "meta_build": self._meta_flash,
            "factory_reset": self._factory_reset,
            "pre_flash_factory_reset": self._factory_reset,
        }

        self.config = kwargs.get("config", None)
        self.power = kwargs.get("power_outlet", None)
        self.conn_type = kwargs.get("connection_type", None)
        self.sr_no = kwargs.get("serial_no", None)
        # the cm_mac is in config["cm_mac"] but really should be in line with
        # the other attrs, see board_decider is invoked
        self.mac = dict(DocsisCPEHw.mac)
        self.mac["cm"] = kwargs.get("cm_mac", None)
        if self.mac["cm"] is None:
            # old way
            self.mac["cm"] = kwargs.get("config")["cm_mac"]
        self.mac["mta"] = kwargs.get("mta_mac", get_mta_mac(self.mac["cm"]))
        self.mac["ertr"] = kwargs.get("erouter_mac", get_erouter_mac(self.mac["cm"]))
        self.mac["wifi2.4"] = kwargs.get("wifi2.4", None)
        self.mac["wifi5.0"] = kwargs.get("wifi5.0", None)

    @property
    def get_mibs_path(self):
        return BoardHWTemplate.get_mibs_path(self) + [
            str(Path(__file__).parent.parent.parent.joinpath("mibs"))
        ]

    @property
    def cm_mac(self):
        return self.mac["cm"]

    def reset(self):
        raise NotImplementedError

    def flash(self, config, env_helper):
        self._flash_docsis_image(
            config,
            env_helper,
            self.dev.board,
            self.dev.lan,
            self.dev.wan,
            self.dev.wan,
        )
        self.reset()
        self.wait_for_hw_boot()

    def env_config(self, cm_boot_file, mta_boot_file, mibs_path):
        self.cm_cfg = self.cm_cfg(cfg_file_str=cm_boot_file, mibs_path=mibs_path)
        self.mta_cfg = self.mta_cfg(mta_file_str=mta_boot_file, mibs_path=mibs_path)


class DocsisCPESw:
    voice: Optional[MTATemplate] = None

    def __init__(self) -> None:
        self._provisioning_messages = {
            "verify_cm_cfg_file_download": "",
            "verify_emta_cfg_file_download": "",
            "verify_emta_config_apply": "",
            "verify_emta_provisioning": "",
        }

    @property
    def provisioning_messages(self):
        return self._provisioning_messages

    @provisioning_messages.setter
    def provisioning_messages(self, value):
        raise NotImplementedError

    def get_sw_version(self):
        raise NotImplementedError


class InterceptDocsisCPE:
    """Any pexpect call made using self will be redirected to self.sw
    if the method is not implemented
    """

    def __getattribute__(self, name):
        try:
            attr = object.__getattribute__(self, name)
        except Exception:
            try:
                attr = self.hw.__getattribute__(name)
            except Exception:
                attr = self.sw.__getattribute__(name)
        return attr


class DocsisCPEInterface(InterceptDocsisCPE):
    """Docsis CPE Interface to be used by a derived class"""

    sw: Optional[BaseDevice] = None
    hw: Optional[DocsisCPEHw] = None
    cm_cfg = None
    mta_cfg = None
    # there must be a better way of finding the mib files!
    mibs_paths = [
        "boardfarm/boardfarm/resources/mibs",
        "boardfarm-docsis/boardfarm_docsis/mibs/",
    ]

    def _get_image(self, env_helper: DocsisEnvHelper):
        sw = env_helper.get_software()
        if "image_uri" in sw:
            image = sw["image_uri"].split("/")[-1]
        elif "load_image" in sw:
            image = sw["load_image"].split("/")[-1]
        else:
            raise CodeError(
                colored(
                    f"Failed to get image from : {sw}",
                    color="red",
                    attrs=["bold"],
                )
            )
        logger.info(
            colored(
                f"Loading SW class for image: {image}",
                color="green",
                attrs=["bold"],
            )
        )
        return image

    def flash(self, env_helper: DocsisEnvHelper):
        self.hw.dev = (
            self.dev
        )  # FIX ME: hack, to be removed when puma6 can import HW manager
        self.hw.flash(self.config, env_helper)
        image = self._get_image(env_helper)
        self.reload_sw_object(image)

    def power_cycle(self):
        self.hw.reset()

    def wait_for_cm_online(self):
        pass

    def break_into_bootloader(self):
        pass

    def reload_sw_object(self, sw):
        # Though the right arguments passed to the method and the method has return pylint throws some false positive error, hence added disable
        sw_class = get_device_mapping_class(sw)  # pylint: disable=E1121, E1111
        if sw_class:
            self.sw = sw_class(self.hw)
        else:
            raise CodeError(f"class for {sw} not found")
        self.sw.version = self.sw.get_sw_version()


class DocsisCPE(DocsisCPEInterface, BaseBoard):
    def __init__(self, *args, **kwargs):
        self.hw = DocsisCPEHw(*args, **kwargs)
