#!/usr/bin/env python3
# Copyright (c) 2020
#
# All rights reserved.
#
# This file is distributed under the Clear BSD license.
# The full text can be found in LICENSE in the root directory.

import logging
import re
import sys
from datetime import datetime
from io import StringIO

import netaddr
import pandas as pd
import pexpect
from boardfarm.devices import connection_decider
from boardfarm.exceptions import CodeError
from boardfarm.lib.regexlib import (
    AllValidIpv6AddressesRegex,
    ValidIpv4AddressRegex,
)
from tabulate import tabulate

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

        if self.conn_cmd is None:
            # TODO: try to parse from ipaddr, etc
            raise Exception("No command specified to connect to Topvision mini CMTS")

        self.connlock = None
        self.name = kwargs.get("name", "mini_cmts")

    @BaseCmts.connect_and_run
    def interact(self):
        super(MiniCMTS, self).interact()

    def connect(self):
        """This method is used to connect to cmts.
        Login to the cmts based on the connection type available

        :raises Exception: Unable to get prompt on Topvision device
        """

        self.connection = connection_decider.connection(
            self.connection_type, device=self, conn_cmd=self.conn_cmd
        )

        self.logfile_read = sys.stdout
        self.connection.connect()
        try:
            if self.expect([pexpect.TIMEOUT, "Username:"]):
                self.sendline(self.username)
                self.expect("Password:")
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
            print(
                "Something went wrong during CMTS initialisation. See exception below:"
            )
            print(repr(e))
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
        self, cmd, columns, index, skiprows=2, skipfooter=1
    ) -> pd.DataFrame:
        """Internal wrapper for (tabbed output->dataframe) parsing

        :param cmd: cmd to read
        :param columns: name of columns in df (same order as in output)
        :param index: column to be dataframe index
        :param skiprows: how many rows to skip in header
        :param skipfooter: how many rows to skip in footer
        :return: parsed dataframe
        """
        output = self.check_output(cmd)
        return pd.read_csv(
            StringIO(output),
            skiprows=skiprows,
            skipfooter=skipfooter,
            names=columns,
            header=None,
            sep=r"\s+",
            engine="python",
            index_col=index,
        )

    def _show_cable_modem(self, additional_args=None) -> pd.DataFrame:
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
        cmd = f"show cable modem {additional_args if additional_args else ''}"
        scm = self.__run_and_return_df(cmd=cmd, columns=columns, index="MAC_ADDRESS")
        return scm

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
        cpe_list = self.__run_and_return_df(
            cmd=cmd, columns=columns, index="CPE_MAC", skiprows=1, skipfooter=6
        )
        return cpe_list

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
            logger.debug("Cable modem is offline")
            return False
        if ignore_bpi is False:
            if not re.search(r"online\(p(t|k)", status):
                logger.debug("Cable modem in BPI is disabled")
                return False
        if ignore_partial is False:
            if re.search(r"p-online", status):
                logger.debug("Cable modem in partial service")
                return False
        if ignore_cpe is False:
            if re.search(r"online\(d", status):
                logger.debug("Cable modem is prohibited from forwarding data")
                return False
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
            print(f"CM {cm_mac} is not found on cmts.")
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

    @BaseCmts.convert_mac_to_cmts_type
    def _get_cable_modem_ip(self, cm_mac: str, ipv6=False) -> [str, None]:
        """Internal function to get cable modem ip

        :param cm_mac: mac address of the CM
        :type cm_mac: str
        :param ipv6: flag to return ipv6 address
        :type ipv6: bool
        :return: ip address of cable modem or "None"
        :rtype: string, None
        """
        if not self.check_online(cm_mac):
            print(f"Modem {cm_mac} is not online. Can not get ip.")
            return None
        additional_args = "ipv6" if ipv6 else ""
        scm = self._show_cable_modem(additional_args)
        try:
            ip = scm.loc[cm_mac]["IP_ADDRESS"].strip("*")
        except KeyError:
            print(f"CM {cm_mac} is not found on cmts.")
            ip = ""
        return ip

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
    def get_cmts_ip_bundle(self) -> [str, None]:
        """Get CMTS bundle IP"""
        # Only one ip bundle present for now on cmts, so just searching for all
        cmd = 'show interface bundle all | include "ip address"'
        output = self.check_output(cmd)
        ipv4 = re.search(ValidIpv4AddressRegex, output)
        if ipv4:
            # Default address is always first one in the output
            return ipv4.group(0)
        else:
            assert 0, "ERROR: Failed to get the CMTS bundle IP"

    @BaseCmts.convert_mac_to_cmts_type
    def get_qos_parameter(self, cm_mac):
        columns = [
            "SFID",
            "SF_REF",
            "DIRECTION",
            "CURR_STATE",
            "SID",
            "SCHED_TYPE",
            "PRORITY",
            "MAX_SUS_RATE",
            "MAX_BURST",
            "MIN_RATE",
            "PEAK_RATE",
            "FLAGS",
        ]
        cmd = f"show cable modem {cm_mac} qos"
        qos_response = self.__run_and_return_df(
            cmd=cmd, columns=columns, index="DIRECTION", skiprows=3, skipfooter=0
        )
        print_dataframe(qos_response)
        return qos_response.to_dict(orient="index")

    @BaseCmts.convert_mac_to_cmts_type
    def get_mtaip(self, cm_mac: str, mta_mac: str) -> str:
        """Get the MTA IP from CMTS

        :param cm_mac: mac address of the CM
        :type cm_mac: string
        :param mta_mac: mta mac address
        :type mta_mac: string
        :return: MTA ip address or "None" if ip not found
        :rtype: string
        """
        cpe_list = self._show_cable_modem_cpe(cm_mac)
        try:
            mtaip = cpe_list.loc[mta_mac]["CPE_IP_ADDRESS"]
        except KeyError:
            print(f"MTA {mta_mac} is not found on cmts.")
            mtaip = ""
        return mtaip

    @BaseCmts.connect_and_run
    def ping(self, ping_ip: str) -> bool:
        """This function to ping the device from cmts
        :param ping_ip: device ip which needs to be verified
        :ping_ip type: string
        :return: True if ping passed else False
        :rtype: bool
        """

        output = self.check_output(f"ping {ping_ip}")
        # Ping command does not have arguments on CC8800, so checking hardcoded
        return "4 packets transmitted, 4 packets received, 0% packet loss" in output

    def run_tcpdump(self, time, iface="any", opts=""):
        """tcpdump capture on the cmts interface

        :param time: timeout to wait till gets prompt
        :type time: integer
        :param iface: any specific interface, defaults to 'any'
        :type iface: string, optional
        :param opts: any other options to filter, defaults to ""
        :type opts: string
        """
        print("TCPDUMP feature is not supported in Topvision CMTS.")

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
        print("Multiple mac domains not supported on Mini CMTS for now.")
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
                    ipv6 = ertr_ipv6.group()
                    return ipv6
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
                    ipv6 = ertr_ipv6.group()
                    return ipv6
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
        for cpe_mac, _ in cpe.iterrows():
            if cpe_mac == ertr_mac:
                return False
        return True

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
        print(
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
