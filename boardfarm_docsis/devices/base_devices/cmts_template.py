from abc import abstractmethod

import boardfarm.devices.connection_decider as conn_dec
from boardfarm.lib.bft_pexpect_helper import bft_pexpect_helper as PexpectHelper
from boardfarm.lib.signature_checker import __MetaSignatureChecker


class CmtsTemplate(PexpectHelper, metaclass=__MetaSignatureChecker):
    """CMTS template class.
    Contains basic list of APIs to be able to connect to CMTS
    and to check if DUT is online.
    All methods, marked with @abstractmethod annotation have to be implemented in derived
    class with the same signatures as in template.
    """

    @property
    @abstractmethod
    def model(cls):
        """This attribute is used by boardfarm to select the class to be used
        to create the object that allows the test fixutes to access the CMTS.
        This property shall be a value that matches the "type"
        attribute of CMTS entry in the inventory file.
        """

    @property
    @abstractmethod
    def prompt(cls):
        """This attribute is used by boardfarm to understand how does device's prompt look like.
        E.g. for CASA3200 CMTS this class atribute may be:
        prompt = [
            "CASA-C3200>",
            "CASA-C3200#",
            r"CASA-C3200\\(.*\\)#",
        ]
        Should be a list.
        May containg regexs.
        """

    @abstractmethod
    def __init__(self, *args, **kwargs) -> None:
        """Initialize CMTS parameters.
        Config data dictionary will be unpacked and passed to init as kwargs.
        You can use kwargs in a following way:
            self.username = kwargs.get("username", "DEFAULT_USERNAME")
            self.password = kwargs.get("password", "DEFAULT_PASSWORD")
        Be sure to add
            self.spawn_device(**kwargs)
            self.connect()
        at the end in order to properly initialize device prompt on init step
        """

    @abstractmethod
    def connect(self) -> None:
        """Connect to CMTS & initialize prompt.
        Here you can run initial commands in order to land on specific prompt
        and/or initialize system
        E.g. enter username/password, set stuff in config or disable pagination"""
        # Use this at the beginning to initialize connection pipe
        self.connection.connect()

    @abstractmethod
    def check_online(self, dut_mac: str) -> bool:
        """Return true if dut_mac modem is online.
        Criteria of 'online' should be defined for concrete CMTS"""

    ######################################################
    # Util methods. Not abstract, can and should be reused
    ######################################################

    def spawn_device(self, **kwargs):
        """Spawns a console device based on the class type specified in
        the paramter device_type. Currently the communication with the console
        occurs via the pexpect module."""
        self.connection = conn_dec.connection(self.conn_type, device=self, **kwargs)
