#!/usr/bin/env python3
# Copyright (c) 2015
#
# All rights reserved.
#
# This file is distributed under the Clear BSD license.
# The full text can be found in LICENSE in the root directory.
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import glob
import hashlib
import ipaddress
import logging
import os
import re
import tempfile
from pathlib import Path

import boardfarm
from aenum import Enum
from boardfarm.exceptions import BftCommandNotFound, BootFail, CodeError
from boardfarm.lib import SnmpHelper
from boardfarm.lib.common import cmd_exists, keccak512_checksum, retry_on_exception
from boardfarm.lib.DeviceManager import device_type
from debtcollector import deprecate

from boardfarm_docsis.exceptions import (
    CfgUnknownType,
    CMCfgEncodeFailed,
    IpAddrMismatch,
    MTACfgEncodeFailed,
)

from .cfg_helper import CfgGenerator

try:
    # Python 2
    import Tkinter
except Exception:
    # Python 3
    import tkinter as Tkinter

logger = logging.getLogger("bft")


class cfg_type(Enum):
    UNKNOWN = 0
    CM = 1
    MTA = 2


class base_cfg:
    """
    Name: docsis module
    Purpose: docsis operating.
    Input: Absolute path of text file
    Fuction:
        decode():
            return output file name(.txt)
        encode()
            return output file name(.cfg or .bin)
    """

    mibs_path_arg = ""

    def __init__(self, file_or_obj, tmpdir=None, mibs_paths=None):
        # TODO: fix at some point, this tmpdir is already relative to the CM config you
        # are grabbing? Not ideal as that dir might not be writeable, or a tftp or http URL
        # at some point - need to use a real local tmpdir or maybe even results so we can
        # save the resulting artifacts in other tools

        self.init_copy(file_or_obj, tmpdir=tmpdir, mibs_paths=mibs_paths)

    def init_copy(self, file_or_obj, tmpdir=None, mibs_paths=None):
        if mibs_paths is None:
            mibs_paths = []

        if tmpdir is None:
            tmpdir = tempfile.mkdtemp()

        if mibs_paths != []:
            mibs_path_arg = "-M "
            for mibs_path in mibs_paths:
                mibs_path_arg = mibs_path_arg + ":" + mibs_path

            self.mibs_path_arg = mibs_path_arg

        # TODO: this is all a bit wild here, need to clean up everything..
        if isinstance(file_or_obj, cm_cfg):
            self.cm_cfg = file_or_obj
            # TODO: this seems like the wrong place to store these but OK
            self.dir_path = os.path.join(os.path.split(__file__)[0], tmpdir)
            self.file = self.cm_cfg.original_fname
            self.file_path = os.path.join(self.dir_path, self.file)
        elif isinstance(file_or_obj, mta_cfg):
            self.mta_cfg = file_or_obj
            # TODO: this seems like the wrong place to store these but OK
            self.dir_path = os.path.join(os.path.split(__file__)[0], tmpdir)
            self.file = self.mta_cfg.original_fname
            self.file_path = os.path.join(self.dir_path, self.file)
        else:
            self.file_path = file_or_obj
            self.dir_path = os.path.join(os.path.split(file_or_obj)[0], tmpdir)
            self.file = os.path.split(file_or_obj)[1]

        # make target tmpdir if it does not exist
        try:
            os.makedirs(self.dir_path)
        except OSError as err:
            import errno

            # Reraise the error unless it's about an already existing directory
            if err.errno != errno.EEXIST or not os.path.isdir(self.dir_path):
                raise

        if isinstance(file_or_obj, cm_cfg):
            self.cm_cfg.save(self.file_path)
        if isinstance(file_or_obj, mta_cfg):
            self.mta_cfg.save(self.file_path)

        # Though the method requires an arg pylint throws some false positive error, hence added disable
        assert cmd_exists("docsis")  # pylint: disable=E1121
        assert cmd_exists("tclsh")  # pylint: disable=E1121
        tclsh = Tkinter.Tcl()
        assert tclsh.eval(
            "package require sha1"
        ), "please run apt-get install tcllib first"

    def get_cfg_type(self):
        with open(self.file_path) as cfg:
            # TODO: this is OK but could be better
            data = cfg.read()
            # BAD: this section needs cleaning up as parts are vendor specific
            if data.startswith("Main"):
                return cfg_type.CM
            elif data.startswith("\t."):
                return cfg_type.MTA
            else:
                return cfg_type.UNKNOWN

    def decode(self):
        if ".cfg" in self.file:
            os.system(
                f"docsis -d {self.file_path} > {self.file_path.replace('.cfg', '.txt')}"
            )
            assert os.path.exists(self.file.replace(".cfg", ".txt"))

            return self.file.replace(".cfg", ".txt")

        # TODO: decode MTA?

    def _run_cmd(self, cmd):
        logger.debug(cmd)
        os.system(cmd)

    # this method can be overridden for vendor specific commands
    def encode_mta(self, mibs_path_arg, file_path, mtacfg_path):
        self._run_cmd(f"docsis {mibs_path_arg} -p {file_path} {mtacfg_path}")
        if not os.path.exists(mtacfg_path):
            raise MTACfgEncodeFailed()
        return mtacfg_path

    # this method can be overridden for vendor specific commands
    def encode_cm(self, mibs_path_arg, file_path, cmcfg_path, key_file="/dev/null"):
        self._run_cmd(f"docsis {mibs_path_arg} -e {file_path} {key_file} {cmcfg_path}")
        if not os.path.exists(cmcfg_path):
            raise CMCfgEncodeFailed()
        return cmcfg_path

    def encode(self):
        def encode_mta():
            mtacfg_name = self.file.replace(".txt", ".bin")
            mtacfg_path = os.path.join(self.dir_path, mtacfg_name)
            if os.path.isfile(mtacfg_path):
                os.remove(mtacfg_path)
            return self.encode_mta(self.mibs_path_arg, self.file_path, mtacfg_path)

        def encode_cm():
            cmcfg_name = self.file.replace(".txt", ".cfg")
            cmcfg_path = os.path.join(self.dir_path, cmcfg_name)
            if os.path.isfile(cmcfg_path):
                os.remove(cmcfg_path)
            return self.encode_cm(self.mibs_path_arg, self.file_path, cmcfg_path)

        if self.get_cfg_type() == cfg_type.CM:
            return encode_cm()
        elif self.get_cfg_type() == cfg_type.MTA:
            return encode_mta()
        else:
            raise CfgUnknownType()

    def load(self, cfg_data, method="txt"):
        """Load cfg from txt file, for modification"""

        if method == "txt":
            self.txt = cfg_data
        if method == "file":
            with open(cfg_data) as txt:
                self.txt = txt.read()

    # this is old. This would go eventually.
    @staticmethod
    def configure_board(provisioner, board, **kwargs):
        cm_cfg = kwargs.pop("cm_cfg", None)
        mta_cfg = kwargs.pop("mta_cfg", None)

        board.update_docsis_config(cm_cfg=cm_cfg, mta_cfg=mta_cfg, **kwargs)

        override = kwargs.get("force", False)
        if not override:
            # calculate and compare sha1 of board cfg file with one present in tftp here.
            pass

        # TODO: we need to have a common lib which marks services running in each device.
        # this needs to be removed at a later point.
        provisioner.tftp_device = board.tftp_dev
        provisioner.provision_board(board.config)

    # This method is old. Added a method on top to calculate sha3.
    @staticmethod
    def validate_modem_cfg_file(board, device):
        """
        To check if the cfg file used in modem and wan container are same.
        This method is used to compare the sha on the cfg file used in the modem and the one on wan.
        Parameters: (object)board
                    (object)wan

        Returns: (bool) True if sha matches else False.
        """
        modem_cfg = board.get_modem_cfg_file(
            device.get_interface_ipaddr(device.iface_dut)
        )
        if modem_cfg:
            device.sendline(f"sha1sum  /tftpboot/tmp/{modem_cfg} /tftpboot/{modem_cfg}")
            device.expect(device.prompt)
            return (
                device.before.split("\n")[1].split(" ")[0]
                == device.before.split("\n")[2].split(" ")[0]
            )
        else:
            return False

    @classmethod
    def copy_cmts_provisioning_files(cls, board_config, tftp_device, board):
        """
        This method looks for board's config file in all overlays.
        The file is then encrypted using docsis and pushed to TFTP server.

        args:
        board_config (dict): requires tftp_cfg_files key in board config.
        """
        # Look in all overlays as well, and PATH as a workaround for standalone
        paths = os.environ["PATH"].split(os.pathsep)
        paths += [
            os.path.dirname(boardfarm.plugins[x].__file__) for x in boardfarm.plugins
        ]
        cfg_list = []

        if "tftp_cfg_files" in board_config:
            for cfg in board_config["tftp_cfg_files"]:
                if isinstance(cfg, (cm_cfg, mta_cfg)):
                    cfg_list.append(cfg)
                else:
                    for path in paths:
                        cfg_list += glob.glob(path + f"/devices/cm-cfg/{cfg}")
        else:
            # TODO: this needs to be removed
            for path in paths:
                cfg_list += glob.glob(path + "/devices/cm-cfg/UNLIMITCASA.cfg")
        cfg_set = set(cfg_list)

        # Copy binary files to tftp server
        for cfg in cfg_set:
            d = cls(cfg, mibs_paths=board.mibs_path)
            ret = d.encode()
            tftp_device.copy_file_to_server(ret)

    def shortname(self, num_digits=None):
        """short name for displaying in summary"""
        h = hashlib.md5(self.txt.encode()).hexdigest()
        if num_digits:
            h = h[0:num_digits]
        return h


class cm_cfg(base_cfg):
    """
    Class for generating CM cfg from nothing, or even importing from a file
    They later need to be encoded via a compiler
    """

    # TODO: all these names will need to be made up once we don't have
    # an input file anymore
    original_fname = None
    original_file = None
    encoded_suffix = ".cfg"
    encoded_fname = None

    # string representation of cm cfg
    # temporary for starting point
    txt = ""

    # plenty of tests reference a file name, and assume it's in a certain
    # place so let's allow for that for now
    legacy_search_path = None

    def __init__(self, start=None, fname=None, cfg_file_str=None, mibs_path=None):
        """Creates a default basic CM cfg file for modification"""
        self.dslite = False

        self._start = start

        if cfg_file_str:
            # This is a config file in a long string format (multiline string)
            self.load_from_string(cm_str_txt=cfg_file_str)
        elif start is None:
            # create a default config file with bare minimum config,
            # no snmp objs, no CVCs, nothing vendor specific!
            # only CM RF minimal config
            # (i.e.: only the RF side configured, no client side, see Prasada)
            start = CfgGenerator()
            start.gen_dual_stack_cfg()
            self.txt = start.generate_cfg(fname)
            self.original_fname = fname
            self.encoded_fname = self.original_fname.replace(
                ".txt", self.encoded_suffix
            )
        elif type(start) is str:
            # OLD fashined: this is a file name, load the contents from the file
            self.original_file = start
            self.original_fname = os.path.split(start)[1]
            self.encoded_fname = self.original_fname.replace(
                ".txt", self.encoded_suffix
            )
            self.load(start)
        elif isinstance(start, CfgGenerator):
            # the dynamic configure class has created this config.... (ok not very OOD to
            # have a class type check in the base class....)
            if fname is None:
                # create a name and add some sha256 digits
                fname = "cm-config-" + self.shortname(10) + ".txt"
                logger.info(f"Config name created: {fname}")
            self.txt = (
                start.generate_cfg()
            )  # the derived class already created the skeleton
            if "DsLite" in self.txt:
                self.dslite = True
            self.original_fname = fname
            self.encoded_fname = self.original_fname.replace(
                ".txt", self.encoded_suffix
            )
        else:
            raise Exception(f"Wrong type {type(start)} received")
        super().init_copy(file_or_obj=self, mibs_paths=mibs_path)

    def encode(self):
        cfg_name = self.file.replace(".txt", ".cfg")
        cfg_path = os.path.join(self.dir_path, cfg_name)
        if os.path.isfile(cfg_path):
            os.remove(cfg_path)
        return self.encode_cm(self.mibs_path_arg, self.file_path, cfg_path)

    def load(self, cm_txt):
        """Load CM cfg from txt file, for modification"""

        if self.legacy_search_path is not None:
            cm_txt = os.path.join(self.legacy_search_path, cm_txt)

        with open(cm_txt) as txt:
            self.txt = txt.read()

    def load_from_string(self, cm_str_txt: str, name_prefix: str = "") -> None:
        """Load CM cfg from text string (e.g. the file is stored in a multiline
        string).
        :parameter cm_str_txt: s string containing the config file
        :type cm_str_txt: string
        :parameter name: name of config file (optional)
        """
        self.txt = cm_str_txt
        num = self.shortname(10)
        self.original_file = None
        if name_prefix:
            name_prefix += "-"
        else:
            name_prefix = "cm-config-"
        self.original_fname = name_prefix + num + ".txt"
        self.encoded_fname = self.original_fname.replace(".txt", self.encoded_suffix)

    def __str__(self):
        """String repr of CM txt"""
        return self.txt

    def save(self, full_path):
        with open(full_path, "w") as txt:
            txt.write(self.txt)

    def generic_re_sub(self, regex, sub):
        """Crude function to replace strings in configs, should be replaced with subclasses"""
        saved_txt = self.txt

        self.txt = re.sub(regex, sub, self.txt)

        if saved_txt == self.txt:
            logger.error(
                f"WARN: no regex sub was made for {regex}, to be replaced with {sub}"
            )

    def _cm_configmode(self):
        """function to check config mode in CM"""
        """0-Disable/Bridge, 1-IPv4, 2-IPv6 (IPv6 | dslite), 3-IPv4 and IPv6(Dual)"""
        modeset = ["0x010100", "0x010101", "0x010102", "0x010103"]
        modestr = ["disabled", "ipv4", "ipv6", "dual-stack"]
        for mode in range(len(modeset)):
            tlv_check = "GenericTLV TlvCode 202 TlvLength 3 TlvValue " + modeset[mode]
            initmode_check = "InitializationMode " + str(mode)
            if (tlv_check in self.txt) or (initmode_check in self.txt):
                return modestr[mode]

    cm_configmode = property(_cm_configmode)


class mta_cfg(base_cfg):
    """MTA specific class for cfgs"""

    encoded_suffix = ".bin"
    txt = ""

    def __init__(self, start=None, fname=None, mta_file_str=None, mibs_path=None):
        """
        Creates a default basic mta  cfg file for modification
        """

        if mta_file_str:
            self.load_from_string(mta_str_txt=mta_file_str)
        elif type(start) is str:
            # OLD fashined: this is a file name, load the contents from the file
            self.original_file = start
            self.original_fname = os.path.split(start)[1]
            self.encoded_fname = self.original_fname.replace(
                ".txt", self.encoded_suffix
            )
            self.load(start)
        elif isinstance(start, CfgGenerator):
            if fname is None:
                # create a name and add some sha256 digits
                fname = "mta-config-" + self.shortname(10) + ".txt"
            self.txt = (
                start.gen_mta_cfg()
            )  # the derived class already created the skeleton
            self.reformatted_txt = self.reformat(self.txt)
            logger.info(f"Config name created: {fname}")
            self.original_fname = fname
            self.encoded_fname = self.original_fname.replace(
                ".txt", self.encoded_suffix
            )
        else:
            raise Exception(f"Wrong type {type(start)} received")
        super().init_copy(file_or_obj=self, mibs_paths=mibs_path)

    def encode(self):
        cfg_name = self.file.replace(".txt", ".bin")
        cfg_path = os.path.join(self.dir_path, cfg_name)
        if os.path.isfile(cfg_path):
            os.remove(cfg_path)
        return self.encode_mta(self.mibs_path_arg, self.file_path, cfg_path)

    def load_from_string(self, mta_str_txt: str, name_prefix: str = "") -> None:
        """Load CM cfg from text string (e.g. the file is stored in a multiline
        string).
        :parameter cm_str_txt: s string containing the config file
        :type cm_str_txt: string
        :parameter name: name of config file (optional)
        """
        self.txt = mta_str_txt
        num = self.shortname(10)

        self.original_file = None
        name_prefix = name_prefix or "mta-config"

        self.reformatted_txt = self.reformat(self.txt)

        self.original_fname = f"{name_prefix}-{num}.txt"
        self.encoded_fname = self.original_fname.replace(".txt", self.encoded_suffix)

    def reformat(self, txt: str) -> str:
        """In-case the generic MTA config text needs to be reformatted as per
        Vendor Specific requirements.

        :returns: string, reformatted text
        """
        return txt

    def save(self, full_path: str) -> None:
        path = Path(full_path)
        txt = getattr(self, "reformatted_txt", "") or self.txt
        path.write_text(txt)


# -----------------------------------Library Methods-----------------------------------


def check_board(board, cmts, cm_mac):
    assert board.is_online(), "CM show not OPERATIONAL on console"
    assert (
        cmts.is_cm_online(ignore_partial=True) is True
    ), "CM is not online"  # check cm online on CMTS
    """
    Removing this assert for the time being.
    assert (
        sum(cmts.DUT_chnl_lock(cm_mac)) == cmts.channel_bonding
    ), "CM is in partial service"
    """
    return True


def check_provisioning(board, mta=False):
    """This function is used to validate the provisioning using sha3

    :param board : board device class to fetch different interfaces
    :type board : boardfarm_docsis.devices.Docsis
    :param mta : to check mta cfg
    :type mta : Boolean
    :return value: out
    :return type: Boolean
    """

    # few cmts methods needs to be added before comparing sha3
    # TODO: need to do this
    def validate_cm_side():
        pass

    def _shortname(cfg):
        d = board.get_docsis(cfg)
        ret = d.encode()
        # Though the method requires an arg pylint throws some false positive error, hence added disable
        return keccak512_checksum(ret)  # pylint: disable=E1121

    try:
        sha3_on_board = board.cfg_sha3()
        sha3_on_fw = _shortname(board.cm_cfg)
        logger.debug(sha3_on_board)
        logger.debug(sha3_on_fw)
        out = [sha3_on_board == sha3_on_fw]
        if mta:
            sha3_on_board = board.cfg_sha3(mta)
            sha3_on_fw = _shortname(board.mta_cfg)
            logger.debug(sha3_on_board)
            logger.debug(sha3_on_fw)
            out.append(sha3_on_board == sha3_on_fw)
        return all(out)
    except BftCommandNotFound:
        logger.error("NOTE: Ignoring provisioning check: sha3Sum command not found")
        return True


def check_interface(board, ip, prov_mode="dual", lan_devices=None):
    """This function is used to validate IP addresses for CPEs

    Possible provisioning modes ["none","bridge", "ipv4", "dslite", "dual"]
    Based on these modes validate IP v4/v6 address on e-router iface on board
    Based on these modes validate IP v4/v6 address of CPEs connected to board

    :param board : board device class to fetch different interfaces
    :type board : boardfarm_docsis.devices.Docsis
    :param ip : a dictionary of IP address for all devices calculated by a test
    :type ip : dict
    :param prov_mode : prov_mode against which CPEs are validated
    :type prov_mode : str
    :param lan_devices : list of CPEs connected to board
    :type lan_device : list

    :raises CodeError : if the IP addresses are not validated as per prov_mode
    """
    if lan_devices is None:
        lan_devices = ["lan"]

    # This is only for erouter and CPE interfaces check.
    def _validate_ertr(iface, mode):
        """This function validates if e-router needs to be considered for assertion

        If the prov_mode is none or bridge, do not expect an entry for erouter
        Else expect an entry for erouter
        This function called internally by check_interface

        :param iface : v6 and v4 details of a board's e-router iface
        :type iface : dict
        :param mode : can be IPv4 or IPv6
        :type mode : str

        :raises CodeError : if the IP addresses are not validated as per prov_mode
        """
        version = {"ipv4": ["ipv4", "dual"], "ipv6": ["dslite", "ipv6", "dual"]}

        def check(x):
            if prov_mode in version[mode.lower()]:
                return x
            else:
                return not x

        assert check(
            iface.get(mode.lower(), None)
        ), f"Failed to fetch E-Router {mode}, mode: {prov_mode}"

    def _validate_cpe(mode):
        """This function validates v4/v6 ip-addresses of CPEs based on prov_mode

        This function is called internally by check_interface

        :param mode : can be IPv4 or IPv6
        :type mode : str

        :raises CodeError : if the IP addresses are not validated as per prov_mode
        """
        prov_info = [
            prov for prov in board.config["devices"] if "provisioner" == prov["name"]
        ]
        for dev in lan_devices:
            if prov_mode == "disabled" and mode.lower() == "ipv4":
                if ipaddress.ip_address(
                    ip[dev].get(mode.lower())
                ) in ipaddress.ip_network(prov_info[0]["open_network"]):
                    pass
                else:
                    raise IpAddrMismatch(
                        f"LAN IP {ip[dev].get(mode.lower())} is not in public IP subnet"
                    )
            else:
                assert ip[dev].get(
                    mode.lower(), None
                ), f"Failed to fetch {dev} {mode}, mode: {prov_mode}"

    # Validate IPv4 conditions
    _validate_ertr(ip["board"][board.erouter_iface], "IPv4")
    _validate_cpe("IPv4")

    # validate IPv6 conditions
    _validate_ertr(ip["board"][board.erouter_iface], "IPv6")

    # since aftr iface does not have an IP address/mac address of it's own
    # just validate if the interface exists
    if prov_mode == "ipv6":
        assert board.check_iface_exists(
            board.aftr_iface
        ), f"{board.aftr_iface} interface didn't come up in prov mode : {prov_mode}"
    if prov_mode != "ipv4":
        _validate_cpe("IPv6")  # validate ipv6 for CPEs


def generate_cfg_file(board, test_args, cfg_mode, filename=None, cfg_args=None):
    if not filename:
        filename = cfg_mode + "_config.txt"

    if cfg_args:
        extra_snmp_default_mibs = []
        for dict_name in cfg_args:
            if dict_name in board.cm_cfg.mib_list:
                extra_snmp_default_mibs += eval("board.cm_cfg." + dict_name)
        test_args["extra_snmp"] = extra_snmp_default_mibs

    return board.generate_cfg(cfg_mode, fname=filename, kwargs=test_args)


def configure_board_v2(provisioner, board, test_args, test_data, **kwargs):
    prov_mode = getattr(test_data, "prov_mode", None)
    filename = getattr(test_data, "filename", None)
    cfg_args = getattr(test_data, "cfg_args", None)

    cm_cfg = kwargs.pop("cm_cfg", None)
    mta_cfg = kwargs.pop("mta_cfg", None)

    if not cm_cfg:
        cm_cfg = generate_cfg_file(board, test_args, prov_mode, filename, cfg_args)
    board.update_docsis_config(cm_cfg=cm_cfg, mta_cfg=mta_cfg, **kwargs)
    provisioner.tftp_device = board.tftp_dev
    provisioner.provision_board(board.config)


def check_cm_firmware_version(board, wan, env_helper):
    """Compare CM firmware version with provided enviornment FM version
    checking all images ending with suffix <fm_version>.*
          eg CH7465LG-NCIP-6.12.18.26-3-GA-SH.p7

    :param board : board DUT device class
    :type board : device_type.DUT
    :param wan : wan is wan device type
    :type wan :  device_type.wan
    :param env_helper : device class to fetch different devices
    :type env_helper : boardfarm_docsis.devices.Docsis
    :rtype: Bool
    :raise Assertion: Asserts when CM FM Mismatch or exception
    :return: returns bool True if FM Matches
    """
    if env_helper.has_image():
        fm_ver = env_helper.get_image(mirror=False).rpartition(".")[0]

        if hasattr(board, "check_fw_version"):
            assert board.check_fw_version(fm_ver)
            return True  # is this needed?

        # TODO: remove the following code once clean arch is used
        cm_ip = board.get_interface_ipaddr(board.wan_iface)
        # Though the right arguments passed to the method and the method has return pylint throws some false positive error, hence added disable
        result = retry_on_exception(  # pylint: disable=E1111, E1121
            SnmpHelper.snmp_v2, [wan, cm_ip, "docsDevSwCurrentVers"], 2
        )
        # temporary fix, needs rework  to being vendor independent
        assert (
            result in fm_ver
        ), f"CM FM Version Mismatch current {result} not in requested {fm_ver}"

    return True


def factoryreset(s, board, method="SNMP"):
    """Reset board to Factory Default

    :param s : object with log_to_file attribute for logging
    :type s : TestStep Obj with attribute log_to_file
    :param board : board DUT device class
    :type board : device_type.DUT
    :param method : ("SNMP", "ACS", "CONSOLE") Default to "SNMP"
    :type method : String value with values("SNMP","ACS","CONSOLE")
    :rtype: Bool
    :raise Assertion: Asserts when FactoryReset failed or arg error
    :return: returns bool True if FactoryReset successful
    """
    logger.debug(f"=======Begin FactoryReset via {method}=======")

    try:
        wan = board.dev.by_type(device_type.wan)
        wan_ip = board.get_interface_ipaddr(board.wan_iface)

        if method == "SNMP":
            if not hasattr(s, "cm_wan_ip"):
                s.cm_wan_ip = wan_ip

            # TODO Need to remove dependency on self
            board.reset_defaults_via_snmp(s, wan)
            board.reboot_modem_os_via_snmp(s, wan)

        elif method == "ACS":
            try:
                board.dev.acs_server.FactoryReset()
            except Exception as e:
                logger.error(
                    "Failed: FactoryReset through ACS '{}'"
                    "\n Restarting tr069 and retry Factory Reset again..".format(str(e))
                )
                board.restart_tr069(wan, wan_ip)
                board.dev.acs_server.FactoryReset()

        elif method == "CONSOLE":
            if board.env_helper.has_image():
                cm_fm = board.env_helper.get_image(mirror=False)
                if "nosh" in cm_fm.lower():
                    logger.error(
                        "Failed FactoryReset via CONSOLE on NOSH Image is not possible"
                    )
                    raise CodeError(
                        "Failed FactoryReset via CONSOLE on NOSH Image is not possible"
                    )

            # TODO Need to remove dependency on self
            board.reset_defaults_via_os(s)

        else:
            raise Exception(
                """WrongValue: Pass any value ['SNMP', 'ACS', 'CONSOLE'] for method arg"""
            )
        # Verify CM status and board ip address
        assert "INTEGER: 12" == board.get_cmStatus(
            wan, wan_ip, "INTEGER: 12"
        ), "board cmstatus is down"

        board.check_valid_docsis_ip_networking()

        logger.debug(f"=======End FactoryReset via {method}=======")
        return True

    except Exception as e:
        logger.error(f"Failed Board FactoryReset using '{method}' \n {str(e)}")
        raise BootFail(f"Failed Board FactoryReset: {str(e)}")


def configure_cm_dhcp_server(board, mode="dual", enable=True):
    """Enable/disable board dhcp 4/6 server

    :param board : board DUT device class
    :type board : device_type.DUT
    :param mode : enable/disable board dhcp ipv4/ipv6/dual
                  ["dual" = ipv4 & ipv6,
                   "ipv4" = only ipv4,
                   "ipv6" = only ipv6
                  ]
    :type mode : string
    :param enable : enable/disable cm dhcp server
    :type enable : boolean
    :rtype: boolean
    :raise Assertion: Asserts when ACS RPC  raise exception
    :return: returns bool True if enable/disable ACS RPC successful
             returns bool False if requested operation is already running
    """
    if not board.get_cpeid():
        board.restart_tr069(board.dev.wan, board.get_interface_ipaddr(board.wan_iface))
    r_status = False

    if mode in ["dual", "ipv4"] and (
        enable != board.dev.acs_server.GPV("Device.DHCPv4.Server.Enable")[0]["value"]
    ):
        r_status = (
            board.dev.acs_server.SPV({"Device.DHCPv4.Server.Enable": enable}) == 0
        )

    if mode in ["dual", "ipv6"] and (
        enable != board.dev.acs_server.GPV("Device.DHCPv6.Server.Enable")[0]["value"]
    ):
        r_status = (
            board.dev.acs_server.SPV({"Device.DHCPv6.Server.Enable": enable}) == 0
        )

    return r_status


class docsis(base_cfg):
    """
    Deprecated use base_cfg, eventually this will be removed.
    """

    def __init__(self, *args, **kw):
        deprecate(
            "Warning!",
            message="Use base_cfg to encode/validate the Docsis related files",
            category=UserWarning,
        )
        super().__init__(*args, **kw)


def reprovision_board(device_mgr, boot_file_txt=None, mta_file_txt=None):
    """Full reprovisioning of the board with the given boot file passed as a string.
    The board is then rebooted and expected to come online (on the CMTS side).

    :param device_mgr: the device manager
    :type device_mgr: object
    :param boot_file_txt: a string containing the boot file (not the file name)
    :type boot_file_txt: string (multiline)
    :param mta_file_txt: a string containing the MTA boot file (not the file name)
    :type mta_file_txt: string (multiline)
    """
    if boot_file_txt:
        device_mgr.board.cm_cfg.load_from_string(boot_file_txt)
    if mta_file_txt:
        device_mgr.board.mta_cfg.load_from_string(mta_file_txt)
    device_mgr.board.reprovision(device_mgr.provisioner)
    device_mgr.board.reset()
    device_mgr.cmts.clear_cm_reset(device_mgr.board.cm_mac)
    device_mgr.cmts.wait_for_cm_online(ignore_partial=True, iterations=50)
