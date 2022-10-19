import logging
import re

from boardfarm.exceptions import BftEnvExcKeyError, BftEnvMismatch, BftSysExit
from boardfarm.lib.env_helper import EnvHelper
from debtcollector import deprecate
from nested_lookup import nested_lookup
from termcolor import colored

from boardfarm_docsis.devices.docsis import Docsis
from boardfarm_docsis.exceptions import EnvKeyError

logger = logging.getLogger("bft")


class DocsisEnvHelper(EnvHelper):
    """
    Docsis specific env helper, adds more options such as  "eRouter_Provisioning_mode": "Bridge"
    """

    mode_dict = {"0": "disabled", "1": "ipv4", "2": "ipv6", "3": "dual"}

    def __init__(self, env, mirror=None):
        super().__init__(env, mirror)
        if not self.has_board_boot_file():
            return
        # the InitializationMode in the boot file must match the
        # erotuer mode in the json!
        cfg_str = self.get_board_boot_file()
        match = re.search(r"InitializationMode((\s|\t){1,}([0-3])\;)", cfg_str)
        mode = "none"
        if match:
            mode = self.mode_dict.get(match.group(3))
        if self.env["environment_def"]["board"]["eRouter_Provisioning_mode"] != mode:
            raise BftSysExit(
                colored(
                    f'Conflicting modes: eRouter_Provisioning_mode: {self.env["environment_def"]["board"]["eRouter_Provisioning_mode"]} <-> boot_file: {mode}',
                    color="red",
                    attrs=["bold"],
                )
            )

    def get_prov_mode(self):
        """
        returns the provisioning mode of the desired environment.
        possible values are: ipv4, ipv6, dslite, dualstack, disabled
        """
        try:
            prov_mode = self.env["environment_def"]["board"][
                "eRouter_Provisioning_mode"
            ]
            if prov_mode in Docsis.erouter_config_modes:
                return prov_mode
            else:
                raise EnvKeyError(
                    "Invalid Provisioning mode " + prov_mode + " Specified "
                )
        except (KeyError, AttributeError):
            raise BftEnvExcKeyError

    def get_config_boot(self):
        """Returns the ["environment_def"]["board"]["config_boot"] dictionary

        :return: the config_boot dictionary
        :rtype: dict

        :raise: BftEnvExcKeyError"""

        try:
            return self.env["environment_def"]["board"]["config_boot"]
        except (KeyError, AttributeError):
            raise BftEnvExcKeyError("config_boot not in env_helper")

    def has_config_boot(self):
        """Returns True or False depending if the environment contains the
        "config_boot" dictionary

        :return: possible values are True/False
        :rtype: boolean
        """

        try:
            self.get_config_boot()
            return True
        except BftEnvExcKeyError:
            return False

    def _is_subset(self, subset, superset):
        """Recursive check for nested config_boot, this behaves slightly differently from the
        default env_helper behaviour"""
        if isinstance(subset, dict):
            return all(
                key in superset and self._is_subset(val, superset[key])
                for key, val in subset.items()
            )

        if isinstance(subset, (list, set)):
            return all(
                any(self._is_subset(subitem, superitem) for superitem in superset)
                for subitem in subset
            )

        # assume that subset is a plain value if none of the above match
        return subset == superset

    def _check_config_boot(self, req_cfg_boot):
        """Validates the config_boot separately as the rules are slightly
        different from the general env
        llc is checked as a subset
        snmp is checked as a subset
        vendor_specific is matched for equality

        NOTE: vendor spcific could be checked as a subset by
        using
            self._is_subset(req_cfg_boot["vendor_specific"],
                            cfg_boot["vendor_specific"])

        but this might create some ambiguities.

        :param req_cfg_boot: requested cfg_boot environment from env_helper
        :type req_cfg_boot: dictionary
        :raise: BftEnvMismatch
        """
        try:
            cfg_boot = self.get_config_boot()
        except BftEnvExcKeyError:
            raise BftEnvMismatch('"config_boot" mismatch')

        if "llc" in req_cfg_boot and (
            "llc" not in cfg_boot
            or not self._is_subset(req_cfg_boot["llc"], cfg_boot["llc"])
        ):
            raise BftEnvMismatch('"llc" mismatch')
        if "snmp" in req_cfg_boot and (
            "snmp" not in cfg_boot
            or not self._is_subset(req_cfg_boot["snmp"], cfg_boot["snmp"])
        ):
            raise BftEnvMismatch('"snmp" mismatch')
        if "vendor_specific" in req_cfg_boot and (
            "vendor_specific" not in cfg_boot
            or req_cfg_boot["vendor_specific"] != cfg_boot["vendor_specific"]
        ):
            raise BftEnvMismatch('"vendor_specific" mismatch')
        if (
            "eRouter" in req_cfg_boot
            and "tlvs" in req_cfg_boot["eRouter"]
            and (
                "eRouter" not in cfg_boot
                or req_cfg_boot["eRouter"]["tlvs"] != cfg_boot["eRouter"]["tlvs"]
            )
        ):
            raise BftEnvMismatch('"eRouter" mismatch')

    def _check_boot_file_conditions(self, req_boot_file_checks):
        """Checks the boot_file string provided in the env based on either the regex match or the exact match provided in test_environment
        :param req_boot_file_checks: checks provided in test_environment to be performed on boot_file of env
        :type req_boot_file_conditions: dict
        .. note:: raises BftEnvMismatch exception if the boot_file in test_environment does not match the requirement in env helper environment
        .. note:: checks for key values of contains_regex, not_contains_regex, contains_exact, not_contains_exact in boot_file parameter
        """
        env = self.env["environment_def"]["board"]["boot_file"]
        boot_contains_regex = req_boot_file_checks.get("contains_regex", None)
        boot_not_contains_regex = req_boot_file_checks.get("not_contains_regex", None)
        boot_contains_exact = req_boot_file_checks.get("contains_exact", None)
        boot_not_contains_exact = req_boot_file_checks.get("not_contains_exact", None)
        if boot_contains_regex and not re.search(boot_contains_regex, env):
            raise BftEnvMismatch('"bootfile" mismatch')
        if boot_not_contains_regex and re.search(boot_not_contains_regex, env):
            raise BftEnvMismatch('"bootfile" mismatch')
        if boot_contains_exact and boot_contains_exact not in env:
            raise BftEnvMismatch('"bootfile" mismatch')
        if boot_not_contains_exact and boot_not_contains_exact in env:
            raise BftEnvMismatch('"bootfile" mismatch')

    def env_check(self, test_environment):
        """Test environment check (overrides behaviour).

        This is needed as some of the list in the config boot file do not follow
        the same rules as the lists in the base class.

        :param test_environment: the environment to be checked against the EnvHelper environment
        :type test_environment: dict

        .. note:: raises BftEnvMismatch  if the test_environment is not contained in the env helper environment
        .. note:: recursively checks dictionaries
        """
        if nested_lookup("config_boot", test_environment):
            req_cfg_boot = test_environment["environment_def"]["board"].get(
                "config_boot", {}
            )
            self._check_config_boot(req_cfg_boot)

        if nested_lookup("boot_file", test_environment) and nested_lookup(
            "boot_file", self.env
        ):
            req_boot_file_checks = test_environment["environment_def"]["board"].get(
                "boot_file", {}
            )
            if type(req_boot_file_checks) is dict:
                deprecate(
                    prefix="Using boot_file checks in env_req via a Dict is deprecated",
                    postfix=" Must be passed as a List.",
                    removal_version="2.0.0",
                )
                self._check_boot_file_conditions(req_boot_file_checks)
            else:
                for boot_checks in req_boot_file_checks:
                    self._check_boot_file_conditions(boot_checks)
            test_environment["environment_def"]["board"].pop("boot_file")
        return super().env_check(test_environment)

    def get_board_boot_file(self):
        """Returns the ["environment_def"]["board"]["boot_file"] value
        :return: the boot file value as a string
        :rtype: String"""
        try:
            return self.env["environment_def"]["board"]["boot_file"]
        except (KeyError, AttributeError):
            raise BftEnvExcKeyError

    def has_board_boot_file(self):
        """Returns True if  ["environment_def"]["board"]["boot_file"] exists
        :return: possible values are True/False
        :rtype: bool"""
        try:
            self.get_board_boot_file()
            return True
        except BftEnvExcKeyError:
            return False

    def is_dhcpv4_enabled_on_lan(self) -> bool:
        """Return dhcpv4 status based on env_req

        :return: False if dhcpv4 is disabled else True
        :rtype: boolean
        """
        boot_file = self.env["environment_def"]["board"].get("boot_file", "").lower()
        enable_dhcpv4 = r"Device\.DHCPv4\.Server\.(\d+)\.Enable\|boolean\|true"
        enable_rip = "Device.Routing.RIP.Enable|boolean|true"
        return enable_rip.lower() not in boot_file or bool(
            re.search(enable_dhcpv4, boot_file)
        )
