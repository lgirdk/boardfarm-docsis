import logging
from collections import OrderedDict

import debtcollector
from boardfarm.devices import get_device_mapping_class
from boardfarm.devices.base import BaseDevice
from boardfarm.devices.base_devices.board import BaseBoard
from boardfarm.exceptions import CodeError
from netaddr import EUI, mac_unix_expanded

from boardfarm_docsis.devices.docsis import Docsis
from boardfarm_docsis.lib.env_helper import DocsisEnvHelper

logger = logging.getLogger("bft")


def __calc_mac(cm_mac: str, offset: int, d=mac_unix_expanded):
    return EUI(int(EUI(cm_mac)) + offset, dialect=d)


def get_mta_mac(cm_mac: str):
    return __calc_mac(cm_mac, 1)


def get_erouter_mac(cm_mac: str):
    return __calc_mac(cm_mac, 2)


class DocsisCPEHw:
    mac = {"cm": "", "mta": "", "ertr": "", "wifi2.4": "", "wifi5": ""}
    sr_no = None
    power = None  # port + credentials. Does it need to Power class object...?
    conn_type = None

    @staticmethod
    def _flash_docsis_image(config, env_helper, board, lan, wan, tftp_device):
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

        def _meta_flash(img):
            """Flash with image."""
            try:
                board.dev.cmts.wait_for_cm_online(ignore_partial=True)
                board.hw.flash_meta(img, wan, lan, check_version=True)
            except Exception as e:
                logger.error("Failed to flash meta image: {meta}")
                logger.error(f"{e}")

        def _factory_reset(img):
            """Reset using factory_reset method."""
            board.hw.factory_reset()

        methods = {
            "meta_build": _meta_flash,
            "atom": board.hw.flash_atom,
            "arm": board.hw.flash_arm,
            "all": board.hw.flash_all,
            "factory_reset": _factory_reset,
        }

        def _perform_flash(boot_sequence):
            """Perform Flash booting."""
            board.hw.reset()
            for i in boot_sequence:
                for strategy, img in i.items():
                    if strategy in ["factory_reset", "meta_build"]:
                        board.hw.wait_for_hw_boot()
                    else:
                        board.hw.wait_for_boot()

                    board.hw.setup_uboot_network(tftp_device.gw)
                    result = methods[strategy](img)

                    if strategy in ["factory_reset", "meta_build"]:
                        if not result:
                            board.hw.reset()
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
        if not stage[2]:
            d = env_helper.get_dependent_software()
            if d:
                fr = d.get("factory_reset", False)
                if fr:
                    stage[1]["factory_reset"] = fr
                strategy = d.get("flash_strategy")
                img = _check_override(strategy, d.get("image_uri"))
                stage[1][strategy] = img

        if not stage[2]:
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
        self.power = kwargs.get("power_outlet", None)
        self.conn_type = kwargs.get("connection_type", None)
        self.sr_no = kwargs.get("serial_no", None)
        # the cm_mac is in config["cm_mac"] but really should be in line with
        # the other attrs, see board_decider is invoked
        self.mac["cm"] = kwargs.get("cm_mac", None)
        if self.mac["cm"] is None:
            # old way
            self.mac["cm"] = kwargs.get("config")["cm_mac"]
        self.mac["mta"] = kwargs.get("mta_mac", get_mta_mac(self.mac["cm"]))
        self.mac["ertr"] = kwargs.get("erouter_mac", get_erouter_mac(self.mac["cm"]))
        self.mac["wifi2.4"] = kwargs.get("wifi2.4", None)
        self.mac["wifi5.0"] = kwargs.get("wifi5.0", None)

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


class DocsisCPESw(Docsis):
    def get_sw_version(self):
        raise NotImplementedError


class DocsisCPE(BaseBoard):
    """Docsis CPE"""

    sw: BaseDevice = None  # is this right?
    hw: DocsisCPEHw = None

    def __init__(self, *args, **kwargs):
        self.hw = DocsisCPEHw(*args, **kwargs)

    def flash(self, env_helper: DocsisEnvHelper):
        self.hw.dev = (
            self.dev
        )  # FIX ME: hack, to be removed when puma6 can import HW manager
        self.hw.flash(self.config, env_helper)
        sw = env_helper.get_software()
        self.reload_sw_object(sw["image_uri"].split("/")[-1])

    def power_cycle(self):
        self.hw.reset()

    def wait_for_cm_online(self):
        pass

    def break_into_bootloader(self):
        pass

    def reload_sw_object(self, sw):
        sw_class = get_device_mapping_class(sw)
        if sw_class:
            self.sw = sw_class(self.hw)
        else:
            raise CodeError(f"class for {sw} not found")
        self.sw.version = self.sw.get_sw_version()
