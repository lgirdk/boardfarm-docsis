"""An add-on to boardfarm that contains DOCSIS specific libraries"""
__version__ = "2025.03.0"

from . import devices  # noqa: F401

selftest_testsuite = "selftest-docsis"
override_probe_devices = True
