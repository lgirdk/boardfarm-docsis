from boardfarm.lib.network_testing import (kill_process, tcpdump_capture,
                                           tshark_read)
from boardfarm.orchestration import TestStep as TS
from boardfarm_docsis.tests.docsis_boot import DocsisBootStub as BF_Test
from requests import HTTPError


class ACS_dos_attack(BF_Test):
    """to look for DOS attack

    """
    def test_main(self):
        param_list = [
            'Device.WiFi.Radio.2.Channel',
            'Device.WiFi.Radio.2.OperatingChannelBandwidth',
            'Device.DeviceInfo.FirstUseDate',
            'Device.ManagementServer.PeriodicInformEnable',
            'Device.DeviceInfo.SoftwareVersion',
            'Device.DeviceInfo.Description',
            'Device.Ethernet.Interface.1.Alias'
        ]
        try:
            capture_file = "acs_pktc.pcap"
            with TS(self, "To induce Dos attack", prefix="Test") as ts:
                count = 0
                ts.call(tcpdump_capture,
                        self.dev.acs_server,
                        "any",
                        capture_file=capture_file)
                for param in param_list:
                    count += 1
                    ts.call(self.dev.acs_server.GPV, param)
        except HTTPError as e:
            if "507" in str(e):
                with TS(self, "To verify packet capture", prefix="Test") as ts:
                    ts.call(kill_process,
                            self.dev.acs_server,
                            process="tcpdump")
                    ts.call(tshark_read,
                            self.dev.acs_server,
                            capture_file,
                            filter_str=
                            "-T fields -e http.response.code | grep \"503\"")
                    ts.verify(
                        "503" in ts.result[-1].output(),
                        "Dos attack happened at " + str(count) + "th GPV")
            else:
                print("No Dos attack")
        finally:
            with TS(self, "Kill tcpdump", prefix="Test") as ts:
                ts.call(kill_process, self.dev.acs_server, process="tcpdump")
