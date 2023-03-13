from typing import Dict, List, Optional

import pytest

from boardfarm_docsis.devices.base_devices.cmts_template import CmtsTemplate


def test_cannot_instantiate_abc_cmts():
    with pytest.raises(TypeError) as err:
        cmts = CmtsTemplate()  # noqa: F841
        print(str(err.value))
    assert "Can't instantiate abstract class CmtsTemplate" in str(err.value)


def test_cannot_instantiate_derived_cmts_missing_model():
    with pytest.raises(TypeError) as err:
        # missing "model" property definition
        class MyCmts(CmtsTemplate):
            def __init__(self, *args, **kwargs) -> None:
                pass

            def connect(self) -> None:
                pass

            def is_cm_online(self, dut_mac: str) -> bool:
                pass

        cmts = MyCmts()  # noqa: F841
    assert "Can't instantiate abstract class MyCmts" in str(err.value)


def test_cannot_instantiate_derived_cmts_missing_prompt():
    with pytest.raises(TypeError) as err:
        # missing "prompt" property definition
        class MyCmts(CmtsTemplate):
            model = "unittest"

            def __init__(self, *args, **kwargs) -> None:
                pass

            def connect(self) -> None:
                pass

            def check_online(self, cm_mac: str) -> bool:
                pass

        cmts = MyCmts()  # noqa: F841

    assert "Can't instantiate abstract class MyCmts" in str(err.value)


def test_cannot_instantiate_derived_cmts_incorrect_signature():
    with pytest.raises(TypeError) as err:

        class MyCmts(CmtsTemplate):
            model = "unittest"

            def __init__(self, *args, **kwargs) -> None:
                pass

            def connect(self) -> None:
                pass

            # cm_mac should be present in arguments
            def check_online(self) -> bool:
                pass

        cmts = MyCmts()  # noqa: F841
    assert (
        "Abstract method 'check_online'  not implemented with correct signature in 'MyCmts'."
        in str(err.value)
    )


def test_can_instantiate_derived_cmts_with_correct_structure():
    class MyCmts(CmtsTemplate):
        model = "unittest"
        prompt = []

        def __init__(self, *args, **kwargs) -> None:
            pass

        def connect(self) -> None:
            pass

        def check_online(self, cm_mac: str) -> bool:
            pass

        def logout(self) -> None:
            pass

        def DUT_chnl_lock(self, cm_mac: str) -> List[int]:
            pass

        def clear_offline(self, cm_mac: str) -> None:
            pass

        def clear_cm_reset(self, cm_mac: str) -> None:
            pass

        def get_cmip(self, cm_mac: str) -> Optional[str]:
            pass

        def get_cmipv6(self, cm_mac: str) -> Optional[str]:
            pass

        def check_partial_service(self, cm_mac: str) -> bool:
            pass

        def get_cmts_ip_bundle(
            self, cm_mac: Optional[str] = None, gw_ip: Optional[str] = None
        ) -> str:
            pass

        def get_qos_parameter(self, cm_mac: str) -> Dict[str, List[dict]]:
            pass

        def get_mtaip(self, cm_mac: str, mta_mac: str = None) -> Optional[str]:
            pass

        def get_cmts_type(self) -> str:
            pass

        def get_center_freq(self, cm_mac: str) -> int:
            pass

        def get_ertr_ipv4(self, mac: str, offset: int = 2) -> Optional[str]:
            pass

        def get_ertr_ipv6(self, mac: str, offset: int = 2) -> Optional[str]:
            pass

        def is_cm_bridged(self, mac: str, offset: int = 2) -> bool:
            pass

        def tcpdump_capture(
            self,
            fname: str,
            interface: str = "any",
            additional_args: Optional[str] = None,
        ) -> None:
            pass

        def tcpdump_read_pcap(
            self,
            fname: str,
            additional_args: Optional[str] = None,
            timeout: int = 30,
            rm_pcap: bool = False,
        ) -> str:
            pass

        def tshark_read_pcap(
            self,
            fname: str,
            additional_args: Optional[str] = None,
            timeout: int = 30,
            rm_pcap: bool = False,
        ) -> str:
            pass

        def ip_route(self) -> str:
            pass

        def _get_cm_channel_bonding_detail(
            self, mac_address: str
        ) -> dict[str, list[str]]:
            pass

        def _get_cm_docsis_provisioned_version(self, mac_address: str) -> float:
            pass

    cmts = MyCmts()  # noqa: F841
