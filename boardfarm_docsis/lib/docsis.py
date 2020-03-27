# Copyright (c) 2015
#
# All rights reserved.
#
# This file is distributed under the Clear BSD license.
# The full text can be found in LICENSE in the root directory.
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import glob
import hashlib
import os
import re
import tempfile

import boardfarm
from aenum import Enum
from boardfarm.lib import SnmpHelper
from boardfarm.lib.common import (cmd_exists, keccak512_checksum,
                                  retry_on_exception)
from boardfarm_docsis.exceptions import (CfgUnknownType, CMCfgEncodeFailed,
                                         MTACfgEncodeFailed)

from .cfg_helper import CfgGenerator

try:
    # Python 2
    import Tkinter
except:
    # Python 3
    import tkinter as Tkinter


class cfg_type(Enum):
    UNKNOWN = 0
    CM = 1
    MTA = 2


class docsis:
    """
    Name: docsis module
    Purpose: docsis operating.
    Input: Absolute path of text file
    Fuction:
        decode():
            return output file name(.txt)
        encode(output_type='cm_cfg')
            return output file name(.cfg or .bin)
    """

    mibs_path_arg = ""

    def __init__(self, file_or_obj, tmpdir=None, mibs_paths=[], board=None):
        # TODO: fix at some point, this tmpdir is already relative to the CM config you
        # are grabbing? Not ideal as that dir might not be writeable, or a tftp or http URL
        # at some point - need to use a real local tmpdir or maybe even results so we can
        # save the resulting artifacts in other tools
        if tmpdir is None:
            tmpdir = tempfile.mkdtemp()

        assert board, "board is a required argument"

        if mibs_paths == []:
            mibs_paths = getattr(board, 'mibs_paths', [])
        if mibs_paths != []:
            default = os.path.expandvars(
                '/home/$USER/.snmp/mibs:/usr/share/snmp/mibs:/usr/share/snmp/mibs/iana:/usr/share/snmp/mibs/ietf:/usr/share/mibs/site:/usr/share/snmp/mibs:/usr/share/mibs/iana:/usr/share/mibs/ietf:/usr/share/mibs/netsnmp'
            )
            mibs_path_arg = "-M " + default

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

        assert cmd_exists('docsis')
        assert cmd_exists('tclsh')
        tclsh = Tkinter.Tcl()
        assert tclsh.eval(
            "package require sha1"), "please run apt-get install tcllib first"

    def get_cfg_type(self):
        with open(self.file_path) as cfg:
            # TODO: this is OK but could be better
            data = cfg.read()
            if data.startswith('Main'):
                return cfg_type.CM
            elif data.startswith('\t.'):
                return cfg_type.MTA
            else:
                return cfg_type.UNKNOWN

    def decode(self):
        if '.cfg' in self.file:
            os.system("docsis -d %s > %s" %
                      (self.file_path, self.file_path.replace('.cfg', '.txt')))
            assert os.path.exists(self.file.replace('.cfg', '.txt'))

            return self.file.replace('.cfg', '.txt')

        # TODO: decode MTA?

    def encode(self, output_type='cm_cfg'):
        def encode_mta():
            mtacfg_name = self.file.replace('.txt', '.bin')
            mtacfg_path = os.path.join(self.dir_path, mtacfg_name)
            if os.path.isfile(mtacfg_path):
                os.remove(mtacfg_path)
            tclsh = Tkinter.Tcl()
            tclsh.eval("source %s/mta_conf_Proc.tcl" %
                       os.path.dirname(__file__))
            tclsh.eval("run [list %s -e -hash eu -out %s]" %
                       (self.file_path, mtacfg_path))
            if not os.path.exists(mtacfg_path):
                raise MTACfgEncodeFailed()

            return mtacfg_path

        def encode_cm():
            cmcfg_name = self.file.replace('.txt', '.cfg')
            cmcfg_path = os.path.join(self.dir_path, cmcfg_name)
            if os.path.isfile(cmcfg_path):
                os.remove(cmcfg_path)
            print("docsis %s -e %s /dev/null %s" %
                  (self.mibs_path_arg, self.file_path, cmcfg_path))
            os.system("docsis %s -e %s /dev/null %s" %
                      (self.mibs_path_arg, self.file_path, cmcfg_path))
            if not os.path.exists(cmcfg_path):
                raise CMCfgEncodeFailed()

            return cmcfg_path

        if output_type == 'mta_cfg':
            return encode_mta()

        if self.get_cfg_type() == cfg_type.CM:
            return encode_cm()
        elif self.get_cfg_type() == cfg_type.MTA:
            return encode_mta()
        else:
            raise CfgUnknownType()

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

        #TODO: we need to have a common lib which marks services running in each device.
        # this needs to be removed at a later point.
        provisioner.tftp_device = board.tftp_dev
        provisioner.provision_board(board.config)

    # This method is old. Added a method on top to calculate sha3.
    @staticmethod
    def validate_modem_cfg_file(board, device):
        '''
        To check if the cfg file used in modem and wan container are same.
        This method is used to compare the sha on the cfg file used in the modem and the one on wan.
        Parameters: (object)board
                    (object)wan

        Returns: (bool) True if sha matches else False.
        '''
        modem_cfg = board.get_modem_cfg_file(
            device.get_interface_ipaddr(device.iface_dut))
        if modem_cfg:
            device.sendline("sha1sum  /tftpboot/tmp/%s /tftpboot/%s" %
                            (modem_cfg, modem_cfg))
            device.expect(device.prompt)
            return (device.before.split("\n")[1].split(" ")[0] ==
                    device.before.split("\n")[2].split(" ")[0])
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
        paths = os.environ['PATH'].split(os.pathsep)
        paths += [
            os.path.dirname(boardfarm.plugins[x].__file__)
            for x in boardfarm.plugins
        ]
        cfg_list = []

        if 'tftp_cfg_files' in board_config:
            for cfg in board_config['tftp_cfg_files']:
                if isinstance(cfg, cm_cfg) or isinstance(cfg, mta_cfg):
                    cfg_list.append(cfg)
                else:
                    for path in paths:
                        cfg_list += glob.glob(path +
                                              '/devices/cm-cfg/%s' % cfg)
        else:
            # TODO: this needs to be removed
            for path in paths:
                cfg_list += glob.glob(path + '/devices/cm-cfg/UNLIMITCASA.cfg')
        cfg_set = set(cfg_list)

        # Copy binary files to tftp server
        for cfg in cfg_set:
            d = cls(cfg, board=board)
            ret = d.encode()
            tftp_device.copy_file_to_server(ret)


class cm_cfg(object):
    '''
    Class for generating CM cfg from nothing, or even importing from a file
    They later need to be encoded via a compiler
    '''

    # TODO: all these names will need to be made up once we don't have
    # an input file anymore
    original_fname = None
    original_file = None
    encoded_suffix = '.cfg'
    encoded_fname = None

    # string representation of cm cfg
    # temporary for starting point
    txt = ""

    # plenty of tests reference a file name, and assume it's in a certain
    # place so let's allow for that for now
    legacy_search_path = None

    def __init__(self, start=None, fname=None):
        '''Creates a default basic CM cfg file for modification'''

        # TODO: we require loading a file for the moment
        if start == None:
            # create a default config file with bare minimum config,
            # no snmp objs, no CVCs, nothing vendor specific!
            # only CM RF minimal config
            # (i.e.: only the RF side configured, no client side, see Prasada)
            if fname is None:
                fname = "default_config.txt"
            start = CfgGenerator()
            start.gen_dual_stack_cfg()
            self.txt = start.generate_cfg(fname)
            self.original_fname = fname
            self.encoded_fname = self.original_fname.replace(
                '.txt', self.encoded_suffix)
        elif type(start) is str:
            # OLD fashined: this is a file name, load the contents from the file
            self.original_file = start
            self.original_fname = os.path.split(start)[1]
            self.encoded_fname = self.original_fname.replace(
                '.txt', self.encoded_suffix)
            self.load(start)
        elif isinstance(start, CfgGenerator):
            # the dynamic configure class has created this config.... (ok not very OOD to
            # have a class type check in the base class....)
            if fname is None:
                # create a name and add some sha256 digits
                fname = "cm-config-" + self.shortname(10) + ".txt"
                print("Config name created: %s" % fname)
            self.txt = start.generate_cfg(
            )  # the derived class already created the skeleton
            self.original_fname = fname
            self.encoded_fname = self.original_fname.replace(
                '.txt', self.encoded_suffix)
        else:
            raise Exception("Wrong type %s received" % type(start))

    def load(self, cm_txt):
        '''Load CM cfg from txt file, for modification'''

        if self.legacy_search_path is not None:
            cm_txt = os.path.join(self.legacy_search_path, cm_txt)

        with open(cm_txt, 'r') as txt:
            self.txt = txt.read()

    def __str__(self):
        '''String repr of CM txt'''
        return self.txt

    def shortname(self, num_digits=None):
        '''short name for displaying in summary'''
        h = hashlib.md5(self.txt.encode()).hexdigest()
        if num_digits:
            h = h[0:num_digits]
        return h

    def save(self, full_path):
        with open(full_path, 'w') as txt:
            txt.write(self.txt)

    def generic_re_sub(self, regex, sub):
        '''Crude function to replace strings in configs, should be replaced with subclasses'''
        saved_txt = self.txt

        self.txt = re.sub(regex, sub, self.txt)

        if saved_txt == self.txt:
            print(
                "WARN: no regex sub was made for %s, to be replaced with %s" %
                (regex, sub))

    def _cm_configmode(self):
        '''function to check config mode in CM'''
        '''0-Disable/Bridge, 1-IPv4, 2-IPv6 (DSlite), 3-IPv4 and IPv6(Dual)'''
        modeset = ['0x010100', '0x010101', '0x010102', '0x010103']
        modestr = ['bridge', 'ipv4', 'dslite', 'dual-stack']
        for mode in range(0, len(modeset)):
            tlv_check = "GenericTLV TlvCode 202 TlvLength 3 TlvValue " + modeset[
                mode]
            initmode_check = "InitializationMode " + str(mode)
            if (tlv_check in self.txt) or (initmode_check in self.txt):
                return modestr[mode]

    cm_configmode = property(_cm_configmode)


class mta_cfg(cm_cfg):
    '''MTA specific class for cfgs'''

    encoded_suffix = '.bin'

    def __init__(self, start=None, fname=None):
        '''
        Creates a default basic mta  cfg file for modification
        '''
        if type(start) is str:
            # OLD fashined: this is a file name, load the contents from the file
            self.original_file = start
            self.original_fname = os.path.split(start)[1]
            self.encoded_fname = self.original_fname.replace(
                '.txt', self.encoded_suffix)
            self.load(start)
        elif isinstance(start, CfgGenerator):
            if fname is None:
                # create a name and add some sha256 digits
                fname = "mta-config-" + self.shortname(10) + ".txt"
            self.txt = start.gen_mta_cfg(
            )  # the derived class already created the skeleton

            high, low = [], []
            for line in self.txt.splitlines():
                if 'pktcSigDevCIDFskAfterRing' in line:
                    low.append(line)
                else:
                    high.append(line)
            self.txt = "\n".join(high + low)
            new_list = self.txt.replace('SnmpMibObject',
                                        '').replace(';',
                                                    '').replace(' ',
                                                                '').split('\n')
            final_list = []
            for val in new_list:
                if val != '':
                    mib_name = val.split()[0].split(".")[0]
                    mib_oid = SnmpHelper.get_mib_oid(mib_name)
                    new_val = val.replace(mib_name, "." + mib_oid)
                    final_list.append(new_val)
            self.txt = '\n'.join(final_list)
            print("Config name created: %s" % fname)
            self.original_fname = fname
            self.encoded_fname = self.original_fname.replace(
                '.txt', self.encoded_suffix)
        else:
            raise Exception("Wrong type %s received" % type(start))


#-----------------------------------Library Methods-----------------------------------


def check_board(board, cmts, cm_mac):

    assert board.is_online(), "CM show not OPERATIONAL on console"
    assert cmts.check_online(
        cm_mac) == True, "CM is not online"  #check cm online on CMTS
    assert sum(cmts.DUT_chnl_lock(
        cm_mac)) == cmts.channel_bonding, "CM is in partial service"

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
    #TODO: need to do this
    def validate_cm_side():
        pass

    # validate_cm_side()

    def _shortname(cfg):
        d = docsis(cfg, board=board)
        ret = d.encode()
        return keccak512_checksum(ret)

    sha3_on_board = board.cfg_sha3()
    sha3_on_fw = _shortname(board.cm_cfg)
    print(sha3_on_board)
    print(sha3_on_fw)
    out = [sha3_on_board == sha3_on_fw]
    if mta:
        sha3_on_board = board.cfg_sha3(mta)
        sha3_on_fw = _shortname(board.mta_cfg)
        print(sha3_on_board)
        print(sha3_on_fw)
        out.append(sha3_on_board == sha3_on_fw)
    return all(out)


def check_interface(board, ip, prov_mode="dual", lan_devices=["lan"]):
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
        version = {"ipv4": ["ipv4", "dual"], "ipv6": ["dslite", "dual"]}
        check = lambda x: x if prov_mode in version[mode.lower()] else not x
        assert check(
            iface.get(mode.lower(),
                      None)), "Failed to fetch E-Router {}, mode: {}".format(
                          mode, prov_mode)

    def _validate_cpe(mode):
        """This function validates v4/v6 ip-addresses of CPEs based on prov_mode

        This function is called internally by check_interface

        :param mode : can be IPv4 or IPv6
        :type mode : str

        :raises CodeError : if the IP addresses are not validated as per prov_mode
        """
        for dev in lan_devices:
            assert ip[dev].get(mode.lower(),
                               None), "Failed to fetch {} {}, mode: {}".format(
                                   dev, mode, prov_mode)

    # Validate IPv4 conditions
    _validate_ertr(ip["board"][board.erouter_iface], "IPv4")
    _validate_cpe("IPv4")

    # validate IPv6 conditions
    _validate_ertr(ip["board"][board.erouter_iface], "IPv6")

    # since aftr iface does not have an IP address/mac address of it's own
    # just validate if the interface exists
    if prov_mode == "dslite":
        assert board.check_iface_exists(board.aftr_iface), \
                "{} interface didn't come up in prov mode : {}".format(board.aftr_iface, prov_mode)
    if prov_mode != "ipv4": _validate_cpe("IPv6")  # validate ipv6 for CPEs


def generate_cfg_file(board,
                      test_args,
                      cfg_mode,
                      filename=None,
                      cfg_args=None):
    if not filename:
        filename = cfg_mode + "_config.txt"

    if cfg_args:
        extra_snmp_default_mibs = []
        for dict_name in cfg_args:
            if dict_name in board.cm_cfg.mib_list:
                extra_snmp_default_mibs += eval("board.cm_cfg." + dict_name)
        test_args["extra_snmp"] = extra_snmp_default_mibs

    cfg_file = board.generate_cfg(cfg_mode, fname=filename, kwargs=test_args)
    return cfg_file


def configure_board_v2(provisioner, board, test_args, test_data, **kwargs):
    prov_mode = getattr(test_data, "prov_mode", None)
    filename = getattr(test_data, "filename", None)
    cfg_args = getattr(test_data, "cfg_args", None)

    cm_cfg = kwargs.pop("cm_cfg", None)
    mta_cfg = kwargs.pop("mta_cfg", None)

    if not cm_cfg:
        cm_cfg = generate_cfg_file(board, test_args, prov_mode, filename,
                                   cfg_args)
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
        cm_ip = board.get_interface_ipaddr(board.wan_iface)
        result = retry_on_exception(SnmpHelper.snmp_v2,
                                    [wan, cm_ip, 'docsDevSwCurrentVers'],
                                    retries=2)
        # temporary fix, needs rework  to being vendor independent
        assert result in fm_ver, "CM FM Version Mismatch current {} not in requested {}".format(
            result, fm_ver)

    return True
