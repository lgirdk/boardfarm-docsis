"""An add-on to boardfarm that contains DOCSIS specific libraries"""
__version__ = "2022.09.0"

from . import devices  # noqa: F401

selftest_testsuite = "selftest-docsis"
override_probe_devices = True
