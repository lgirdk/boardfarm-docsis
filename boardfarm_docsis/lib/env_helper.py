from boardfarm.lib.env_helper import EnvHelper
from boardfarm.exceptions import BftEnvExcKeyError


class DocsisEnvHelper(EnvHelper):
    '''
    Docsis specific env helper, adds more options such as  "eRouter_Provisioning_mode": "Bridge"
    '''
    def get_prov_mode(self):
        '''
        returns the provisioning mode of the desired environment.
        possible values are: ipv4, ipv6, dslite, dualstack, bridge
        '''

        try:
            return self.env['environment_def']['board'][
                'eRouter_Provisioning_mode']
        except (KeyError, AttributeError):
            raise BftEnvExcKeyError

    def has_prov_mode(self):
        '''
        returns true or false depending if the environment has specified a
        provisioning mode
        '''
        try:
            self.get_prov_mode()
            return True
        except:
            return False

    def get_ertr_mode(self):
        return {'max_config': True}

    def get_country(self):
        """This method returns the country name from env json.

        :return: possible values are NL,AT,CH,CZ,DE,HU,IE,PL,RO,SK
        :rtype: string
        """
        try:
            return self.env['environment_def']['board']['country']
        except (KeyError, AttributeError):
            raise BftEnvExcKeyError

    def voice_enabled(self):
        """This method returns true if voice is enabled in env JSON.

        :return: possible values are True/False
        :rtype: boolean
        """
        try:
            return self.env['environment_def']['board']['voice']
        except (KeyError, AttributeError):
            raise BftEnvExcKeyError