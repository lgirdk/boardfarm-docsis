from boardfarm.exceptions import BftEnvExcKeyError, BftEnvMismatch
from boardfarm.lib.env_helper import EnvHelper
from nested_lookup import nested_lookup

from boardfarm_docsis.devices.docsis import Docsis
from boardfarm_docsis.exceptions import EnvKeyError


class DocsisEnvHelper(EnvHelper):
    """
    Docsis specific env helper, adds more options such as  "eRouter_Provisioning_mode": "Bridge"
    """

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

    def has_prov_mode(self):
        """
        returns true or false depending if the environment has specified a
        provisioning mode
        """
        try:
            self.get_prov_mode()
            return True
        except (KeyError, AttributeError):
            return False

    def get_ertr_mode(self):
        return {"max_config": True}

    def get_country(self):
        """This method returns the country name from env json.

        :return: possible values are NL,AT,CH,CZ,DE,HU,IE,PL,RO,SK
        :rtype: string
        """
        try:
            return self.env["environment_def"]["board"]["country"]
        except (KeyError, AttributeError):
            raise BftEnvExcKeyError

    def voice_enabled(self):
        """This method returns true if voice is enabled in env JSON.

        :return: possible values are True/False
        :rtype: boolean
        """
        try:
            if "voice" in self.env["environment_def"]:
                return True
            else:
                return False

        except (KeyError, AttributeError):
            raise BftEnvExcKeyError

    def has_lan_advertise_identity(self, idx):
        """Return lan identity value defined in lan_clients of env else return False.

        :idx: lan client index from lan_clients to return corresponding value
        :type: integer

        :return: possible values are True/False
        :rtype: boolean
        """

        try:
            return self.env["environment_def"]["board"]["lan_clients"][idx][
                "advertise_identity"
            ]
        except (KeyError, AttributeError):
            return False

    def get_mitm_devices(self):
        """
        returns list of mitm'ed devices of the desired environment.
        """
        try:
            devices = self.env["environment_def"]["mitm"]
        except (KeyError, AttributeError):
            return list()
        return devices

    def mitm_enabled(self):
        """Flag to see if we have any devices mitm'ed

        :return: True if at least 1 device mitm'ed, False otherwise
        """
        if self.get_mitm_devices():
            return True
        return False

    def get_tr069_provisioning(self):
        """Return list of ACS APIs to be executed during tr069 provisioning.

        :return: object containing list ACS APIs to call for provisioning
        :rtype: dictionary
        """

        try:
            return self.env["environment_def"]["tr-069"]["provisioning"]
        except (KeyError, AttributeError):
            return False

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

        if isinstance(subset, list) or isinstance(subset, set):
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

        if "llc" in req_cfg_boot:
            if "llc" not in cfg_boot or not self._is_subset(
                req_cfg_boot["llc"], cfg_boot["llc"]
            ):
                raise BftEnvMismatch('"llc" mismatch')
        if "snmp" in req_cfg_boot:
            if "snmp" not in cfg_boot or not self._is_subset(
                req_cfg_boot["snmp"], cfg_boot["snmp"]
            ):
                raise BftEnvMismatch('"snmp" mismatch')
        if "vendor_specific" in req_cfg_boot:
            if (
                "vendor_specific" not in cfg_boot
                or req_cfg_boot["vendor_specific"] != cfg_boot["vendor_specific"]
            ):
                raise BftEnvMismatch('"vendor_specific" mismatch')

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
        return super().env_check(test_environment)

    def get_mta_config(self):
        """Returns the ["environment_def"]["voice"]["mta_config_boot"]["snmp_mibs"] values
        :return: the vendor specific mta dict
        :rtype: list, bool if Key/Attribure Error"""

        try:
            return self.env["environment_def"]["voice"]["mta_config_boot"]["snmp_mibs"]
        except (KeyError, AttributeError):
            return False

    def get_emta_config_template(self):
        """Return the ["environment_def"]["board"]["emta"]["config_template"] value
        :return: emta config template ex: "CH_Compal"
        :rtype: string
        """
        try:
            return self.env["environment_def"]["board"]["emta"]["config_template"]
        except (KeyError, AttributeError):
            return False

    def get_dns_dict(self):
        """Returns the dict of reachable and unreachable IP address from DNS.

        :return: number of reachable and unreachable IP address to be fetched from DNS
        :rtype: dictionary
        """
        try:
            return self.env["environment_def"]["DNS"]
        except (KeyError, AttributeError):
            return False
