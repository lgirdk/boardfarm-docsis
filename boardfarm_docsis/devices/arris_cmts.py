# Copyright (c) 2018
#
# All rights reserved.
#
# This file is distributed under the Clear BSD license.
# The full text can be found in LICENSE in the root directory.
#!/usr/bin/env python

import pexpect
import netaddr
import sys
import re

import base_cmts
from boardfarm.devices import connection_decider
from boardfarm.lib.regexlib import AllValidIpv6AddressesRegex, ValidIpv4AddressRegex
import ipaddress

class ArrisCMTS(base_cmts.BaseCmts):
    '''
    Connects to and configures a Arris CMTS
    '''

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
        conn_cmd = kwargs.get('conn_cmd', None)
        connection_type = kwargs.get('connection_type', 'local_serial')
        self.username = kwargs.get('username', 'boardfarm')
        self.password = kwargs.get('password', 'boardfarm')
        self.password_admin = kwargs.get('password_admin', 'boardfarm')
        self.ssh_password = kwargs.get('ssh_password', 'boardfarm')
        self.mac_domain = kwargs.get('mac_domain', None)

        if conn_cmd is None:
            # TODO: try to parse from ipaddr, etc
            raise Exception("No command specified to connect to Arris CMTS")

        self.connection = connection_decider.connection(connection_type, device = self, conn_cmd = conn_cmd, ssh_password = self.ssh_password)
        self.connection.connect()
        self.connect()
        self.logfile_read = sys.stdout

        self.name = kwargs.get('name', self.model)

    def connect(self):
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
        self.sendline('exit')
        self.sendline('exit')

    @ArrisCMTSDecorators.mac_to_cmts_type_mac_decorator
    def check_online(self, cmmac):
        """
        Function checks the encrytion mode and returns True if online
        Args: cmmac
        Return: True if the CM is operational
                The actual status otherwise
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
        """
        Reset a modem
        Args: cmmac
        """
        self.sendline('exit')
        self.expect(self.prompt)
        self.sendline('clear cable modem %s offline' % cmmac)
        self.expect(self.prompt)
        self.sendline('configure')
        self.expect(self.prompt)

    @ArrisCMTSDecorators.mac_to_cmts_type_mac_decorator
    def clear_cm_reset(self, cmmac):
        """
        Reset a modem
        Args: cmmac
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
        """
        Gets the mta ip address
        Args: cmmac, mtamac(not used)
        Return: mta ip or None if not found
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
        """
        Gets an ip address according to a regexpr (helper function)
        Args: cmmac, ip_regexpr
        Return: ip addr (ipv4/6 according to regexpr) or None if not found
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
        """
        Returns the CM mgmt ipv4 address
        Args: cmmac
        Return: ip addr (ipv4) or None if not found
        """
        return self.get_ip_from_regexp(cmmac, ValidIpv4AddressRegex)

    def get_cmipv6(self, cmmac):
        """
        Returns the CM mgmt ipv6 address
        Args: cmmac
        Return: ip addr (ipv4) or None if not found
        """
        return self.get_ip_from_regexp(cmmac, AllValidIpv6AddressesRegex)

    @ArrisCMTSDecorators.mac_to_cmts_type_mac_decorator
    def get_cm_mac_domain(self, cm_mac):
        """
        Returns the Mac-domain of Cable modem
        Args: cm_mac
        Return: ip addr (ipv4) or None if not found
        """
        mac_domain = None
        self.sendline('show cable modem %s detail | include Cable-Mac=' % cm_mac)
        if 0 == self.expect(['Cable-Mac= ([0-9]{1,3}),', pexpect.TIMEOUT], timeout=5):
            mac_domain = self.match.group(1)
        self.expect(self.prompt)
        return mac_domain

    @ArrisCMTSDecorators.mac_to_cmts_type_mac_decorator
    def check_PartialService(self, cmmac):
        self.sendline('show cable modem %s' % cmmac)
        self.expect(self.prompt)
        if "impaired" in self.before:
            output = 1
        else:
            output = 0
        return output

    @ArrisCMTSDecorators.mac_to_cmts_type_mac_decorator
    def DUT_chnl_lock(self, cm_mac):
        """Check the CM channel locks with 24*8 """
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
        '''
        This function is to save the running config file of the CMTS to the local directory.
        Input : filename to save the config
        Output : writing the CMTS config to the file with specified name
        '''
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
        '''
        This function is to over write the startup config file of the CMTS with the current running config file.
        Input : None
        Output : Overwritten startup-config file with running-config file on CMTS
        '''
        self.sendline('exit')
        self.expect(self.prompt)
        self.sendline('copy running-config startup-config')
        self.expect(self.prompt)
        self.sendline('config')
        self.expect(self.prompt)

    def get_qam_module(self):
        '''
        This function is to return the qam (DCAM) modules on cmts.
        Input : None
        Output : Returns the qam (DCAM) modules on cmts.
        '''
        self.sendline('show linecard status | include DMM/DMM')
        self.expect(self.prompt)
        return  self.before.split("\n",1)[1]

    def get_ups_module(self):
        '''
        This function is to return the upc (UCAM) modules on cmts.
        Input : None
        Output : Returns the upc (UCAM) modules on cmts.
        '''
        self.sendline('show linecard status | include CAM/CAM')
        self.expect(self.prompt)
        results = list(map(int, re.findall('(\d+)    CAM ', self.before)))
        return results

    def set_iface_ipaddr(self, iface, ipaddr):
        '''
        This function is to set an ip address to an interface on cmts.
        Input : arg1: interface name , arg2: <ip></><subnet> using 24 as default if subnet is not provided.
        Output : None (sets the ip address to an interface specified).
        '''
        if  "/" not in ipaddr:
            ipaddr  += "/24"
            ipaddr = ipaddress.IPv4Interface(unicode(ipaddr))
        else:
            ipaddr = ipaddress.IPv4Interface(unicode(ipaddr))
        self.sendline('interface %s' % iface)
        self.expect(self.prompt)
        self.sendline('ip address %s %s'  %(ipaddr.ip, ipaddr.netmask))
        self.expect(self.prompt)
        self.sendline('no shutdown')
        self.expect(self.prompt)
        self.sendline('exit')
        self.expect(self.prompt)

    def set_iface_ipv6addr(self, iface, ipaddr):
        '''
        This function is to set an ipv6 address to an interface on cmts.
        Input : arg1: interface name , arg2: ipv6 address / prefix as one string.
        Output : None (sets the ipv6 address to an interface specified).
        '''
        self.sendline('interface %s' % iface)
        self.expect(self.prompt)
        self.sendline('ipv6 address %s' % ipaddr)
        self.expect(self.prompt)
        self.sendline('no shutdown')
        self.expect(self.prompt)
        self.sendline('exit')
        self.expect(self.prompt)

    def unset_iface_ipaddr(self, iface):
        '''
        This function is to unset an ipv4 address of an interface on cmts.
        Input : arg1: interface name.
        Output : None (unsets the ip address of an interface specified).
        '''
        self.sendline('interface %s' % iface)
        self.expect(self.prompt)
        self.sendline('no ip address')
        self.expect(self.prompt)
        self.sendline('exit')
        self.expect(self.prompt)

    def unset_iface_ipv6addr(self, iface):
        '''
        This function is to unset an ipv6 address of an interface on cmts.
        Input : arg1: interface name.
        Output : None (unsets the ipv6 address of an interface specified).
        '''
        self.sendline('interface %s' % iface)
        self.expect(self.prompt)
        self.sendline('no ipv6 address')
        self.expect(self.prompt)
        self.sendline('exit')
        self.expect(self.prompt)

    def del_file(self, f):
        '''
        This function is to delete a file on cmts.
        Input : arg: file name to be deleted if in current directory relative file name to be deleted from /system if in different directory.
        Output : None (specifie file will be deleted on cmts.)
        '''
        self.sendline('exit')
        self.expect(self.prompt)
        self.sendline('delete %s' % f)
        self.expect(self.prompt)

    def check_docsis_mac_ip_provisioning_mode(self, index):
        '''
        This function is to return the ip provisioning mode of a mac domain.
        Input : arg: integer value of the mac domain for which we need the mode supported.
        Output : Return the mode supports in the form of string (Ex: ipv4only)
        '''
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
        '''
        This function is to set the ip provisioning mode.
        Input : arg1 : index of the interface, arg2 : ip provisioning mode to be set on the interface (default is dual-stack).
        Output : None (wait if any interface is down until it is up).
        '''
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
        '''
        This function is to add route.
        Input : arg1 : <network ip></><subnet ip> take subnet 24 if not provided, arg2 : gateway ip.
        Output : None (adds the route to the specified parameters).
        '''
        if  "/" not in ipaddr:
            ipaddr  += "/24"
            ipaddr = ipaddress.IPv4Interface(unicode(ipaddr))
        else:
            ipaddr = ipaddress.IPv4Interface(unicode(ipaddr))
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
        '''
        This function is to add ipv6 route.
        Input : arg1 : network ip/subnet, arg3 : gateway ip.
        Output : None (adds the route to the specified parameters).
        '''
        self.sendline('ipv6 route %s %s' % (net, gw))
        self.expect(self.prompt)
        if 'error' in self.before.lower():
            print("An error occured while adding the route.")
        self.sendline('show ipv6 route')
        self.expect(self.prompt)
        if str(ipaddress.IPv6Address(unicode(gw))).lower() in self.before.lower():
            print("The route is available on cmts.")
        else:
            print("The route is not available on cmts.")

    def del_route(self, ipaddr, gw):
        '''
        This function is to delete route.
        Input : arg1 : <network ip></><subnet ip> take subnet 24 if not provided, arg2 : gateway ip.
        Output : None (deletes the route to the specified parameters).
        '''
        if  "/" not in ipaddr:
            ipaddr  += "/24"
            ipaddr = ipaddress.IPv4Interface(unicode(ipaddr))
        else:
            ipaddr = ipaddress.IPv4Interface(unicode(ipaddr))
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
        '''
        This function is to delete ipv6 route.
        Input : arg1 : <network ip></><subnet>,arg3 : gateway ip with no subnet.
        Output : None (deletes the route to the specified parameters).
        '''
        self.sendline('no ipv6 route %s %s' % (net, gw))
        self.expect(self.prompt)
        if 'error' in self.before.lower():
            print("An error occured while deleting the route.")
        self.sendline('show ipv6 route')
        self.expect(self.prompt)
        if str(ipaddress.ip_address(unicode(gw)).compressed).lower() in self.before.lower() or gw.lower() in self.before.lower():
            print("The route is still available on cmts.")
        else:
            print("The route is not available on cmts.")

    def add_ip_bundle(self, index, helper_ip, ipaddr, secondary_ips = []):
        '''
        This function is to add ip bundle to a cable mac.
        Input : arg1 : cable mac index, arg2 : helper ip to be used, arg3 : actual ip to be assiged to cable mac in the format <ip></><subnet> subnet defaut taken as 24 if not provided, arg4 : list of seconday ips  in the format <ip></><subnet> subnet defaut taken as 24 if not provided.
        Output : None (sets the ip bundle to a cable mac).
        '''
        if  "/" not in ipaddr:
            ipaddr  += "/24"
            ipaddr = ipaddress.IPv4Interface(unicode(ipaddr))
        else:
            ipaddr = ipaddress.IPv4Interface(unicode(ipaddr))
        self.sendline('interface cable-mac %s' % index)
        self.expect(self.prompt)
        self.sendline('ip address %s %s'  %(ipaddr.ip, ipaddr.netmask))
        self.expect(self.prompt)
        for ip2 in secondary_ips:
            if  "/" not in ip2:
                ip2  += "/24"
                ip2 = ipaddress.IPv4Interface(unicode(ip2))
            else:
                ip2 = ipaddress.IPv4Interface(unicode(ip2))
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
        '''
        This function is to add ipv6 bundle to a cable mac.
        Input : arg1 : cable mac index, arg2 : helper ip to be used, arg3 : actual ip to be assiged to cable mac in the format <ipv6/subnet>, arg4 : list of seconday ips  in the format <ipv6/subnet> (ignored in arris).
        Output : None (sets the ipv6 bundle to a cable mac).
        '''
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
        if str(ipaddress.ip_address(unicode(ip[:-3])).compressed) in self.before:
            print("The ipv6 bundle is successfully set.")
        else:
            print("An error occured while setting the ipv6 bundle.")

    def set_iface_qam(self, index, sub, annex, interleave, power):
        '''
        This function is to set the power level on downstraem channel, setting of annex and interleave are global in arris.
        Input : arg1 : cable mac index, arg2 : channel to be used, arg3 : annnex to be set (ignored in arris), arg4 : interleave to be set (ignored in arris), arg5 : power level to be set.
        Output : None (sets the power level on channel as defined).
        '''
        self.sendline('interface cable-downstream %s/%s' % (index, sub))
        self.expect(self.prompt)
        self.sendline('cable power %s' % power)
        self.expect(self.prompt)
        self.sendline('no shutdown')
        self.expect(self.prompt)
        self.sendline('exit')
        self.expect(self.prompt)

    def wait_for_ready(self):
        '''
        This function is to wait until all the interface are up and available.
        Input : None.
        Output : None (wait if any interface is down until it is up for a maximum of 5 times with a wait of 1min each).
        '''
        max_iteration = 5
        self.sendline('show linecard status')
        while 0 == self.expect(['Down | OOS'] + self.prompt) and max_iteration>0:
            max_iteration-= 1
            self.expect(self.prompt)
            self.expect(pexpect.TIMEOUT, timeout = 5)
            self.sendline('show linecard status')

    def set_iface_qam_freq(self, index, sub, channel, freq):
        '''
        This function is to set the frequency on downstream channel.
        Input : arg1 : cable mac index, arg2 : channel to be used, arg3 : channel to be used (ignored in arris as sub and channel are same), arg4 : frequency to set.
        Output : None (sets the frequency on channel as defined).
        '''
        self.sendline('interface cable-downstream %s/%s' % (index, sub))
        self.expect(self.prompt)
        self.sendline('cable frequency %s' % freq)
        self.expect(self.prompt)
        self.sendline('no shutdown' )
        self.expect(self.prompt)
        self.sendline('exit')
        self.expect(self.prompt)

    def add_service_group(self, index, qam_idx, qam_sub, qam_channels, ups_idx, ups_channels):
        print("Service group is auto configured in ARRIS once mac domain is created.")

    def mirror_traffic(self, macaddr = ""):
        print("Mirror traffic feature is not supported in ARRIS unless we use lawful intercept functionality.")

    def unmirror_traffic(self):
        print("Unmirror traffic feature is not supported in ARRIS unless we use lawful intercept functionality.")

    def run_tcpdump(self, time, iface = 'any', opts = ""):
        print("TCPDUMP feature is not supported in ARRIS.")

    @ArrisCMTSDecorators.mac_to_cmts_type_mac_decorator
    def is_cm_bridged(self, mac, offset = 2):
        '''
        This function is to check if the modem is in bridge mode.
        Input : arg1 : Mac address of the modem, arg2 : offset.
        Output : Returns True if the modem is bridged else False.
        '''
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
        '''
        This function is to return the ipv4 address of erouter of modem.
        Input : arg1 : Mac address of the modem, arg2 : offset.
        Output : Returns the ipv4 address of the erouter if exists else None.
        '''
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
        '''
        This function is to return the ipv6 address of erouter of modem.
        Input : arg1 : Mac address of the modem, arg2 : offset.
        Output : Returns the ipv6 address of the erouter (not link local ip) if exists else None.
        '''
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
        '''
        This function is to return the center frequency of cmts.
        Input : arg1 : Mac Domain.
        Output : Returns center frequency in string format.
        '''
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
        '''
        This function is to set the frequency, width and power on upstream channel.
        Input : arg1 : cable mac index, arg2 : channel to be used, arg3 : frequency to set, arg4 : width to set, arg5 : power to set.
        Output : None (sets the frequency, width and power on channel as defined).
        '''
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
        """Get the bundle id from mac-domain """
        self.sendline('show running-config interface cable-mac %s | include cable-mac [0-9]+.[0-9]+' % mac_domain)
        index = self.expect(['(interface cable-mac )([0-9]+.[0-9]+)'] + self.prompt)
        if index != 0:
            assert 0, "ERROR:Failed to get the CM bundle id from CMTS"
        bundle = self.match.group(2)
        self.expect(self.prompt)
        return bundle

    def get_cmts_ip_bundle(self, cm_mac, gw_ip=None):
        '''
        get CMTS bundle IP
        to get a gw ip, use get_gateway_address from mv1.py(board.get_gateway_address())
        '''
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
        '''
        This function is to reset the cmts.
        Input : None.
        Output : None (resets the cmts).
        '''
        self.sendline('erase nvram')
        self.expect(self.prompt)
        self.sendline('reload')
        self.expect(self.prompt)

    def add_service_class(self, index, name, max_rate, max_burst, max_tr_burst = None, downstream = False):
        '''
        This function is to add service class on cmts and set it parameters.
        Input : arg1 : cable mac index (ignored in arris), arg2 : name to be used for qos, arg3 : the max_rate, arg4 : max transmission burst , arg5 : max burst to be set (used in arris), arg 6 : downstream = True if we want the service class to be used for downstream.
        Output : None (creates and sets parameters on service class).
        '''
        self.sendline('qos-sc name %s max-tr-rate %s max-tr-burst %s max-burst %s' % (name, max_rate,max_tr_burst,max_burst))
        self.expect(self.prompt)
        if downstream:
            self.sendline('qos-sc name %s dir 1' % name)
            self.expect(self.prompt)

    def add_iface_docsis_mac(self, index, ip_bundle, qam_idx, qam_ch, ups_idx, ups_ch, qam_sub = None, prov_mode = None):
        '''
        This function is to create a mac domain and set its parameters.
        Input : arg1 : cable mac index, arg2 :  ip to be assiged to cable mac in the format <ip><space><subnet>, arg 3: the slot of downstream to be used on arris, arg 4: list containing the channels to be bonded to mac domain
        arg 5: the slot of upstream to be used on arris, arg 6: list containing the channels to be bonded to mac domain
        arg 7: qam sub  (ignored in arris), arg 8 : the provision mode to be set.
        Output : None (creates and sets parameters on mac domain).
        '''
        if  "/" not in ip_bundle:
            ip_bundle  += "/24"
            ip_bundle = ipaddress.IPv4Interface(unicode(ip_bundle))
        else:
            ip_bundle = ipaddress.IPv4Interface(unicode(ip_bundle))
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
        '''
        This function is to get the chassis type on cmts.
        Input : None.
        Output : Returns the cmts chassis type.
        '''
        self.sendline('show linecard status | include chassis')
        self.expect('Chassis Type:(.*)\r\n')
        result = self.match.group(1)
        if self.match != None:
            output = result
        else:
            output = "None"
        self.expect(self.prompt)
        return output.strip().lower()
