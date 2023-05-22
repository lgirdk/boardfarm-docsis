"""Boardfarm plugin for DOCSIS devices."""

from argparse import ArgumentParser

from boardfarm3 import hookimpl
from boardfarm3.devices.base_devices import BoardfarmDevice

from boardfarm3_docsis.devices.isc_provisioner import ISCProvisioner
from boardfarm3_docsis.devices.minicmts import MiniCMTS


@hookimpl
def boardfarm_add_cmdline_args(argparser: ArgumentParser) -> None:
    """Add new command line arguments to boardfarm.

    :param argparser: argument parser

    """
    docsis_group = argparser.add_argument_group("docsis")
    docsis_group.add_argument(
        "--ldap-credentials",
        default=None,
        help="LDAP credential <username;password>",
    )


@hookimpl
def boardfarm_add_devices() -> dict[str, type[BoardfarmDevice]]:
    """Add devices to known devices for deployment.

    :returns: devices dictionary
    """
    return {
        "mini_cmts": MiniCMTS,
        "debian-isc-provisioner": ISCProvisioner,
    }
