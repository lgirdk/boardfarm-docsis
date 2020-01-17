import netaddr
import pexpect
import sys
import re

from boardfarm.devices import connection_decider
from boardfarm.lib.regexlib import ValidIpv4AddressRegex, AllValidIpv6AddressesRegex
from . import base_cmts


class CBR8CMTS(base_cmts.BaseCmts):
    """Connects to and configures a CBR8 CMTS
    """

    prompt = ['cBR-8(.*)>', 'cBR-8(.*)#', r'cBR-8\(.*\)> ', r'cBR-8\(.*\)# ']
    model = "cBR8_cmts"

    def __init__(self,
                 *args,
                 **kwargs):
        """Constructor method
        """
        conn_cmd = kwargs.get('conn_cmd', None)
        connection_type = kwargs.get('connection_type', 'local_serial')
        self.password = kwargs.get('password', 'cisco')
        self.password_admin = kwargs.get('password_admin', 'cisco')
        self.mac_domain = kwargs.get('mac_domain', None)
        self.channel_bonding = kwargs.get('channel_bonding', 24) # 16x8 : total 24

        if conn_cmd is None:
            # TODO: try to parse from ipaddr, etc
            raise Exception("No command specified to connect to CBR8 CMTS")

        self.connection = connection_decider.connection(connection_type, device=self, conn_cmd=conn_cmd)
        if kwargs.get('debug', False):
            self.logfile_read = sys.stdout
        self.connection.connect()
        self.connect()
        self.logfile_read = sys.stdout

        self.name = kwargs.get('name', 'cBR8_cmts')

    def connect(self):
        """This method is used to connect cmts.
        Login to the cmts based on the connection type available

        :raises Exception: Unable to get prompt on CBR8 device
        """
        try:
            if 1 != self.expect(['User Access Verification', pexpect.TIMEOUT]):
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
            return
        except:
            raise Exception("Unable to get prompt on CBR8 device")

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
            print('clear offline feature is not supported on cbr8 product name c3000')
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

    def get_mtaip(self, cmmac, mtamac):
        """Get the MTA IP from CMTS

        :param cmmac: mac address of the CM
        :type cmmac: string
        :param mtamac: mta mac address
        :type mtamac: string
        :return: MTA ip address or "None" if ip not found
        :rtype: string
        """
        self.sendline("show cable modem %s cpe" % cmmac)
        self.expect(self.prompt)
        mac = netaddr.EUI(mtamac)
        ertr_mac = netaddr.EUI(int(mac) + 0)
        ertr_mac.dialect = netaddr.mac_cisco
        ertr_ipv4 = re.search('(%s) .* (%s)' % (ertr_mac, ValidIpv4AddressRegex), self.before)
        if ertr_ipv4:
            ipv4 = ertr_ipv4.group(2)
            return ipv4
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
        self.sendline('show controllers integrated-Cable %s rf-ch 0' %mac_domain)
        self.expect(r'.*UP\s+(\d+)\s+DOCSIS')
        freq = self.match.group(1)
        if self.match != None:
            output = freq
        else:
            output = "None"
        self.expect(self.prompt)
        return output

    def get_ertr_ipv4(self, mac, offset = 2):
        """Getting erouter ipv4 from CMTS

        :param mac: mac address of the cable modem
        :type mac: string
        :param offset: ignored in casa specific to cbr8, defaults to 2
        :return: returns ipv4 address of erouter else None
        :rtype: string
        """
        self.sendline("show cable modem %s cpe" % mac)
        self.expect(self.prompt)
        mac = netaddr.EUI(mac)
        ertr_mac = netaddr.EUI(int(mac) + offset)
        ertr_mac.dialect = netaddr.mac_cisco
        ertr_ipv4 = re.search('(%s) .* (%s)' % (ertr_mac, ValidIpv4AddressRegex), self.before)
        if ertr_ipv4:
            ipv4 = ertr_ipv4.group(2)
            return ipv4
        else:
            return None

    def get_ertr_ipv6(self, mac, offset = 2):
        """Getting erouter ipv6 from CMTS

        :param mac: mac address of the cable modem
        :type mac: string
        :param offset: ignored in casa specific to cbr8, defaults to 2
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
