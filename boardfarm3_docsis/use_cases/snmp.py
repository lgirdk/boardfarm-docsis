"""SNMP Use Cases."""

from __future__ import annotations

from typing import TYPE_CHECKING

from boardfarm3.lib.SNMPv2 import SNMPv2

if TYPE_CHECKING:
    from boardfarm3.templates.cpe import CPE
    from boardfarm3.templates.wan import WAN

    from boardfarm3_docsis.templates.cmts import CMTS


def snmp_get(  # pylint: disable=too-many-arguments  # noqa: PLR0913
    mib_name: str,
    wan: WAN,
    board: CPE,
    cmts: CMTS,
    index: int = 0,
    community: str = "private",
    extra_args: str = "",
    timeout: int = 10,
    retries: int = 3,
    cmd_timeout: int = 30,
) -> tuple[str, str, str]:
    """SNMP Get board MIB from WAN device via SNMPv2.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Verify Nm Access IP value via SNMP Get
        - Verify the LLC filter rules removed for IPv4 via SNMP
        - Get the values of [mib_name] via SNMP

    :param mib_name: MIB name. Will be searched in loaded MIB libraries.
    :type mib_name: str
    :param wan: WAN device instance
    :type wan: WAN
    :param board: CPE device instance
    :type board: CPE
    :param cmts: CMTS device instance
    :type cmts: CMTS
    :param index: MIB index, defaults to 0
    :type index: int
    :param community: public/private, defaults to "private"
    :type community: str
    :param extra_args: see ``man snmpget`` for extra args, defaults to ""
    :type extra_args: str
    :param timeout: seconds, defaults to 10
    :type timeout: int
    :param retries: number of retries, defaults to 3
    :type retries: int
    :param cmd_timeout: timeout to wait for command to give otuput
    :type cmd_timeout: int
    :return: value, type, full SNMP output
    :rtype: tuple[str, str, str]
    """
    return SNMPv2(
        wan,
        cmts.get_cable_modem_ip_address(board.cm_mac),  # type: ignore [attr-defined]
        board.sw.get_mibs_compiler(),  # type: ignore [attr-defined]
    ).snmpget(
        mib_name,
        index,
        community,
        extra_args,
        timeout,
        retries,
        cmd_timeout=cmd_timeout,
    )


def snmp_set(  # pylint: disable=too-many-arguments  # noqa: PLR0913
    mib_name: str,
    value: str,
    stype: str,
    wan: WAN,
    board: CPE,
    cmts: CMTS,
    index: int = 0,
    community: str = "private",
    extra_args: str = "",
    timeout: int = 10,
    retries: int = 3,
    cmd_timeout: int = 30,
) -> tuple[str, str, str]:
    """SNMP Set board MIB from WAN device via SNMPv2.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Perform SNMP Set operation on [mib_name]
        - Reset the DUT using SNMP command
        - Set the values of [mib_name] via SNMP

    :param mib_name: MIB name. Will be searched in loaded MIB libraries.
    :type mib_name: str
    :param value: value to be set.
    :type value: str
    :param stype: defines the datatype of value to be set for mib_name.
                  One of the following values:

                  * i: INTEGER,
                  * u: unsigned INTEGER,
                  * t: TIMETICKS,
                  * a: IPADDRESS,
                  * o: OBJID,
                  * s: STRING,
                  * x: HEX STRING,
                  * d: DECIMAL STRING,
                  * b: BITS
                  * U: unsigned int64,
                  * I: signed int64,
                  * F: float,
                  * D: double

    :type stype: str
    :param wan: WAN device instance
    :type wan: WAN
    :param board: CPE device instance
    :type board: CPE
    :param cmts: CMTS device instance
    :type cmts: CMTS
    :param index: MIB index, defaults to 0
    :type index: int
    :param community: public/private, defaults to "private"
    :type community: str
    :param extra_args: see ``man snmpset`` for extra args, defaults to ""
    :type extra_args: str
    :param timeout: seconds, defaults to 10
    :type timeout: int
    :param retries: number of retries, defaults to 3
    :type retries: int
    :param cmd_timeout: timeout to wait for command to give otuput
    :type cmd_timeout: int
    :return: value, type, full SNMP output
    :rtype: tuple[str, str, str]
    """
    return SNMPv2(
        wan,
        cmts.get_cable_modem_ip_address(board.cm_mac),  # type: ignore [attr-defined]
        board.sw.get_mibs_compiler(),  # type: ignore [attr-defined]
    ).snmpset(
        mib_name,
        value,
        stype,
        index,
        community,
        extra_args,
        timeout,
        retries,
        cmd_timeout=cmd_timeout,
    )


def snmp_walk(  # pylint: disable=too-many-arguments  # noqa: PLR0913
    mib_name: str,
    wan: WAN,
    board: CPE,
    cmts: CMTS,
    index: int = 0,
    community: str = "private",
    extra_args: str = "",
    timeout: int = 10,
    retries: int = 3,
    cmd_timeout: int = 30,
) -> tuple[dict[str, list[str]], str]:
    """SNMP Walk board MIB from WAN device via SNMPv2.

    .. hint:: This Use Case implements statements from the test suite such as:

        - Do SNMP Walk on [mib_name] MIB object on DUT
        - Perform SNMP Walk on DUT

    :param mib_name: MIB name. Will be searched in loaded MIB libraries.
    :type mib_name: str
    :param wan: WAN device instance
    :type wan: WAN
    :param board: CPE instance
    :type board: CPE
    :param cmts: CMTS device instance
    :type cmts: CMTS
    :param index: MIB index, defaults to 0
    :type index: int
    :param community: public/private, defaults to "private"
    :type community: str
    :param extra_args: see ``man snmpwalk`` for extra args, defaults to ""
    :type extra_args: str
    :param timeout: seconds, defaults to 10
    :type timeout: int
    :param retries: number of retries, defaults to 3
    :type retries: int
    :param cmd_timeout: timeout to wait for command to give otuput
    :type cmd_timeout: int
    :return: (dictionary of mib_oid as key and tuple(mib value, mib type) as value,
             complete output)
    :rtype: tuple[dict[str, List[str]], str]
    """
    return SNMPv2(
        wan,
        cmts.get_cable_modem_ip_address(board.cm_mac),  # type: ignore [attr-defined]
        board.sw.get_mibs_compiler(),  # type: ignore [attr-defined]
    ).snmpwalk(
        mib_name,
        index,
        community,
        retries,
        timeout,
        extra_args,
        cmd_timeout=cmd_timeout,
    )


def get_mib_oid(mib_name: str, device: CPE) -> str:
    """Return the Object Identifier (OID) for a given MIB.

    :param mib_name: MIB name. Will be searched in loaded MIB libraries.
    :type mib_name: str
    :param device: CPE device instance
    :type device: CPE
    :return: OID of the MIB
    :rtype: str
    """
    # TODO: To be revisited when 2 CPE's of different board types
    # are present.  # BOARDFARM-5015
    return device.sw.get_mibs_compiler().get_mib_oid(  # type: ignore [attr-defined]
        mib_name
    )


def snmp_bulk_get(  # pylint: disable=too-many-arguments  # noqa: PLR0913
    board: CPE,
    wan: WAN,
    cmts: CMTS,
    mib_name: str,
    index: int | None = None,
    community: str = "private",
    non_repeaters: int = 0,
    max_repetitions: int = 10,
    retries: int = 3,
    timeout: int = 100,
    extra_args: str = "",
    cmd_timeout: int = 30,
) -> list[tuple[str, str, str]]:
    """Perform SNMP BulkGet on the device with given arguments.

    :param board: CPE device instance
    :type board: CPE
    :param wan: WAN device instance
    :type wan: WAN
    :param cmts: CMTS device instance
    :type cmts: CMTS
    :param mib_name: MIB name used to perform SNMP query
    :type mib_name: str
    :param index: index used along with mib_name, defaults to None
    :type index: int | None
    :param community: SNMP Community string, defaults to "private"
    :type community: str
    :param non_repeaters: value treated as get request, defaults to 0
    :type non_repeaters: int
    :param max_repetitions: value treated as get next operation, defaults to 10
    :type max_repetitions: int
    :param retries: number of time commands are executed on exception, defaults to 3
    :type retries: int
    :param timeout: timeout in seconds, defaults to 100
    :type timeout: int
    :param extra_args: extra arguments to be passed in the command, defaults to ""
    :type extra_args: str
    :param cmd_timeout: timeout to wait for command to give otuput
    :type cmd_timeout: int
    :return: output of snmpbulkget command
    :rtype: list[tuple[str, str, str]]
    """
    return SNMPv2(
        wan,
        cmts.get_cable_modem_ip_address(board.cm_mac),  # type: ignore [attr-defined]
        board.sw.get_mibs_compiler(),  # type: ignore [attr-defined]
    ).snmpbulkget(
        mib_name,
        index,
        community,
        non_repeaters,
        max_repetitions,
        retries,
        timeout,
        extra_args,
        cmd_timeout=cmd_timeout,
    )
