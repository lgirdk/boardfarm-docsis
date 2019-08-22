# Copyright (c) 2018
#
# All rights reserved.
#
# This file is distributed under the Clear BSD license.
# The full text can be found in LICENSE in the root directory.
#!/usr/bin/env python

import pexpect
import sys

import re
import connection_decider
import base_cmts
from lib.regexlib import AllValidIpv6AddressesRegex, ValidIpv4AddressRegex


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
                #import pdb; pdb.set_trace()
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
        self.mac_domain = kwargs.get('mac_domain', None)

        if conn_cmd is None:
            # TODO: try to parse from ipaddr, etc
            raise Exception("No command specified to connect to Arris CMTS")

        self.connection = connection_decider.connection(connection_type, device=self, conn_cmd=conn_cmd)
        self.connection.connect()
        self.connect()
        self.logfile_read = sys.stdout

        self.name = kwargs.get('name', self.model)

    def connect(self):
        try:
            try:
                self.expect_exact("Escape character is '^]'.", timeout=5)
            except:
                pass
            self.sendline()
            if 1 != self.expect(['\r\nLogin:', pexpect.TIMEOUT], timeout=10):
                self.sendline(self.username)
                self.expect('assword:')
                self.sendline(self.password)
                self.expect(self.prompt)
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
            raise Exception("Unable to get prompt on CASA device")

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
            return re.findall('State=(.*?\s)', self.before)[0].strip()

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
        self.sendline('show cable modem %s | include impaired' % cmmac)
        self.expect('\(impaired:\s')
        match = self.match.group(1)
        self.expect(self.prompt)
        return match != None

    @ArrisCMTSDecorators.mac_to_cmts_type_mac_decorator
    def DUT_chnl_lock(self, cm_mac):
        """Check the CM channel locks with 24*8 """
        self.sendline("show cable modem | include %s" % cm_mac)
        index = self.expect(["(24x8)"], timeout=3)
        self.expect(self.prompt)
        return 0 == index

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
        return self.before.split("\n",1)[1]

    def set_or_unset_iface_ipaddr(self, iface, ipaddr='',set='',shutdown=''):
        '''
        This function is to set an ipv4 address to an interface on cmts.
        Input : arg1: interface name , arg2: ipv4 address / prefix as one string., agr3 : set or unset the ip and arg4 to shutdown the interface (yes/no)
        Output : None (sets/unsets the ipv4 address to an interface specified).
        '''
        if set.lower()!='no':
            self.sendline('interface %s' % iface)
            self.expect(self.prompt)
            self.sendline('ip address %s' % ipaddr)
            self.expect(self.prompt)
            self.sendline('no shutdown')
            self.expect(self.prompt)
            self.sendline('exit')
            self.expect(self.prompt)
        else:
            self.sendline('interface %s' % iface)
            self.expect(self.prompt)
            self.sendline('no ip address')
            self.expect(self.prompt)
            self.sendline('exit')
            self.expect(self.prompt)
        if shutdown.lower()=='yes':
            self.sendline('interface %s' % iface)
            self.expect(self.prompt)
            self.sendline('shutdown')
            self.expect(self.prompt)
            self.sendline('exit')
            self.expect(self.prompt)

    def set_or_unset_iface_ipv6addr(self, iface, ipaddr='',set='',shutdown=''):
        '''
        This function is to set an ipv6 address to an interface on cmts.
        Input : arg1: interface name , arg2: ipv6 address / prefix as one string., agr3 : set or unset the ip and arg4 to shutdown the interface (yes/no)
        Output : None (sets/unsets the ipv4 address to an interface specified).
        '''
        if set.lower()!='no':
            self.sendline('interface %s' % iface)
            self.expect(self.prompt)
            self.sendline('ipv6 address %s' % ipaddr)
            self.expect(self.prompt)
            self.sendline('no shutdown')
            self.expect(self.prompt)
            self.sendline('exit')
            self.expect(self.prompt)
        else:
            self.sendline('interface %s' % iface)
            self.expect(self.prompt)
            self.sendline('no ipv6 address')
            self.expect(self.prompt)
            self.sendline('exit')
            self.expect(self.prompt)
        if shutdown.lower()=='yes':
            self.sendline('interface %s' % iface)
            self.expect(self.prompt)
            self.sendline('shutdown')
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
        return result

    def wait_for_ready(self):
        '''
        This function is to wait until all the interface are up and available.
        Input : None.
        Output : None (wait if any interface is down until it is up for a maximum of 5 times with a wait of 1min each).
        '''
        max_iteration=5
        self.sendline('show linecard status')
        while 0 == self.expect(['Down | OOS'] + self.prompt) and max_iteration>0:
            max_iteration-=1
            self.expect(self.prompt)
            self.expect(pexpect.TIMEOUT, timeout=5)
            self.sendline('show linecard status')

    def modify_docsis_mac_ip_provisioning_mode(self, index, ip_pvmode='dual-stack'):
        '''
        This function is to set the ip provisioning mode.
        Input : arg1 : index of the interface, arg2 : ip provisioning mode to be set on the interface (default is dual-stack).
        Output : None (wait if any interface is down until it is up).
        '''
        if (ip_pvmode=='dual-stack'):
            self.sendline('show linecard status | include chassis')
            self.expect(self.prompt)
            if ('Chassis Type: C4' in self.before):
                print 'dual-stack ip provisioning modem is not supported on Chassis Type : C4 please choose apm'
                return

        self.sendline('interface cable-mac %s' % index)
        self.expect(self.prompt)
        self.sendline('cable cm-ip-prov-mode %s' % ip_pvmode)
        self.expect(self.prompt)
        self.sendline('exit')
        self.expect(self.prompt)

    def add_route(self, net, mask, gw):
        '''
        This function is to add route.
        Input : arg1 : network ip, arg2 : subnet ip, arg3 : gateway ip.
        Output : None (adds the route to the specified parameters).
        '''
        self.sendline('ip route %s %s %s' % (net, mask, gw))
        self.expect(self.prompt)

    def add_route6(self, net, gw):
        '''
        This function is to add ipv6 route.
        Input : arg1 : network ip/subnet, arg3 : gateway ip.
        Output : None (adds the route to the specified parameters).
        '''
        self.sendline('ipv6 route %s %s' % (net, gw))
        self.expect(self.prompt)

    def del_route(self, net, mask, gw):
        '''
        This function is to delete route.
        Input : arg1 : network ip, arg2 : subnet ip, arg3 : gateway ip.
        Output : None (deletes the route to the specified parameters).
        '''
        self.sendline('no ip route %s %s %s' % (net, mask, gw))
        self.expect(self.prompt)

    def del_route6(self, net, gw):
        '''
        This function is to delete ipv6 route.
        Input : arg1 : network ip, arg2 : subnet ip, arg3 : gateway ip.
        Output : None (deletes the route to the specified parameters).
        '''
        self.sendline('no ipv6 route %s %s' % (net, gw))
        self.expect(self.prompt)

    def add_ip_bundle(self, index, helper_ip, ip, secondary_ips=[]):
        '''
        This function is to add ip bundle to a cable mac.
        Input : arg1 : cable mac index, arg2 : helper ip to be used, arg3 : actual ip to be assiged to cable mac in the format <ip><space><subnet>, arg4 : list of seconday ips  in the format <ip><space><subnet>.
        Output : None (sets the ip bundle to a cable mac).
        '''
        self.sendline('interface cable-mac %s' % index)
        self.expect(self.prompt)
        self.sendline('ip address %s' % ip)
        self.expect(self.prompt)
        for ip2 in secondary_ips:
            self.sendline('ip address %s secondary' % ip2)
            self.expect(self.prompt)
        self.sendline('cable helper-address %s cable-modem' % helper_ip)
        self.expect(self.prompt)
        self.sendline('cable helper-address %s mta' % helper_ip)
        self.expect(self.prompt)
        self.sendline('cable helper-address %s host' % helper_ip)
        self.expect(self.prompt)
        self.sendline('exit')
        self.expect(self.prompt)

    def add_ipv6_bundle_addrs(self, index, helper_ip, ip, secondary_ips=[]):
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
        max_iteration=5
        self.sendline('show linecard status')
        while 0 == self.expect(['Down | OOS'] + self.prompt) and max_iteration>0:
            max_iteration-=1
            self.expect(self.prompt)
            self.expect(pexpect.TIMEOUT, timeout=5)
            self.sendline('show linecard status')

    def modify_docsis_mac_ip_provisioning_mode(self, index, ip_pvmode='dual-stack'):
        '''
        This function is to set the ip provisioning mode.
        Input : arg1 : index of the interface, arg2 : ip provisioning mode to be set on the interface (default is dual-stack).
        Output : None (wait if any interface is down until it is up).
        '''
        if (ip_pvmode=='dual-stack'):
            self.sendline('show linecard status | include chassis')
            self.expect(self.prompt)
            if ('Chassis Type: C4' in self.before):
                print 'dual-stack ip provisioning modem is not supported on Chassis Type : C4 please choose apm'
                return

        self.sendline('interface cable-mac %s' % index)
        self.expect(self.prompt)
        self.sendline('cable cm-ip-prov-mode %s' % ip_pvmode)

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

    def is_cm_bridged(self, mac,offset=2):
        '''
        This function is to check if the modem is in bridge mode.
        Input : arg1 : Mac address of the modem, arg2 : offset.
        Output : Returns True if the modem is bridged else False.
        '''
        self.sendline("show cable modem %s detail" % mac)
        self.expect(self.prompt)
        from netaddr import EUI
        import netaddr
        mac = EUI(mac)
        ertr_mac = EUI(int(mac) + offset)
        ertr_mac.dialect = netaddr.mac_cisco
        if str(ertr_mac) in self.before:
            return False
        else:
            return True

    def get_ertr_ipv4(self, mac,offset=2):
       '''
       This function is to return the ipv4 address of erouter of modem.
       Input : arg1 : Mac address of the modem, arg2 : offset.
       Output : Returns the ipv4 address of the erouter if exists else None.
       '''
       self.sendline("show cable modem %s detail" % mac)
       self.expect(self.prompt)
       from netaddr import EUI
       import netaddr
       mac = EUI(mac)
       ertr_mac = EUI(int(mac) + offset)
       ertr_mac.dialect = netaddr.mac_cisco
       ertr_ipv4 = re.search('(%s) .*=(%s)' % (ertr_mac,ValidIpv4AddressRegex), self.before)
       if ertr_ipv4:
           ipv4 = ertr_ipv4.group(2)
           return ipv4
       else:
           return None

    def get_ertr_ipv6(self, mac,offset=2):
       '''
       This function is to return the ipv6 address of erouter of modem.
       Input : arg1 : Mac address of the modem, arg2 : offset.
       Output : Returns the ipv6 address of the erouter (not link local ip) if exists else None.
       '''
       self.sendline("show cable modem %s detail" % mac)
       self.expect(self.prompt)
       from netaddr import EUI
       import netaddr
       mac = EUI(mac)
       ertr_mac = EUI(int(mac) + offset)
       ertr_mac.dialect = netaddr.mac_cisco
       ertr_ipv6 = re.search('(%s) IPv6=(%s)' % (ertr_mac,AllValidIpv6AddressesRegex), self.before)
       if ertr_ipv6:
           ipv6 = ertr_ipv6.group(2)
           return ipv6
       else:
           return None

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
