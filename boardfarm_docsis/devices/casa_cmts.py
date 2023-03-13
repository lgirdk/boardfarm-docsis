#!/usr/bin/env python3
# Copyright (c) 2018
#
# All rights reserved.
#
# This file is distributed under the Clear BSD license.
# The full text can be found in LICENSE in the root directory.
import collections
import ipaddress
import logging
import re
import sys
from collections import defaultdict
from ipaddress import IPv4Address, IPv6Address
from typing import Any, Dict, List, Optional

import netaddr
import pexpect
from boardfarm.devices import connection_decider
from boardfarm.lib.regexlib import AllValidIpv6AddressesRegex, ValidIpv4AddressRegex

from boardfarm_docsis.devices.base_devices.cmts_template import CmtsTemplate

logger = logging.getLogger("bft")


class CasaCMTS(CmtsTemplate):
    """Connects to and configures a CASA CMTS"""

    prompt = [
        "CASA-C3200>",
        "CASA-C3200#",
        r"CASA-C3200\(.*\)#",
        "CASA-C3000>",
        "CASA-C3000#",
        r"CASA-C3000\(.*\)#",
        "CASA-C10G>",
        "CASA-C10G#",
        r"CASA-C10G\(.*\)#",
        "CASA-C2200>",
        "CASA-C2200#",
        r"CASA-C2200\(.*\)#",
    ]
    model = "casa_cmts"

    def __init__(self, *args, **kwargs) -> None:
        """Constructor method"""
        # self.before is set to empty str to avoid the pylint unsupported-membership-test
        self.before = ""
        super().__init__(*args, **kwargs)
        conn_cmd = kwargs.get("conn_cmd", None)
        connection_type = kwargs.get("connection_type", "local_serial")
        self.ipaddr = kwargs.get("ipaddr", None)
        self.username = kwargs.get("username", "root")
        self.password = kwargs.get("password", "casa")
        self.password_admin = kwargs.get("password_admin", "casa")
        self.mac_domain = kwargs.get("mac_domain", None)
        self.channel_bonding = kwargs.get("channel_bonding", 24)  # 16x8 : total 24
        if conn_cmd is None:
            # TODO: try to parse from ipaddr, etc
            raise Exception("No command specified to connect to Casa CMTS")
        self.connection = connection_decider.connection(
            connection_type, device=self, conn_cmd=conn_cmd, password=self.password
        )
        if kwargs.get("debug", False):
            self.logfile_read = sys.stdout
        self.connection.connect()
        self.connect()
        self.logfile_read = sys.stdout
        self.name = kwargs.get("name", "casa_cmts")

    def connect(self) -> None:
        """This method is used to connect cmts.
        Login to the cmts based on the connection type available
        :raises Exception: Unable to get prompt on CASA device
        """
        try:
            self.sendline()
            result = self.expect(
                ["\r\n(.*) login:", "(.*) login:", pexpect.TIMEOUT] + self.prompt
            )
            if result == 0 or result == 1:
                hostname = (
                    self.match.group(1).replace("\n", "").replace("\r", "").strip()
                )
                self.prompt.append(hostname + ">")
                self.prompt.append(hostname + "#")
                self.prompt.append(hostname + r"\(.*\)#")
                self.sendline(self.username)
                self.expect("assword:")
                self.sendline(self.password)
                self.expect(self.prompt)
            elif result == 2:
                # Over telnet we come in at the right prompt
                # over serial it could be stale so we try to recover
                self.sendline("q")
                self.sendline("exit")
                self.expect([pexpect.TIMEOUT] + self.prompt, timeout=20)
            self.sendline("enable")
            if 0 == self.expect(["Password:"] + self.prompt):
                self.sendline(self.password_admin)
                self.expect(self.prompt)
            self.sendline("config")
            self.expect(self.prompt)
            self.sendline("page-off")
            self.expect(self.prompt)
            return
        except Exception:
            raise Exception("Unable to get prompt on CASA device")

    def logout(self) -> None:
        """Logout of the CMTS device"""
        self.sendline("exit")
        self.sendline("exit")

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
        b = self.check_output(f"show cable modem {self.board_wan_mac}")
        if "offline cm 1" in b:
            return False
        if ignore_bpi is False:
            if not re.search(r"online\(p(t|k)", b):
                return False
        if ignore_partial is False:
            if self.check_PartialService(self.board_wan_mac) == 1:
                logger.debug("Cable modem in partial service")
                return False
        if ignore_cpe is False:
            if re.search(r"online\(d", b) or re.search(r"online\(p.d", b):
                return False
        return True

    def check_online(self, cm_mac: str) -> bool:
        """Check the CM status from CMTS
        Function checks the encryption mode and returns True if online
        :param cm_mac: mac address of the CM
        :type cm_mac: string
        :raises assert:  incorrect cmstatus in cmts
        :return: True if the CM is operational else actual status on cmts
        :rtype: boolean or string
        """
        cm_mac = self.get_cm_mac_cmts_format(cm_mac)
        self.sendline(f"show cable modem {cm_mac}")
        self.expect(r".+ranging cm \d+")
        result = self.match.group()
        match = re.search(
            r"\d+/\d+/\d+\**\s+([^\s]+)\s+\d+\s+.+\d+\s+(\w+)\r\n", result
        )
        if match:
            status = match.group(1)
            encrytion = match.group(2)
            if status == "online(pt)" and encrytion == "yes":
                output = True
            elif status == "online" and encrytion == "no":
                output = True
            elif "online" not in status and status is not None:
                output = status
            else:
                assert 0, (
                    'ERROR: incorrect cmstatus "'
                    + status
                    + '" in cmts for bpi encrytion "'
                    + encrytion
                    + '"'
                )
        else:
            assert 0, "ERROR: Couldn't fetch CM status from cmts"
        self.expect(self.prompt)
        return output

    def clear_offline(self, cm_mac: str) -> None:
        """Clear the CM entry from cmts which is offline -clear cable modem <mac> offline
        :param cm_mac: mac address of the CM
        :type cm_mac: string
        """
        cm_mac = self.get_cm_mac_cmts_format(cm_mac)
        if "c3000" in self._get_cmts_type():
            logger.error(
                "clear offline feature is not supported on casa product name c3000"
            )
            return
        self.sendline(f"clear cable modem {cm_mac} offline")
        self.expect(self.prompt)

    def clear_cm_reset(self, cm_mac: str) -> None:
        """Reset the CM from cmts using cli -clear cable modem <mac> reset
        :param cm_mac: mac address of the CM
        :type cm_mac: string
        """
        cm_mac = self.get_cm_mac_cmts_format(cm_mac)
        self.sendline(f"clear cable modem {cm_mac} reset")
        self.expect(self.prompt)
        online_state = self.check_online(cm_mac)
        self.expect(pexpect.TIMEOUT, timeout=5)
        if online_state is True:
            logger.debug("CM is still online after 5 seconds.")
        else:
            logger.debug("CM reset is initiated.")

    def check_partial_service(self, cm_mac: str) -> bool:
        """Check the cable modem is in partial service
        :param cm_mac: mac address of the CM
        :type cm_mac: string
        :return: 1 if is true else return the value as 0
        :rtype: integer
        """
        cm_mac = self.get_cm_mac_cmts_format(cm_mac)
        return (
            False if (sum(self.DUT_chnl_lock(cm_mac)) == self.channel_bonding) else True
        )

    def get_cmip(self, cm_mac: str) -> Optional[str]:
        """Get the IP of the Cable modem from CMTS
        :param cm_mac: mac address of the CM
        :type cm_mac: string
        :return: ip address of cable modem or "None"
        :rtype: string
        """
        cm_mac = self.get_cm_mac_cmts_format(cm_mac)
        self.sendline(f"show cable modem {cm_mac}")
        self.expect(cm_mac + r"\s+(" + ValidIpv4AddressRegex + "+)")
        output = "None"
        if self.match and self.match.group(1) != "0.0.0.0":
            output = self.match.group(1)
        self.expect(self.prompt)
        return output

    def get_cmipv6(self, cm_mac: str) -> Optional[str]:
        """Get IPv6 address of the Cable modem from CMTS
        :param cm_mac: mac address of the CM
        :type cm_mac: string
        :return: ipv6 address(str) of cable modem or "None"
        :rtype: string
        """
        cm_mac = self.get_cm_mac_cmts_format(cm_mac)
        self.sendline(f"show cable modem {cm_mac}")
        self.expect(self.prompt)
        match = re.search(AllValidIpv6AddressesRegex, self.before)
        if match:
            output = match.group(0)
        else:
            output = "None"
        return output

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
        self.sendline(f"show cable modem {cm_mac} cpe")
        self.expect(r"([\d\.]+)\s+dhcp\s+" + str(mta_mac))
        result = self.match.group(1)
        if self.match is not None:
            output = result
        else:
            output = "None"
        self.expect(self.prompt)
        return output

    def DUT_chnl_lock(self, cm_mac: str) -> List[int]:
        """Check the CM channel locks based on cmts type
        :param cm_mac: mac address of the CM
        :type cm_mac: string
        :returns: Locked channels of downstream and upstream
        :rtype: list
        """
        cm_mac = self.get_cm_mac_cmts_format(cm_mac)
        streams = ["Upstream", "Downstream"]
        channel_list = []
        for stream in streams:
            self.sendline(
                f'show cable modem {cm_mac} verbose | inc "{stream} Channel Set"'
            )
            self.expect(self.prompt)
            if stream == "Upstream":
                match = re.search(r"(\d+/\d+.\d+/\d+).+", self.before)
            elif stream == "Downstream":
                match = re.search(r"(\d+/\d+/\d+).+", self.before)
            if match:
                channel = len(match.group().split(","))
                channel_list.append(channel)
        return channel_list

    def get_cm_bundle(self, mac_domain: str) -> str:
        """Get the bundle id from cable modem
        :param mac_domain: Mac_domain of the cable modem
        :type mac_domain: string
        :raises assert: Failed to get the CM bundle id from CMTS
        :return: bundle id
        :rtype: string
        """
        self.sendline("show interface docsis-mac " + mac_domain + ' | i "ip bundle"')
        index = self.expect(["(ip bundle)[ ]{1,}([0-9]|[0-9][0-9])"] + self.prompt)
        if index != 0:
            assert 0, "ERROR:Failed to get the CM bundle id from CMTS"
        bundle = self.match.group(2)
        self.expect(self.prompt)
        return bundle

    def get_cm_mac_domain(self, cm_mac: Optional[str]) -> str:
        """Get the Mac-domain of Cable modem
        :param cm_mac: mac address of the CM
        :type cm_mac: string
        :raises assert: Failed to get the CM mac domain from CMTS
        :return: mac_domain of the particular cable modem
        :rtype: string
        """
        cm_mac = self.get_cm_mac_cmts_format(cm_mac)
        self.sendline("show cable modem " + str(cm_mac) + ' verbose | i "MAC Domain"')
        idx = self.expect([r"(MAC Domain)[ ]{2,}\:([0-9]|[0-9][0-9])"] + self.prompt)
        if idx != 0:
            assert 0, "ERROR: Failed to get the CM Mac Domain from the CMTS"
        mac_domain = self.match.group(2)
        self.expect(self.prompt)
        return mac_domain

    def get_cmts_ip_bundle(
        self, cm_mac: Optional[str] = None, gw_ip: Optional[str] = None
    ) -> str:
        """Get CMTS bundle IP
        to get a gw ip, use get_gateway_address from mv1.py(board.get_gateway_address())
        :param cm_mac: mac address of the CM
        :type cm_mac: string
        :raises assert: ERROR: Failed to get the CMTS bundle IP
        :return: returns cmts ip configured on the bundle
        :rtype: string
        """
        mac_domain = self.get_cm_mac_domain(cm_mac)
        bundle_id = self.get_cm_bundle(mac_domain)
        self.sendline(f"show interface ip-bundle {bundle_id} | i secondary")
        self.expect(self.prompt)
        if gw_ip is None:
            return self.before
        cmts_ip_match = re.search(f"ip address ({gw_ip}) .* secondary", self.before)
        if cmts_ip_match:
            cmts_ip = cmts_ip_match.group(1)
        else:
            assert 0, "ERROR: Failed to get the CMTS bundle IP"
        return str(cmts_ip)

    def reset(self) -> None:
        """Delete the startup config and Reboot the CMTS"""
        self.sendline("exit")
        self.expect(self.prompt)
        self.sendline("del startup-config")
        self.expect("Please type YES to confirm deleting startup-config:")
        self.sendline("YES")
        self.expect(self.prompt)
        self.sendline("system reboot")
        if 0 == self.expect(
            [
                r"Proceed with reload\? please type YES to confirm :",
                "starting up console shell ...",
            ],
            timeout=180,
        ):
            self.sendline("YES")
            self.expect("starting up console shell ...", timeout=150)
        self.sendline()
        self.expect(self.prompt)
        self.sendline("page-off")
        self.expect(self.prompt)
        self.sendline("enable")
        self.expect("Password:")
        self.sendline(self.password)
        self.expect(self.prompt)
        self.sendline("config")
        self.expect(self.prompt)

    def wait_for_ready(self) -> None:
        """Check the cmts status"""
        self.sendline("show system")
        while 0 == self.expect(["NotReady"] + self.prompt):
            self.expect(self.prompt)
            self.expect(pexpect.TIMEOUT, timeout=5)
            self.sendline("show system")

    def save_running_to_startup_config(self) -> None:
        """save the running config to startup"""
        self.sendline("exit")
        self.expect(self.prompt)
        self.sendline("copy running-config startup-config")
        self.expect(self.prompt)
        self.sendline("config")
        self.expect(self.prompt)

    def save_running_config_to_local(self, filename: str) -> None:
        """Saves the running config to a file on the local machine"""
        self.sendline("show running-config")
        self.expect("show running-config")
        self.expect(self.prompt)
        f = open(filename, "w")
        f.write(self.before)
        f.close()

    def set_iface_ipaddr(self, iface: str, ipaddr: IPv4Address) -> None:
        """This function sets the ipv4 address of an interface on the cmts
        :param iface: interface name
        :type iface: string
        :param ipaddr: <ip></><subnet> using 24 as default if subnet is not provided.
        :type ipaddr: string
        """
        self.sendline(f"interface {iface}")
        self.expect(self.prompt)
        self.sendline(f"ip address {str(ipaddr)}/24")
        self.expect(self.prompt)
        self.sendline("no shutdown")
        self.expect(self.prompt)
        self.sendline("exit")
        self.expect(self.prompt)

    def set_iface_ipv6addr(self, iface: str, ipaddr: IPv6Address) -> None:
        """This function sets the ipv6 address of an interface on the cmts
        :param iface: interface name
        :type iface: string
        :param ipaddr: ipaddress to configure
        :type ipaddr: string
        """
        self.sendline(f"interface {iface}")
        self.expect(self.prompt)
        self.sendline(f"ipv6 address {str(ipaddr)}")
        self.expect(self.prompt)
        self.sendline("no shutdown")
        self.expect(self.prompt)
        self.sendline("exit")
        self.expect(self.prompt)

    def unset_iface_ipaddr(self, iface: str) -> None:
        """This function is to unset an ipv4 address of an interface on cmts.
        :param iface: interface name
        :type iface: string
        """
        self.sendline(f"interface {iface}")
        self.expect(self.prompt)
        self.sendline("no ip address")
        self.expect(self.prompt)
        self.sendline("exit")
        self.expect(self.prompt)

    def unset_iface_ipv6addr(self, iface: str) -> None:
        """This function is to unset an ipv6 address of an interface on cmts.
        :param iface: interface name.
        :type iface: string
        """
        self.sendline(f"interface {iface}")
        self.expect(self.prompt)
        self.sendline("no ipv6 address")
        self.expect(self.prompt)
        self.sendline("exit")
        self.expect(self.prompt)

    def add_ip_bundle(
        self,
        index: str,
        helper_ip: str,
        ipaddr: str,
        secondary_ips: Optional[List[Any]] = None,
    ) -> None:
        """This function is to add ip bundle to a cable mac.
        :param index: cable mac index,
        :type index: string
        :param helper_ip: helper ip to be used,
        :type helper_ip: string
        :param ipaddr: actual ip to be assiged to cable mac in the format  <ip></><subnet> subnet defaut taken as 24 if not provided,
        :type ipaddr: string
        :param secondary_ips: list of seconday ips  in the format  <ip></><subnet> subnet defaut taken as 24 if not provided.
        :type secondary_ips: list
        """
        if secondary_ips is None:
            secondary_ips = []
        self.expect(self.prompt)
        self.sendline(f"ip address {ipaddr} /24")
        self.expect(self.prompt)
        for ip2 in secondary_ips:
            self.sendline(f"ip address {ip2} /24 secondary")
            self.expect(self.prompt)
        self.sendline(f"cable helper-address {helper_ip} cable-modem")
        self.expect(self.prompt)
        self.sendline(f"cable helper-address {helper_ip} mta")
        self.expect(self.prompt)
        self.sendline(f"cable helper-address {helper_ip} host")
        self.expect(self.prompt)
        self.sendline("exit")
        self.expect(self.prompt)
        self.sendline(f'show interface ip-bundle {index} | include "ip address"')
        self.expect(self.prompt)
        if str(ipaddr) in self.before:
            logger.info("The ip bundle is successfully set.")
        else:
            logger.error("An error occured while setting the ip bundle.")

    def add_ipv6_bundle_addrs(
        self,
        index: str,
        helper_ip: str,
        ipaddr: str,
        secondary_ips: Optional[List[str]] = None,
    ) -> None:
        """This function is to add ipv6 bundle to a cable mac.
        :param index: cable mac index,
        :type index: string
        :param helper_ip: helper ip to be used,
        :type helper_ip: string
        :param ip: actual ip to be assiged to cable mac in the format  <ip></><subnet> subnet defaut taken as 24 if not provided,
        :type ip: string
        :param secondary_ips: list of seconday ips  in the format  <ip></><subnet> subnet defaut taken as 24 if not provided.
        :type secondary_ips: list
        """
        if secondary_ips is None:
            secondary_ips = []
        self.sendline(f"interface ip-bundle {index}")
        self.expect(self.prompt)
        self.sendline(f"ipv6 address {ipaddr}")
        self.expect(self.prompt)
        for ip2 in secondary_ips:
            self.sendline(f"ipv6 address {ip2} secondary")
            self.expect(self.prompt)
        self.sendline(f"cable helper-ipv6-address {helper_ip}")
        self.expect(self.prompt)
        self.sendline("exit")
        self.expect(self.prompt)
        self.sendline(f'show interface ip-bundle {index} | include "ipv6 address"')
        self.expect(self.prompt)
        if str(ipaddress.ip_address(str(ipaddr[:-3])).compressed) in self.before:
            logger.info("The ipv6 bundle is successfully set.")
        else:
            logger.error("An error occured while setting the ipv6 bundle.")

    def add_route(self, ipaddr: str, gw: str) -> None:
        """This function adds an ipv4 network route entry.
        :param ipaddr: <network ip></><subnet ip> take subnet 24 if not provided,
        :param ipaddr: string
        :param gw: gateway ip.
        :type gw: string
        """
        self.sendline(f"route net {ipaddr} /24 gw {gw}")
        self.expect(self.prompt)
        if "error" in self.before.lower():
            logger.error("An error occured while adding the route.")
        self.sendline("show ip route")
        self.expect(self.prompt)
        if gw in self.before:
            logger.debug("The route is available on cmts.")
        else:
            logger.debug("The route is not available on cmts.")

    def add_route6(self, net: str, gw: str) -> None:
        """This function adds an ipv6 network route entry.
        :param net: <network ip></><subnet ip> take subnet 24 if not provided,
        :param net: string
        :param gw: gateway ip.
        :type gw: string
        """
        self.sendline(f"route6 net {net} gw {gw}")
        self.expect(self.prompt)
        if "error" in self.before.lower():
            logger.error("An error occured while adding the route.")
        self.sendline("show ipv6 route")
        self.expect(self.prompt)
        if str(ipaddress.IPv6Address(str(gw))).lower() in self.before.lower():
            logger.debug("The route is available on cmts.")
        else:
            logger.debug("The route is not available on cmts.")

    def del_route(self, ipaddr: str, gw: str) -> None:
        """This function removes an ipv4 network route entry.
        :param ipaddr: <network ip></><subnet ip> take subnet 24 if not provided,
        :type ipaddr: string
        :param gw: gateway ip
        :type gw: string
        """
        self.sendline(f"no route net {ipaddr} /24 gw {gw}")
        self.expect(self.prompt)
        if "error" in self.before.lower():
            logger.error("An error occured while deleting the route.")
        self.expect(pexpect.TIMEOUT, timeout=10)
        self.sendline("show ip route")
        self.expect(self.prompt)
        if gw in self.before:
            logger.debug(
                "The route is still available on cmts might be delayed to reflect on cmts."
            )
        else:
            logger.debug("The route is not available on cmts.")

    def del_route6(self, net: str, gw: str) -> None:
        """This function removes an ipv6 network route entry.
        :param net: <network ip></><subnet ip> take subnet 24 if not provided,
        :type net: string
        :param gw: gateway ip
        :type gw: string
        """
        self.sendline(f"no route6 net {net} gw {gw}")
        self.expect(self.prompt)
        if "error" in self.before.lower():
            logger.error("An error occured while deleting the route.")
        self.sendline("show ipv6 route")
        self.expect(self.prompt)
        if (
            str(ipaddress.ip_address(str(gw)).compressed).lower() in self.before.lower()
            or gw.lower() in self.before.lower()
        ):
            logger.debug("The route is still available on cmts.")
        else:
            logger.debug("The route is not available on cmts.")

    def get_qam_module(self) -> str:
        """Get the module of the qam
        :return: Module of the qam
        :rtype: string
        """
        self.sendline("show system")
        self.expect(self.prompt)
        return re.findall(r"Module (\d+) QAM", self.before)[0]

    def get_ups_module(self) -> list:
        """Get the upstream module of the qam
        :return: list of module number of the qam
        :rtype: list
        """
        self.sendline("show system")
        self.expect(self.prompt)
        results = list(map(int, re.findall(r"Module (\d+) UPS", self.before)))
        return results

    def set_iface_qam(
        self, index: str, sub: str, annex: str, interleave: str, power: str
    ) -> None:
        """Configure the qam interface with annex, interleave and power
        :param index: index number of the qam
        :type index: string
        :param sub: qam slot number
        :type sub: string
        :param annex: annex a or b or c to configure
        :type annex: string
        :param interleave: interleave depth to configure
        :type interleave: string
        :param power: power level
        :type power: string
        """
        self.sendline(f"interface qam {index}/{sub}")
        self.expect(self.prompt)
        self.sendline(f"annex {annex}")
        self.expect(self.prompt)
        self.sendline(f"interleave {interleave}")
        self.expect(self.prompt)
        self.sendline(f"power {power}")
        self.expect(self.prompt)
        self.sendline("no shutdown")
        self.expect(self.prompt)
        self.sendline("exit")
        self.expect(self.prompt)

    def set_iface_qam_freq(self, index: str, sub: str, channel: str, freq: str) -> None:
        """Configure the qam interface with channel and frequency
        :param index: index number of the qam
        :type index: string
        :param sub: qam slot number
        :type sub: string
        :param channel: channel number
        :type channel: string
        :param freq: frequency for the channel
        :type freq: string
        """
        self.sendline(f"interface qam {index}/{sub}")
        self.expect(self.prompt)
        self.sendline(f"channel {channel} freq {freq}")
        self.expect(self.prompt)
        self.sendline(f"no channel {channel} shutdown")
        self.expect(self.prompt)
        self.sendline("exit")
        self.expect(self.prompt)

    def get_iface_qam_freq(self, cm_mac: str) -> dict:
        """Get the qam interface with channel and frequency
        :param cm_mac: mac address of the CM
        :type cm_mac: string
        :return: Downstream index, sub, channel and frequency values.
        ex.OrderedDict([('8/4/0', '512000000'), ('8/4/1', '520000000'), ('8/4/2', '528000000'), ('8/4/3', '536000000'),
                        ('8/4/4', '544000000'), ('8/4/5', '552000000'), ('8/4/6', '560000000'), ('8/4/7', '568000000'),
                        ('8/5/0', '576000000'), ('8/5/1', '584000000'), ('8/5/2', '592000000'), ('8/5/3', '600000000'),
                        ('8/5/4', '608000000'), ('8/5/5', '616000000'), ('8/5/6', '624000000'), ('8/5/7', '632000000'),
                        ('8/6/0', '640000000'), ('8/6/1', '648000000'), ('8/6/2', '656000000'), ('8/6/3', '664000000'),
                        ('8/6/4', '672000000'), ('8/6/5', '680000000'), ('8/6/6', '688000000'), ('8/6/7', '696000000')])
        :rtype: dict
        """
        mac_domain = self.get_cm_mac_domain(cm_mac)
        self.sendline(f"show interface docsis-mac {mac_domain} | inc downstream")
        self.expect(self.prompt)
        tmp = re.findall(r"downstream\s\d+\sinterface\sqam\s(.*)/\d+", self.before)
        downs = {x for x in tmp if tmp.count(x) > 1}
        get_iface_qam_freq = collections.OrderedDict()
        for index_sub in sorted(downs):
            self.sendline(f'show interface qam {index_sub} | inc "channel"')
            self.expect(self.prompt)
            tmp = re.findall(r"channel\s(\d+)\sfrequency\s(\d+)", self.before)
            for channel, freq in tmp:
                get_iface_qam_freq[index_sub + "/" + channel] = freq
        return get_iface_qam_freq

    def set_iface_upstream(
        self, ups_idx: str, ups_ch: str, freq: str, width: str, power: str
    ) -> None:
        """Configure the interface for upstream
        :param ups_idx: upstream index number of the interface
        :type ups_idx: string
        :param ups_ch: upstream channel number for the interface
        :type ups_ch: string
        :param freq: frequency to configure the upstream
        :type freq: string
        :param width: width of the qam
        :type width: string
        :param power: power of the qam
        :type power: string
        """
        self.sendline(f"interface upstream {ups_idx}/{ups_ch}")
        self.expect(self.prompt)
        self.sendline(f"frequency {freq}")
        self.expect(self.prompt)
        self.sendline(f"channel-width {width}")
        self.expect(self.prompt)
        self.sendline(f"power-level {power}")
        self.expect(self.prompt)
        self.sendline("ingress-cancellation")
        self.expect(self.prompt)
        self.sendline("logical-channel 0 profile 3")
        self.expect(self.prompt)
        self.sendline("logical-channel 0 minislot 1")
        self.expect(self.prompt)
        self.sendline("no logical-channel 0 shutdown")
        self.expect(self.prompt)
        self.sendline("logical-channel 1 shutdown")
        self.expect(self.prompt)
        self.sendline("no shutdown")
        self.expect(self.prompt)
        self.sendline("exit")
        self.expect(self.prompt)

    def add_iface_docsis_mac(
        self,
        index,
        ip_bundle,
        qam_idx,
        qam_ch,
        ups_idx,
        ups_ch,
        qam_sub=None,
        prov_mode=None,
    ):
        """configure docsis-mac domain
        :param index: docsis mac index
        :type index: string
        :param ip_bundle: bundle id of the cable modem
        :type ip_bundle: string
        :param qam_idx: slot number of the qam to configure
        :type qam_idx: string
        :param qam_ch: qam channel number
        :type qam_ch: string
        :param ups_idx: upstream slot number
        :type ups_idx: string
        :param ups_ch: upstream channel number
        :type ups_ch: string
        :param qam_sub: port number of the qam, defaults to None
        :type qam_sub: string , optional
        :param prov_mode: provisioning mode if any, defaults to None
        :type prov_mode: string, optional
        """
        self.sendline(f"interface docsis-mac {index}")
        self.expect(self.prompt)
        self.sendline("no shutdown")
        self.expect(self.prompt)
        self.sendline("early-authentication-encryption ranging")
        self.expect(self.prompt)
        self.sendline("no dhcp-authorization")
        self.expect(self.prompt)
        self.sendline("no multicast-dsid-forward")
        self.expect(self.prompt)
        self.sendline("no tftp-enforce")
        self.expect(self.prompt)
        self.sendline("tftp-proxy")
        self.expect(self.prompt)
        self.sendline(f"ip bundle {ip_bundle}")
        self.expect(self.prompt)
        self.sendline("ip-provisioning-mode dual-stack")
        self.expect(self.prompt)
        if type(qam_sub) is int:
            qam_sub = [qam_sub]
        count = 1
        for qs in qam_sub:
            for ch in qam_ch:
                self.sendline(f"downstream {count} interface qam {qam_idx}/{qs}/{ch}")
                self.expect(self.prompt)
                count += 1
        count = 1
        for ch in ups_ch:
            self.sendline(f"upstream {count} interface upstream {ups_idx}/{ch}/0")
            self.expect(self.prompt)
            count += 1
        self.sendline("exit")
        self.expect(self.prompt)

    def modify_docsis_mac_ip_provisioning_mode(
        self, index: str, ip_pvmode: str = "dual-stack"
    ) -> None:
        """Change the mac-domain ip provisioning mode.
        :param index: mac domain of the cable modem configured
        :type index: string
        :param ip_pvmode: provisioning mode can ipv4, ipv6 or 'dual-stack', defaults to 'dual-stack'
        :type ip_pvmode: string, optional
        """
        self.sendline(f"interface docsis-mac {index}")
        self.expect(self.prompt)
        self.sendline(f"ip-provisioning-mode {ip_pvmode}")
        self.expect(self.prompt)
        self.sendline("exit")
        self.expect(self.prompt)
        check_docsis_mac_ip_provisioning_mode = (
            self.check_docsis_mac_ip_provisioning_mode(index)
        )
        if check_docsis_mac_ip_provisioning_mode in ip_pvmode:
            logger.info("The ip provision mode is successfully set.")
        else:
            logger.error("An error occured while setting the ip provision mode.")

    def add_service_class(
        self,
        index: str,
        name: str,
        max_rate: str,
        max_burst: str,
        max_tr_burst: Optional[str] = None,
        downstream: bool = False,
    ) -> None:
        """Add a service class
        :param index: service class number
        :type index: string
        :param name: service name
        :type name: string
        :param max_rate: maximum traffic rate
        :type max_rate: string
        :param max_burst: maximum traffic burst
        :type max_burst: string
        :param max_tr_burst: If anything, defaults to None
        :param downstream: True or False, defaults to False
        """
        self.sendline(f"cable service-class {index}")
        self.expect(self.prompt)
        self.sendline(f"name {name}")
        self.expect(self.prompt)
        self.sendline(f"max-traffic-rate {max_rate}")
        self.expect(self.prompt)
        self.sendline(f"max-traffic-burst {max_burst}")
        self.expect(self.prompt)
        self.sendline("max-concat-burst 0")
        self.expect(self.prompt)
        if downstream:
            self.sendline("downstream")
            self.expect(self.prompt)
        self.sendline("exit")
        self.expect(self.prompt)

    def add_service_group(
        self,
        index: str,
        qam_idx: List[str],
        qam_sub: str,
        qam_channels: str,
        ups_idx: str,
        ups_channels: str,
    ) -> None:
        """Add a service group
        :param index: service group number
        :type index: string
        :param qam_idx: slot number of the qam
        :type qam_idx: string
        :param qam_sub: port number of the qam
        :type qam_sub: List[str]
        :param qam_channels: channel number of the qam
        :type qam_channels: string
        :param ups_idx: upstream slot number
        :type ups_idx: string
        :param ups_channels: channel number of the upstream
        :type ups_channels: string
        """
        self.sendline(f"service group {index}")
        self.expect(self.prompt)
        for qs in qam_sub:
            for ch in qam_channels:
                self.sendline(f"qam {qam_idx}/{qs}/{ch}")
                self.expect(self.prompt)
        for ch in ups_channels:
            self.sendline(f"upstream {ups_idx}/{ch}")
            self.expect(self.prompt)
        self.sendline("exit")
        self.expect(self.prompt)

    def mirror_traffic(self, macaddr: str = "") -> None:
        """Send the mirror traffic
        :param macaddr: mac address of the device if avaliable, defaults to ""
        :type macaddr: string
        """
        self.sendline("diag")
        self.expect("Password:")
        self.sendline("casadiag")
        self.expect(self.prompt)
        self.sendline(f"mirror cm traffic 127.1.0.7 {macaddr}")
        if 0 == self.expect(
            ["Please type YES to confirm you want to mirror all CM traffic:"]
            + self.prompt
        ):
            self.sendline("YES")
            self.expect(self.prompt)
        self.sendline("exit")
        self.expect(self.prompt)

    def unmirror_traffic(self) -> None:
        """stop mirroring the traffic"""
        self.sendline("diag")
        self.expect("Password:")
        self.sendline("casadiag")
        self.expect(self.prompt)
        self.sendline("mirror cm traffic 0")
        self.expect(self.prompt)
        self.sendline("exit")
        self.expect(self.prompt)

    def del_file(self, f: str) -> None:
        """delete the file
        :param f: filename to delete from cmts
        :type f: string
        """
        self.sendline(f"del {f}")
        self.expect(self.prompt)

    def is_cm_bridged(self, mac: str, offset: int = 2) -> bool:
        """This function is to check if the modem is in bridge mode.
        :param mac: Mac address of the modem,
        :param offset: ignored in casa specific to arris, defaults to 2
        :return: Returns True if the modem is bridged else False.
        :rtype: boolean
        """
        self.sendline("show cable modem " + mac + " cpe")
        if 0 == self.expect(["eRouter"] + self.prompt):
            self.expect(self.prompt)
            return False
        else:
            return True

    def check_docsis_mac_ip_provisioning_mode(self, index: str) -> str:
        """
        Get the provisioning mode of the cable modem from CMTS
        :param index: mac domain of the cable modem
        :type index: string
        :return: mode of the provisioning(ipv4, ipv6, dual-stack, apm)
        :rtype: string
        """
        self.sendline(f"show interface docsis-mac {index}")
        self.expect(r"ip-provisioning-mode (\w+\-\w+)")
        result = self.match.group(1)
        self.expect(self.prompt)
        if self.match is not None:
            if "ipv4" in result.lower():
                result = "ipv4"
            elif "dual" in result.lower():
                result = "dual-stack"
            elif "ipv6" in result.lower():
                result = "ipv6"
            elif "apm" in result.lower():
                result = "apm"
            return result
        else:
            return "Not able to fetch ip provisioning mode on CMTS"

    def get_ertr_ipv4(self, mac: str, offset: int = 2) -> Optional[str]:
        """Getting erouter ipv4 from CMTS
        :param mac: mac address of the cable modem
        :type mac: string
        :param offset: ignored in casa specific to arris, defaults to 2
        :return: returns ipv4 address of erouter else None
        :rtype: string
        """
        self.sendline(f"show cable modem {mac} cpe")
        self.expect(self.prompt)
        mac = netaddr.EUI(mac)
        ertr_mac = netaddr.EUI(int(mac) + offset)
        ertr_mac.dialect = netaddr.mac_cisco
        ertr_ipv4 = re.search(f"({ValidIpv4AddressRegex}) .* ({ertr_mac})", self.before)
        if ertr_ipv4:
            ipv4 = ertr_ipv4.group(1)
            return ipv4
        else:
            return None

    def get_ertr_ipv6(self, mac: str, offset: int = 2) -> Optional[str]:
        """Getting erouter ipv6 from CMTS
        :param mac: mac address of the cable modem
        :type mac: string
        :param offset: ignored in casa specific to arris, defaults to 2
        :return: returns ipv6 address of erouter else None
        :rtype: string
        """
        self.sendline(f"show cable modem {mac} cpe")
        self.expect(self.prompt)
        mac = netaddr.EUI(mac)
        ertr_mac = netaddr.EUI(int(mac) + offset)
        ertr_mac.dialect = netaddr.mac_cisco
        output = self.before.replace("\r", "").replace("\n", "")
        ertr_ipv6 = re.search(
            rf"({AllValidIpv6AddressesRegex}) .* ({ertr_mac})", output
        )
        if ertr_ipv6:
            ipv6 = ertr_ipv6.group(1)
            return ipv6
        else:
            return None

    def get_center_freq(self, mac_domain=None) -> int:
        """This function is to return the center frequency of cmts.
        :param mac_domain: Mac Domain of the cable modem
        :type mac_domain: string
        :raises assert: if mac domain is not there and downstream qam is not in output
        :return: Returns center frequency configured on the qam
        :rtype: string
        """
        if mac_domain is None:
            mac_domain = self.mac_domain
        assert mac_domain is not None, "get_center_freq() requires mac_domain to be set"
        self.sendline(
            r"show interface docsis-mac %s | inc downstream\s1\s" % mac_domain
        )
        self.expect_exact(
            r"show interface docsis-mac %s | inc downstream\s1\s" % mac_domain
        )
        self.expect(self.prompt)
        assert "downstream 1 interface qam" in self.before
        major, minor, sub = self.before.strip().split(" ")[-1].split("/")
        self.sendline(rf"show interface qam {major}/{minor} | inc channel\s{sub}\sfreq")
        self.expect_exact(
            rf"show interface qam {major}/{minor} | inc channel\s{sub}\sfreq"
        )
        self.expect(self.prompt)
        assert f"channel {sub} frequency" in self.before
        return int(self.before.split(" ")[-1])

    def get_ip_from_regexp(self, cm_mac: str, ip_regexpr: str) -> Optional[str]:
        """Gets an ip address according to a regexpr (helper function)
        :param cm_mac: cable modem mac address
        :param ip_regexpr: regular expression for ip
        :return: ip addr (ipv4/6 according to regexpr) or None if not found
        :rtype: string
        """
        cm_mac = self.get_cm_mac_cmts_format(cm_mac)
        self.sendline(f"show cable modem | include {cm_mac}")
        if 1 == self.expect(
            [cm_mac + r"\s+(" + ip_regexpr + ")", pexpect.TIMEOUT], timeout=2
        ):
            output = "None"
        else:
            result = self.match.group(1)
            if self.match is not None:
                output = result
            else:
                output = "None"
        self.expect(self.prompt)
        return output

    def _get_cmts_type(self) -> str:
        """This function is to get the product type on cmts.
        :return: Returns the cmts module type.
        :rtype: string
        """
        self.sendline("show system | include Product")
        self.expect(self.prompt)
        return self.before.split(",")[0].split(":")[1].strip().lower()

    def get_qos_parameter(self, cm_mac: str) -> Dict[str, List[dict]]:
        """To get the qos related parameters of CM
        Example output format : {'DS':  [{'Sfid': '1' ..},
                                         {'Sfid': '2' ..}
                                 'US': [{{'Sfid': '1' ..},
                                  'Maximum Burst': '128000',
                                  'IP ToS Overwrite [AND-msk, OR-mask]':
                                  ['0x00', '0x00'], ...},
                                  {'Sfid': '1' ..}}
        The units for measuring are
        1) Maximum Sustained rate, Minimum Reserved rate -- bits/sec
        2) Maximum Burst, Minimum Packet Size, Maximum Concatenated Burst,
            Bytes received, Packet dropped -- bytes
        3) Admitted Qos Timeout, Active QoS Timeout -- seconds
        4) Current Throughput -- [bits/sec, packets/sec]
        :param cm_mac: mac address of the cable modem
        :type cm_mac: string
        :return: containing the qos related parameters.
        :rtype: dictionary
        """
        qos_dict: Dict[str, list] = {"US": [], "DS": []}
        service_flow_direction = ["US", "DS"]
        for value in service_flow_direction:
            self.sendline(f"show cable modem {cm_mac} qos | include {value}")
            self.expect(self.prompt)
            for ele in self.before.split("\n"):
                match = re.search(r"([\d]+)[\s]+" + value, ele)
                if match:
                    stream_id = match.groups(0)[0]
                    qos_dict[value].append(str(stream_id))
        # mapping of the ouput stream to the US/DS and using the index.
        self.sendline(f"show cable modem {cm_mac} qos verbose")
        self.expect(self.prompt)
        service_flows = re.split(r"\n\s*\n", "\n".join(self.before.split("\n")[3:]))[
            :-1
        ]
        strip_units = ["kbps", "(bytes)", "bytes", "seconds", "packets/sec"]
        for service_flow in service_flows:
            service_flow_list = [i for i in service_flow.splitlines() if i]
            qos_dict_flow = {}
            for service in service_flow_list:
                service = service.split(":")
                key, value = (i.strip() for i in service)
                for i in strip_units:
                    value = value.replace(i, "").strip()
                if "scheduling type" in str(key.lower()):
                    qos_dict_flow[key] = value
                elif (
                    "ip tos" not in key.lower()
                    and "current throughput" not in key.lower()
                ):
                    # this is to replace Mimimum with Minimum typo on casa cmts
                    # and convert unit of measure like kbpc to bitespersecond.
                    if "mimimum reserved rate" in key.lower():
                        key = "Minimum Reserved rate"
                    if (
                        "Minimum Reserved rate" in key
                        or "Maximum Sustained rate" in key
                    ):
                        qos_dict_flow[key] = int(value) * 1000
                    else:
                        qos_dict_flow[key] = value
                else:
                    # convert unit of measure from kbpc to bitespersecond.
                    if "current throughput" in key.lower():
                        qos_dict_flow[key] = [
                            int(value.split(" ")[0]) * 1000,
                            value.split(" ")[1].replace(",", ""),
                        ]
                    else:
                        qos_dict_flow[key] = [
                            value.split(" ")[0].replace(",", ""),
                            value.split(" ")[1],
                        ]
            if qos_dict_flow.get("Sfid") in qos_dict["US"]:
                qos_dict["US"].remove(qos_dict_flow.get("Sfid"))
                qos_dict["US"].append(qos_dict_flow)
            elif qos_dict_flow.get("Sfid") in qos_dict["DS"]:
                qos_dict["DS"].remove(qos_dict_flow.get("Sfid"))
                qos_dict["DS"].append(qos_dict_flow)
        return qos_dict

    def get_upstream(self, cm_mac: str):
        """This function is to get the upstream channel type on cmts.
        :param cm_mac: mac address of the CM
        :type cm_mac: string
        :return: Upstream channel type 1.0 -> tdma[1], 2.0 -> atdma[2], 3.0 -> scdma[3]
        :rtype: string
        """
        mac_domain = self.get_cm_mac_domain(cm_mac)
        self.sendline(f"show interface docsis-mac {mac_domain} | inc upstream")
        self.expect(self.prompt)
        tmp = re.findall(r"upstream\s\d\sinterface\supstream\s(.*)/(.*)/0", self.before)
        get_upstream = defaultdict(list)
        for ups_idx, ups_ch in tmp:
            self.sendline(
                f'show interface upstream {ups_idx}/{ups_ch} | inc "frequency"'
            )
            self.expect(r"frequency\s(.*)")
            get_upstream["frequency"].append(self.match.group(1).strip())
            self.expect(self.prompt)
            self.expect(pexpect.TIMEOUT, timeout=1)
            self.sendline(
                'show interface upstream %s/%s | inc "logical-channel 0 profile"'
                % (ups_idx, ups_ch)
            )
            self.expect(r"logical-channel 0 profile\s(.*)")
            get_upstream["channel_type"].append(self.match.group(1).strip())
            self.expect(self.prompt)
            self.expect(pexpect.TIMEOUT, timeout=1)
            self.sendline(
                r'show interface upstream %s/%s | inc "^\s+channel-width"'
                % (ups_idx, ups_ch)
            )
            self.expect(r"channel-width\s(.*)")
            get_upstream["channel_with"].append(
                self.match.group(1).strip().split("\r\n")[0]
            )
            self.expect(self.prompt)
            self.expect(pexpect.TIMEOUT, timeout=1)
        return get_upstream

    def set_upstream(self, cm_mac: str, get_upstream: dict) -> None:
        """This function is to set the upstream channel type on cmts.
        :param cm_mac: mac address of the CM
        :type cm_mac: string
        :param channel_type: channel_type 1.0 -> tdma[1], 2.0 -> atdma[2], 3.0 -> scdma[3].
        :type channel_type: string
        :raises assert: bonding index error
        """
        mac_domain = self.get_cm_mac_domain(cm_mac)
        self.sendline(f"show interface docsis-mac {mac_domain} | inc upstream")
        self.expect(self.prompt)
        tmp = re.findall(r"upstream\s\d\sinterface\supstream\s(.*)/(.*)/0", self.before)
        index = 0
        for ups_idx, ups_ch in tmp:
            self.sendline(f"interface upstream {ups_idx}/{ups_ch}")
            self.expect(self.prompt)
            self.sendline(f"frequency {get_upstream['frequency'][index]}")
            self.expect(self.prompt)
            self.sendline(
                f"logical-channel 0 profile {get_upstream['channel_type'][index]}"
            )
            self.expect(self.prompt)
            self.sendline(f"channel-width {get_upstream['channel_with'][index]}")
            self.expect(self.prompt)
            self.sendline("exit")
            self.expect(self.prompt)
            self.expect(pexpect.TIMEOUT, timeout=1)
            index = index + 1

    def get_downstream_qam(self, cm_mac: str) -> Dict[str, str]:
        """This function is to get downstream modulation type(64qam, 256qam...)
        :param cm_mac: mac address of the CM
        :type cm_mac: string
        :return: Downstream modulation qam values. ex.{'8/6': '256qam', '8/4': '256qam', '8/5': '256qam'}
        :rtype: dict
        """
        mac_domain = self.get_cm_mac_domain(cm_mac)
        self.sendline(f"show interface docsis-mac {mac_domain} | inc downstream")
        self.expect(self.prompt)
        tmp = re.findall(r"downstream\s\d+\sinterface\sqam\s(.*)/\d+", self.before)
        downs = {x for x in tmp if tmp.count(x) > 1}
        get_downstream_qam = dict()
        for i in downs:
            self.sendline(f'show interface qam {i} | inc "modulation"')
            self.expect(r"modulation\s(.*)")
            get_downstream_qam[i] = self.match.group(1).strip()
            self.expect(self.prompt)
        return get_downstream_qam

    def set_downstream_qam(self, get_downstream_qam: dict) -> None:
        """This function is to set downstream modulation type(64qam, 256qam...)
        :param get_downstream_qam: ex.{'8/6': '256qam', '8/4': '256qam', '8/5': '256qam'}
        :type get_downstream_qam: dict
        """
        for k, v in get_downstream_qam.items():
            self.sendline(f"interface qam {k}")
            self.expect(self.prompt)
            self.sendline(f"modulation {v}")
            self.expect(self.prompt)

    def ping(self, ping_ip: str, ping_count: int = 3, timeout: int = 10) -> bool:
        """This function to ping the device from cmts
        :param ping_ip: device ip which needs to be verified
        :ping_ip type: string
        :param ping_count: Repeating ping packets, defaults to 3
        :ping_count type: integer
        :param timeout: timeout for the packets, defaults to 10 sec
        :type timeout: integer
        :return: True if ping passed else False
        """
        mode = f"ipv{ipaddress.ip_address(ping_ip).version}"
        basic_ping = (
            f"ping repeat {ping_count} timeout {timeout}" if mode == "ipv4" else "ping6"
        )
        self.sendline(f"{basic_ping} {ping_ip}")
        self.expect(self.prompt)
        match = re.search(
            "{} packets transmitted, {} (.*)received, 0% packet loss".format(
                ping_count, ping_count
            ),
            self.before,
        )
        if match:
            return True
        else:
            return False

    def get_current_time(self, fmt: str = "%Y-%m-%dT%H:%M:%S%z") -> str:
        """Returns the current time on the CMTS
        :return: the current time as a string formatted as "YYYY-MM-DD hh:mm:ss"
        :raises ValueError: if the conversion failed for whatever reason
        :raises CodeError: if there is no timestamp
        """
        self.current_time_cmd = "show clock"
        self.dateformat = "%a %b %d %H:%M:%S %Z %Y"
        return super().get_current_time(fmt)

    def ip_route(self) -> str:
        """Perfrom show ip route command and return output


        :return: ip routes available on cmts
        :rtype: str
        """
        self.sendline("show ip route")
        self.expect(self.prompt)
        return self.before

    def _get_cm_docsis_provisioned_version(self, mac_address: str) -> float:
        """Get docsis version of CM.

        :param mac_address: mac address of the cm
        :type mac_address: str
        :return: Docsis version of the cm
        :rtype: float
        :raises CodeError: Failed to get docsis version
        """
        raise NotImplementedError

    def _get_cm_channel_bonding_detail(self, mac_address: str) -> dict[str, list[str]]:
        """Get the list of primary channel.

        :param mac_address: mac address of the cm
        :type mac_address: str
        :return: upstream and downstream channel list
        :rtype: dict[str, list[str]]
        :raises CodeError: Failed to get the channel values
        """
        raise NotImplementedError


# Small test to verify basic CasaCMTS connectivity.
# Will be run once someone runs this file directly, e.g. python3 casa_cmts.py
# Just add your local casa cmts details
if __name__ == "__main__":
    cmts = CasaCMTS(
        conn_cmd="your_connection_cmd",
        username="your_cmts_username",
        password="your_cmts_password",
    )
    print(cmts.check_output("show cable modem"))
