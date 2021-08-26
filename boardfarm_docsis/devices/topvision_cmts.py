#!/usr/bin/env python3
# Copyright (c) 2020
#
# All rights reserved.
#
# This file is distributed under the Clear BSD license.
# The full text can be found in LICENSE in the root directory.

import ipaddress
import logging
import re
import sys
from collections import defaultdict
from datetime import datetime
from io import StringIO
from typing import Dict, List, Optional

import netaddr
import pandas as pd
import pexpect
from boardfarm.exceptions import CodeError, PexpectErrorTimeout
from boardfarm.lib.bft_pexpect_helper import bft_pexpect_helper
from boardfarm.lib.regexlib import AllValidIpv6AddressesRegex, ValidIpv4AddressRegex
from tabulate import tabulate
from termcolor import colored

from .base_cmts import BaseCmts

logger = logging.getLogger("bft")


class MiniCMTS(BaseCmts):
    """Connects to and configures a Topvision 1U mini CMTS"""

    prompt = [
        "Topvision(.*)>",
        "Topvision(.*)#",
        r"Topvision\(.*\)#",
        r"Topvision\(.*\)>",
    ]
    model = "mini_cmts"

    def __init__(self, *args, **kwargs):
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

        self.connlock = None
        self.name = kwargs.get("name", "cmts")

    @BaseCmts.connect_and_run
    def interact(self):
        super().interact()

    def connect(self):
        """This method is used to connect to cmts.
        Login to the cmts based on the connection type available

        :raises Exception: Unable to get prompt on Topvision device
        """

        for run in range(3):
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
                    break
                except PexpectErrorTimeout:
                    raise Exception(f"Unable to connect to {self.name}.")
                except pexpect.EOF:
                    if hasattr(self, "before"):
                        logger.debug(self.before)
                        raise Exception(f"Unable to connect to {self.name}.")

            except Exception as e:
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
        else:
            raise Exception(f"Unable to connect to {self.name}.")
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
            raise Exception(
                "Unable to get prompt on Topvision mini CMTS device due to timeout."
            )
        except Exception as e:
            logger.error(
                "Something went wrong during CMTS initialisation. See exception below:"
            )
            logger.error(repr(e))
            raise e

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

    def logout(self):
        """Logout of the CMTS device"""
        self.sendline("quit")

    @BaseCmts.connect_and_run
    def __run_and_return_df(
        self, cmd, columns, index, skiprows=2, skipfooter=1, dtype=None
    ) -> pd.DataFrame:
        """Internal wrapper for (tabbed output->dataframe) parsing

        :param cmd: cmd to read
        :param columns: name of columns in df (same order as in output)
        :param index: column to be dataframe index
        :param skiprows: how many rows to skip in header
        :param skipfooter: how many rows to skip in footer
        :param dtype: columns types dict
        :return: parsed dataframe
        """
        output = self.check_output(cmd)
        return pd.read_csv(
            StringIO(output),
            skiprows=skiprows,
            skipfooter=skipfooter,
            names=columns,
            header=None,
            delim_whitespace=True,
            engine="python",
            index_col=index,
            dtype=dtype,
        )

    def _show_cable_modem(self, additional_args="") -> pd.DataFrame:
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

    @BaseCmts.convert_mac_to_cmts_type
    def _show_cable_modem_cpe(self, cm_mac: str) -> pd.DataFrame:
        """Internal api to return scm cpe dataframe"""
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

    @BaseCmts.convert_mac_to_cmts_type
    def _show_cable_modem_bonded_channels(self, cm_mac: str) -> pd.DataFrame:
        """Internal api to return scm bonded channels dataframe"""
        columns = [
            "MAC_ADDRESS",
            "IP_ADDRESS",
            "I/F",
            "MAC_STATE",
            "PRIMARY_SID",
            "UPSTREAM_PRIMARY",
            "DOWNSTREAM_PRIMARY",
        ]
        cmd = f"show cable modem {cm_mac} primary-channel"
        result = self.__run_and_return_df(
            cmd=cmd, columns=columns, index="MAC_ADDRESS", skiprows=2, skipfooter=0
        )
        return result

    @BaseCmts.convert_mac_to_cmts_type
    def DUT_chnl_lock(self, cm_mac: str) -> List[int]:
        """Return amount of upstream / downstream channels that modem is bonded to

        :param cm_mac: cable modem mac address
        :return: [upstream_channels_count, downstream_channels_count]
        """
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

    @BaseCmts.connect_and_run
    def is_cm_online(self, ignore_bpi=False, ignore_partial=False, ignore_cpe=False):
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
            raise CodeError

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
        if ignore_bpi is False and not re.search(r"online\(p(t|k)", status):
            logger.debug(f"Cable modem in BPI is disabled: {status}")
            return False
        if ignore_partial is False and re.search(r"p-online", status):
            logger.debug(f"Cable modem in partial service: {status}")
            return False
        if ignore_cpe is False and re.search(r"online\(d", status):
            logger.debug(f"Cable modem is prohibited from forwarding data: {status}")
            return False
        logger.debug(f"Cable modem is online: {status}")
        return True

    @BaseCmts.convert_mac_to_cmts_type
    def check_online(self, cm_mac: str) -> bool:
        """Check the CM status from CMTS
        Function checks the CM mode and returns True if online

        :param cm_mac: mac address of the CM
        :type cm_mac: str
        :return: True if the CM is online False otherwise
        :rtype: boolean
        """
        scm = self._show_cable_modem()
        try:
            result = scm.loc[cm_mac]["MAC_STATE"] in ["online", "w-online(pt)"]
        except KeyError:
            logger.error(f"CM {cm_mac} is not found on cmts.")
            result = False
        return result

    @BaseCmts.convert_mac_to_cmts_type
    @BaseCmts.connect_and_run
    def clear_offline(self, cm_mac: str) -> None:
        """Clear the CM entry from cmts which is offline -clear cable modem <cm_mac> delete
        :param cm_mac: mac address of the CM
        :type cm_mac: str
        """
        self.sendline(f"clear cable modem {cm_mac} delete")
        self.expect(self.prompt)

    @BaseCmts.convert_mac_to_cmts_type
    @BaseCmts.connect_and_run
    def clear_cm_reset(self, cm_mac: str) -> None:
        """Reset the CM from cmts using cli -clear cable modem <cm_mac> reset

        :param cm_mac: mac address of the CM
        :type cm_mac: str
        """
        self.sendline(f"clear cable modem {cm_mac} reset")
        self.expect(self.prompt)

    @BaseCmts.convert_mac_to_cmts_type
    def get_cmip(self, cm_mac: str) -> [str, None]:
        """API to get modem IPv4 address

        :param cm_mac: cable modem mac address
        :return: CM ip in case CM is online, None otherwise
        """
        return self._get_cable_modem_ip(cm_mac, ipv6=False)

    @BaseCmts.convert_mac_to_cmts_type
    def get_cmipv6(self, cm_mac: str) -> [str, None]:
        """PI to get modem IPv6 address

        :param cm_mac: cable modem mac address
        :return: CM ip in case CM is online, None otherwise
        """
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
        if not self.is_cm_online(ignore_partial=True):
            logger.debug(f"Modem {cm_mac} is not online. Can not get ip.")
            return "None"
        additional_args = "ipv6" if ipv6 else ""
        scm = self._show_cable_modem(additional_args)
        try:
            ip_str = scm.loc[cm_mac]["IP_ADDRESS"].strip("*")
            ip = netaddr.IPAddress(ip_str)
        except KeyError:
            logger.error(f"CM {cm_mac} is not found on cmts.")
            ip = ""
        except netaddr.core.AddrFormatError:
            ip = ""
            msg = (
                "Modem {cm_mac} offline"
                if ip_str == "--"
                else f"Failed to convert {ip_str}"
            )
            logger.error(msg)
        return str(ip)

    @BaseCmts.convert_mac_to_cmts_type
    def check_partial_service(self, cm_mac: str) -> bool:
        """Check the CM status from CMTS
        Function checks the show cable modem and returns True if p-online

        :param cm_mac: cm mac
        :type cm_mac: str
        :return: True if modem is in partial service, False otherwise
        :rtype: bool
        """
        scm = self._show_cable_modem()
        return "p-online" in scm.loc[cm_mac]["MAC_STATE"]

    @BaseCmts.connect_and_run
    def get_cmts_ip_bundle(self, cm_mac: str = None, gw_ip: str = None) -> [str]:
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

    @BaseCmts.convert_mac_to_cmts_type
    def get_qos_parameter(self, cm_mac) -> Dict[str, List[dict]]:
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

    @BaseCmts.convert_mac_to_cmts_type
    def get_mtaip(self, cm_mac: str, mta_mac: str = None) -> str:
        """Get the MTA IP from CMTS

        :param cm_mac: mac address of the CM
        :type cm_mac: string
        :param mta_mac: mta mac address
        :type mta_mac: string
        :return: MTA ip address or "None" if ip not found
        :rtype: string
        """
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

    @BaseCmts.connect_and_run
    def ping(
        self,
        ping_ip: str,
        ping_count: Optional[int] = 4,
        timeout: Optional[int] = 4,
    ) -> bool:
        """Ping the device from cmts
        :param ping_ip: device ip which needs to be pinged.
        :param ping_count: optional. Number of ping packets.
        :param timeout: optional, seconds. Timeout for each packet.
        :return: True if all ping packets passed else False
        """
        timeout = (
            timeout * 1000
        )  # Convert timeout from seconds to milliseconds for backward compatibility
        command_timeout = (ping_count * timeout) / 1000 + 5  # Seconds
        output = self.check_output(
            f"ping {ping_ip} timeout {timeout} pktnum {ping_count}",
            timeout=command_timeout,
        )
        match = re.search(
            f"{ping_count} packets transmitted, {ping_count} packets received", output
        )
        return bool(match)

    def run_tcpdump(self, time, iface="any", opts=""):
        """tcpdump capture on the cmts interface

        :param time: timeout to wait till gets prompt
        :type time: integer
        :param iface: any specific interface, defaults to 'any'
        :type iface: string, optional
        :param opts: any other options to filter, defaults to ""
        :type opts: string
        """
        logger.error("TCPDUMP feature is not supported in Topvision CMTS.")

    def get_cmts_type(self):
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
        logger.error("Multiple mac domains not supported on Mini CMTS for now.")
        return ""

    @BaseCmts.convert_mac_to_cmts_type
    @BaseCmts.connect_and_run
    def get_center_freq(self, cm_mac: str) -> int:
        """Get center frequency for CM

        :param cm_mac: CM mac address
        :return:CM primary channel center frequency
        """
        scm = self._show_cable_modem()
        primary_sid = scm.loc[cm_mac]["PRIMARY_SID"]
        # Only one ccmts configured for now, so index is hardcoded
        freq_config = self.check_output(
            f'show running-config interface ccmts 1 | include "cable downstream {primary_sid} frequency"'
        )
        # E.g. " cable downstream 1 frequency 440000000 modulation qam256 annex a power-level 25.0"
        return int(freq_config.split(" ")[4])

    def get_ertr_ipv4(self, mac: str, offset=2) -> [str, None]:
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

    def get_ertr_ipv6(self, mac: str, offset=2) -> [str, None]:
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

    def is_cm_bridged(self, mac, offset=2):
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

    def _get_current_time(self, fmt="%Y-%m-%dT%H:%M:%S%z"):
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

    @BaseCmts.connect_and_run
    def get_current_time(self, fmt="%Y-%m-%dT%H:%M:%S%z"):
        """Returns the current time on the CMTS
        This is full override as the topvision device is a little "different"
        NOTE: this is missing the timezone

        :return: the current time as a string formatted as "YYYY-MM-DD hh:mm:ss"
        :raises CodeError: if anything went wrong in getting the time
        """
        return self._get_current_time(fmt=fmt)


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
