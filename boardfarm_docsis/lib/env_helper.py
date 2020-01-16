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
            return self.env['environment_def']['board']['eRouter_Provisioning_mode']
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
