#!/usr/bin/env python3
# Copyright (c) 2020
#
# All rights reserved.
#
# This file is distributed under the Clear BSD license.
# The full text can be found in LICENSE in the root directory.
import io
import ipaddress
import logging
import re
import sys
from collections import defaultdict
from datetime import datetime
from time import sleep
from typing import Dict, List, Optional

import netaddr
import pandas as pd
import pexpect
from boardfarm.devices.quagga_router import QuaggaRouter
from boardfarm.exceptions import CodeError, ConnectionRefused, PexpectErrorTimeout
from boardfarm.lib.bft_pexpect_helper import bft_pexpect_helper
from boardfarm.lib.regexlib import AllValidIpv6AddressesRegex, ValidIpv4AddressRegex
from tabulate import tabulate
from termcolor import colored

from boardfarm_docsis.devices.base_devices.cmts_template import CmtsTemplate
from boardfarm_docsis.use_cases.cmts_interactions import is_bpi_privacy_disabled

logger = logging.getLogger("bft")


class MiniCMTS(CmtsTemplate):
    """Connects to and configures a Topvision 1U mini CMTS"""

    prompt = [
        "Topvision(.*)>",
        "Topvision(.*)#",
        r"Topvision\(.*\)#",
        r"Topvision\(.*\)>",
    ]
    model = "mini_cmts"

    def __init__(self, *args, **kwargs) -> None:
        """Constructor method"""
        super().__init__(*args, **kwargs)
        self.conn_cmd = kwargs.get("conn_cmd", None)
        self.connection_type = kwargs.get("connection_type", "local_serial")
        self.ipaddr = kwargs.get("ipaddr", None)
        self.username = kwargs.get("username", "admin")
        self.password = kwargs.get("password", "admin")
        self.password_admin = kwargs.get("password_admin", "admin")
        self.mac_domain = kwargs.get("mac_domain", None)
        self.port = kwargs.get("port", 22)
        self.router_ipaddr = kwargs.get("router_ipaddr", None)
        self.router_username = kwargs.get("router_username", "root")
        self.router_password = kwargs.get("router_password", "bigfoot1")
        self.router_port = kwargs.get("router_port", None)
        if all(
            [
                self.router_ipaddr,
                self.router_username,
                self.router_password,
                self.router_port,
            ]
        ):
            self.__router = QuaggaRouter(
                ipaddr=self.router_ipaddr,
                port=self.router_port,
                username=self.router_username,
                password=self.router_password,
            )
        else:
            self.__router = None

        self.name = kwargs.get("name", "cmts")
        self.connlock = None

    @property
    def _mini_cmts_router(self) -> Optional[QuaggaRouter]:
        """To access mini cmts router object in order to perfrom operations

        mini cmts router access is composed in cmts class as protected and
        will be accessable in usecases using this protected property object.

        :return: protected object of QuaggaRouter class if ip,passwd,user,port
                configs are given else None
        :rtype: QuaggaRouter
        """
        return self.__router

    def connect(self) -> None:
        """This method is used to connect to cmts.
        Login to the cmts based on the connection type available
        :raises Exception: Unable to get prompt on Topvision device
        """
        for run in range(5):
            try:
                bft_pexpect_helper.spawn.__init__(
                    self,
                    command="ssh",
                    args=[
                        f"{self.username}@{self.ipaddr}",
                        "-p",
                        str(self.port),
                        "-o",
                        "StrictHostKeyChecking=no",
                        "-o",
                        "UserKnownHostsFile=/dev/null",
                        "-o",
                        "ServerAliveInterval=60",
                        "-o",
                        "ServerAliveCountMax=5",
                    ],
                )
                try:
                    i = self.expect(
                        [
                            "yes/no",
                            "assword:",
                            "Last login",
                            self.username + ".*'s password:",
                        ]
                        + self.prompt,
                        timeout=30,
                    )
                except PexpectErrorTimeout as err:
                    logger.error(err)
                    raise
                except pexpect.EOF:
                    if hasattr(self, "before"):
                        logger.debug(self.before)
                        raise
            except (PexpectErrorTimeout, pexpect.EOF) as e:
                logger.error(e)
                logger.error(
                    colored(
                        f"Failed to connect to CMTS. Attempt {run+1}",
                        color="red",
                        attrs=["bold"],
                    )
                )
                self.close()
                self.pid = None
                sleep(5)  # take a moment before retrying
                continue
            try:
                self.logfile_read = sys.stdout
                if i == 0:
                    self.sendline("yes")
                    i = self.expect(["Last login", "assword:"])
                if i in [1, 3]:
                    self.sendline(self.password)
                    self.expect(self.prompt[0])
                    self.sendline("enable")
                    self.expect(self.prompt[1])
                    self.additional_setup()
                return
            except pexpect.exceptions.TIMEOUT:
                logger.error(
                    "Unable to get prompt on Topvision mini CMTS device due to timeout."
                )
                self.close()
                self.pid = None
            except pexpect.EOF as e:
                logger.error(
                    "Something went wrong during CMTS initialisation. See exception below:"
                )
                logger.error(repr(e))
                self.close()
                self.pid = None

        raise ConnectionRefused(f"Unable to connect to {self.name}.")

    def check_online(self, cm_mac: str) -> bool:
        """Check the CM status from CMTS
        Function checks the CM mode and returns True if online
        :param cm_mac: mac address of the CM
        :type cm_mac: str
        :return: True if the CM is online False otherwise
        :rtype: boolean
        """
        cm_mac = self.get_cm_mac_cmts_format(cm_mac)
        scm = self._show_cable_modem()
        try:
            result = scm.loc[cm_mac]["MAC_STATE"] in ["online", "w-online(pt)"]
        except KeyError:
            logger.error(f"CM {cm_mac} is not found on cmts.")
            result = False
        return result

    def logout(self) -> None:
        """Logout of the CMTS device"""
        self.sendline("quit")

    @CmtsTemplate.connect_and_run
    def interact(self, escape_character=None, input_filter=None, output_filter=None):
        """To open interact session"""
        super().interact()

    def additional_setup(self):
        """Function to contain additional initialization steps"""
        # Change terminal length to inf in order to avoid pagination
        self.sendline("terminal length 0")
        self.expect(self.prompt[1])
        # Increase connection timeout until better solution
        self.sendline("config terminal")
        self.expect(self.prompt)
        self.sendline("line vty")
        self.expect(self.prompt)
        self.sendline("exec-timeout 60")
        self.expect(self.prompt)
        self.sendline("end")
        self.expect(self.prompt)

    @CmtsTemplate.connect_and_run
    def __run_and_return_df(
        self,
        cmd: str,
        columns: str,
        index: int,
        skiprows: int = 2,
        skipfooter: int = 1,
        dtype: Optional[dict] = None,
    ) -> pd.DataFrame:
        """Internal wrapper for (tabbed output->dataframe) parsing
        :param cmd: cmd to read
        :type cmd: str
        :param columns: name of columns in df (same order as in output)
        :type columns: str
        :param index: column to be dataframe index
        :type index: int
        :param skiprows: how many rows to skip in header
        :type skiproews: int
        :param skipfooter: how many rows to skip in footer
        :type skipfooter: int
        :param dtype: columns
        :types dtypr: dict or None
        :return: parsed dataframe
        """
        output = self.check_output(cmd)
        return pd.read_csv(
            io.StringIO(output),
            skiprows=skiprows,
            skipfooter=skipfooter,
            names=columns,
            header=None,
            delim_whitespace=True,
            engine="python",
            index_col=index,
            dtype=dtype,
        )

    @CmtsTemplate.connect_and_run
    def _show_cable_modem(self, additional_args: str = "") -> pd.DataFrame:
        """Internal api to return scm dataframe"""
        columns = [
            "MAC_ADDRESS",
            "IP_ADDRESS",
            "I/F",
            "MAC_STATE",
            "PRIMARY_SID",
            "RXPWR(dBmV)",
            "TIMING_OFFSET",
            "NUMBER_CPE",
            "BPI_ENABLED",
            "ONLINE_TIME",
        ]
        cmd = f"show cable modem {additional_args}"
        return self.__run_and_return_df(cmd=cmd, columns=columns, index="MAC_ADDRESS")

    @CmtsTemplate.connect_and_run
    def _show_cable_modem_cpe(self, cm_mac: str) -> pd.DataFrame:
        """Internal api to return scm cpe dataframe
        :param cm_mac: mac address of the CM
        :type cm_mac: str
        :return: dataframe"""
        cm_mac = self.get_cm_mac_cmts_format(cm_mac)
        columns = [
            "CPE_MAC",
            "CMC_INDEX",
            "CM_MAC",
            "CPE_IP_ADDRESS",
            "DUAL_IP",
            "CPE_TYPE",
            "LEASE_TIME",
            "LEARNED",
        ]
        cmd = f"show cable modem {cm_mac} cpe"
        return self.__run_and_return_df(
            cmd=cmd, columns=columns, index="CPE_MAC", skiprows=1, skipfooter=6
        )

    @CmtsTemplate.connect_and_run
    def _show_cable_modem_bonded_channels(self, cm_mac: str) -> pd.DataFrame:
        """Internal api to return scm bonded channels dataframe
        :param cm_mac: mac address of the CM
        :type cm_mac: str
        :return: dataframe
        """
        cm_mac = self.get_cm_mac_cmts_format(cm_mac)
        columns = [
            "MAC_ADDRESS",
            "IP_ADDRESS",
            "I/F",
            "MAC_STATE",
            "PRIMARY_SID",
            "UPSTREAM_PRIMARY",
            "DOWNSTREAM_PRIMARY",
        ]
        cm_mac = self.get_cm_mac_cmts_format(cm_mac)
        cmd = f"show cable modem {cm_mac} primary-channel"
        result = self.__run_and_return_df(
            cmd=cmd, columns=columns, index="MAC_ADDRESS", skiprows=2, skipfooter=0
        )
        return result

    def DUT_chnl_lock(self, cm_mac: str) -> List[int]:
        """Return amount of upstream / downstream channels that modem is bonded to
        :param cm_mac: cable modem mac address
        :type cm_mac: str
        :return: [upstream_channels_count, downstream_channels_count]
        """
        cm_mac = self.get_cm_mac_cmts_format(cm_mac)
        scm = self._show_cable_modem_bonded_channels(cm_mac)
        upstream_list = str(scm.loc[cm_mac]["UPSTREAM_PRIMARY"])
        downstream_list = str(scm.loc[cm_mac]["DOWNSTREAM_PRIMARY"])
        # 4(1,2,3,5,6,7,8) 1(2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24)
        upstream_channels_count = len(
            upstream_list.replace("(", ",").replace(")", "").split(",")
        )
        downstream_channels_count = len(
            downstream_list.replace("(", ",").replace(")", "").split(",")
        )
        return [upstream_channels_count, downstream_channels_count]

    @CmtsTemplate.connect_and_run
    def is_cm_online(
        self,
        ignore_bpi: bool = False,
        ignore_partial: bool = False,
        ignore_cpe: bool = False,
    ) -> bool:
        """Returns True if the CM status is operational
        :param ignore_bpi: returns True even when BPI is disabled
        :type ignore_bpi: boolean
        :param ignore_partial: returns True even when the CM is in partial service
        :type ignore_partial: boolean
        :param ignore_cpe: returns True even when LAN<->WAN forwarding is disabled
        :type ignore_cpe: boolean
        :return: True if the CM is operational, False otherwise
        :rtype: boolean
        """
        scm = self._show_cable_modem()
        try:
            status = scm.loc[str(self.board_wan_mac)]["MAC_STATE"]
        except KeyError:
            logger.error(f"CM {self.board_wan_mac} is not found on cmts.")
            raise
        if "offline" in status:
            logger.debug(f"Cable modem is {status}")
            return False
        if "init" in status:
            logger.debug(f"Cable modem is initialising: {status} ")
            return False
        if "online" not in status:
            logger.debug(f"Cable modem in unkown state: {status} ")
            return False
        # now it must be in some sort of online state
        if not ignore_bpi and not re.search(r"online\(p(t|k)", status):
            logger.debug(f"Cable modem in BPI is disabled: {status}")
            return False
        if not ignore_partial and re.search(r"p-online", status):
            logger.debug(f"Cable modem in partial service: {status}")
            return False
        if not ignore_cpe and re.search(r"online\(d", status):
            logger.debug(f"Cable modem is prohibited from forwarding data: {status}")
            return False
        logger.debug(f"Cable modem is online: {status}")
        return True

    @CmtsTemplate.connect_and_run
    def _clear_offline(self, cm_mac: str) -> None:
        """Internal function to clear the CM entry from CMTS"""
        cm_mac = self.get_cm_mac_cmts_format(cm_mac)
        self.sendline(f"clear cable modem {cm_mac} delete")
        self.expect(self.prompt)

    def clear_offline(self, cm_mac: str) -> None:
        """Clear the CM entry from cmts which is offline -clear cable modem <cm_mac> delete
        :param cm_mac: mac address of the CM
        :type cm_mac: str
        """
        self._clear_offline(cm_mac)

    def clear_cm_reset(self, cm_mac: str) -> None:
        """Reset the CM from cmts using cli -clear cable modem <cm_mac> reset
        :param cm_mac: mac address of the CM
        :type cm_mac: str
        """
        self._clear_cm_reset(cm_mac)

    @CmtsTemplate.connect_and_run
    def _clear_cm_reset(self, cm_mac: str) -> None:
        """Internal function to reset the CM from cmts"""
        cm_mac = self.get_cm_mac_cmts_format(cm_mac)
        self.sendline(f"clear cable modem {cm_mac} reset")
        self.expect(self.prompt)

    def get_cmip(self, cm_mac: str) -> Optional[str]:
        """API to get modem IPv4 address
        :param cm_mac: cable modem mac address
        :return: CM ip in case CM is online, None otherwise
        """
        cm_mac = self.get_cm_mac_cmts_format(cm_mac)
        return self._get_cable_modem_ip(cm_mac, ipv6=False)

    def get_cmipv6(self, cm_mac: str) -> Optional[str]:
        """PI to get modem IPv6 address
        :param cm_mac: cable modem mac address
        :return: CM ip in case CM is online, None otherwise
        """
        cm_mac = self.get_cm_mac_cmts_format(cm_mac)
        return self._get_cable_modem_ip(cm_mac, ipv6=True)

    def _get_cable_modem_ip(self, cm_mac: str, ipv6=False) -> str:
        """Internal function to get cable modem ip
        :param cm_mac: mac address of the CM
        :type cm_mac: str
        :param ipv6: flag to return ipv6 address
        :type ipv6: bool
        :return: ip address of cable modem or "None"
        :rtype: string
        """
        # FIXME: BOARDFARM-2422
        if not self.is_cm_online(
            ignore_bpi=is_bpi_privacy_disabled(), ignore_partial=True
        ):
            logger.debug(f"Modem {cm_mac} is not online. Can not get ip.")
            return "None"
        additional_args = "ipv6" if ipv6 else ""
        for _ in range(5):
            scm = self._show_cable_modem(additional_args)
            try:
                ip_str = scm.loc[cm_mac]["IP_ADDRESS"].strip("*")
                ip = netaddr.IPAddress(ip_str)
                break
            except KeyError:
                logger.error(f"CM {cm_mac} is not found on cmts.")
                ip = ""
                break
            except netaddr.core.AddrFormatError:
                ip = ""
                if ip_str == "--":
                    logger.error(f"Modem {cm_mac} offline")
                    break
                logger.error(f"Failed to convert {ip_str}")
                sleep(5)
        else:
            ip = None
        return str(ip)

    def check_partial_service(self, cm_mac: str) -> bool:
        """Check the CM status from CMTS
        Function checks the show cable modem and returns True if p-online
        :param cm_mac: cm mac
        :type cm_mac: str
        :return: True if modem is in partial service, False otherwise
        :rtype: bool
        """
        cm_mac = self.get_cm_mac_cmts_format(cm_mac)
        scm = self._show_cable_modem()
        return "p-online" in scm.loc[cm_mac]["MAC_STATE"]

    def get_cmts_ip_bundle(
        self, cm_mac: Optional[str] = None, gw_ip: Optional[str] = None
    ) -> str:
        """Get CMTS bundle IP, Validate if Gateway IP is configured in CMTS and both are in same network
        The first host address within the network will be assumed to be gateway for Mini CMTS
        :param cm_mac: cm mac
        :type cm_mac: str
        :param gw_ip: gateway ip
        :type gw_ip: str
        :raises assertion error: ERROR: Failed to get the CMTS bundle IP
        :return: gateway ip if address configured on mini cmts else return all ip bundles
        :rtype: str
        """
        return self._get_cmts_ip_bundle(cm_mac=cm_mac, gw_ip=gw_ip)

    @CmtsTemplate.connect_and_run
    def _get_cmts_ip_bundle(
        self, cm_mac: Optional[str] = None, gw_ip: Optional[str] = None
    ) -> str:
        """Internal function to get CMTS bundle IP"""
        if cm_mac:
            cm_mac = self.get_cm_mac_cmts_format(cm_mac)
        cmd = 'show running-config | include "ip address"'
        output = self.check_output(cmd)
        if gw_ip is None:
            return output
        for line in output.splitlines():
            addr, mask = line.split()[2:-1]
            cmts_ip = ipaddress.ip_interface(addr + "/" + mask)
            if gw_ip == str(next(cmts_ip.network.hosts())):
                return gw_ip
        assert 0, "ERROR: Failed to get the CMTS bundle IP"

    def get_qos_parameter(self, cm_mac: str) -> Dict[str, List[dict]]:
        cm_mac = self.get_cm_mac_cmts_format(cm_mac)
        columns = (
            [  # Renamed columns to keep output backward compatible with legacy tests
                "Sfid",
                "SF_REF",
                "Direction",
                "Current State",
                "Sid",
                "Scheduling Type",
                "Traffic Priority",
                "Maximum Sustained rate",
                "Maximum Burst",
                "Minimum Reserved rate",
                "Peak rate",
                "FLAGS",
            ]
        )
        cmd = f"show cable modem {cm_mac} qos"
        qos_response = self.__run_and_return_df(
            cmd=cmd,
            columns=columns,
            index=["Sfid", "Direction"],
            skiprows=3,
            skipfooter=0,
            dtype={"Sid": "object"},
        )
        result = defaultdict(list)
        for key, data in qos_response.to_dict("index").items():
            data.update({"Sfid": str(key[0])})
            result[key[1]].append(data)
        return result

    def get_mtaip(self, cm_mac: str, mta_mac: str = None) -> Optional[str]:
        """Get the MTA IP from CMTS
        :param cm_mac: mac address of the CM
        :type cm_mac: string
        :param mta_mac: mta mac address
        :type mta_mac: string
        :return: MTA ip address or "None" if ip not found
        :rtype: string
        """
        cm_mac = self.get_cm_mac_cmts_format(cm_mac)
        if mta_mac:
            mta_mac = self.get_cm_mac_cmts_format(mta_mac)
        else:
            mta_mac = self.board_mta_mac
        cpe_list = self._show_cable_modem_cpe(cm_mac)
        try:
            mtaip = cpe_list.loc[mta_mac]["CPE_IP_ADDRESS"]
        except KeyError:
            logger.error(f"MTA {mta_mac} is not found on cmts.")
            mtaip = ""
        return mtaip

    def get_cmts_type(self) -> str:
        """This function is to get the product type on cmts
        :return: Returns the cmts module type.
        :rtype: string
        """
        # Hardcoded for now. Didn't find a place to read this info from terminal yet.
        return "CC8800"

    def get_cm_mac_domain(self, cm_mac: str) -> str:
        """API stub. Not supported on Topvision CC8800
        :param cm_mac: CM mac string. Added for compatibility
        :return: empty string
        """
        raise NotImplementedError("Not supported on Topvision")

    def get_center_freq(self, cm_mac: str) -> int:
        """Get center frequency for CM
        :param cm_mac: CM mac address
        :return:CM primary channel center frequency
        """
        cm_mac = self.get_cm_mac_cmts_format(cm_mac)
        scm = self._show_cable_modem()
        primary_sid = scm.loc[cm_mac]["PRIMARY_SID"]
        # Only one ccmts configured for now, so index is hardcoded
        freq_config = self.check_output(
            f'show running-config interface ccmts 1 | include "cable downstream {primary_sid} frequency"'
        )
        # E.g. " cable downstream 1 frequency 440000000 modulation qam256 annex a power-level 25.0"
        return int(freq_config.split(" ")[4])

    def get_ertr_ipv4(self, mac: str, offset: int = 2) -> Optional[str]:
        """Get erouter ipv4 from CMTS
        :param mac: mac address of the cable modem
        :type mac: string
        :param offset: eRouter mac address offset, defaults to 2
        :return: returns ipv4 address of erouter else None
        :rtype: string, None
        """
        cpe = self._show_cable_modem_cpe(mac)
        mac = netaddr.EUI(mac)
        # eRouter mac address is always +2 from CM mac address by convention
        ertr_mac = netaddr.EUI(int(mac) + offset)
        ertr_mac.dialect = netaddr.mac_cisco
        for cpe_mac, cpe_details in cpe.iterrows():
            if cpe_mac == ertr_mac:
                ertr_ipv6 = re.search(
                    ValidIpv4AddressRegex, cpe_details["CPE_IP_ADDRESS"]
                )
                if ertr_ipv6:
                    return ertr_ipv6.group()
        return None

    def get_ertr_ipv6(self, mac: str, offset: int = 2) -> Optional[str]:
        """Get erouter ipv4 from CMTS
        :param mac: mac address of the cable modem
        :type mac: string
        :param offset: eRouter mac address offset, defaults to 2
        :return: returns ipv4 address of erouter else None
        :rtype: string, None
        """
        cpe = self._show_cable_modem_cpe(mac)
        mac = netaddr.EUI(mac)
        # eRouter mac address is always +2 from CM mac address by convention
        ertr_mac = netaddr.EUI(int(mac) + offset)
        ertr_mac.dialect = netaddr.mac_cisco
        for cpe_mac, cpe_details in cpe.iterrows():
            if cpe_mac == ertr_mac:
                ertr_ipv6 = re.search(
                    AllValidIpv6AddressesRegex, cpe_details["CPE_IP_ADDRESS"]
                )
                if ertr_ipv6:
                    return ertr_ipv6.group()
        return None

    def is_cm_bridged(self, mac: str, offset: int = 2) -> bool:
        """Check if the modem is in bridge mode
        :param mac: Mac address of the modem,
        :param offset: eRouter mac address offset, defaults to 2
        :return: True if the modem is bridged mode else False.
        :rtype: boolean
        """

        cpe = self._show_cable_modem_cpe(mac)
        mac = netaddr.EUI(mac)
        # eRouter mac address is always +2 from CM mac address by convention
        ertr_mac = netaddr.EUI(int(mac) + offset)
        ertr_mac.dialect = netaddr.mac_cisco
        return all(cpe_mac != ertr_mac for cpe_mac, _ in cpe.iterrows())

    def _get_current_time(self, fmt: str = "%Y-%m-%dT%H:%M:%S%z") -> str:
        """used for unittests"""
        output = self.check_output("show sys-date")
        # TO DO: get tiem timezone as well
        pattern = r"\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[1-2]\d|3[0-1]) (?:[0-1]\d|2[0-3]):[0-5]\d:[0-5]\d"
        time_now = re.search(pattern, output)
        if time_now:
            return datetime.strptime(time_now.group(0), "%Y-%m-%d %H:%M:%S").strftime(
                fmt
            )
        else:
            raise CodeError("Failed to get CMTS current time")

    @CmtsTemplate.connect_and_run
    def get_current_time(self, fmt: str = "%Y-%m-%dT%H:%M:%S%z") -> str:
        """Returns the current time on the CMTS
        This is full override as the topvision device is a little "different"
        NOTE: this is missing the timezone
        :return: the current time as a string formatted as "YYYY-MM-DD hh:mm:ss"
        :raises CodeError: if anything went wrong in getting the time
        """
        return self._get_current_time(fmt=fmt)

    @CmtsTemplate.connect_and_run
    def ping(self, ping_ip: str, ping_count: int = 4, timeout: int = 4) -> bool:
        """Ping the device from cmts
        :param ping_ip: device ip which needs to be pinged.
        :param ping_count: optional. Number of ping packets.
        :param timeout: optional, seconds. Timeout for each packet.
        :return: True if all ping packets passed else False
        """
        return super().ping(ping_ip=ping_ip, ping_count=ping_count, timeout=timeout)

    def tcpdump_capture(
        self,
        fname: str,
        interface: str = "any",
        additional_args: Optional[str] = None,
    ) -> None:
        """Capture packets from specified interface

        Packet capture using tcpdump utility at a specified interface.

        :param fname: name of the file where packet captures will be stored
        :type fname: str
        :param interface: name of the interface, defaults to "all"
        :type interface: str, optional
        :param additional_args: argument arguments to tcpdump executable, defaults to None
        :type additional_args: Optional[str], optional
        :yield: process id of tcpdump process
        :rtype: None
        """

        if not self.__router:
            raise NotImplementedError(
                "CMTS does not support tcpdump, mini cmts router is required for tcpdump"
            )

        return self.__router.tcpdump_capture(
            fname=fname,
            interface=self.__router.iface_dut,
            additional_args=additional_args,
        )

    def tcpdump_read_pcap(
        self,
        fname: str,
        additional_args: Optional[str] = None,
        timeout: int = 30,
        rm_pcap: bool = False,
    ) -> str:
        """Read packet captures using tcpdump from a device given the file name

        :param fname: name of file to read from
        :type fname: str
        :param additional_args: filter to apply on packet display, defaults to None
        :type additional_args: Optional[str], optional
        :param timeout: time for tcpdump read command to complete, defaults to 30
        :type timeout: int, optional
        :param rm_pcap: if True remove packet capture file after read, defaults to False
        :type rm_pcap: bool, optional
        :return: console output from the command execution
        :rtype: str
        """

        if not self.__router:
            raise NotImplementedError(
                "CMTS does not support tcpdump, mini cmts router is required for tcpdump"
            )

        return self.__router.tcpdump_read_pcap(
            fname=fname,
            additional_args=additional_args,
            timeout=timeout,
            rm_pcap=rm_pcap,
        )

    def tshark_read_pcap(
        self,
        fname: str,
        additional_args: Optional[str] = None,
        timeout: int = 30,
        rm_pcap: bool = False,
    ) -> str:
        """Read packet captures from an existing file

        :param fname: name of the file in which captures are saved
        :type fname: str
        :param additional_args: additional arguments for tshark command to display filtered output, defaults to None
        :type additional_args: Optional[str], optional
        :param timeout: time out for tshark command to be executed, defaults to 30
        :type timeout: int, optional
        :param rm_pcap: If True remove the packet capture file after reading it, defaults to False
        :type rm_pcap: bool, optional
        :return: return tshark read command console output
        :rtype: str
        """

        if not self.__router:
            raise NotImplementedError(
                "CMTS does not support tcpdump, mini cmts router is required for tcpdump"
            )

        return self.__router.tshark_read_pcap(
            fname=fname,
            additional_args=additional_args,
            timeout=timeout,
            rm_pcap=rm_pcap,
        )

    def ip_route(self) -> str:
        """Execute ip router command on cmts router and return output.

        :return: ip route from router object
        :rtype: str
        """
        return self._mini_cmts_router.ip_route()


def print_dataframe(dataframe: pd.DataFrame, column_number=15):
    """Util method to pretty print dataframes to log. Has nothing to do with CMTS itself.
    :param dataframe: dataframe to print
    :param column_number: amount of columns to print in one row
    """
    if dataframe.index.names != [None]:
        index_column_name = ["(" + ", ".join(dataframe.index.names) + ")"]
    else:
        index_column_name = ["INDEX"]
    start_column = 0
    columns_number = len(dataframe.columns)
    end_column = column_number if columns_number > column_number else columns_number
    while start_column != columns_number:
        table_headers = (
            index_column_name + dataframe.columns[start_column:end_column].to_list()
        )
        logger.debug(
            "\n"
            + tabulate(
                dataframe.loc[:, dataframe.columns[start_column:end_column]],
                tablefmt="psql",
                headers=table_headers,
            )
        )
        start_column = end_column
        end_column = (
            end_column + column_number
            if columns_number - end_column > column_number
            else columns_number
        )
