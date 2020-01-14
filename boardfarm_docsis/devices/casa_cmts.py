# Copyright (c) 2018
#
# All rights reserved.
#
# This file is distributed under the Clear BSD license.
# The full text can be found in LICENSE in the root directory.
#!/usr/bin/env python

import netaddr
import pexpect
import six
import sys
import re
import collections

from boardfarm.devices import connection_decider
from boardfarm.lib.regexlib import ValidIpv4AddressRegex, AllValidIpv6AddressesRegex
from . import base_cmts
import ipaddress


class CasaCMTS(base_cmts.BaseCmts):
    """Connects to and configures a CASA CMTS
    """

    prompt = ['CASA-C3200>', 'CASA-C3200#', r'CASA-C3200\(.*\)#', 'CASA-C10G>', 'CASA-C10G#', r'CASA-C10G\(.*\)#']
    model = "casa_cmts"

    def __init__(self,
                 *args,
                 **kwargs):
        """Constructor method
        """
        conn_cmd = kwargs.get('conn_cmd', None)
        connection_type = kwargs.get('connection_type', 'local_serial')
        self.username = kwargs.get('username', 'root')
        self.password = kwargs.get('password', 'casa')
        self.password_admin = kwargs.get('password_admin', 'casa')
        self.mac_domain = kwargs.get('mac_domain', None)
        self.channel_bonding = kwargs.get('channel_bonding', 24) # 16x8 : total 24

        if conn_cmd is None:
            # TODO: try to parse from ipaddr, etc
            raise Exception("No command specified to connect to Casa CMTS")

        self.connection = connection_decider.connection(connection_type, device=self, conn_cmd=conn_cmd)
        if kwargs.get('debug', False):
            self.logfile_read = sys.stdout
        self.connection.connect()
        self.connect()
        self.logfile_read = sys.stdout

        self.name = kwargs.get('name', 'casa_cmts')

    def connect(self):
        """This method is used to connect cmts.
        Login to the cmts based on the connection type available

        :raises Exception: Unable to get prompt on CASA device
        """
        try:
            if 2 != self.expect(['\r\n(.*) login:', '(.*) login:', pexpect.TIMEOUT]):
                hostname = self.match.group(1).replace('\n', '').replace('\r', '').strip()
                self.prompt.append(hostname + '>')
                self.prompt.append(hostname + '#')
                self.prompt.append(hostname + r'\(.*\)#')
                self.sendline(self.username)
                self.expect('assword:')
                self.sendline(self.password)
                self.expect(self.prompt)
            else:
                # Over telnet we come in at the right prompt
                # over serial it could be stale so we try to recover
                self.sendline('q')
                self.sendline('exit')
                self.expect([pexpect.TIMEOUT] + self.prompt, timeout = 20)
            self.sendline('enable')
            if 0 == self.expect(['Password:'] + self.prompt):
                self.sendline(self.password_admin)
                self.expect(self.prompt)
            self.sendline('config')
            self.expect(self.prompt)
            self.sendline('page-off')
            self.expect(self.prompt)
            return
        except:
            raise Exception("Unable to get prompt on CASA device")

    def logout(self):
        """Logout of the CMTS device
        """
        self.sendline('exit')
        self.sendline('exit')

    def check_online(self, cmmac):
        """Check the CM status from CMTS
        Function checks the encryption mode and returns True if online

        :param cmmac: mac address of the CM
        :type cmmac: string
        :raises assert:  incorrect cmstatus in cmts
        :return: True if the CM is operational else actual status on cmts
        :rtype: boolean or string
        """
        self.sendline('show cable modem %s' % cmmac)
        self.expect(r'.+ranging cm \d+')
        result = self.match.group()
        match = re.search(r'\d+/\d+/\d+\**\s+([^\s]+)\s+\d+\s+.+\d+\s+(\w+)\r\n', result)
        if match:
            status = match.group(1)
            encrytion = match.group(2)
            if status == "online(pt)" and encrytion == "yes":
                output = True
            elif status == "online" and encrytion == "no":
                output = True
            elif "online" not in status and status != None:
                output = status
            else:
                assert 0, "ERROR: incorrect cmstatus \""+status+"\" in cmts for bpi encrytion \""+encrytion+"\""
        else:
            assert 0, "ERROR: Couldn't fetch CM status from cmts"
        self.expect(self.prompt)
        return output

    def clear_offline(self, cmmac):
        """Clear the CM entry from cmts which is offline -clear cable modem <mac> offline

        :param cmmac: mac address of the CM
        :type cmmac: string
        """
        if ('c3000' in self.get_cmts_type()):
            print('clear offline feature is not supported on casa product name c3000')
            return
        self.sendline('clear cable modem %s offline' % cmmac)
        self.expect(self.prompt)

    def clear_cm_reset(self, cmmac):
        """Reset the CM from cmts using cli -clear cable modem <mac> reset

        :param cmmac: mac address of the CM
        :type cmmac: string
        """
        self.sendline("clear cable modem %s reset" % cmmac)
        self.expect(self.prompt)
        online_state=self.check_online(cmmac)
        self.expect(pexpect.TIMEOUT, timeout = 5)
        if(online_state==True):
            print("CM is still online after 5 seconds.")
        else:
            print("CM reset is initiated.")

    def check_PartialService(self, cmmac):
        """Check the cable modem is in partial service

        :param cmmac: mac address of the CM
        :type cmmac: string
        :return: 1 if is true else return the value as 0
        :rtype: integer
        """
        self.sendline('show cable modem %s' % cmmac)
        self.expect(r'(\d+/\d+\.\d+/\d+(\*|\#)\s+\d+/\d+/\d+(\*|\#))\s+online')
        result = self.match.group(1)
        match = re.search(r'\#', result)
        if match != None:
            output = 1
        else:
            output = 0
        self.expect(self.prompt)
        return output

    def get_cmip(self, cmmac):
        """Get the IP of the Cable modem from CMTS

        :param cmmac: mac address of the CM
        :type cmmac: string
        :return: ip address of cable modem or "None"
        :rtype: string
        """
        cmmac=self.get_cm_mac_cmts_format(cmmac)
        self.sendline('show cable modem %s' % cmmac)
        self.expect(cmmac + r'\s+([\d\.]+)')
        result = self.match.group(1)
        if self.match != None:
            output = result
        else:
            output = "None"
        self.expect(self.prompt)
        return output

    def get_cmipv6(self, cmmac):
        """Get IPv6 address of the Cable modem from CMTS

        :param cmmac: mac address of the CM
        :type cmmac: string
        :return: ipv6 address(str) of cable modem or "None"
        :rtype: string
        """
        self.sendline('show cable modem %s' % cmmac)
        self.expect(self.prompt)
        match = re.search(AllValidIpv6AddressesRegex, self.before)
        if match:
            output = match.group(0)
        else:
            output = "None"
        return output

    def get_mtaip(self, cmmac, mtamac):
        """Get the MTA IP from CMTS

        :param cmmac: mac address of the CM
        :type cmmac: string
        :param mtamac: mta mac address
        :type mtamac: string
        :return: MTA ip address or "None" if ip not found
        :rtype: string
        """
        if ':' in mtamac:
            mtamac = self.get_cm_mac_cmts_format(mtamac)
        self.sendline('show cable modem %s cpe' % cmmac)
        self.expect(r'([\d\.]+)\s+dhcp\s+' + mtamac)
        result = self.match.group(1)
        if self.match != None:
            output = result
        else:
            output = "None"
        self.expect(self.prompt)
        return output

    def DUT_chnl_lock(self, cm_mac):
        """Check the CM channel locks based on cmts type

        :param cm_mac: mac address of the CM
        :type cm_mac: string
        :returns: Locked channels of downstream and upstream
        :rtype: list
        """
        streams = ['Upstream', 'Downstream']
        channel_list = []
        for stream in streams:
            self.sendline("show cable modem %s verbose | inc \"%s Channel Set\"" % (cm_mac, stream))
            self.expect(self.prompt)
            if stream == 'Upstream':
                match = re.search(r'(\d+/\d+.\d+/\d+).+', self.before)
            elif stream == 'Downstream':
                match = re.search(r'(\d+/\d+/\d+).+', self.before)
            channel = len(match.group().split(","))
            channel_list.append(channel)
        return channel_list

    def get_cm_bundle(self, mac_domain):
        """Get the bundle id from cable modem

        :param mac_domain: Mac_domain of the cable modem
        :type mac_domain: string
        :raises assert: Failed to get the CM bundle id from CMTS
        :return: bundle id
        :rtype: string
        """
        self.sendline('show interface docsis-mac '+mac_domain+' | i "ip bundle"')
        index = self.expect(['(ip bundle)[ ]{1,}([0-9]|[0-9][0-9])'] + self.prompt)
        if index != 0:
            assert 0, "ERROR:Failed to get the CM bundle id from CMTS"
        bundle = self.match.group(2)
        self.expect(self.prompt)
        return bundle

    def get_cm_mac_domain(self, cm_mac):
        """Get the Mac-domain of Cable modem

        :param cm_mac: mac address of the CM
        :type cm_mac: string
        :raises assert: Failed to get the CM mac domain from CMTS
        :return: mac_domain of the particular cable modem
        :rtype: string
        """
        self.sendline('show cable modem '+cm_mac+' verbose | i "MAC Domain"')
        idx = self.expect([r'(MAC Domain)[ ]{2,}\:([0-9]|[0-9][0-9])'] + self.prompt)
        if idx != 0:
            assert 0, "ERROR: Failed to get the CM Mac Domain from the CMTS"
        mac_domain = self.match.group(2)
        self.expect(self.prompt)
        return mac_domain

    def get_cmts_ip_bundle(self, cm_mac, gw_ip=None):
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
        self.sendline('show interface ip-bundle %s | i secondary' % bundle_id)
        self.expect(self.prompt)

        if gw_ip is None:
            return self.before

        cmts_ip = re.search('ip address (%s) .* secondary' % gw_ip, self.before)
        if cmts_ip:
            cmts_ip = cmts_ip.group(1)
        else:
            assert 0, "ERROR: Failed to get the CMTS bundle IP"
        return cmts_ip

    def reset(self):
        """Delete the startup config and Reboot the CMTS
        """
        self.sendline('exit')
        self.expect(self.prompt)
        self.sendline('del startup-config')
        self.expect('Please type YES to confirm deleting startup-config:')
        self.sendline('YES')
        self.expect(self.prompt)
        self.sendline('system reboot')
        if 0 == self.expect([r'Proceed with reload\? please type YES to confirm :', 'starting up console shell ...'], timeout = 180):
            self.sendline('YES')
            self.expect('starting up console shell ...', timeout = 150)
        self.sendline()
        self.expect(self.prompt)
        self.sendline('page-off')
        self.expect(self.prompt)
        self.sendline('enable')
        self.expect('Password:')
        self.sendline(self.password)
        self.expect(self.prompt)
        self.sendline('config')
        self.expect(self.prompt)

    def wait_for_ready(self):
        """Check the cmts status
        """
        self.sendline('show system')
        while 0 == self.expect(['NotReady'] + self.prompt):
            self.expect(self.prompt)
            self.expect(pexpect.TIMEOUT, timeout = 5)
            self.sendline('show system')

    def save_running_to_startup_config(self):
        """save the running config to startup
        """
        self.sendline('exit')
        self.expect(self.prompt)
        self.sendline('copy running-config startup-config')
        self.expect(self.prompt)
        self.sendline('config')
        self.expect(self.prompt)

    def save_running_config_to_local(self, filename):
        """Saves the running config to a file on the local machine
        """
        self.sendline('show running-config')
        self.expect('show running-config')
        self.expect(self.prompt)

        f = open(filename, "w")
        f.write(self.before)
        f.close()

    def set_iface_ipaddr(self, iface, ipaddr):
        """This function sets the ipv4 address of an interface on the cmts

        :param iface: interface name
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
        """This function sets the ipv6 address of an interface on the cmts

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
        """This function is to unset an ipv4 address of an interface on cmts.

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
        """This function is to unset an ipv6 address of an interface on cmts.

        :param iface: interface name.
        :type iface: string
        """
        self.sendline('interface %s' % iface)
        self.expect(self.prompt)
        self.sendline('no ipv6 address')
        self.expect(self.prompt)
        self.sendline('exit')
        self.expect(self.prompt)

    def add_ip_bundle(self, index, helper_ip, ipaddr, secondary_ips = []):
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
        if  "/" not in ipaddr:
            ipaddr  += "/24"
            ipaddr = ipaddress.IPv4Interface(six.text_type(ipaddr))
        else:
            ipaddr = ipaddress.IPv4Interface(six.text_type(ipaddr))
        self.sendline('interface ip-bundle %s' % index)
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
        self.sendline('show interface ip-bundle %s | include \"ip address\"' % index)
        self.expect(self.prompt)
        if str(ipaddr.ip) in self.before:
            print("The ip bundle is successfully set.")
        else:
            print("An error occured while setting the ip bundle.")

    def add_ipv6_bundle_addrs(self, index, helper_ip, ip, secondary_ips = []):
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
        self.sendline('interface ip-bundle %s' % index)
        self.expect(self.prompt)
        self.sendline('ipv6 address %s' % ip)
        self.expect(self.prompt)
        for ip2 in secondary_ips:
            self.sendline('ipv6 address %s secondary' % ip2)
            self.expect(self.prompt)
        self.sendline('cable helper-ipv6-address %s' % helper_ip)
        self.expect(self.prompt)
        self.sendline('exit')
        self.expect(self.prompt)
        self.sendline('show interface ip-bundle %s | include \"ipv6 address\"' % index)
        self.expect(self.prompt)
        if str(ipaddress.ip_address(six.text_type(ip[:-3])).compressed) in self.before:
            print("The ipv6 bundle is successfully set.")
        else:
            print("An error occured while setting the ipv6 bundle.")

    def add_route(self, ipaddr, gw):
        """This function adds an ipv4 network route entry.

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
        self.sendline('route net %s %s gw %s' % (ipaddr.ip, ipaddr.network.prefixlen, gw))
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
        """This function adds an ipv6 network route entry.

        :param net: <network ip></><subnet ip> take subnet 24 if not provided,
        :param net: string
        :param gw: gateway ip.
        :type gw: string
        """
        self.sendline('route6 net %s gw %s' % (net, gw))
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
        """This function removes an ipv4 network route entry.

        :param ipaddr: <network ip></><subnet ip> take subnet 24 if not provided, 
        :type ipaddr: string
        :param gw: gateway ip
        :type gw: string
        """
        if  "/" not in ipaddr:
            ipaddr  += "/24"
            ipaddr = ipaddress.IPv4Interface(six.text_type(ipaddr))
        else:
            ipaddr = ipaddress.IPv4Interface(six.text_type(ipaddr))
        self.sendline('no route net %s %s gw %s' % (ipaddr.ip, ipaddr.network.prefixlen, gw))
        self.expect(self.prompt)
        if 'error' in self.before.lower():
            print("An error occured while deleting the route.")
        self.expect(pexpect.TIMEOUT, timeout = 10)
        self.sendline('show ip route')
        self.expect(self.prompt)
        if gw in self.before:
            print("The route is still available on cmts might be delayed to reflect on cmts.")
        else:
            print("The route is not available on cmts.")

    def del_route6(self, net, gw):
        """This function removes an ipv6 network route entry.

        :param net: <network ip></><subnet ip> take subnet 24 if not provided,
        :type net: string
        :param gw: gateway ip
        :type gw: string
        """
        self.sendline('no route6 net %s gw %s' % (net, gw))
        self.expect(self.prompt)
        if 'error' in self.before.lower():
            print("An error occured while deleting the route.")
        self.sendline('show ipv6 route')
        self.expect(self.prompt)
        if str(ipaddress.ip_address(six.text_type(gw)).compressed).lower() in self.before.lower() or gw.lower() in self.before.lower():
            print("The route is still available on cmts.")
        else:
            print("The route is not available on cmts.")
    def get_qam_module(self):
        """Get the module of the qam

        :return: Module of the qam
        :rtype: string
        """
        self.sendline('show system')
        self.expect(self.prompt)
        return re.findall(r'Module (\d+) QAM', self.before)[0]

    def get_ups_module(self):
        """Get the upstream module of the qam

        :return: list of module number of the qam
        :rtype: list
        """
        self.sendline('show system')
        self.expect(self.prompt)
        results = list(map(int, re.findall(r'Module (\d+) UPS', self.before)))
        return results

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
        self.sendline('interface qam %s/%s' % (index, sub))
        self.expect(self.prompt)
        self.sendline('annex %s' % annex)
        self.expect(self.prompt)
        self.sendline('interleave %s' % interleave)
        self.expect(self.prompt)
        self.sendline('power %s' % power)
        self.expect(self.prompt)
        self.sendline('no shutdown')
        self.expect(self.prompt)
        self.sendline('exit')
        self.expect(self.prompt)

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
        self.sendline('interface qam %s/%s' % (index, sub))
        self.expect(self.prompt)
        self.sendline('channel %s freq %s' % (channel, freq))
        self.expect(self.prompt)
        self.sendline('no channel %s shutdown' % channel)
        self.expect(self.prompt)
        self.sendline('exit')
        self.expect(self.prompt)

    def get_iface_qam_freq(self, cm_mac):
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
        self.sendline('show interface docsis-mac %s | inc downstream' % mac_domain)
        self.expect(self.prompt)
        tmp = re.findall(r'downstream\s\d+\sinterface\sqam\s(.*)/\d+', self.before)
        downs = set([x for x in tmp if tmp.count(x) > 1])
        get_iface_qam_freq = collections.OrderedDict()
        for index_sub in sorted(downs):
            self.sendline('show interface qam %s | inc "channel"' % index_sub)
            self.expect(self.prompt)
            tmp = re.findall(r'channel\s(\d+)\sfrequency\s(\d+)', self.before)
            for channel,freq in tmp:
                get_iface_qam_freq[index_sub+'/'+channel] = freq

        return get_iface_qam_freq

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
        self.sendline('interface upstream %s/%s' % (ups_idx, ups_ch))
        self.expect(self.prompt)
        self.sendline('frequency %s' % freq)
        self.expect(self.prompt)
        self.sendline('channel-width %s' % width)
        self.expect(self.prompt)
        self.sendline('power-level %s' % power)
        self.expect(self.prompt)
        self.sendline('ingress-cancellation')
        self.expect(self.prompt)
        self.sendline('logical-channel 0 profile 3')
        self.expect(self.prompt)
        self.sendline('logical-channel 0 minislot 1')
        self.expect(self.prompt)
        self.sendline('no logical-channel 0 shutdown')
        self.expect(self.prompt)
        self.sendline('logical-channel 1 shutdown')
        self.expect(self.prompt)
        self.sendline('no shutdown')
        self.expect(self.prompt)
        self.sendline('exit')
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
        self.sendline('interface docsis-mac %s' % index)
        self.expect(self.prompt)
        self.sendline('no shutdown')
        self.expect(self.prompt)
        self.sendline('early-authentication-encryption ranging')
        self.expect(self.prompt)
        self.sendline('no dhcp-authorization')
        self.expect(self.prompt)
        self.sendline('no multicast-dsid-forward')
        self.expect(self.prompt)
        self.sendline('no tftp-enforce')
        self.expect(self.prompt)
        self.sendline('tftp-proxy')
        self.expect(self.prompt)
        self.sendline('ip bundle %s' % ip_bundle)
        self.expect(self.prompt)
        self.sendline('ip-provisioning-mode dual-stack')
        self.expect(self.prompt)
        count = 1
        for ch in qam_ch:
            self.sendline('downstream %s interface qam %s/%s/%s' % (count, qam_idx, qam_sub, ch))
            self.expect(self.prompt)
            count += 1
        count = 1
        for ch in ups_ch:
            self.sendline('upstream %s interface upstream %s/%s/0' % (count, ups_idx, ch))
            self.expect(self.prompt)
            count += 1
        self.sendline('exit')
        self.expect(self.prompt)

    def modify_docsis_mac_ip_provisioning_mode(self, index, ip_pvmode = 'dual-stack'):
        """Change the mac-domain ip provisioning mode.

        :param index: mac domain of the cable modem configured
        :type index: string
        :param ip_pvmode: provisioning mode can ipv4, ipv6 or 'dual-stack', defaults to 'dual-stack'
        :type ip_pvmode: string, optional
        """
        self.sendline('interface docsis-mac %s' % index)
        self.expect(self.prompt)
        self.sendline('ip-provisioning-mode %s' % ip_pvmode)
        self.expect(self.prompt)
        self.sendline('exit')
        self.expect(self.prompt)
        check_docsis_mac_ip_provisioning_mode = self.check_docsis_mac_ip_provisioning_mode(index)
        if check_docsis_mac_ip_provisioning_mode in ip_pvmode:
            print("The ip provision mode is successfully set.")
        else:
            print("An error occured while setting the ip provision mode.")

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
        :param downstream: True or False, defaults to False
        """
        self.sendline('cable service-class %s' % index)
        self.expect(self.prompt)
        self.sendline('name %s' % name)
        self.expect(self.prompt)
        self.sendline('max-traffic-rate %s' % max_rate)
        self.expect(self.prompt)
        self.sendline('max-traffic-burst %s' % max_burst)
        self.expect(self.prompt)
        self.sendline('max-concat-burst 0')
        self.expect(self.prompt)
        if downstream:
            self.sendline('downstream')
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
        self.sendline('service group %s' % index)
        self.expect(self.prompt)
        for ch in qam_channels:
            self.sendline('qam %s/%s/%s' % (qam_idx, qam_sub, ch))
            self.expect(self.prompt)
        for ch in ups_channels:
            self.sendline('upstream %s/%s' % (ups_idx, ch))
            self.expect(self.prompt)
        self.sendline('exit')
        self.expect(self.prompt)

    def mirror_traffic(self, macaddr = ""):
        """Send the mirror traffic

        :param macaddr: mac address of the device if avaliable, defaults to ""
        :type macaddr: string
        """
        self.sendline('diag')
        self.expect('Password:')
        self.sendline('casadiag')
        self.expect(self.prompt)
        self.sendline('mirror cm traffic 127.1.0.7 %s' % macaddr)
        if 0 == self.expect(['Please type YES to confirm you want to mirror all CM traffic:'] + self.prompt):
            self.sendline("YES")
            self.expect(self.prompt)
        self.sendline('exit')
        self.expect(self.prompt)

    def unmirror_traffic(self):
        """stop mirroring the traffic
        """
        self.sendline('diag')
        self.expect('Password:')
        self.sendline('casadiag')
        self.expect(self.prompt)
        self.sendline('mirror cm traffic 0')
        self.expect(self.prompt)
        self.sendline('exit')
        self.expect(self.prompt)

    def run_tcpdump(self, time, iface = 'any', opts = ""):
        """tcpdump capture on the cmts interface

        :param time: timeout to wait till gets prompt
        :type time: integer
        :param iface: any specific interface, defaults to 'any'
        :type iface: string, optional
        :param opts: any other options to filter, defaults to ""
        """
        self.sendline('diag')
        self.expect('Password:')
        self.sendline('casadiag')
        self.expect(self.prompt)
        self.sendline('tcpdump "-i%s %s"' % (iface, opts))
        self.expect(self.prompt + [pexpect.TIMEOUT], timeout = time)
        self.sendcontrol('c')
        self.expect(self.prompt)
        self.sendline('exit')
        self.expect(self.prompt)

    def del_file(self, f):
        """delete the file

        :param f: filename to delete from cmts
        :type f: string
        """
        self.sendline('del %s' % f)
        self.expect(self.prompt)

    def is_cm_bridged(self, mac, offset = 2):
        """This function is to check if the modem is in bridge mode.

        :param mac: Mac address of the modem,
        :param offset: ignored in casa specific to arris, defaults to 2
        :return: Returns True if the modem is bridged else False.
        :rtype: boolean
        """
        self.sendline("show cable modem "+mac+" cpe")
        if 0 == self.expect(['eRouter']+self.prompt):
            self.expect(self.prompt)
            return False
        else:
            return True

    def check_docsis_mac_ip_provisioning_mode(self, index):
        """
        Get the provisioning mode of the cable modem from CMTS

        :param index: mac domain of the cable modem
        :type index: string
        :return: mode of the provisioning(ipv4, ipv6, dual-stack, bridge)
        :rtype: string
        """
        self.sendline('show interface docsis-mac %s' % index)
        self.expect(r'ip-provisioning-mode (\w+\-\w+)')
        result = self.match.group(1)
        self.expect(self.prompt)
        if self.match != None:
            if "ipv4" in result.lower():
                result ="ipv4"
            elif "dual" in result.lower():
                result ="dual-stack"
            elif "ipv6" in result.lower():
                result ="ipv6"
            elif "bridge" in result.lower():
                result ="bridge"
            return result
        else:
            return "Not able to fetch ip provisioning mode on CMTS"

    def get_ertr_ipv4(self, mac, offset = 2):
        """Getting erouter ipv4 from CMTS

        :param mac: mac address of the cable modem
        :type mac: string
        :param offset: ignored in casa specific to arris, defaults to 2
        :return: returns ipv4 address of erouter else None
        :rtype: string
        """
        self.sendline("show cable modem %s cpe" % mac)
        self.expect(self.prompt)
        mac = netaddr.EUI(mac)
        ertr_mac = netaddr.EUI(int(mac) + offset)
        ertr_mac.dialect = netaddr.mac_cisco
        ertr_ipv4 = re.search('(%s) .* (%s)' % (ValidIpv4AddressRegex, ertr_mac), self.before)
        if ertr_ipv4:
            ipv4 = ertr_ipv4.group(1)
            return ipv4
        else:
            return None

    def get_ertr_ipv6(self, mac, offset = 2):
        """Getting erouter ipv6 from CMTS

        :param mac: mac address of the cable modem
        :type mac: string
        :param offset: ignored in casa specific to arris, defaults to 2
        :return: returns ipv6 address of erouter else None
        :rtype: string
        """
        self.sendline("show cable modem %s cpe" % mac)
        self.expect(self.prompt)
        ertr_ipv6 = re.search(AllValidIpv6AddressesRegex, self.before)
        if ertr_ipv6:
            ipv6 = ertr_ipv6.group()
            return ipv6
        else:
            return None

    def get_center_freq(self, mac_domain = None):
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
        self.sendline(r'show interface docsis-mac %s | inc downstream\s1\s' % mac_domain)
        self.expect_exact(r'show interface docsis-mac %s | inc downstream\s1\s' % mac_domain)
        self.expect(self.prompt)
        assert 'downstream 1 interface qam' in self.before
        major, minor, sub = self.before.strip().split(' ')[-1].split('/')
        self.sendline(r'show interface qam %s/%s | inc channel\s%s\sfreq' % (major, minor, sub))
        self.expect_exact(r'show interface qam %s/%s | inc channel\s%s\sfreq' % (major, minor, sub))
        self.expect(self.prompt)
        assert 'channel %s frequency' % sub in self.before
        return str(int(self.before.split(' ')[-1]))

    def get_ip_from_regexp(self, cmmac, ip_regexpr):
        """Gets an ip address according to a regexpr (helper function)

        :param cmmac: cable modem mac address
        :param ip_regexpr: regular expression for ip
        :return: ip addr (ipv4/6 according to regexpr) or None if not found
        :rtype: string
        """
        cmmac=self.get_cm_mac_cmts_format(cmmac)
        self.sendline('show cable modem | include %s' % cmmac)
        if 1 == self.expect([cmmac + r'\s+(' + ip_regexpr + ')', pexpect.TIMEOUT], timeout=2):
            output = "None"
        else:
            result = self.match.group(1)
            if self.match != None:
                output = result
            else:
                output = "None"
        self.expect(self.prompt)
        return output

    def get_cmts_type(self):
        """This function is to get the product type on cmts.

        :return: Returns the cmts module type.
        :rtype: string
        """
        self.sendline('show system | include Product')
        self.expect(self.prompt)
        return self.before.split(",")[0].split(":")[1].strip().lower()

    def get_qos_parameter(self, cm_mac, traffic_priority = 1):
        """To get the qos related parameters of CM
        Example output format : {'DS': {'Maximum Sustained rate': '0', 'Maximum Burst': '128000',  ....},
                                 'US': {'Maximum Sustained rate': '0', 'Maximum Burst': '128000', 'IP ToS Overwrite [AND-msk, OR-mask]': ['0x00', '0x00'], ...}}

        :param cm_mac: mac address of the cable modem
        :type cm_mac: string
        :param traffic_priority: the traffic priority of service flow to be used to filter, defaults to 1.
        :type traffic_priority: int
        :return: containing the qos related parameters.
        :rtype: dictionary
        """
        qos_dict = {}
        service_flow_direction = ["US" , "DS"]
        for value in service_flow_direction:
            self.sendline("show cable modem %s qos | include %s" % (cm_mac, value))
            self.expect(self.prompt)
            qos_dict[value] = {"sfid" : self.before.split("\n")[-2].split(" ")[0].strip()}

        #mapping of the ouput stream to the US/DS and using the index.
        self.sendline("show cable modem %s qos verbose" % (cm_mac))
        self.expect(self.prompt)
        service_flows = re.split(r"\n\s*\n", self.before)[1:-1]
        for service_flow in service_flows:
            service_flow_list = [i for i in service_flow.split("\n") if i]
            matching = [s for s in service_flow_list if "Traffic Priority" in s]
            qos_dict_flow = {}
            if(traffic_priority == int(matching[0].split(":")[1].strip())):
                for service in service_flow_list:
                    service = re.sub(' +', ' ', service)
                    if "scheduling type" in service.lower():
                        qos_dict_flow[service.split(":")[0].strip()] = service.split(":")[1].strip()
                    elif not ("ip tos" or "current throughput") in service.lower():
                        qos_dict_flow[service.split(":")[0].strip()] = service.split(":")[1].strip().split(" ")[0]
                    else:
                        qos_dict_flow[service.split(":")[0].strip()] = [service.split(":")[1].strip().split(" ")[0][:-1], service.split(":")[1].strip().split(" ")[1]]
            if qos_dict["US"].get("sfid") == qos_dict_flow.get('Sfid'):
                qos_dict["US"] = qos_dict_flow
            else:
                qos_dict["DS"] = qos_dict_flow
        #this is to replace Mimimum with Minimum typo on casa cmts and convert to unit of measure like kbpc to bitespersecond.
        for value in service_flow_direction:
            if "Mimimum Reserved rate" in qos_dict[value] :
                qos_dict[value].update({"Minimum Reserved rate" : int(qos_dict[value]["Mimimum Reserved rate"]) * 1000})
                del qos_dict[value]["Mimimum Reserved rate"]
            for val in ["Minimum Reserved rate", "Maximum Sustained rate"]:
                if val in qos_dict[value]:
                    qos_dict[value].update({val : int(qos_dict[value][val]) * 1000})
        return qos_dict

    def get_upstream(self, cm_mac):
        """This function is to get the upstream channel type on cmts.

        :param cm_mac: mac address of the CM
        :type cm_mac: string
        :return: Upstream channel type 1.0 -> tdma[1], 2.0 -> atdma[2], 3.0 -> scdma[3]
        :rtype: string
        """
        from collections import defaultdict
        mac_domain = self.get_cm_mac_domain(cm_mac)
        self.sendline('show interface docsis-mac %s | inc upstream' % mac_domain)
        self.expect(self.prompt)
        tmp = re.findall(r"upstream\s\d\sinterface\supstream\s(.*)/(.*)/0", self.before)
        get_upstream = defaultdict(list)
        for ups_idx, ups_ch in tmp:
            self.sendline('show interface upstream %s/%s | inc "frequency"' % (ups_idx, ups_ch))
            self.expect(r'frequency\s(.*)')
            get_upstream['frequency'].append(self.match.group(1).strip())
            self.expect(self.prompt)
            self.expect(pexpect.TIMEOUT, timeout=1)
            self.sendline('show interface upstream %s/%s | inc "logical-channel 0 profile"' % (ups_idx, ups_ch))
            self.expect(r'logical-channel 0 profile\s(.*)')
            get_upstream['channel_type'].append(self.match.group(1).strip())
            self.expect(self.prompt)
            self.expect(pexpect.TIMEOUT, timeout=1)
            self.sendline(r'show interface upstream %s/%s | inc "^\s+channel-width"' % (ups_idx, ups_ch))
            self.expect(r'channel-width\s(.*)')
            get_upstream['channel_with'].append(self.match.group(1).strip().split('\r\n')[0])
            self.expect(self.prompt)
            self.expect(pexpect.TIMEOUT, timeout=1)

        return get_upstream

    def set_upstream(self, cm_mac, get_upstream):
        """This function is to set the upstream channel type on cmts.

        :param cm_mac: mac address of the CM
        :type cm_mac: string
        :param channel_type: channel_type 1.0 -> tdma[1], 2.0 -> atdma[2], 3.0 -> scdma[3].
        :type channel_type: string
        :raises assert: bonding index error
        """
        mac_domain = self.get_cm_mac_domain(cm_mac)
        self.sendline('show interface docsis-mac %s | inc upstream' % mac_domain)
        self.expect(self.prompt)
        tmp = re.findall(r"upstream\s\d\sinterface\supstream\s(.*)/(.*)/0", self.before)
        index = 0
        for ups_idx, ups_ch in tmp:
            self.sendline('interface upstream %s/%s' % (ups_idx, ups_ch))
            self.expect(self.prompt)
            self.sendline('frequency %s' %get_upstream['frequency'][index])
            self.expect(self.prompt)
            self.sendline('logical-channel 0 profile %s' %get_upstream['channel_type'][index])
            self.expect(self.prompt)
            self.sendline('channel-width %s' %get_upstream['channel_with'][index])
            self.expect(self.prompt)
            self.sendline('exit')
            self.expect(self.prompt)
            self.expect(pexpect.TIMEOUT, timeout=1)
            index = index+1

    def get_downstream_qam(self, cm_mac):
        """This function is to get downstream modulation type(64qam, 256qam...)

        :param cm_mac: mac address of the CM
        :type cm_mac: string
        :return: Downstream modulation qam values. ex.{'8/6': '256qam', '8/4': '256qam', '8/5': '256qam'}
        :rtype: dict
        """
        mac_domain = self.get_cm_mac_domain(cm_mac)
        self.sendline('show interface docsis-mac %s | inc downstream' % mac_domain)
        self.expect(self.prompt)
        tmp = re.findall(r'downstream\s\d+\sinterface\sqam\s(.*)/\d+', self.before)
        downs = set([x for x in tmp if tmp.count(x) > 1])
        get_downstream_qam = dict()
        for i in downs:
            self.sendline('show interface qam %s | inc "modulation"' % i)
            self.expect(r'modulation\s(.*)')
            get_downstream_qam[i] = self.match.group(1).strip()
            self.expect(self.prompt)

        return get_downstream_qam

    def set_downstream_qam(self, get_downstream_qam):
        """This function is to set downstream modulation type(64qam, 256qam...)

        :param get_downstream_qam: ex.{'8/6': '256qam', '8/4': '256qam', '8/5': '256qam'}
        :type get_downstream_qam: dict
        """
        for k,v in get_downstream_qam.items():
            self.sendline('interface qam %s' % k)
            self.expect(self.prompt)
            self.sendline('modulation %s' %v)
            self.expect(self.prompt)
