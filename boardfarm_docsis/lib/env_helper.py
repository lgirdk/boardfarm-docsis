from boardfarm.exceptions import BftEnvExcKeyError
from boardfarm.lib.env_helper import EnvHelper
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

    def get_tr069_provisioning(self):
        """Return list of ACS APIs to be executed during tr069 provisioning.

        :return: object containing list ACS APIs to call for provisioning
        :rtype: dictionary
        """

        try:
            return self.env["environment_def"]["tr-069"]["provisioning"]
        except (KeyError, AttributeError):
            return False
