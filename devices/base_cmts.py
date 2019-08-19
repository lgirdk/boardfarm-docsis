import base


class BaseCmts(base.BaseDevice):
    '''
    Common API for the CMTS type devices
    '''
    model = "undefined"

    def connect(self):
        raise Exception("Not implemented!")

    def logout(self):
        raise Exception("Not implemented!")

    def check_online(self, cmmac):
        raise Exception("Not implemented!")

    def get_cmip(self, cmmac):
        raise Exception("Not implemented!")

    def get_cmipv6(self, cmmac):
        raise Exception("Not implemented!")

    def get_mtaip(self, cmmac, mtamac):
        raise Exception("Not implemented!")

    # this should be get_md_bundle
    def get_cm_bundle(self, mac_domain):
        raise Exception("Not implemented!")

    def get_cm_mac_domain(self, cm_mac):
        raise Exception("Not implemented!")

    def get_cmts_ip_bundle(self, bundle):
        raise Exception("Not implemented!")

    def get_cmts_model(self):
        return self.model

    def clear_offline(self, cmmac):
        raise Exception("Not implemented!")

    def clear_cm_reset(self, cmmac):
        raise Exception("Not implemented!")

    def save_running_to_startup_config(self):
        raise Exception("Not implemented!")

    def save_running_config_to_local(self,filename):
        raise Exception("Not implemented!")

    def get_qam_module(self):
        raise Exception("Not implemented!")

    def get_ups_module(self):
        raise Exception("Not implemented!")

    def set_iface_ipaddr(self, iface, ipaddr):
        raise Exception("Not implemented!")

    def set_iface_ipv6addr(self, iface, ipaddr):
        raise Exception("Not implemented!")

    def del_file(self, f):
        raise Exception("Not implemented!")

    def check_docsis_mac_ip_provisioning_mode(self, index):
        raise Exception("Not implemented!")

    def get_cm_mac_cmts_format(self, mac):
        """
        Function:   get_cm_mac_cmts_format(mac)
        Parameters: mac        (mac address XX:XX:XX:XX:XX:XX)
        returns:    the cm_mac in cmts format xxxx.xxxx.xxxx (lowercase)
        """
        if mac == None:
            return None
        # the mac cmts syntax format example is 3843.7d80.0ac0
        tmp = mac.replace(':', '')
        mac_cmts_format = tmp[:4]+"."+tmp[4:8]+"."+tmp[8:]
        return mac_cmts_format.lower()

    def show_cable_modems(self):
        """
        Shows all the cable modems on this cmts.
        This function is used by the unit test.
        Input : None
        Output : show cable modem output
        Author : Rajan
        """
        self.sendline('show cable modem')
        self.expect(self.prompt)
        return self.before

    def unit_test(self):
        """
        This function is designed to do the unit test on the functions in the cmts
        Input : None (will be called by cmts object)
        Output : None (will validate the cmts funcions based on the call)
        Author : Rajan
        """
        #calling the cmts modules for unit test arris
        self.set_iface_ipaddr("gigabitEthernet 17/3","10.64.42.10 255.255.254.0")
        self.set_iface_ipv6addr("gigabitEthernet 17/3","2001:730:1f:60d::cbfe:0/64")
        self.del_file("test.txt")
        ip_provisioning_mode=self.check_docsis_mac_ip_provisioning_mode(2)
        #printing to verify the return value
        print ip_provisioning_mode
