#!/usr/bin/env python3
import logging
import re
import sys
from typing import Dict, List, Optional

import netaddr
import pexpect
from boardfarm.devices import connection_decider
from boardfarm.lib.regexlib import AllValidIpv6AddressesRegex, ValidIpv4AddressRegex

from boardfarm_docsis.devices.base_devices.cmts_template import CmtsTemplate

logger = logging.getLogger("bft")


class CBR8CMTS(CmtsTemplate):
    """Connects to and configures a CBR8 CMTS"""

    prompt = ["cBR-8(.*)>", "cBR-8(.*)#", r"cBR-8\(.*\)> ", r"cBR-8\(.*\)# "]
    model = "cBR8_cmts"

    def __init__(self, *args, **kwargs) -> None:
        """Constructor method"""
        conn_cmd = kwargs.get("conn_cmd", None)
        connection_type = kwargs.get("connection_type", "local_serial")
        self.ipaddr = kwargs.get("ipaddr", None)
        self.password = kwargs.get("password", "cisco")
        self.password_admin = kwargs.get("password_admin", "cisco")
        self.mac_domain = kwargs.get("mac_domain", None)
        self.channel_bonding = kwargs.get("channel_bonding", 24)  # 16x8 : total 24

        if conn_cmd is None:
            # TODO: try to parse from ipaddr, etc
            raise Exception("No command specified to connect to CBR8 CMTS")

        self.connection = connection_decider.connection(
            connection_type, device=self, conn_cmd=conn_cmd
        )
        if kwargs.get("debug", False):
            self.logfile_read = sys.stdout
        self.connection.connect()
        self.connect()
        self.logfile_read = sys.stdout

        self.name = kwargs.get("name", "cBR8_cmts")

    def connect(self) -> None:
        """This method is used to connect cmts.
        Login to the cmts based on the connection type available

        :raises Exception: Unable to get prompt on CBR8 device
        """
        try:
            if self.expect(["User Access Verification", pexpect.TIMEOUT]) != 1:
                self.expect("assword:")
                self.sendline(self.password)
                self.expect(self.prompt)
            else:
                # Over telnet we come in at the right prompt
                # over serial it could be stale so we try to recover
                self.sendline("q")
                self.sendline("exit")
                self.expect([pexpect.TIMEOUT] + self.prompt, timeout=20)
            self.sendline("enable")
            if self.expect(["Password:"] + self.prompt) == 0:
                self.sendline(self.password_admin)
                self.expect(self.prompt)
            return
        except Exception:
            raise Exception("Unable to get prompt on CBR8 device")

    def logout(self) -> None:
        """Logout of the CMTS device"""
        self.sendline("exit")
        self.sendline("exit")

    def check_online(self, cm_mac: str) -> bool:
        """Check the CM status from CMTS
        Function checks the encryption mode and returns True if online

        :param cm_mac: mac address of the CM
        :type cm_mac: string
        :raises assert:  incorrect cmstatus in cmts
        :return: True if the CM is operational else actual status on cmts
        :rtype: boolean or string
        """
        self.sendline(f"show cable modem {cm_mac}")
        self.expect(self.prompt)
        result = self.before
        match = re.search(r"\w+/\w+/\w+/\w+\s+((\w+\-?\(?\)?)+)", result)
        if match:
            status = match.group(1)
            if status in [
                "w-online(pt)",
                "w-online",
                "w-online(d)",
                "p-online(pt)",
                "p-online",
                "p-online(d)",
            ]:
                output = True
            elif "online" not in status and status is not None:
                output = False
            else:
                assert 0, 'ERROR: incorrect cmstatus "' + status + '" in cmts'
        else:
            assert 0, "ERROR: Couldn't fetch CM status from cmts"
        return output

    def clear_offline(self, cm_mac: str) -> None:
        """Clear the CM entry from cmts which is offline -clear cable modem <mac> offline

        :param cm_mac: mac address of the CM
        :type cm_mac: string
        """
        self.sendline(f"clear cable modem {cm_mac} offline")
        self.expect(self.prompt)

    def clear_cm_reset(self, cm_mac: str) -> None:
        """Reset the CM from cmts using cli -clear cable modem <mac> reset

        :param cm_mac: mac address of the CM
        :type cm_mac: string
        """
        self.sendline(f"clear cable modem {cm_mac} reset")
        self.expect(self.prompt)
        online_state = self.check_online(cm_mac)
        self.expect(pexpect.TIMEOUT, timeout=5)
        if online_state is True:
            logger.debug("CM is still online after 5 seconds.")
        else:
            logger.debug("CM reset is initiated.")

    def get_cmip(self, cm_mac: str) -> Optional[str]:
        """Get the IP of the Cable modem from CMTS

        :param cm_mac: mac address of the CM
        :type cm_mac: string
        :return: ip address of cable modem or "None"
        :rtype: string
        """
        cm_mac = self.get_cm_mac_cmts_format(cm_mac)
        self.sendline(f"show cable modem {cm_mac}")
        self.expect(cm_mac + r"\s+([\d\.]+)")
        result = self.match.group(1)
        output = result if self.match is not None else "None"
        self.expect(self.prompt)
        return output

    def get_cmipv6(self, cm_mac: str) -> Optional[str]:
        """Get IPv6 address of the Cable modem from CMTS

        :param cm_mac: mac address of the CM
        :type cm_mac: string
        :return: ipv6 address(str) of cable modem or "None"
        :rtype: string
        """
        self.sendline(f"show cable modem {cm_mac} ipv6")
        self.expect(self.prompt)
        match = re.search(AllValidIpv6AddressesRegex, self.before)
        return match.group(0) if match else "None"

    def get_mtaip(self, cm_mac: str, mta_mac: str = None) -> Optional[str]:
        """Get the MTA IP from CMTS

        :param cm_mac: mac address of the CM
        :type cm_mac: string
        :param mta_mac: mta mac address
        :type mta_mac: string
        :return: MTA ip address or "None" if ip not found
        :rtype: string
        """
        self.sendline(f"show cable modem {cm_mac} cpe")
        self.expect(self.prompt)
        mac = netaddr.EUI(mta_mac)
        ertr_mac = netaddr.EUI(int(mac) + 0)
        ertr_mac.dialect = netaddr.mac_cisco
        ertr_ipv4 = re.search(f"({ertr_mac}) .* ({ValidIpv4AddressRegex})", self.before)
        if ertr_ipv4:
            return ertr_ipv4.group(2)
        else:
            return None

    def get_center_freq(self, mac_domain=None) -> int:
        """This function is to return the center frequency of cmts

        :param mac_domain: Mac Domain of the cable modem
        :type mac_domain: string
        :return: Returns center frequency configured on the qam
        :rtype: string
        """
        if mac_domain is None:
            mac_domain = self.mac_domain
        assert mac_domain is not None, "get_center_freq() requires mac_domain to be set"
        self.sendline(f"show controllers integrated-Cable {mac_domain} rf-ch 0")
        self.expect(r".*UP\s+(\d+)\s+DOCSIS")
        freq = self.match.group(1)
        output = freq if self.match is not None else "None"
        self.expect(self.prompt)
        return output

    def get_ertr_ipv4(self, mac: str, offset: int = 2) -> Optional[str]:
        """Getting erouter ipv4 from CMTS

        :param mac: mac address of the cable modem
        :type mac: string
        :param offset: ignored in casa specific to cbr8, defaults to 2
        :return: returns ipv4 address of erouter else None
        :rtype: string
        """
        self.sendline(f"show cable modem {mac} cpe")
        self.expect(self.prompt)
        mac = netaddr.EUI(mac)
        ertr_mac = netaddr.EUI(int(mac) + offset)
        ertr_mac.dialect = netaddr.mac_cisco
        ertr_ipv4 = re.search(f"({ertr_mac}) .* ({ValidIpv4AddressRegex})", self.before)
        if ertr_ipv4:
            return ertr_ipv4.group(2)
        else:
            return None

    def get_ertr_ipv6(self, mac: str, offset: int = 2) -> Optional[str]:
        """Getting erouter ipv6 from CMTS

        :param mac: mac address of the cable modem
        :type mac: string
        :param offset: ignored in casa specific to cbr8, defaults to 2
        :return: returns ipv6 address of erouter else None
        :rtype: string
        """
        self.sendline(f"show cable modem {mac} ipv6 cpe")
        self.expect(self.prompt)
        ertr_ipv6 = re.search(AllValidIpv6AddressesRegex, self.before)
        if ertr_ipv6:
            return ertr_ipv6.group()
        else:
            return None

    def DUT_chnl_lock(self, cm_mac: str) -> List[int]:
        """Return amount of upstream / downstream channels that modem is bonded to
        :param cm_mac: cable modem mac address
        :return: [upstream_channels_count, downstream_channels_count]
        """
        raise NotImplementedError

    def check_partial_service(self, cm_mac: str) -> bool:
        """Check the CM status from CMTS
        Function checks the show cable modem and returns True if p-online
        :param cm_mac: cm mac
        :type cm_mac: str
        :return: True if modem is in partial service, False otherwise
        :rtype: bool
        """
        raise NotImplementedError

    def get_cmts_ip_bundle(
        self, cm_mac: Optional[str] = None, gw_ip: Optional[str] = None
    ) -> str:
        """Get CMTS bundle IP, Validate if Gateway IP is configured in CMTS and both are in same network
        The first host address within the network will be assumed to be gateway for Mini CMTS
        :param cm_mac: cm mac
        :type cm_mac: str
        :param gw_ip: gateway ip
        :type gw_ip: str
        :raises assertion error: ERROR: Failed to get the CMTS bundle IP
        :return: gateway ip if address configured on mini cmts else return all ip bundles
        :rtype: str
        """
        raise NotImplementedError

    def get_qos_parameter(self, cm_mac: str) -> Dict[str, List[dict]]:
        """To get the qos related parameters of CM
        Example output format : {'DS':  [{'Sfid': '1' ..},
                                         {'Sfid': '2' ..}
                                 'US': [{{'Sfid': '1' ..},
                                  'Maximum Burst': '128000',
                                  'IP ToS Overwrite [AND-msk, OR-mask]':
                                  ['0x00', '0x00'], ...},
                                  {'Sfid': '1' ..}}
        The units for measuring are
        1) Maximum Sustained rate, Minimum Reserved rate -- bits/sec
        2) Maximum Burst, Minimum Packet Size, Maximum Concatenated Burst,
            Bytes received, Packet dropped -- bytes
        3) Admitted Qos Timeout, Active QoS Timeout -- seconds
        4) Current Throughput -- [bits/sec, packets/sec]
        :param cm_mac: mac address of the cable modem
        :type cm_mac: string
        :return: containing the qos related parameters.
        :rtype: dictionary
        """
        raise NotImplementedError

    def run_tcpdump(self, timeout: int, iface: str = "any", opts: str = "") -> None:
        """tcpdump capture on the cmts interface
        :param timeout: timeout to wait till gets prompt
        :type timeout: integer
        :param iface: any specific interface, defaults to 'any'
        :type iface: string, optional
        :param opts: any other options to filter, defaults to ""
        :type opts: string
        """
        raise NotImplementedError

    def is_cm_bridged(self, mac: str, offset: int = 2) -> bool:
        """Check if the modem is in bridge mode
        :param mac: Mac address of the modem,
        :param offset: eRouter mac address offset, defaults to 2
        :return: True if the modem is bridged mode else False.
        :rtype: boolean
        """
        raise NotImplementedError
