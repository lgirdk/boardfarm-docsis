# Copyright (c) 2018
#
# All rights reserved.
#
# This file is distributed under the Clear BSD license.
# The full text can be found in LICENSE in the root directory.

import ipaddress
import logging
import re
import sys

import netaddr
import pexpect
import six
from boardfarm.devices import connection_decider
from boardfarm.lib.regexlib import (
    AllValidIpv6AddressesRegex,
    ValidIpv4AddressRegex,
)

from . import base_cmts
from .base_cmts import BaseCmts

logger = logging.getLogger("bft")


class ArrisCMTS(BaseCmts):
    """Connects to and configures a ARRIS CMTS"""

    prompt = ["arris(.*)>", "arris(.*)#", r"arris\(.*\)> ", r"arris\(.*\)# "]
    model = "arris_cmts"

    def __init__(self, *args, **kwargs):
        """Constructor method"""
        super().__init__(*args, **kwargs)
        self.conn_cmd = kwargs.get("conn_cmd", None)
        self.connection_type = kwargs.get("connection_type", "local_serial")
        self.username = kwargs.get("username", "boardfarm")
        self.password = kwargs.get("password", "boardfarm")
        self.password_admin = kwargs.get("password_admin", "boardfarm")
        self.ssh_password = kwargs.get("ssh_password", "boardfarm")
        self.mac_domain = kwargs.get("mac_domain", None)
        self.channel_bonding = kwargs.get("channel_bonding", 32)  # 24x8 : total 32

        self.connlock = None
        if self.conn_cmd is None:
            # TODO: try to parse from ipaddr, etc
            raise Exception("No command specified to connect to Arris CMTS")

        self.logfile_read = sys.stdout
        self.name = kwargs.get("name", self.model)

    @BaseCmts.connect_and_run
    def interact(self):
        super(ArrisCMTS, self).interact()

    def __str__(self):
        txt = []
        txt.append("name: {}".format(self.name))
        txt.append("command: {}".format(self.conn_cmd))
        txt.append("class: {}".format(type(self).__name__))
        return "\n".join(txt)

    def connect(self):
        """This method is used to connect cmts, login to the cmts based on the connection type available

        :raises Exception: Unable to get prompt on ARRIS device
        """
        self.connection = connection_decider.connection(
            self.connection_type,
            device=self,
            conn_cmd=self.conn_cmd,
            ssh_password=self.ssh_password,
        )
        self.connection.connect()
        try:
            try:
                self.expect_exact("Escape character is '^]'.", timeout=5)
            except Exception:
                pass
            self.sendline()
            idx = self.expect(["\r\nLogin:", pexpect.TIMEOUT] + self.prompt, timeout=10)
            if 0 == idx:
                self.sendline(self.username)
                self.expect("assword:")
                self.sendline(self.password)
                self.expect(self.prompt)
            elif idx > 1:
                # if we get a prompt we have probably ssh to the device
                pass
            else:
                # Over telnet we come in at the right prompt
                # over serial we could have a double login
                # not yet implemented
                raise Exception("Failed to connect to Arris via telnet")
            self.sendline("enable")
            if 0 == self.expect(["Password:"] + self.prompt):
                self.sendline(self.password_admin)
                self.expect(self.prompt)
            self.sendline("config")
            self.expect(
                "Enter configuration commands, one per line. End with exit or quit or CTRL Z"
            )
            self.expect(self.prompt)
            self.sendline("no pagination")
            self.expect(self.prompt)
            return
        except Exception:
            self.close()
            self.pid = None
            raise Exception("Unable to get prompt on Arris device")

    def logout(self):
        """Logout of the CMTS device"""
        try:
            self.sendline("exit")
            self.sendline("exit")
        except Exception:
            self.close()

    def _is_cm_online(self, ignore_bpi=False, ignore_partial=False, ignore_cpe=False):
        """Unittest helper invoked by is_cm_online
        Returns True if the CM status is operational
        see is_cm_online(...)
        """
        b = self.check_output(f"show cable modem {self.board_wan_mac} detail")

        if not re.search(r"State=(Operational|Online-d)", b):
            return False
        if ignore_bpi is False:
            if not re.search(r"Privacy=Ready((\s){1,})Ver=BPI", b):
                return False
        if ignore_partial is False:
            if self._check_PartialService(self.board_wan_mac):
                logger.debug("Cable modem in partial service")
                return False
        if ignore_cpe is False:
            if re.search(r"State=Online-d", b):
                return False
        return True

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
        return self._is_cm_online(
            ignore_bpi=ignore_bpi, ignore_partial=ignore_partial, ignore_cpe=ignore_cpe
        )

    @BaseCmts.convert_mac_to_cmts_type
    def _check_online(self, cmmac=None):
        """Internal fuction to Check the CM status from CMTS function checks the encrytion mode and returns True if online
        It is not decarated by BaseCmts.connect_and_run

        :param cmmac: mac address of the CM
        :type cmmac: string
        :return: True if the CM is operational else actual status on cmts
        :rtype: string / boolean
        """
        self.sendline("no pagination")
        self.expect_prompt()
        self.sendline("show cable modem | include %s" % cmmac)
        self.expect_prompt()

        if "Operational" in self.before:
            return True
        else:
            try:
                # Regex matches any status after digit (e.g 24x8) up until first space
                r = re.findall(r"(?!(\d+)\s+)([A-Z])\w+[^\s]+", self.before)[0].strip()
            except Exception:
                r = "Offline"
        return r

    @BaseCmts.connect_and_run
    @base_cmts.deco_get_mac
    def check_online(self, cmmac):
        """Check the CM status from CMTS function checks the encrytion mode and returns True if online

        :param cmmac: mac address of the CM
        :type cmmac: string
        :return: True if the CM is operational else actual status on cmts
        :rtype: string / boolean
        """
        return self._check_online(cmmac)

    @BaseCmts.connect_and_run
    @BaseCmts.convert_mac_to_cmts_type
    def clear_offline(self, cmmac):
        """Clear the CM entry from cmts which is offline -clear cable modem <mac> delete

        :param cmmac: mac address of the CM
        :type cmmac: string
        """
        self.sendline("exit")
        self.expect(self.prompt)
        self.sendline("clear cable modem %s delete" % cmmac)
        self.expect(self.prompt)
        self.sendline("configure")
        self.expect(self.prompt)

    @BaseCmts.connect_and_run
    @BaseCmts.convert_mac_to_cmts_type
    def clear_cm_reset(self, cmmac):
        """Reset the CM from cmts using cli -clear cable modem <mac> reset

        :param cmmac: mac address of the CM
        :type cmmac: string
        """
        self.sendline("exit")
        self.expect(self.prompt)
        """ NB: this command does not reboot the CM, but forces it to reinitialise """
        self.sendline("clear cable modem %s reset" % cmmac)
        self.expect(self.prompt)
        self.sendline("configure")
        self.expect(self.prompt)
        self.expect(pexpect.TIMEOUT, timeout=5)
        online_state = self._check_online(cmmac)
        if online_state is True:
            logger.debug("CM is still online after 5 seconds.")
        else:
            logger.info("CM reset is initiated.")

    @BaseCmts.connect_and_run
    @BaseCmts.convert_mac_to_cmts_type
    def get_mtaip(self, cmmac, mtamac=None):
        """Get the MTA IP from CMTS

        :param cmmac: mac address of the CM
        :type cmmac: string
        :param mtamac: mta mac address
        :type mtamac: string
        :return: MTA ip address or "None" if ip not found
        :rtype: string
        """
        self.sendline("show cable modem %s detail | include MTA" % (cmmac))
        self.expect(r"CPE\(MTA\)\s+.*IPv4=(" + ValidIpv4AddressRegex + ")\r\n")
        result = self.match.group(1)
        if self.match is not None:
            output = result
        else:
            output = "None"
        self.expect(self.prompt)
        return output

    @BaseCmts.connect_and_run
    @BaseCmts.convert_mac_to_cmts_type
    def get_ip_from_regexp(self, cmmac, ip_regexpr):
        """Gets an ip address according to a regexpr (helper function)

        :param cmmac: cable modem mac address
        :type cmmac: string
        :param ip_regexpr: regular expression for ip
        :type ip_regexpr: string
        :return: ip addr (ipv4/6 according to regexpr) or None if not found
        :rtype: string
        """
        self.sendline("show cable modem | include %s" % cmmac)
        if 1 == self.expect(
            [cmmac + r"\s+(" + ip_regexpr + ")", pexpect.TIMEOUT], timeout=2
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

    @BaseCmts.convert_mac_to_cmts_type
    def get_cmip(self, cmmac):
        """Get the IP of the Cable modem from CMTS

        :param cmmac: mac address of the CM
        :type cmmac: string
        :return: ip address of cable modem or "None"
        :rtype: string
        """
        return self.get_ip_from_regexp(cmmac, ValidIpv4AddressRegex)

    def get_cmipv6(self, cmmac):
        """Get IPv6 address of the Cable modem from CMTS

        :param cmmac: mac address of the CM
        :type cmmac: string
        :return: ipv6 address(str) of cable modem or "None"
        :rtype: string
        """
        return self.get_ip_from_regexp(cmmac, AllValidIpv6AddressesRegex)

    @BaseCmts.connect_and_run
    @BaseCmts.convert_mac_to_cmts_type
    def get_cm_mac_domain(self, cm_mac):
        """Get the Mac-domain of Cable modem

        :param cm_mac: mac address of the CM
        :type cm_mac: string
        :return: mac_domain of the particular cable modem
        :rtype: string
        """
        mac_domain = None
        self.sendline("show cable modem %s detail | include Cable-Mac=" % cm_mac)
        if 0 == self.expect(["Cable-Mac= ([0-9]{1,3}),", pexpect.TIMEOUT], timeout=5):
            mac_domain = self.match.group(1)
        self.expect(self.prompt)
        return mac_domain

    def _check_PartialService(self, cmmac):
        """Helper function for check_PartialService"""
        self.sendline("show cable modem %s" % cmmac)
        self.expect(self.prompt)
        if "impaired" in self.before:
            output = 1
        else:
            output = 0
        return output

    @base_cmts.deco_get_mac
    @BaseCmts.connect_and_run
    @BaseCmts.convert_mac_to_cmts_type
    def check_PartialService(self, cmmac):
        """Check the cable modem is in partial service

        :param cmmac: mac address of the CM
        :type cmmac: string
        :return: 1 if is true else return the value as 0
        :rtype: int
        """
        return self._check_PartialService(cmmac)

    @BaseCmts.connect_and_run
    @BaseCmts.convert_mac_to_cmts_type
    def DUT_chnl_lock(self, cm_mac):
        """Check the CM channel locks based on cmts type

        :param cm_mac: mac address of the CM
        :type cm_mac: string
        :returns: Locked channels of upstream and downstream
        :rtype: list
        """
        self.sendline("show cable modem  %s bonded-impaired" % cm_mac)
        self.expect(self.prompt)
        bonded_impared_status = self.before
        if "No CMs were found" in bonded_impared_status:
            self.sendline("show cable modem  %s " % cm_mac)
            self.expect(r"(\d+)x(\d+)")
            downstream = int(self.match.group(1))
            upstream = int(self.match.group(2))
            self.expect(self.prompt)
        else:
            downstream = int(
                re.findall(r"(\d+x\d+)", bonded_impared_status)[1].split("x")[0]
            )
            upstream = int(
                re.findall(r"(\d+x\d+)", bonded_impared_status)[1].split("x")[1]
            )
        return [upstream, downstream]

    @BaseCmts.connect_and_run
    def save_running_config_to_local(self, filename):
        """save the running config to startup"""
        self.sendline("no pagination")
        self.expect(self.prompt)
        # show running-config will display the current running config file of CMTS
        self.sendline("show running-config")
        self.expect(r"arrisc4\(config\)\#")
        f = open(filename, "w")
        f.write(self.before)
        f.write(self.after)
        f.close()

    @BaseCmts.connect_and_run
    def save_running_to_startup_config(self):
        """Copy running config to local machine"""
        self.sendline("exit")
        self.expect(self.prompt)
        self.sendline("copy running-config startup-config")
        self.expect(self.prompt)
        self.sendline("config")
        self.expect(self.prompt)

    @BaseCmts.connect_and_run
    def get_qam_module(self):
        """Get the module of the qam

        :return: Module of the qam
        :rtype: string
        """
        self.sendline("show linecard status | include DMM/DMM")
        self.expect(self.prompt)
        return self.before.split("\n", 1)[1]

    @BaseCmts.connect_and_run
    def get_ups_module(self):
        """Get the upstream module of the qam

        :return: list of module number of the qam
        :rtype: list
        """
        self.sendline("show linecard status | include CAM/CAM")
        self.expect(self.prompt)
        results = list(map(int, re.findall(r"(\d+)    CAM ", self.before)))
        return results

    @BaseCmts.connect_and_run
    def set_iface_ipaddr(self, iface, ipaddr):
        """This function is to set an ip address to an interface on cmts

        :param iface: interface name ,
        :type iface: string
        :param ipaddr: <ip></><subnet> using 24 as default if subnet is not provided.
        :type ipaddr: string
        """
        if "/" not in ipaddr:
            ipaddr += "/24"
            ipaddr = ipaddress.IPv4Interface(six.text_type(ipaddr))
        else:
            ipaddr = ipaddress.IPv4Interface(six.text_type(ipaddr))
        self.sendline("interface %s" % iface)
        self.expect(self.prompt)
        self.sendline("ip address %s %s" % (ipaddr.ip, ipaddr.netmask))
        self.expect(self.prompt)
        self.sendline("no shutdown")
        self.expect(self.prompt)
        self.sendline("exit")
        self.expect(self.prompt)

    @BaseCmts.connect_and_run
    def set_iface_ipv6addr(self, iface, ipaddr):
        """Configure ipv6 address

        :param iface: interface name
        :type iface: string
        :param ipaddr: ipaddress to configure
        :type ipaddr: string
        """
        self.sendline("interface %s" % iface)
        self.expect(self.prompt)
        self.sendline("ipv6 address %s" % ipaddr)
        self.expect(self.prompt)
        self.sendline("no shutdown")
        self.expect(self.prompt)
        self.sendline("exit")
        self.expect(self.prompt)

    @BaseCmts.connect_and_run
    def unset_iface_ipaddr(self, iface):
        """This function is to unset an ipv4 address of an interface on cmts

        :param iface: interface name
        :type iface: string
        """
        self.sendline("interface %s" % iface)
        self.expect(self.prompt)
        self.sendline("no ip address")
        self.expect(self.prompt)
        self.sendline("exit")
        self.expect(self.prompt)

    @BaseCmts.connect_and_run
    def unset_iface_ipv6addr(self, iface):
        """This function is to unset an ipv6 address of an interface on cmts

        :param iface: interface name.
        :type iface: string
        """
        self.sendline("interface %s" % iface)
        self.expect(self.prompt)
        self.sendline("no ipv6 address")
        self.expect(self.prompt)
        self.sendline("exit")
        self.expect(self.prompt)

    @BaseCmts.connect_and_run
    def del_file(self, f):
        """delete file on cmts

        :param f: filename to delete from cmts
        :type f: string
        """
        self.sendline("exit")
        self.expect(self.prompt)
        self.sendline("delete %s" % f)
        self.expect(self.prompt)

    @BaseCmts.connect_and_run
    def check_docsis_mac_ip_provisioning_mode(self, index):
        """
        Get the provisioning mode of the cable modem from CMTS
        :param index: mac domain of the cable modem
        :type index: string
        :return: mode of the provisioning(ipv4, ipv6, dual-stack, apm)
        :rtype: string
        """
        self.sendline(
            "show running-config interface cable-mac %s | include cm-ip-prov-mode"
            % index
        )
        self.expect(self.prompt)
        result = self.before.split("\n")[1].split(" ")[-1]
        if "ipv4" in result.lower():
            result = "ipv4"
        elif "dual" in result.lower():
            result = "dual-stack"
        elif "ipv6" in result.lower():
            result = "ipv6"
        elif "apm" in result.lower():
            result = "apm"
        return result

    @BaseCmts.connect_and_run
    def modify_docsis_mac_ip_provisioning_mode(self, index, ip_pvmode="dual-stack"):
        """Change the ip provsioning mode

        :param index: mac domain of the cable modem configured
        :type index: string
        :param ip_pvmode: provisioning mode can ipv4, ipv6 or 'dual-stack', defaults to 'dual-stack'
        :type ip_pvmode: string
        """
        if "dual-stack" in ip_pvmode.lower() and "c4" in self.get_cmts_type():
            logger.error(
                "dual-stack ip provisioning modem is not supported on Chassis Type : C4 please choose apm"
            )
            return
        self.sendline("interface cable-mac %s" % index)
        self.expect(self.prompt)
        self.sendline("cable cm-ip-prov-mode %s" % ip_pvmode)
        self.expect(self.prompt)
        self.sendline("exit")
        self.expect(self.prompt)
        self.sendline(
            "show running-config interface cable-mac %s | include cm-ip-prov-mode"
            % index
        )
        self.expect(self.prompt)
        check_docsis_mac_ip_provisioning_mode = (
            self.check_docsis_mac_ip_provisioning_mode(index)
        )
        if check_docsis_mac_ip_provisioning_mode in ip_pvmode:
            logger.info("The ip provision mode is successfully set.")
        else:
            logger.error("An error occured while setting the ip provision mode.")

    @BaseCmts.connect_and_run
    def add_route(self, ipaddr, gw):
        """This function is to add route

        :param ipaddr: <network ip></><subnet ip> take subnet 24 if not provided,
        :param ipaddr: string
        :param gw: gateway ip.
        :type gw: string
        """
        if "/" not in ipaddr:
            ipaddr += "/24"
            ipaddr = ipaddress.IPv4Interface(six.text_type(ipaddr))
        else:
            ipaddr = ipaddress.IPv4Interface(six.text_type(ipaddr))
        self.sendline("ip route %s %s %s" % (ipaddr.ip, ipaddr.netmask, gw))
        self.expect(self.prompt)
        if "error" in self.before.lower():
            logger.error("An error occured while adding the route.")
        self.sendline("show ip route")
        self.expect(self.prompt)
        if gw in self.before:
            logger.info("The route is available on cmts.")
        else:
            logger.info("The route is not available on cmts.")

    @BaseCmts.connect_and_run
    def add_route6(self, net, gw):
        """This function is to add route6

        :param net: <network ip></><subnet ip> take subnet 24 if not provided,
        :param net: string
        :param gw: gateway ip.
        :type gw: string
        """
        self.sendline("ipv6 route %s %s" % (net, gw))
        self.expect(self.prompt)
        if "error" in self.before.lower():
            logger.error("An error occured while adding the route.")
        self.sendline("show ipv6 route")
        self.expect(self.prompt)
        if str(ipaddress.IPv6Address(six.text_type(gw))).lower() in self.before.lower():
            logger.info("The route is available on cmts.")
        else:
            logger.info("The route is not available on cmts.")

    @BaseCmts.connect_and_run
    def del_route(self, ipaddr, gw):
        """This function is to delete route

        :param ipaddr: <network ip></><subnet ip> take subnet 24 if not provided
        :type ipaddr: string
        :param gw: gateway ip
        :type gw: string
        """
        if "/" not in ipaddr:
            ipaddr += "/24"
            ipaddr = ipaddress.IPv4Interface(six.text_type(ipaddr))
        else:
            ipaddr = ipaddress.IPv4Interface(six.text_type(ipaddr))
        self.sendline("no ip route %s %s %s" % (ipaddr.ip, ipaddr.netmask, gw))
        self.expect(self.prompt)
        if "error" in self.before.lower():
            logger.error("An error occured while deleting the route.")
        self.expect(pexpect.TIMEOUT, timeout=10)
        self.sendline("show ip route")
        self.expect(self.prompt)
        if gw in self.before:
            logger.debug("The route is still available on cmts.")
        else:
            logger.info("The route is not available on cmts.")

    @BaseCmts.connect_and_run
    def del_route6(self, net, gw):
        """This function is to delete ipv6 route

        :param net: <network ip></><subnet ip> take subnet 24 if not provided,
        :type net: string
        :param gw: gateway ip
        :type gw: string
        """
        self.sendline("no ipv6 route %s %s" % (net, gw))
        self.expect(self.prompt)
        if "error" in self.before.lower():
            logger.error("An error occured while deleting the route.")
        self.sendline("show ipv6 route")
        self.expect(self.prompt)
        if (
            str(ipaddress.ip_address(six.text_type(gw)).compressed).lower()
            in self.before.lower()
            or gw.lower() in self.before.lower()
        ):
            logger.debug("The route is still available on cmts.")
        else:
            logger.debug("The route is not available on cmts.")

    @BaseCmts.connect_and_run
    def add_ip_bundle(self, index, helper_ip, ipaddr, secondary_ips=None):
        """This function is to add ip bundle to a cable mac

        :param index: cable mac index,
        :type index: string
        :param helper_ip: helper ip to be used,
        :type helper_ip: string
        :param ipaddr: actual ip to be assiged to cable mac in the format  <ip></><subnet> subnet defaut taken as 24 if not provided,
        :type ipaddr: string
        :param secondary_ips: list of seconday ips  in the format  <ip></><subnet> subnet defaut taken as 24 if not provided, defaults to empty list []
        :type secondary_ips: list
        """

        if secondary_ips is None:
            secondary_ips = []

        if "/" not in ipaddr:
            ipaddr += "/24"
            ipaddr = ipaddress.IPv4Interface(six.text_type(ipaddr))
        else:
            ipaddr = ipaddress.IPv4Interface(six.text_type(ipaddr))
        self.sendline("interface cable-mac %s" % index)
        self.expect(self.prompt)
        self.sendline("ip address %s %s" % (ipaddr.ip, ipaddr.netmask))
        self.expect(self.prompt)
        for ip2 in secondary_ips:
            if "/" not in ip2:
                ip2 += "/24"
                ip2 = ipaddress.IPv4Interface(six.text_type(ip2))
            else:
                ip2 = ipaddress.IPv4Interface(six.text_type(ip2))
            self.sendline("ip address %s %s secondary" % (ip2.ip, ip2.netmask))
            self.expect(self.prompt)
        self.sendline("cable helper-address %s cable-modem" % helper_ip)
        self.expect(self.prompt)
        self.sendline("cable helper-address %s mta" % helper_ip)
        self.expect(self.prompt)
        self.sendline("cable helper-address %s host" % helper_ip)
        self.expect(self.prompt)
        self.sendline("exit")
        self.expect(self.prompt)
        self.sendline(
            "show running-config interface cable-mac %s | include ip address" % index
        )
        self.expect(self.prompt)
        if str(ipaddr.ip) in self.before:
            logger.info("The ip bundle is successfully set.")
        else:
            logger.error("An error occured while setting the ip bundle.")

    @BaseCmts.connect_and_run
    def add_ipv6_bundle_addrs(self, index, helper_ip, ip, secondary_ips=None):
        """This function is to add ipv6 bundle to a cable mac

        :param index: cable mac index
        :type index: string
        :param helper_ip: helper ip to be used
        :type helper_ip: string
        :param ip: actual ip to be assiged to cable mac in the format  <ip></><subnet> subnet defaut taken as 24 if not provided
        :type ip: string
        :param secondary_ips: list of seconday ips  in the format  <ip></><subnet> subnet defaut taken as 24 if not provided defaults to empty list []
        :type secondary_ips: list
        """
        if secondary_ips is None:
            secondary_ips = []

        self.sendline("interface cable-mac %s" % index)
        self.expect(self.prompt)
        self.sendline("ipv6 address %s" % ip)
        self.expect(self.prompt)
        self.sendline("ipv6 dhcp relay destination %s" % helper_ip)
        self.expect(self.prompt)
        self.sendline("exit")
        self.expect(self.prompt)
        self.sendline(
            "show running-config interface cable-mac %s | include ipv6 address" % index
        )
        self.expect(self.prompt)
        if str(ipaddress.ip_address(six.text_type(ip[:-3])).compressed) in self.before:
            logger.info("The ipv6 bundle is successfully set.")
        else:
            logger.error("An error occured while setting the ipv6 bundle.")

    @BaseCmts.connect_and_run
    def set_iface_qam(self, index, sub, annex, interleave, power):
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
        self.sendline("interface cable-downstream %s/%s" % (index, sub))
        self.expect(self.prompt)
        self.sendline("cable power %s" % power)
        self.expect(self.prompt)
        self.sendline("no shutdown")
        self.expect(self.prompt)
        self.sendline("exit")
        self.expect(self.prompt)

    @BaseCmts.connect_and_run
    def wait_for_ready(self):
        """Check the cmts status"""
        max_iteration = 5
        self.sendline("show linecard status")
        while 0 == self.expect(["Down | OOS"] + self.prompt) and max_iteration > 0:
            max_iteration -= 1
            self.expect(self.prompt)
            self.expect(pexpect.TIMEOUT, timeout=5)
            self.sendline("show linecard status")

    @BaseCmts.connect_and_run
    def set_iface_qam_freq(self, index, sub, channel, freq):
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
        self.sendline("interface cable-downstream %s/%s" % (index, sub))
        self.expect(self.prompt)
        self.sendline("cable frequency %s" % freq)
        self.expect(self.prompt)
        self.sendline("no shutdown")
        self.expect(self.prompt)
        self.sendline("exit")
        self.expect(self.prompt)

    @BaseCmts.connect_and_run
    def add_service_group(
        self, index, qam_idx, qam_sub, qam_channels, ups_idx, ups_channels
    ):
        """Add a service group

        :param index: service group number
        :type index: string
        :param qam_idx: slot number of the qam
        :type qam_idx: string
        :param qam_sub: port number of the qam
        :type qam_sub: string
        :param qam_channels: channel number of the qam
        :type qam_channels: string
        :param ups_idx: upstream slot number
        :type ups_idx: string
        :param ups_channels: channel number of the upstream
        :type ups_channels: string
        """
        logger.debug(
            "Service group is auto configured in ARRIS once mac domain is created."
        )

    @BaseCmts.connect_and_run
    def mirror_traffic(self, macaddr=""):
        """Send the mirror traffic

        :param macaddr: mac address of the device if avaliable, defaults to empty string ""
        :type macaddr: string
        """
        logger.error(
            "Mirror traffic feature is not supported in ARRIS unless we use lawful intercept functionality."
        )

    @BaseCmts.connect_and_run
    def unmirror_traffic(self):
        """stop mirroring the traffic"""
        logger.error(
            "Unmirror traffic feature is not supported in ARRIS unless we use lawful intercept functionality."
        )

    @BaseCmts.connect_and_run
    def run_tcpdump(self, time, iface="any", opts=""):
        """tcpdump capture on the cmts interface

        :param time: timeout to wait till gets prompt
        :type time: integer
        :param iface: any specific interface, defaults to 'any'
        :type iface: string, optional
        :param opts: any other options to filter, defaults to ""
        :type opts: string
        """
        logger.error("TCPDUMP feature is not supported in ARRIS.")

    @BaseCmts.connect_and_run
    @BaseCmts.convert_mac_to_cmts_type
    def is_cm_bridged(self, mac, offset=2):
        """This function is to check if the modem is in bridge mode

        :param mac: Mac address of the modem,
        :param offset: ignored in casa specific to arris, defaults to 2
        :return: Returns True if the modem is bridged else False.
        :rtype: boolean
        """
        self.sendline("show cable modem %s detail" % mac)
        self.expect(self.prompt)
        mac = netaddr.EUI(mac)
        ertr_mac = netaddr.EUI(int(mac) + offset)
        ertr_mac.dialect = netaddr.mac_cisco
        if str(ertr_mac) in self.before:
            return False
        else:
            return True

    @BaseCmts.connect_and_run
    @BaseCmts.convert_mac_to_cmts_type
    def get_ertr_ipv4(self, mac, offset=2):
        """Getting erouter ipv4 from CMTS

        :param mac: mac address of the cable modem
        :type mac: string
        :param offset: ignored in casa specific to arris, defaults to 2
        :return: returns ipv4 address of erouter else None
        :rtype: string
        """
        self.sendline("show cable modem %s detail" % mac)
        self.expect(self.prompt)
        mac = netaddr.EUI(mac)
        ertr_mac = netaddr.EUI(int(mac) + offset)
        ertr_mac.dialect = netaddr.mac_cisco
        ertr_ipv4 = re.search(
            "(%s) .*=(%s)" % (ertr_mac, ValidIpv4AddressRegex), self.before
        )
        if ertr_ipv4:
            ipv4 = ertr_ipv4.group(2)
            return ipv4
        else:
            return None

    @BaseCmts.connect_and_run
    @BaseCmts.convert_mac_to_cmts_type
    def get_ertr_ipv6(self, mac, offset=2):
        """Getting erouter ipv6 from CMTS

        :param mac: mac address of the cable modem
        :type mac: string
        :param offset: ignored in casa specific to arris, defaults to 2
        :return: returns ipv6 address of erouter else None
        :rtype: string
        """
        self.sendline("show cable modem %s detail" % mac)
        self.expect(self.prompt)
        mac = netaddr.EUI(mac)
        ertr_mac = netaddr.EUI(int(mac) + offset)
        ertr_mac.dialect = netaddr.mac_cisco
        ertr_ipv6 = re.search(
            "(%s) IPv6=(%s)" % (ertr_mac, AllValidIpv6AddressesRegex), self.before
        )
        if ertr_ipv6:
            ipv6 = ertr_ipv6.group(2)
            return ipv6
        else:
            return None

    @BaseCmts.connect_and_run
    def get_center_freq(self, mac_domain=None):
        """This function is to return the center frequency of cmts

        :param mac_domain: Mac Domain of the cable modem
        :type mac_domain: string
        :return: Returns center frequency configured on the qam
        :rtype: string
        """
        if mac_domain is None:
            mac_domain = self.mac_domain
        assert mac_domain is not None, "get_center_freq() requires mac_domain to be set"
        self.sendline("no pagination")
        self.expect(self.prompt)
        self.sendline("show interface cable downstream")
        self.expect(self.prompt)
        freq_list = []
        for row in self.before.split("\n")[3:]:
            match_grp = re.match(
                r"\d{1,2}/\d{1,2}\s+" + str(mac_domain) + r"\s.*\s(\d{6,10})\s+\w+", row
            )
            if match_grp is not None and match_grp.groups(0)[0] is not None:
                freq_list.append(match_grp.groups(0)[0])
        freq_list = map(int, freq_list)
        return str(min(freq_list))

    @BaseCmts.connect_and_run
    def set_iface_upstream(self, ups_idx, ups_ch, freq, width, power):
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
        self.sendline("interface cable-upstream %s/%s" % (ups_idx, ups_ch))
        self.expect(self.prompt)
        self.sendline("cable frequency %s" % freq)
        self.expect(self.prompt)
        self.sendline("cable channel-width %s" % width)
        self.expect(self.prompt)
        self.sendline("cable power-level %s" % power)
        self.expect(self.prompt)
        self.sendline("cable modulation-profile 64")
        self.expect(self.prompt)
        self.sendline("cable mini-slot-size 2")
        self.sendline("no shutdown")
        self.expect(self.prompt)
        self.sendline("exit")
        self.expect(self.prompt)

    @BaseCmts.connect_and_run
    def get_cm_bundle(self, mac_domain):
        """Get the bundle id from cable modem

        :param mac_domain: Mac_domain of the cable modem connected
        :type mac_domain: string
        :return: bundle id
        :rtype: string
        """
        self.sendline(
            "show running-config interface cable-mac %s | include cable-mac [0-9]+.[0-9]+"
            % mac_domain
        )
        index = self.expect(["(interface cable-mac )([0-9]+.[0-9]+)"] + self.prompt)
        if index != 0:
            assert 0, "ERROR:Failed to get the CM bundle id from CMTS"
        bundle = self.match.group(2)
        self.expect(self.prompt)
        return bundle

    @BaseCmts.connect_and_run
    def get_cmts_ip_bundle(self, cm_mac, gw_ip=None):
        """Get CMTS bundle IP

        :param cm_mac: mac address of the CM
        :type cm_mac: string
        :param gw_ip: gateway ip address
        :type gw_ip: string
        :return: returns cmts ip configured on the bundle
        :rtype: string
        """
        mac_domain = self.get_cm_mac_domain(cm_mac)
        self.get_cm_bundle(mac_domain)
        self.sendline(
            "show running-config interface cable-mac %s | include secondary"
            % mac_domain
        )
        self.expect(self.prompt)
        cmts_ip = re.search("ip address (%s) .* secondary" % gw_ip, self.before)

        if gw_ip is None:
            return self.before

        if cmts_ip:
            cmts_ip = cmts_ip.group(1)
        else:
            assert 0, "ERROR: Failed to get the CMTS bundle IP"
        return cmts_ip

    @BaseCmts.connect_and_run
    def reset(self):
        """Delete the startup config and Reboot the CMTS"""
        self.sendline("erase nvram")
        self.expect(self.prompt)
        self.sendline("reload")
        self.expect(self.prompt)

    @BaseCmts.connect_and_run
    def add_service_class(
        self, index, name, max_rate, max_burst, max_tr_burst=None, downstream=False
    ):
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
        :type max_tr_burst: optional
        :param downstream: True or False, defaults to False
        :type downstream: boolean
        """
        self.sendline(
            "qos-sc name %s max-tr-rate %s max-tr-burst %s max-burst %s"
            % (name, max_rate, max_tr_burst, max_burst)
        )
        self.expect(self.prompt)
        if downstream:
            self.sendline("qos-sc name %s dir 1" % name)
            self.expect(self.prompt)

    @BaseCmts.connect_and_run
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
        if "/" not in ip_bundle:
            ip_bundle += "/24"
            ip_bundle = ipaddress.IPv4Interface(six.text_type(ip_bundle))
        else:
            ip_bundle = ipaddress.IPv4Interface(six.text_type(ip_bundle))
        self.sendline("interface cable-mac %s" % index)
        self.expect(self.prompt)
        self.sendline("no shutdown")
        self.expect(self.prompt)
        self.sendline("cable ranging-interval 2000")
        self.expect(self.prompt)
        self.sendline("cable tftp-enforce")
        self.expect(self.prompt)
        self.sendline("cable dynamic-secret reject")
        self.expect(self.prompt)
        self.sendline("cable cm-ip-prov-mode %s" % prov_mode)
        self.expect(self.prompt)
        self.sendline("cable mcast-fwd-by-dsid no")
        self.expect(self.prompt)
        self.sendline("cable dynamic-rcc")
        self.expect(self.prompt)
        self.sendline("cable downstream-bonding-group dynamic enable")
        self.expect(self.prompt)
        self.sendline("cable mult-tx-chl-mode")
        self.expect(self.prompt)
        self.sendline("cable upstream ranging-poll t4-multiplier")
        self.expect(self.prompt)
        self.sendline("cable privacy mandatory bpi-plus")
        self.expect(self.prompt)
        self.sendline("ip address %s %s" % (ip_bundle.ip, ip_bundle.netmask))
        self.expect(self.prompt)
        self.sendline("exit")
        self.expect(self.prompt)
        for ch in qam_ch:
            self.sendline(
                "interface cable-downstream %s/%s cable cable-mac %s"
                % (qam_idx, ch, index)
            )
            self.expect(self.prompt)
            self.sendline(
                "interface cable-downstream %s/%s no shutdown" % (qam_idx, ch)
            )
            self.expect(self.prompt)
        for ch in ups_ch:
            self.sendline(
                "interface cable-upstream %s/%s cable cable-mac %s"
                % (qam_idx, ch, index)
            )
            self.expect(self.prompt)
            self.sendline("interface cable-upstream %s/%s no shutdown" % (qam_idx, ch))
            self.expect(self.prompt)

    @BaseCmts.connect_and_run
    def get_cmts_type(self):
        """This function is to get the product type on cmts

        :return: Returns the cmts module type.
        :rtype: string
        """
        self.sendline("show linecard status | include chassis")
        self.expect("Chassis Type:(.*)\r\n")
        result = self.match.group(1)
        if self.match is not None:
            output = result
        else:
            output = "None"
        self.expect(self.prompt)
        return output.strip().lower()

    @BaseCmts.connect_and_run
    @BaseCmts.convert_mac_to_cmts_type
    def get_qos_parameter(self, cm_mac):
        """To get the qos related parameters of CM
        Example output format : {'DS':  [{'Sfid': '1' ..},
                                         {'Sfid': '2' ..}
                                 'US': [{{'Sfid': '1' ..},
                                  'Maximum Burst': '128000',
                                  'IP ToS Overwrite [AND-msk, OR-mask]':
                                  ['0x00', '0x00'], ...},
                                  {'Sfid': '1' ..}}
        The units for measuring are
        1) Peak rate, Maximum Sustained rate,
           Minimum Reserved rate -- bits/sec
        2) Maximum Burst, Minimum Packet Size -- bytes
        3) Admitted Qos Timeout, Maximum Latency -- seconds
        4) Current Throughput -- [bits/sec, packets/sec]

        :param cm_mac: mac address of the cable modem
        :type cm_mac: string
        :return: containing the qos related parameters.
        :rtype: dictionary
        """
        self.sendline("no pagination")
        self.expect(self.prompt)
        qos_dict = {"US": [], "DS": []}
        self.sendline("show cable modem qos %s verbose" % (cm_mac))
        self.expect(self.prompt)
        service_flows = re.split(r"\n\s*\n", self.before)[1:-1]
        strip_units = ["bits/sec", "bytes", "seconds", "packets/sec", "usecs"]
        for service_flow in service_flows:
            service_flow_list = [i for i in service_flow.splitlines() if i]
            qos_dict_flow = {}
            for service in service_flow_list:
                service = service.split(":")
                key, value = [i.strip() for i in service]
                for i in strip_units:
                    value = value.replace(i, "").strip()

                if "scheduling type" in key:
                    qos_dict_flow[key] = value
                elif (
                    "ip tos" not in key.lower()
                    and "current throughput" not in key.lower()
                ):
                    qos_dict_flow[key] = value
                else:
                    qos_dict_flow[key] = [
                        value.split(" ")[0].replace(",", ""),
                        value.split(" ")[1].replace(",", ""),
                    ]
            if bool(qos_dict_flow):
                if "US" in qos_dict_flow.get("Direction"):
                    qos_dict["US"].append(qos_dict_flow)
                else:
                    qos_dict["DS"].append(qos_dict_flow)
        return qos_dict

    @BaseCmts.connect_and_run
    def ping(self, ping_ip, ping_count=5, timeout=10):
        """This function to ping the device from cmts
        :param ping_ip: device ip which needs to be verified
        :ping_ip type: string
        :param ping_count: Repeating ping packets, defaults to 3
        :ping_count type: integer
        :param timeout: timeout for the packets, defaults to 10 sec
        :type timeout: integer
        :return: True if ping passed else False
        """

        mode = "ipv%s" % ipaddress.ip_address(ping_ip).version
        basic_ping = (
            "ping repeat-count {} timeout {}".format(ping_count, timeout)
            if mode == "ipv4"
            else "ping ipv6"
        )

        self.check_output("end")
        self.sendline("{} {}".format(basic_ping, ping_ip))
        self.expect(self.prompt)
        match = re.search(
            "{} packets transmitted, {} packets received".format(
                ping_count, ping_count
            ),
            self.before,
        )
        if match:
            return True
        else:
            return False

    @BaseCmts.connect_and_run
    def check_output(self, cmd):
        """get check_output out from parent class """
        return super().check_output(cmd)

    def get_current_time(self, fmt="%Y-%m-%dT%H:%M:%S%z"):
        """Returns the current time on the CMTS
        :return: the current time as a string formatted as "%Y-%m-%dT%H:%M:%S%z"
        :raises CodeError: if anything went wrong in getting the time
        """
        self.current_time_cmd = "show clock"
        self.dateformat = "%Y %B %d %H:%M:%S"
        return super().get_current_time(fmt)
