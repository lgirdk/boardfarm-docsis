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
        Author : Rajan
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
        Author : Rajan
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
        Author : Rajan
        '''
        self.sendline('show linecard status | include DMM/DMM')
        self.expect(self.prompt)
        return  self.before.split("\n",1)[1]

    def get_ups_module(self):
        '''
        This function is to return the upc (UCAM) modules on cmts.
        Input : None
        Output : Returns the upc (UCAM) modules on cmts.
        Author : Rajan
        '''
        self.sendline('show linecard status | include CAM/CAM')
        self.expect(self.prompt)
        return self.before.split("\n",1)[1]

    def set_iface_ipaddr(self, iface, ipaddr):
        '''
        This function is to set an ip address to an interface on cmts.
        Input : arg1: interface name , arg2: ip address followed by subnet as one string.
        Output : None 9 (sets the ip address to an interface specified).
        Author : Rajan.
        '''
        self.sendline('interface %s' % iface)
        self.expect(self.prompt)
        self.sendline('ip address %s' % ipaddr)
        self.expect(self.prompt)
        self.sendline('no shutdown')
        self.expect(self.prompt)
        self.sendline('exit')
        self.expect(self.prompt)

    def set_iface_ipv6addr(self, iface, ipaddr):
        '''
        This function is to set an ipv6 address to an interface on cmts.
        Input : arg1: interface name , arg2: ipv6 address / prefix as one string.
        Output : None 9 (sets the ipv6 address to an interface specified).
        Author : Rajan.
        '''
        self.sendline('interface %s' % iface)
        self.expect(self.prompt)
        self.sendline('ipv6 address %s' % ipaddr)
        self.expect(self.prompt)
        self.sendline('no shutdown')
        self.expect(self.prompt)
        self.sendline('exit')
        self.expect(self.prompt)

    def del_file(self, f):
        '''
        This function is to delete a file on cmts.
        Input : arg: file name to be deleted if in current directory relative file name to be deleted from /system if in different directory.
        Output : None (specifie file will be deleted on cmts.
        Author : Rajan.
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
        Author : Rajan.
        '''
        self.sendline('show running-config interface cable-mac %s | include cm-ip-prov-mode' % index)
        self.expect(self.prompt)
        result = self.before.split("\n")[1].split(" ")[-1]
        return result

if __name__ == '__main__':
    # Quick  unit test that attempts to run all the functions in this module
    # Pre condition: cmts MUST have at least 1 cm (in any state)        # To run checkout all the needed repos/overlays, then try the following:
    #    cd ./boardfarm-docsis
    #    BFT_DEBUG=y PYTHONPATH="./:../boardfarm:../boardfarm/devices/:../boardfarm/tests/" python ./devices/arris_cmts.py
    #
    # this could be improved (i.e. the conn_cmd, user, passwd are passed on the cli)
    #passing the cmts details from cmd
    kwargs = {"name": "cmts", "conn_cmd": sys.argv[1],"username": sys.argv[2],"password":sys.argv[3]}
    arriscmts = None
    try:
        arriscmts = ArrisCMTS(None, **kwargs)
        #calling the unit test method in the base_cmts
        arriscmts.unit_test()
    except Exception as e:
        print(e)
