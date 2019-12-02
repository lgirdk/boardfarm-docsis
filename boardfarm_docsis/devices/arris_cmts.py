# Copyright (c) 2018
#
# All rights reserved.
#
# This file is distributed under the Clear BSD license.
# The full text can be found in LICENSE in the root directory.
#!/usr/bin/env python

import pexpect
import netaddr
import six
import sys
import re

from . import base_cmts
from boardfarm.devices import connection_decider
from boardfarm.lib.regexlib import AllValidIpv6AddressesRegex, ValidIpv4AddressRegex
import ipaddress

class ArrisCMTS(base_cmts.BaseCmts):
    """Connects to and configures a ARRIS CMTS
    """
    prompt = ['arris(.*)>', 'arris(.*)#', 'arris\(.*\)> ', 'arris\(.*\)# ']
    model = "arris_cmts"

    class ArrisCMTSDecorators():

        @classmethod
        def mac_to_cmts_type_mac_decorator(cls, function):
            def wrapper(*args, **kwargs):
                args = list(args)
                if ':' in args[1]:
                    args[1] = args[0].get_cm_mac_cmts_format(args[1])
                return function(*args)
            return wrapper

    def __init__(self,
                 *args,
                 **kwargs):
        """Constructor method
        """
        conn_cmd = kwargs.get('conn_cmd', None)
        connection_type = kwargs.get('connection_type', 'local_serial')
        self.username = kwargs.get('username', 'boardfarm')
        self.password = kwargs.get('password', 'boardfarm')
        self.password_admin = kwargs.get('password_admin', 'boardfarm')
        self.ssh_password = kwargs.get('ssh_password', 'boardfarm')
        self.mac_domain = kwargs.get('mac_domain', None)
        self.channel_bonding = kwargs.get('channel_bonding', 32) # 24x8 : total 32

        if conn_cmd is None:
            # TODO: try to parse from ipaddr, etc
            raise Exception("No command specified to connect to Arris CMTS")

        self.connection = connection_decider.connection(connection_type, device = self, conn_cmd = conn_cmd, ssh_password = self.ssh_password)
        self.connection.connect()
        self.connect()
        self.logfile_read = sys.stdout

        self.name = kwargs.get('name', self.model)

    def connect(self):
        """This method is used to connect cmts, login to the cmts based on the connection type available

        :raises Exception: Unable to get prompt on ARRIS device
        """
        try:
            try:
                self.expect_exact("Escape character is '^]'.", timeout = 5)
            except:
                pass
            self.sendline()
            idx = self.expect(['\r\nLogin:', pexpect.TIMEOUT] + self.prompt, timeout = 10)
            if 0 == idx:
                self.sendline(self.username)
                self.expect('assword:')
                self.sendline(self.password)
                self.expect(self.prompt)
            elif idx > 1:
                # if we get a prompt we have probably ssh to the device
                pass
            else:
                # Over telnet we come in at the right prompt
                # over serial we could have a double login
                # not yet implemented
                raise('Failed to connect to Arris via telnet')
            self.sendline('enable')
            if 0 == self.expect(['Password:'] + self.prompt):
                self.sendline(self.password_admin)
                self.expect(self.prompt)
            self.sendline('config')
            self.expect('Enter configuration commands, one per line. End with exit or quit or CTRL Z')
            self.expect(self.prompt)
            self.sendline('pagination')
            self.expect(self.prompt)
            return
        except:
            raise Exception("Unable to get prompt on Arris device")

    def logout(self):
        """Logout of the CMTS device
        """
        self.sendline('exit')
        self.sendline('exit')

    @ArrisCMTSDecorators.mac_to_cmts_type_mac_decorator
    def check_online(self, cmmac):
        """Check the CM status from CMTS function checks the encrytion mode and returns True if online

        :param cmmac: mac address of the CM
        :type cmmac: string
        :return: True if the CM is operational else actual status on cmts
        :rtype: string / boolean
        """
        self.sendline('show cable modem  %s detail' % cmmac)
        self.expect(self.prompt)
        if 'State=Operational' in self.before:
            return True
        else:
            try:
                r = re.findall('State=(.*?\s)', self.before)[0].strip()
            except:
                r = 'Offline'
        return r

    @ArrisCMTSDecorators.mac_to_cmts_type_mac_decorator
    def clear_offline(self, cmmac):
        """Clear the CM entry from cmts which is offline -clear cable modem <mac> delete

        :param cmmac: mac address of the CM
        :type cmmac: string
        """
        self.sendline('exit')
        self.expect(self.prompt)
        self.sendline('clear cable modem %s delete' % cmmac)
        self.expect(self.prompt)
        self.sendline('configure')
        self.expect(self.prompt)

    @ArrisCMTSDecorators.mac_to_cmts_type_mac_decorator
    def clear_cm_reset(self, cmmac):
        """Reset the CM from cmts using cli -clear cable modem <mac> reset

        :param cmmac: mac address of the CM
        :type cmmac: string
        """
        self.sendline('exit')
        self.expect(self.prompt)
        """ NB: this command does not reboot the CM, but forces it to reinitialise """
        self.sendline("clear cable modem %s reset" % cmmac)
        self.expect(self.prompt)
        self.sendline('configure')
        self.expect(self.prompt)
        self.expect(pexpect.TIMEOUT, timeout = 5)
        online_state=self.check_online(cmmac)
        if(online_state==True):
            print("CM is still online after 5 seconds.")
        else:
            print("CM reset is initiated.")

    @ArrisCMTSDecorators.mac_to_cmts_type_mac_decorator
    def get_mtaip(self, cmmac, mtamac):
        """Get the MTA IP from CMTS

        :param cmmac: mac address of the CM
        :type cmmac: string
        :param mtamac: mta mac address
        :type mtamac: string
        :return: MTA ip address or "None" if ip not found
        :rtype: string
        """
        self.sendline('show cable modem %s detail | include MTA' % (cmmac))
        self.expect('CPE\(MTA\)\s+.*IPv4=(' + ValidIpv4AddressRegex + ')\r\n')
        result = self.match.group(1)
        if self.match != None:
            output = result
        else:
            output = "None"
        self.expect(self.prompt)
        return output

    @ArrisCMTSDecorators.mac_to_cmts_type_mac_decorator
    def get_ip_from_regexp(self, cmmac, ip_regexpr):
        """Gets an ip address according to a regexpr (helper function)

        :param cmmac: cable modem mac address
        :type cmmac: string
        :param ip_regexpr: regular expression for ip
        :type ip_regexpr: string
        :return: ip addr (ipv4/6 according to regexpr) or None if not found
        :rtype: string
        """
        self.sendline('show cable modem | include %s' % cmmac)
        if 1 == self.expect([cmmac + '\s+(' + ip_regexpr + ')', pexpect.TIMEOUT], timeout=2):
            output = "None"
        else:
            result = self.match.group(1)
            if self.match != None:
                output = result
            else:
                output = "None"
        self.expect(self.prompt)
        return output

    @ArrisCMTSDecorators.mac_to_cmts_type_mac_decorator
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

    @ArrisCMTSDecorators.mac_to_cmts_type_mac_decorator
    def get_cm_mac_domain(self, cm_mac):
        """Get the Mac-domain of Cable modem

        :param cm_mac: mac address of the CM
        :type cm_mac: string
        :return: mac_domain of the particular cable modem
        :rtype: string
        """
        mac_domain = None
        self.sendline('show cable modem %s detail | include Cable-Mac=' % cm_mac)
        if 0 == self.expect(['Cable-Mac= ([0-9]{1,3}),', pexpect.TIMEOUT], timeout=5):
            mac_domain = self.match.group(1)
        self.expect(self.prompt)
        return mac_domain

    @ArrisCMTSDecorators.mac_to_cmts_type_mac_decorator
    def check_PartialService(self, cmmac):
        """Check the cable modem is in partial service

        :param cmmac: mac address of the CM
        :type cmmac: string
        :return: 1 if is true else return the value as 0
        :rtype: int
        """
        self.sendline('show cable modem %s' % cmmac)
        self.expect(self.prompt)
        if "impaired" in self.before:
            output = 1
        else:
            output = 0
        return output

    @ArrisCMTSDecorators.mac_to_cmts_type_mac_decorator
    def DUT_chnl_lock(self, cm_mac):
        """Check the CM channel locks based on cmts type

        :param cm_mac: mac address of the CM
        :type cm_mac: string
        :returns: Locked channels of upstream and downstream
        :rtype: list
        """
        self.sendline("show cable modem  %s bonded-impaired" % cm_mac)
        self.expect(self.prompt)
        bonded_impared_status = self.before;
        if "No CMs were found" in bonded_impared_status:
            self.sendline("show cable modem  %s " % cm_mac)
            self.expect('(\d+)x(\d+)')
            downstream = int(self.match.group(1))
            upstream = int(self.match.group(2))
            self.expect(self.prompt)
        else:
            downstream = int(re.findall('(\d+x\d+)',bonded_impared_status)[1].split("x")[0])
            upstream = int(re.findall('(\d+x\d+)',bonded_impared_status)[1].split("x")[1])
        return [upstream,downstream]

    def save_running_config_to_local(self, filename):
        """save the running config to startup
        """
        self.sendline('no pagination')
        self.expect(self.prompt)
        #show running-config will display the current running config file of CMTS
        self.sendline('show running-config')
        self.expect('arrisc4\(config\)\#')
        f = open(filename, "w")
        f.write(self.before)
        f.write(self.after)
        f.close()

    def save_running_to_startup_config(self):
        """Copy running config to local machine
        """
        self.sendline('exit')
        self.expect(self.prompt)
        self.sendline('copy running-config startup-config')
        self.expect(self.prompt)
        self.sendline('config')
        self.expect(self.prompt)

    def get_qam_module(self):
        """Get the module of the qam

        :return: Module of the qam
        :rtype: string
        """
        self.sendline('show linecard status | include DMM/DMM')
        self.expect(self.prompt)
        return  self.before.split("\n",1)[1]

    def get_ups_module(self):
        """Get the upstream module of the qam

        :return: list of module number of the qam
        :rtype: list
        """
        self.sendline('show linecard status | include CAM/CAM')
        self.expect(self.prompt)
        results = list(map(int, re.findall('(\d+)    CAM ', self.before)))
        return results

    def set_iface_ipaddr(self, iface, ipaddr):
        """This function is to set an ip address to an interface on cmts

        :param iface: interface name ,
        :type iface: string
        :param ipaddr: <ip></><subnet> using 24 as default if subnet is not provided.
        :type ipaddr: string
        """
        if  "/" not in ipaddr:
            ipaddr  += "/24"
            ipaddr = ipaddress.IPv4Interface(six.text_type(ipaddr))
        else:
            ipaddr = ipaddress.IPv4Interface(six.text_type(ipaddr))
        self.sendline('interface %s' % iface)
        self.expect(self.prompt)
        self.sendline('ip address %s %s'  %(ipaddr.ip, ipaddr.netmask))
        self.expect(self.prompt)
        self.sendline('no shutdown')
        self.expect(self.prompt)
        self.sendline('exit')
        self.expect(self.prompt)

    def set_iface_ipv6addr(self, iface, ipaddr):
        """Configure ipv6 address

        :param iface: interface name
        :type iface: string
        :param ipaddr: ipaddress to configure
        :type ipaddr: string
        """
        self.sendline('interface %s' % iface)
        self.expect(self.prompt)
        self.sendline('ipv6 address %s' % ipaddr)
        self.expect(self.prompt)
        self.sendline('no shutdown')
        self.expect(self.prompt)
        self.sendline('exit')
        self.expect(self.prompt)

    def unset_iface_ipaddr(self, iface):
        """This function is to unset an ipv4 address of an interface on cmts

        :param iface: interface name
        :type iface: string
        """
        self.sendline('interface %s' % iface)
        self.expect(self.prompt)
        self.sendline('no ip address')
        self.expect(self.prompt)
        self.sendline('exit')
        self.expect(self.prompt)

    def unset_iface_ipv6addr(self, iface):
        """This function is to unset an ipv6 address of an interface on cmts

        :param iface: interface name.
        :type iface: string
        """
        self.sendline('interface %s' % iface)
        self.expect(self.prompt)
        self.sendline('no ipv6 address')
        self.expect(self.prompt)
        self.sendline('exit')
        self.expect(self.prompt)

    def del_file(self, f):
        """delete file on cmts

        :param f: filename to delete from cmts
        :type f: string
        """
        self.sendline('exit')
        self.expect(self.prompt)
        self.sendline('delete %s' % f)
        self.expect(self.prompt)

    def check_docsis_mac_ip_provisioning_mode(self, index):
        """
        Get the provisioning mode of the cable modem from CMTS
        :param index: mac domain of the cable modem
        :type index: string
        :return: mode of the provisioning(ipv4, ipv6, dual-stack, bridge)
        :rtype: string
        """
        self.sendline('show running-config interface cable-mac %s | include cm-ip-prov-mode' % index)
        self.expect(self.prompt)
        result = self.before.split("\n")[1].split(" ")[-1]
        if "ipv4" in result.lower():
            result = "ipv4"
        elif "dual" in result.lower():
            result = "dual-stack"
        elif "ipv6" in result.lower():
            result = "ipv6"
        elif "bridge" in result.lower():
            result = "bridge"
        return result

    def modify_docsis_mac_ip_provisioning_mode(self, index, ip_pvmode = 'dual-stack'):
        """Change the ip provsioning mode

        :param index: mac domain of the cable modem configured
        :type index: string
        :param ip_pvmode: provisioning mode can ipv4, ipv6 or 'dual-stack', defaults to 'dual-stack'
        :type ip_pvmode: string
        """
        if ('dual-stack' in ip_pvmode.lower() and 'c4' in self.get_cmts_type()):
            print('dual-stack ip provisioning modem is not supported on Chassis Type : C4 please choose apm')
            return
        self.sendline('interface cable-mac %s' % index)
        self.expect(self.prompt)
        self.sendline('cable cm-ip-prov-mode %s' % ip_pvmode)
        self.expect(self.prompt)
        self.sendline('exit')
        self.expect(self.prompt)
        self.sendline('show running-config interface cable-mac %s | include cm-ip-prov-mode' % index)
        self.expect(self.prompt)
        check_docsis_mac_ip_provisioning_mode = self.check_docsis_mac_ip_provisioning_mode(index)
        if check_docsis_mac_ip_provisioning_mode in ip_pvmode:
            print("The ip provision mode is successfully set.")
        else:
            print("An error occured while setting the ip provision mode.")

    def add_route(self, ipaddr, gw):
        """This function is to add route

        :param ipaddr: <network ip></><subnet ip> take subnet 24 if not provided,
        :param ipaddr: string
        :param gw: gateway ip.
        :type gw: string
        """
        if  "/" not in ipaddr:
            ipaddr  += "/24"
            ipaddr = ipaddress.IPv4Interface(six.text_type(ipaddr))
        else:
            ipaddr = ipaddress.IPv4Interface(six.text_type(ipaddr))
        self.sendline('ip route %s %s %s' % (ipaddr.ip, ipaddr.netmask, gw))
        self.expect(self.prompt)
        if 'error' in self.before.lower():
            print("An error occured while adding the route.")
        self.sendline('show ip route')
        self.expect(self.prompt)
        if gw in self.before:
            print("The route is available on cmts.")
        else:
            print("The route is not available on cmts.")

    def add_route6(self, net, gw):
        """This function is to add route6

        :param net: <network ip></><subnet ip> take subnet 24 if not provided,
        :param net: string
        :param gw: gateway ip.
        :type gw: string
        """
        self.sendline('ipv6 route %s %s' % (net, gw))
        self.expect(self.prompt)
        if 'error' in self.before.lower():
            print("An error occured while adding the route.")
        self.sendline('show ipv6 route')
        self.expect(self.prompt)
        if str(ipaddress.IPv6Address(six.text_type(gw))).lower() in self.before.lower():
            print("The route is available on cmts.")
        else:
            print("The route is not available on cmts.")

    def del_route(self, ipaddr, gw):
        """This function is to delete route

        :param ipaddr: <network ip></><subnet ip> take subnet 24 if not provided
        :type ipaddr: string
        :param gw: gateway ip
        :type gw: string
        """
        if  "/" not in ipaddr:
            ipaddr  += "/24"
            ipaddr = ipaddress.IPv4Interface(six.text_type(ipaddr))
        else:
            ipaddr = ipaddress.IPv4Interface(six.text_type(ipaddr))
        self.sendline('no ip route %s %s %s' % (ipaddr.ip, ipaddr.netmask, gw))
        self.expect(self.prompt)
        if 'error' in self.before.lower():
            print("An error occured while deleting the route.")
        self.expect(pexpect.TIMEOUT, timeout = 10)
        self.sendline('show ip route')
        self.expect(self.prompt)
        if gw in self.before:
            print("The route is still available on cmts.")
        else:
            print("The route is not available on cmts.")

    def del_route6(self, net, gw):
        """This function is to delete ipv6 route

        :param net: <network ip></><subnet ip> take subnet 24 if not provided,
        :type net: string
        :param gw: gateway ip
        :type gw: string
        """
        self.sendline('no ipv6 route %s %s' % (net, gw))
        self.expect(self.prompt)
        if 'error' in self.before.lower():
            print("An error occured while deleting the route.")
        self.sendline('show ipv6 route')
        self.expect(self.prompt)
        if str(ipaddress.ip_address(six.text_type(gw)).compressed).lower() in self.before.lower() or gw.lower() in self.before.lower():
            print("The route is still available on cmts.")
        else:
            print("The route is not available on cmts.")

    def add_ip_bundle(self, index, helper_ip, ipaddr, secondary_ips = []):
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
        if  "/" not in ipaddr:
            ipaddr  += "/24"
            ipaddr = ipaddress.IPv4Interface(six.text_type(ipaddr))
        else:
            ipaddr = ipaddress.IPv4Interface(six.text_type(ipaddr))
        self.sendline('interface cable-mac %s' % index)
        self.expect(self.prompt)
        self.sendline('ip address %s %s'  %(ipaddr.ip, ipaddr.netmask))
        self.expect(self.prompt)
        for ip2 in secondary_ips:
            if  "/" not in ip2:
                ip2  += "/24"
                ip2 = ipaddress.IPv4Interface(six.text_type(ip2))
            else:
                ip2 = ipaddress.IPv4Interface(six.text_type(ip2))
            self.sendline('ip address %s %s secondary' %(ip2.ip, ip2.netmask))
            self.expect(self.prompt)
        self.sendline('cable helper-address %s cable-modem' % helper_ip)
        self.expect(self.prompt)
        self.sendline('cable helper-address %s mta' % helper_ip)
        self.expect(self.prompt)
        self.sendline('cable helper-address %s host' % helper_ip)
        self.expect(self.prompt)
        self.sendline('exit')
        self.expect(self.prompt)
        self.sendline('show running-config interface cable-mac %s | include ip address' % index)
        self.expect(self.prompt)
        if str(ipaddr.ip) in self.before:
            print("The ip bundle is successfully set.")
        else:
            print("An error occured while setting the ip bundle.")

    def add_ipv6_bundle_addrs(self, index, helper_ip, ip, secondary_ips = []):
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
        self.sendline('interface cable-mac %s' % index)
        self.expect(self.prompt)
        self.sendline('ipv6 address %s' % ip)
        self.expect(self.prompt)
        self.sendline('ipv6 dhcp relay destination %s' % helper_ip)
        self.expect(self.prompt)
        self.sendline('exit')
        self.expect(self.prompt)
        self.sendline('show running-config interface cable-mac %s | include ipv6 address' % index)
        self.expect(self.prompt)
        if str(ipaddress.ip_address(six.text_type(ip[:-3])).compressed) in self.before:
            print("The ipv6 bundle is successfully set.")
        else:
            print("An error occured while setting the ipv6 bundle.")

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
        self.sendline('interface cable-downstream %s/%s' % (index, sub))
        self.expect(self.prompt)
        self.sendline('cable power %s' % power)
        self.expect(self.prompt)
        self.sendline('no shutdown')
        self.expect(self.prompt)
        self.sendline('exit')
        self.expect(self.prompt)

    def wait_for_ready(self):
        """Check the cmts status
        """
        max_iteration = 5
        self.sendline('show linecard status')
        while 0 == self.expect(['Down | OOS'] + self.prompt) and max_iteration>0:
            max_iteration-= 1
            self.expect(self.prompt)
            self.expect(pexpect.TIMEOUT, timeout = 5)
            self.sendline('show linecard status')

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
        self.sendline('interface cable-downstream %s/%s' % (index, sub))
        self.expect(self.prompt)
        self.sendline('cable frequency %s' % freq)
        self.expect(self.prompt)
        self.sendline('no shutdown' )
        self.expect(self.prompt)
        self.sendline('exit')
        self.expect(self.prompt)

    def add_service_group(self, index, qam_idx, qam_sub, qam_channels, ups_idx, ups_channels):
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
        print("Service group is auto configured in ARRIS once mac domain is created.")

    def mirror_traffic(self, macaddr = ""):
        """Send the mirror traffic

        :param macaddr: mac address of the device if avaliable, defaults to empty string ""
        :type macaddr: string
        """
        print("Mirror traffic feature is not supported in ARRIS unless we use lawful intercept functionality.")

    def unmirror_traffic(self):
        """stop mirroring the traffic
        """
        print("Unmirror traffic feature is not supported in ARRIS unless we use lawful intercept functionality.")

    def run_tcpdump(self, time, iface = 'any', opts = ""):
        """tcpdump capture on the cmts interface

        :param time: timeout to wait till gets prompt
        :type time: integer
        :param iface: any specific interface, defaults to 'any'
        :type iface: string, optional
        :param opts: any other options to filter, defaults to ""
        :type opts: string
        """
        print("TCPDUMP feature is not supported in ARRIS.")

    @ArrisCMTSDecorators.mac_to_cmts_type_mac_decorator
    def is_cm_bridged(self, mac, offset = 2):
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

    @ArrisCMTSDecorators.mac_to_cmts_type_mac_decorator
    def get_ertr_ipv4(self, mac, offset = 2):
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
        ertr_ipv4 = re.search('(%s) .*=(%s)' % (ertr_mac,ValidIpv4AddressRegex), self.before)
        if ertr_ipv4:
            ipv4 = ertr_ipv4.group(2)
            return ipv4
        else:
            return None

    @ArrisCMTSDecorators.mac_to_cmts_type_mac_decorator
    def get_ertr_ipv6(self, mac, offset = 2):
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
        ertr_ipv6 = re.search('(%s) IPv6=(%s)' % (ertr_mac,AllValidIpv6AddressesRegex), self.before)
        if ertr_ipv6:
            ipv6 = ertr_ipv6.group(2)
            return ipv6
        else:
            return None

    def get_center_freq(self, mac_domain = None):
        """This function is to return the center frequency of cmts

        :param mac_domain: Mac Domain of the cable modem
        :type mac_domain: string
        :return: Returns center frequency configured on the qam
        :rtype: string
        """
        if mac_domain is None:
            mac_domain = self.mac_domain
        assert mac_domain is not None, "get_center_freq() requires mac_domain to be set"
        self.sendline('no pagination')
        self.expect(self.prompt)
        self.sendline('show interface cable downstream')
        self.expect(self.prompt)
        freq_list=[]
        for row in self.before.split("\n")[3:]:
            match_grp=re.match("\d{1,2}/\d{1,2}\s+"+str(mac_domain)+"\s.*\s(\d{6,10})\s+\w+",row)
            if match_grp!=None and match_grp.groups(0)[0]!=None:
                freq_list.append(match_grp.groups(0)[0])
        freq_list = map(int, freq_list)
        return str(min(freq_list))

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
        self.sendline('interface cable-upstream %s/%s' % (ups_idx, ups_ch))
        self.expect(self.prompt)
        self.sendline('cable frequency %s' % freq)
        self.expect(self.prompt)
        self.sendline('cable channel-width %s' % width)
        self.expect(self.prompt)
        self.sendline('cable power-level %s' % power)
        self.expect(self.prompt)
        self.sendline('cable modulation-profile 64')
        self.expect(self.prompt)
        self.sendline('cable mini-slot-size 2')
        self.sendline('no shutdown')
        self.expect(self.prompt)
        self.sendline('exit')
        self.expect(self.prompt)

    def get_cm_bundle(self, mac_domain):
        """Get the bundle id from cable modem

        :param mac_domain: Mac_domain of the cable modem connected
        :type mac_domain: string
        :return: bundle id
        :rtype: string
        """
        self.sendline('show running-config interface cable-mac %s | include cable-mac [0-9]+.[0-9]+' % mac_domain)
        index = self.expect(['(interface cable-mac )([0-9]+.[0-9]+)'] + self.prompt)
        if index != 0:
            assert 0, "ERROR:Failed to get the CM bundle id from CMTS"
        bundle = self.match.group(2)
        self.expect(self.prompt)
        return bundle

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
        self.sendline('show running-config interface cable-mac %s | include secondary' % mac_domain)
        self.expect(self.prompt)
        cmts_ip = re.search('ip address (%s) .* secondary' % gw_ip, self.before)

        if gw_ip is None:
            return self.before

        if cmts_ip:
            cmts_ip = cmts_ip.group(1)
        else:
            assert 0, "ERROR: Failed to get the CMTS bundle IP"
        return cmts_ip

    def reset(self):
        """Delete the startup config and Reboot the CMTS
        """
        self.sendline('erase nvram')
        self.expect(self.prompt)
        self.sendline('reload')
        self.expect(self.prompt)

    def add_service_class(self, index, name, max_rate, max_burst, max_tr_burst = None, downstream = False):
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
        self.sendline('qos-sc name %s max-tr-rate %s max-tr-burst %s max-burst %s' % (name, max_rate,max_tr_burst,max_burst))
        self.expect(self.prompt)
        if downstream:
            self.sendline('qos-sc name %s dir 1' % name)
            self.expect(self.prompt)

    def add_iface_docsis_mac(self, index, ip_bundle, qam_idx, qam_ch, ups_idx, ups_ch, qam_sub = None, prov_mode = None):
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
        if  "/" not in ip_bundle:
            ip_bundle  += "/24"
            ip_bundle = ipaddress.IPv4Interface(six.text_type(ip_bundle))
        else:
            ip_bundle = ipaddress.IPv4Interface(six.text_type(ip_bundle))
        self.sendline('interface cable-mac %s' % index)
        self.expect(self.prompt)
        self.sendline('no shutdown')
        self.expect(self.prompt)
        self.sendline('cable ranging-interval 2000')
        self.expect(self.prompt)
        self.sendline('cable tftp-enforce')
        self.expect(self.prompt)
        self.sendline('cable dynamic-secret reject')
        self.expect(self.prompt)
        self.sendline('cable cm-ip-prov-mode %s'% prov_mode)
        self.expect(self.prompt)
        self.sendline('cable mcast-fwd-by-dsid no')
        self.expect(self.prompt)
        self.sendline('cable dynamic-rcc')
        self.expect(self.prompt)
        self.sendline('cable downstream-bonding-group dynamic enable')
        self.expect(self.prompt)
        self.sendline('cable mult-tx-chl-mode')
        self.expect(self.prompt)
        self.sendline('cable upstream ranging-poll t4-multiplier')
        self.expect(self.prompt)
        self.sendline('cable privacy mandatory bpi-plus')
        self.expect(self.prompt)
        self.sendline('ip address %s %s'  %(ip_bundle.ip, ip_bundle.netmask))
        self.expect(self.prompt)
        self.sendline('exit')
        self.expect(self.prompt)
        for ch in qam_ch:
            self.sendline('interface cable-downstream %s/%s cable cable-mac %s'% (qam_idx, ch, index))
            self.expect(self.prompt)
            self.sendline('interface cable-downstream %s/%s no shutdown'% (qam_idx, ch))
            self.expect(self.prompt)
        for ch in ups_ch:
            self.sendline('interface cable-upstream %s/%s cable cable-mac %s'% (qam_idx, ch, index))
            self.expect(self.prompt)
            self.sendline('interface cable-upstream %s/%s no shutdown'% (qam_idx, ch))
            self.expect(self.prompt)

    def get_cmts_type(self):
        """This function is to get the product type on cmts

        :return: Returns the cmts module type.
        :rtype: string
        """
        self.sendline('show linecard status | include chassis')
        self.expect('Chassis Type:(.*)\r\n')
        result = self.match.group(1)
        if self.match != None:
            output = result
        else:
            output = "None"
        self.expect(self.prompt)
        return output.strip().lower()

    @ArrisCMTSDecorators.mac_to_cmts_type_mac_decorator
    def get_qos_parameter(self, cm_mac):
        """To get the qos related parameters of CM, to get the qos related parameters ["Maximum Concatenated Burst", "Maximum Burst", "Maximum Sustained rate", "Mimimum Reserved rate", "Scheduling Type"] of CM

        :param cm_mac: mac address of the cable modem
        :type cm_mac: string
        :return: containing the qos related parameters.
        :rtype: dictionary
        """
        self.sendline('no pagination')
        self.expect(self.prompt)
        qos_dict = {}
        service_flows = ["US" , "DS"]
        for value in service_flows:
            self.sendline("show cable modem qos %s | include %s" % (cm_mac, value))
            self.expect(self.prompt)
            qos_dict[value] = {"sfid" : self.before.split("\n")[-2].split(" ")[0].strip()}

        #mapping of the ouput stream to the US/DS and using the index
        self.sendline("show cable modem qos %s verbose" % (cm_mac))
        self.expect(self.prompt)

        #setting the index to filter the US/DS parameters from cmts.
        US_index = 0 if qos_dict["US"]["sfid"] in self.before.split("Sfid")[1] else 1
        qos_parameters = ["Maximum Concatenated Burst", "Maximum Burst", "Maximum Sustained rate", "Minimum Reserved rate", "Scheduling Type"]
        qos_data = []
        for i in range(1,3):
            qos_data.append([string[:-1] for string in self.before.split("Sfid")[i].split("\n") if any(param in string for param in qos_parameters)])

        qos_dict["US"].update(dict([x.split(":")[0].strip(), x.split(":")[1].strip()] for x in qos_data[US_index]))
        del qos_data[US_index]
        qos_dict["DS"].update(dict([x.split(":")[0].strip(), x.split(":")[1].strip()] for x in qos_data[0]))

        #removing the unit of measure
        for value in service_flows:
            for param in qos_parameters[:-1]:
                if qos_dict[value].get(param) : qos_dict[value].update({ param : int(qos_dict[value][param].split(" ")[0])})
        return qos_dict
