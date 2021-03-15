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

            def check_online(self, dut_mac: str) -> bool:
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

            # dut_mac should be present in arguments
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

        def check_online(self, dut_mac: str) -> bool:
            pass

    cmts = MyCmts()  # noqa: F841
