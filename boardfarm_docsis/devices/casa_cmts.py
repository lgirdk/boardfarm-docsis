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

from boardfarm.devices import connection_decider
from boardfarm.lib.regexlib import ValidIpv4AddressRegex, AllValidIpv6AddressesRegex
from . import base_cmts
import ipaddress


class CasaCMTS(base_cmts.BaseCmts):
    '''
    Connects to and configures a CASA CMTS
    '''

    prompt = ['CASA-C3200>', 'CASA-C3200#', 'CASA-C3200\(.*\)#', 'CASA-C10G>', 'CASA-C10G#', 'CASA-C10G\(.*\)#']
    model = "casa_cmts"

    def __init__(self,
                 *args,
                 **kwargs):
        conn_cmd = kwargs.get('conn_cmd', None)
        connection_type = kwargs.get('connection_type', 'local_serial')
        self.username = kwargs.get('username', 'root')
        self.password = kwargs.get('password', 'casa')
        self.password_admin = kwargs.get('password_admin', 'casa')
        self.mac_domain = kwargs.get('mac_domain', None)


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
        try:
            if 2 != self.expect(['\r\n(.*) login:', '(.*) login:', pexpect.TIMEOUT]):
                hostname = self.match.group(1).replace('\n', '').replace('\r', '').strip()
                self.prompt.append(hostname + '>')
                self.prompt.append(hostname + '#')
                self.prompt.append(hostname + '\(.*\)#')
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
        self.sendline('exit')
        self.sendline('exit')

    def check_online(self, cmmac):
        """Function checks the encrytion mode and returns True if online"""
        """Function returns actual status if status other than online"""
        self.sendline('show cable modem %s' % cmmac)
        self.expect('.+ranging cm \d+')
        result = self.match.group()
        match = re.search('\d+/\d+/\d+\**\s+([^\s]+)\s+\d+\s+.+\d+\s+(\w+)\r\n', result)
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
        if ('c3000' in self.get_cmts_type()):
            print('clear offline feature is not supported on casa product name c3000')
            return
        self.sendline('clear cable modem %s offline' % cmmac)
        self.expect(self.prompt)

    def clear_cm_reset(self, cmmac):
        self.sendline("clear cable modem %s reset" % cmmac)
        self.expect(self.prompt)
        online_state=self.check_online(cmmac)
        self.expect(pexpect.TIMEOUT, timeout = 5)
        if(online_state==True):
            print("CM is still online after 5 seconds.")
        else:
            print("CM reset is initiated.")

    def check_PartialService(self, cmmac):
        self.sendline('show cable modem %s' % cmmac)
        self.expect('(\d+/\d+\.\d+/\d+(\*|\#)\s+\d+/\d+/\d+(\*|\#))\s+online')
        result = self.match.group(1)
        match = re.search('\#', result)
        if match != None:
            output = 1
        else:
            output = 0
        self.expect(self.prompt)
        return output

    def get_cmip(self, cmmac):
        cmmac=self.get_cm_mac_cmts_format(cmmac)
        self.sendline('show cable modem %s' % cmmac)
        self.expect(cmmac + '\s+([\d\.]+)')
        result = self.match.group(1)
        if self.match != None:
            output = result
        else:
            output = "None"
        self.expect(self.prompt)
        return output

    def get_cmipv6(self, cmmac):
        self.sendline('show cable modem %s' % cmmac)
        self.expect(self.prompt)
        match = re.search(AllValidIpv6AddressesRegex, self.before)
        if match:
            output = match.group(0)
        else:
            output = "None"
        return output

    def get_mtaip(self, cmmac, mtamac):
        if ':' in mtamac:
            mtamac = self.get_cm_mac_cmts_format(mtamac)
        self.sendline('show cable modem %s cpe' % cmmac)
        self.expect('([\d\.]+)\s+dhcp\s+' + mtamac)
        result = self.match.group(1)
        if self.match != None:
            output = result
        else:
            output = "None"
        self.expect(self.prompt)
        return output

    def DUT_chnl_lock(self, cm_mac):
        """Check the CM channel locks based on cmts type"""
        streams = ['Upstream', 'Downstream']
        channel_list = []
        for stream in streams:
            self.sendline("show cable modem %s verbose | inc \"%s Channel Set\"" % (cm_mac, stream))
            self.expect(self.prompt)
            if stream == 'Upstream':
                match = re.search('(\d+/\d+.\d+/\d+).+', self.before)
            elif stream == 'Downstream':
                match = re.search('(\d+/\d+/\d+).+', self.before)
            channel = len(match.group().split(","))
            channel_list.append(channel)
        return channel_list

    def get_cm_bundle(self, mac_domain):
        """Get the bundle id from mac-domain """
        self.sendline('show interface docsis-mac '+mac_domain+' | i "ip bundle"')
        index = self.expect(['(ip bundle)[ ]{1,}([0-9]|[0-9][0-9])'] + self.prompt)
        if index != 0:
            assert 0, "ERROR:Failed to get the CM bundle id from CMTS"
        bundle = self.match.group(2)
        self.expect(self.prompt)
        return bundle

    def get_cm_mac_domain(self, cm_mac):
        """Get the Mac-domain of Cable modem """
        self.sendline('show cable modem '+cm_mac+' verbose | i "MAC Domain"')
        idx = self.expect(['(MAC Domain)[ ]{2,}\:([0-9]|[0-9][0-9])'] + self.prompt)
        if idx != 0:
            assert 0, "ERROR: Failed to get the CM Mac Domain from the CMTS"
        mac_domain = self.match.group(2)
        self.expect(self.prompt)
        return mac_domain

    def get_cmts_ip_bundle(self, cm_mac, gw_ip=None):
        '''
        get CMTS bundle IP
        to get a gw ip, use get_gateway_address from mv1.py(board.get_gateway_address())
        '''
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
        self.sendline('exit')
        self.expect(self.prompt)
        self.sendline('del startup-config')
        self.expect('Please type YES to confirm deleting startup-config:')
        self.sendline('YES')
        self.expect(self.prompt)
        self.sendline('system reboot')
        if 0 == self.expect(['Proceed with reload\? please type YES to confirm :', 'starting up console shell ...'], timeout = 180):
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
        self.sendline('show system')
        while 0 == self.expect(['NotReady'] + self.prompt):
            self.expect(self.prompt)
            self.expect(pexpect.TIMEOUT, timeout = 5)
            self.sendline('show system')

    def save_running_to_startup_config(self):
        self.sendline('exit')
        self.expect(self.prompt)
        self.sendline('copy running-config startup-config')
        self.expect(self.prompt)
        self.sendline('config')
        self.expect(self.prompt)

    def save_running_config_to_local(self, filename):
        self.sendline('show running-config')
        self.expect('show running-config')
        self.expect(self.prompt)

        f = open(filename, "w")
        f.write(self.before)
        f.close()

    def set_iface_ipaddr(self, iface, ipaddr):
        '''
        This function is to set an ip address to an interface on cmts.
        Input : arg1: interface name , arg2: <ip></><subnet> using 24 as default if subnet is not provided.
        Output : None (sets the ip address to an interface specified).
        '''
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

    def add_ip_bundle(self, index, helper_ip, ipaddr, secondary_ips = []):
        '''
        This function is to add ip bundle to a cable mac.
        Input : arg1 : cable mac index, arg2 : helper ip to be used, arg3 : actual ip to be assiged to cable mac in the format  <ip></><subnet> subnet defaut taken as 24 if not provided, arg4 : list of seconday ips  in the format  <ip></><subnet> subnet defaut taken as 24 if not provided.
        Output : None (sets the ip bundle to a cable mac).
        '''
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
        '''
        This function is to add route.
        Input : arg1 : <network ip></><subnet ip> take subnet 24 if not provided, arg2 : gateway ip.
        Output : None (adds the route to the specified parameters).
        '''
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
        '''
        This function is to delete route.
        Input : arg1 : <network ip></><subnet ip> take subnet 24 if not provided, arg2 : gateway ip.
        Output : None (deletes the route to the specified parameters).
        '''
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
        '''
        This function is to delete ipv6 route.
        Input : arg1 : network ip, arg2 : subnet ip, arg3 : gateway ip.
        Output : None (deletes the route to the specified parameters).
        '''
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
        self.sendline('show system')
        self.expect(self.prompt)
        return re.findall('Module (\d+) QAM', self.before)[0]

    def get_ups_module(self):
        self.sendline('show system')
        self.expect(self.prompt)
        results = list(map(int, re.findall('Module (\d+) UPS', self.before)))
        return results

    def set_iface_qam(self, index, sub, annex, interleave, power):
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
        self.sendline('interface qam %s/%s' % (index, sub))
        self.expect(self.prompt)
        self.sendline('channel %s freq %s' % (channel, freq))
        self.expect(self.prompt)
        self.sendline('no channel %s shutdown' % channel)
        self.expect(self.prompt)
        self.sendline('exit')
        self.expect(self.prompt)

    def set_iface_upstream(self, ups_idx, ups_ch, freq, width, power):
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
        self.sendline('diag')
        self.expect('Password:')
        self.sendline('casadiag')
        self.expect(self.prompt)
        self.sendline('mirror cm traffic 0')
        self.expect(self.prompt)
        self.sendline('exit')
        self.expect(self.prompt)

    def run_tcpdump(self, time, iface = 'any', opts = ""):
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
        self.sendline('del %s' % f)
        self.expect(self.prompt)

    def is_cm_bridged(self, mac, offset = 2):
        '''
        This function is to check if the modem is in bridge mode.
        Input : arg1 : Mac address of the modem, arg2 : offset (ignored in casa specific to arris).
        Output : Returns True if the modem is bridged else False.
        '''
        self.sendline("show cable modem "+mac+" cpe")
        if 0 == self.expect(['eRouter']+self.prompt):
            self.expect(self.prompt)
            return False
        else:
            return True

    def check_docsis_mac_ip_provisioning_mode(self, index):
        self.sendline('show interface docsis-mac %s' % index)
        self.expect('ip-provisioning-mode (\w+\-\w+)')
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
        '''Getting erouter ipv4 from CMTS '''
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
        '''Getting erouter ipv6 from CMTS '''
        self.sendline("show cable modem %s cpe" % mac)
        self.expect(self.prompt)
        ertr_ipv6 = re.search(AllValidIpv6AddressesRegex, self.before)
        if ertr_ipv6:
            ipv6 = ertr_ipv6.group()
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
        self.sendline('show interface docsis-mac %s | inc downstream\s1\s' % mac_domain)
        self.expect_exact('show interface docsis-mac %s | inc downstream\s1\s' % mac_domain)
        self.expect(self.prompt)
        assert 'downstream 1 interface qam' in self.before
        major, minor, sub = self.before.strip().split(' ')[-1].split('/')
        self.sendline('show interface qam %s/%s | inc channel\s%s\sfreq' % (major, minor, sub))
        self.expect_exact('show interface qam %s/%s | inc channel\s%s\sfreq' % (major, minor, sub))
        self.expect(self.prompt)
        assert 'channel %s frequency' % sub in self.before
        return str(int(self.before.split(' ')[-1]))

    def get_ip_from_regexp(self, cmmac, ip_regexpr):
        """
        Gets an ip address according to a regexpr (helper function)
        Args: cmmac, ip_regexpr
        Return: ip addr (ipv4/6 according to regexpr) or None if not found
        """
        cmmac=self.get_cm_mac_cmts_format(cmmac)
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

    def get_cmts_type(self):
        '''
        This function is to get the product type on cmts.
        Input : None.
        Output : Returns the cmts module type.
        '''
        self.sendline('show system | include Product')
        self.expect(self.prompt)
        return self.before.split(",")[0].split(":")[1].strip().lower()

    def get_qos_parameter(self, cm_mac):
        """
        To get the qos related parameters of CM.
        To get the qos related parameters ["Maximum Concatenated Burst", "Maximum Burst", "Maximum Sustained rate", "Mimimum Reserved rate", "Scheduling Type"] of CM.
        Parameters: (string)cm_mac
        Returns: (dict) containing the qos related parameters.
        """
        qos_dict = {}
        service_flows = ["US" , "DS"]
        for value in service_flows:
            self.sendline("show cable modem %s qos | include %s" % (cm_mac, value))
            self.expect(self.prompt)
            qos_dict[value] = {"sfid" : self.before.split("\n")[-2].split(" ")[0].strip()}

        #mapping of the ouput stream to the US/DS and using the index.
        self.sendline("show cable modem %s qos verbose" % (cm_mac))
        self.expect(self.prompt)

        #setting the index to filter the US/DS parameters from cmts.
        US_index = 0 if qos_dict["US"]["sfid"] in self.before.split("Sfid")[1] else 1
        qos_parameters = ["Maximum Concatenated Burst", "Maximum Burst", "Maximum Sustained rate", "Mimimum Reserved rate", "Scheduling Type"]

        qos_data = []
        for i in range(1,3):
            qos_data.append([string[:-1] for string in self.before.split("Sfid")[i].split("\n") if any(param in string for param in qos_parameters)])
        qos_dict["US"].update(dict([x.split(":")[0].strip(), x.split(":")[1].strip()] for x in qos_data[US_index]))
        del qos_data[US_index]
        qos_dict["DS"].update(dict([x.split(":")[0].strip(), x.split(":")[1].strip()] for x in qos_data[0]))

        #this is to replace Mimimum with Minimum typo on casa cmts and convert to unit of measure like kbpc to bitespersecond.
        for value in service_flows:
            qos_dict[value].update({"Minimum Reserved rate" : int(qos_dict[value]["Mimimum Reserved rate"].split(" ")[0])*1000})
            del qos_dict[value]["Mimimum Reserved rate"]
            qos_dict[value].update({"Maximum Sustained rate" : int(qos_dict[value]["Maximum Sustained rate"].split(" ")[0])*1000})
            qos_dict[value].update({"Maximum Concatenated Burst" : int(qos_dict[value]["Maximum Concatenated Burst"].split(" ")[0])})
            qos_dict[value].update({"Maximum Burst" : int(qos_dict[value]["Maximum Burst"].split(" ")[0])})
        return qos_dict

    def get_upstream_channel(self):
        '''
        This function is to get the upstream channel type on cmts.
        Input : None.
        Output : Upstream channel type 1.0 -> tdma[1], 2.0 -> atdma[2], 3.0 -> scdma[3].
        '''
        self.sendline('show interface docsis-mac %s | inc upstream' % self.mac_domain)
        self.expect(self.prompt)
        tmp = re.findall(r"upstream\s\d\sinterface\supstream\s(.*)/(.*)/0", self.before)
        channel_type = list()
        for ups_idx, ups_ch in tmp:
            self.sendline('show interface upstream %s/%s | inc "logical-channel 0 profile"' % (ups_idx, ups_ch))
            self.expect('logical-channel 0 profile\s(.*)')
            channel_type.append(self.match.group(1).strip())
            self.expect(self.prompt)
            self.expect(pexpect.TIMEOUT, timeout=1)

        return channel_type

    def set_upstream_channel(self, channel_type):
        '''
        This function is to set the upstream channel type on cmts.
        Input : channel_type 1.0 -> tdma[1], 2.0 -> atdma[2], 3.0 -> scdma[3].
        Output : None.
        '''
        self.sendline('show interface docsis-mac %s | inc upstream' % self.mac_domain)
        self.expect(self.prompt)
        tmp = re.findall(r"upstream\s\d\sinterface\supstream\s(.*)/(.*)/0", self.before)
        assert len(tmp) == len(channel_type), 'boning index error'
        for ups, channel in zip(tmp, channel_type):
            self.sendline('interface upstream %s/%s' % (ups[0], ups[1]))
            self.expect(self.prompt)
            self.sendline('logical-channel 0 profile %s' % channel)
            self.expect(self.prompt)
            self.sendline('exit')
            self.expect(self.prompt)
            self.expect(pexpect.TIMEOUT, timeout=1)
