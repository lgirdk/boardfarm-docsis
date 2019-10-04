
from boardfarm.devices import base

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

    def get_cmts_ip_bundle(self, cm_mac, gw_ip):
        raise Exception("Not implemented!")

    def get_cmts_model(self):
        return self.model

    def clear_offline(self, cmmac):
        raise Exception("Not implemented!")

    def clear_cm_reset(self, cmmac):
        raise Exception("Not implemented!")

    def save_running_to_startup_config(self):
        raise Exception("Not implemented!")

    def save_running_config_to_local(self, filename):
        raise Exception("Not implemented!")

    def get_qam_module(self):
        raise Exception("Not implemented!")

    def get_ups_module(self):
        raise Exception("Not implemented!")

    def set_iface_ipaddr(self, iface, ipaddr):
        raise Exception("Not implemented!")

    def set_iface_ipv6addr(self, iface, ipaddr):
        raise Exception("Not implemented!")

    def unset_iface_ipaddr(self, iface):
        raise Exception("Not implemented!")

    def unset_iface_ipv6addr(self, iface):
        raise Exception("Not implemented!")

    def del_file(self, f):
        raise Exception("Not implemented!")

    def check_docsis_mac_ip_provisioning_mode(self, index):
        raise Exception("Not implemented!")

    def wait_for_ready(self):
        raise Exception("Not implemented!")

    def modify_docsis_mac_ip_provisioning_mode(self, index, ip_pvmode = 'dual-stack'):
        raise Exception("Not implemented!")

    def get_ertr_ipv4(self, mac, offset = 2):
        raise Exception("Not implemented!")

    def get_ertr_ipv6(self, mac, offset = 2):
        raise Exception("Not implemented!")

    def get_center_freq(self, mac_domain = None):
        raise Exception("Not implemented!")

    def check_PartialService(self, cmmac):
        raise Exception("Not implemented!")

    def DUT_chnl_lock(self, cm_mac):
        raise Exception("Not implemented!")

    def add_route(self, ipaddr, gw):
        raise Exception("Not implemented!")

    def add_route6(self, net, gw):
        raise Exception("Not implemented!")

    def del_route(self, ipaddr, gw):
        raise Exception("Not implemented!")

    def del_route6(self, net, gw):
        raise Exception("Not implemented!")

    def add_ip_bundle(self, index, helper_ip, ipaddr, secondary_ips = []):
        raise Exception("Not implemented!")

    def add_ipv6_bundle_addrs(self, index, helper_ip, ip, secondary_ips = []):
        raise Exception("Not implemented!")

    def set_iface_qam(self, index, sub, annex, interleave, power):
        raise Exception("Not implemented!")

    def set_iface_qam_freq(self, index, sub, channel, freq):
        raise Exception("Not implemented!")

    def set_iface_upstream(self, ups_idx, ups_ch, freq, width, power):
        raise Exception("Not implemented!")

    def reset(self):
        raise Exception("Not implemented!")

    def is_cm_bridged(self, mac, offset = 2):
        raise Exception("Not implemented!")

    def get_ip_from_regexp(self, cmmac, ip_regexpr):
        raise Exception("Not implemented!")

    def add_service_class(self, index, name, max_rate, max_burst, max_tr_burst = None, downstream = False):
        raise Exception("Not implemented!")

    def add_iface_docsis_mac(self, index, ip_bundle, qam_idx, qam_ch, ups_idx, ups_ch, qam_sub = None, prov_mode = None):
        raise Exception("Not implemented!")

    def get_cmts_type(self):
        raise Exception("Not implemented!")

    def add_service_group(self, index, qam_idx, qam_sub, qam_channels, ups_idx, ups_channels):
        raise Exception("Not implemented!")

    def mirror_traffic(self, macaddr = ""):
        raise Exception("Not implemented!")

    def unmirror_traffic(self):
        raise Exception("Not implemented!")

    def run_tcpdump(self, time, iface = 'any', opts = ""):
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
