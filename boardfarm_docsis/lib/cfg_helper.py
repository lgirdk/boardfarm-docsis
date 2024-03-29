import collections
import copy
import json
import logging
from collections import OrderedDict
from pathlib import Path
from typing import Dict

logger = logging.getLogger("bft")


def get_base_cfg(
    cfg_name: str = "mta_config.json",
) -> Dict[str, Dict[str, Dict[str, str]]]:
    """Helper function to get base config from json

    :param cfg_name : json file name
    :type cfg_name : string
    :return : json file extracted as dict
    :rtype : dict
    """
    return json.loads(Path(__file__).parent.joinpath(cfg_name).read_text())


def indent_str(string, indent, pad=" "):
    """Helper function to indent a string (padded with spaces by default)

    :param string : pattern to be indented
    :type string : string
    :param indent : indentation count
    :type indent : integer
    :param pad : passed with spaces , defaults to ' '
    :type pad : empty string(, optional)
    :return : string with indentation
    :rtype : string
    """
    string_length = len(string) + indent
    return string.rjust(string_length, pad)


def update_dict(d, **kwargs):
    """Helper function to update a config dictionary

    :param string : dictionary already available
    :type string : dict
    :param **kwargs : dictionary to be updated
    :type **kwargs : dict
    """
    for k, v in kwargs.items():
        if k in d:
            d[k] = v


def dict_to_str(d, name=None, indent=4):
    """Helper function to convert a config dictionary to string.
    It takes care of the list elements (like SnmpMibObject).

    :param string : dictionary already available
    :type string : dict
    :param **kwargs : dictionary to be updated
    :type **kwargs : dict
    """
    s = ""
    for k, v in d.items():
        if v is None:
            continue
        if type(v) is list:
            if all(isinstance(x, str) for x in v):
                # we need to unroll the list into a multiline sequence of values (like SnmpMibObject)
                for list_val in v:
                    s += indent_str(k, indent) + " " + str(list_val) + ";\n"
            elif all(isinstance(x, collections.OrderedDict) for x in v) or all(
                isinstance(x, dict) for x in v
            ):
                # we could have a list of dictionaries (i.e. several Ds/UsServiceFlow specs)
                for dict_val in v:
                    # recursively parse the dictionary
                    s += dict_to_str(dict_val, k, indent)
            else:
                logger.error(
                    f"Skipping list {k} as not all elements are of the same type"
                )
        elif type(v) is collections.OrderedDict or type(v) is dict:
            # recursively parse the dictionary
            s += dict_to_str(v, k, indent)
        else:
            # single value string, append it to the rest
            s += indent_str(k, indent) + " " + str(v) + ";\n"

    if name and len(s):
        s = (
            indent_str(name, indent)
            + "\n"
            + indent_str("{", indent)
            + "\n"
            + "\n".join(indent_str(i, indent) for i in s.split("\n"))
        ) + "}\n"

    return s


#############################
#
# The following classes could take the default vals from json
# Or the whole obj could be jsonised maybe


class GeneralServiceFlow:
    """Class to create the service flow parameters in config file"""

    GeneralServiceFlow_dict = OrderedDict()

    QosParamSetType = "QosParamSetType"
    TrafficPriority = "TrafficPriority"
    MaxRateSustained = "MaxRateSustained"
    MaxTrafficBurst = "MaxTrafficBurst"
    MinReservedRate = "MinReservedRate"
    MinResPacketSize = "MinResPacketSize"
    ActQosParamsTimeout = "ActQosParamsTimeout"
    AdmQosParamsTimeout = "AdmQosParamsTimeout"
    ServiceClassName = "ServiceClassName"

    GeneralServiceFlow_dict_defaults = {
        QosParamSetType: 7,
        TrafficPriority: 1,
        MaxRateSustained: 0,
        MaxTrafficBurst: None,
        MinReservedRate: None,
        MinResPacketSize: None,
        ActQosParamsTimeout: None,
        AdmQosParamsTimeout: None,
        ServiceClassName: None,
    }

    def __init__(self, **kwargs):
        """Constructor method to copy the service flow params and update the dict"""
        self.GeneralServiceFlow_dict = copy.deepcopy(
            self.GeneralServiceFlow_dict_defaults
        )
        update_dict(self.GeneralServiceFlow_dict, **kwargs)

    def __str__(self):
        """Method to get the service flow params string format from method to_str

        :return : conversion of dict to string
        :rtype : string
        """
        return self.to_str()

    def to_str(self):
        """Method to get the string from dictionary of service flow params

        :return : conversion of dict to string
        :rtype : string
        """
        return dict_to_str(self.GeneralServiceFlow_dict)

    def get_dict(self):
        """Method to get the dictionary of service flow

        :return : service flow in dictionary format
        :rtype : dict
        """
        return self.GeneralServiceFlow_dict


class GeneralClassifierParameters:
    """Class to create the classifier parameters in config file"""

    GeneralClassifierParameters_dict = OrderedDict()

    ClassifierRef = "ClassifierRef"
    ServiceFlowRef = "ServiceFlowRef"
    RulePriority = "RulePriority"
    ActivationState = "ActivationState"
    DscAction = "DscAction"
    GenericTLV = "GenericTLV"  # list
    GeneralClassifierParameters_defaults = {
        ClassifierRef: None,
        ServiceFlowRef: None,
        RulePriority: None,
        ActivationState: None,
        DscAction: None,
        GenericTLV: None,
    }

    def __init__(self, **kwargs):
        """Constructor method to copy the classifier params and update the dict"""
        self.GeneralClassifierParameters_dict = copy.deepcopy(
            self.GeneralClassifierParameters_defaults
        )
        update_dict(self.GeneralClassifierParameters_dict, **kwargs)

    def __str__(self):
        """Method to get the classifer params string format from method to_str

        :return : conversion of dict to string
        :rtype : string
        """
        return self.to_str()

    def to_str(self):
        """Method to get the string from dictionary of classifier params

        :return : conversion of dict to string
        :rtype : string
        """
        return dict_to_str(self.GeneralClassifierParameters_dict)

    def get_dict(self):
        """Method to get the dictionary of classifier

        :return : general classifier in dictionary format
        :rtype : dict
        """
        return self.GeneralClassifierParameters_dict


class LLCPacketClassifier(GeneralClassifierParameters):
    """Class to create the LLC packet classifier parameters in config file"""

    LLCPacketClassifier_dict = OrderedDict()

    DstMacAddress = "DstMacAddress"
    SrcMacAddress = "SrcMacAddress"
    EtherType = "EtherType"

    LLCPacketClassifier_defaults = {
        DstMacAddress: None,
        SrcMacAddress: None,
        EtherType: "0x030f16",
    }

    @classmethod
    def name(cls):
        return "LLCPacketClassifier"

    def __init__(self, **kwargs):
        """Constructor method to copy the LLC packet classifier params and update the dict
        of general classifire params
        """
        super().__init__(**kwargs)
        self.LLCPacketClassifier_dict = copy.deepcopy(self.LLCPacketClassifier_defaults)
        update_dict(self.LLCPacketClassifier_dict, **kwargs)
        self.LLCPacketClassifier_dict.update(self.GeneralClassifierParameters_dict)

    def __str__(self):
        """Method to get the LLC packet classifer params string format from method to_str

        :return : conversion of dict to string
        :rtype : string
        """
        return self.to_str()

    def to_str(self):
        """Method to get the string from dictionary of LLC packet classifier params

        :return : conversion of dict to string
        :rtype : string
        """
        return dict_to_str(self.LLCPacketClassifier_dict, name=self.__class__.__name__)

    def get_dict(self):
        """Method to get the dictionary of LLC packet classifier

        :return : LLC packet classifier in dictionary format
        :rtype : dict
        """
        return self.LLCPacketClassifier_dict


class IpPacketClassifier(GeneralClassifierParameters):
    """Class to create the IP packet classifier parameters in config file"""

    IpPacketClassifier_dict = OrderedDict()

    IpSrcAddr = "IpSrcAddr"
    IpSrcMask = "IpSrcMask"
    SrcPortStart = "SrcPortStart"
    SrcPortEnd = "SrcPortEnd"
    IpDstAddr = "IpDstAddr"
    IpDstMask = "IpDstMask"
    DstPortStart = "DstPortStart"
    DstPortEnd = "DstPortEnd"
    IpProto = "IpProto"

    IpPacketClassifier_dict_defaults = {
        IpSrcAddr: None,
        IpSrcMask: None,
        SrcPortStart: None,
        SrcPortEnd: None,
        IpDstAddr: None,
        IpDstMask: None,
        DstPortStart: None,
        DstPortEnd: None,
        IpProto: None,
    }

    @classmethod
    def name(cls):
        return "IpPacketClassifier"

    def __init__(self, **kwargs):
        """Constructor method to copy the IP packet classifier params and update the dict
        of general classifier params
        """
        super().__init__(**kwargs)
        self.IpPacketClassifier_dict = copy.deepcopy(
            self.IpPacketClassifier_dict_defaults
        )
        update_dict(self.IpPacketClassifier_dict, **kwargs)
        self.IpPacketClassifier_dict.update(self.GeneralClassifierParameters_dict)

    def __str__(self):
        """Method to get the IP packet classifer params string format from method to_str

        :return : conversion of dict to string
        :rtype : string
        """
        return self.to_str()

    def to_str(self):
        """Method to get the string from dictionary of IP packet classifier params

        :return : conversion of dict to string
        :rtype : string
        """
        return dict_to_str(self.IpPacketClassifier_dict, name=self.__class__.__name__)

    def get_dict(self):
        """Method to get the dictionary of IP packet classifier

        :return : Ip packet classifier in dictionary format
        :rtype : dict
        """
        return self.IpPacketClassifier_dict


class DsPacketClass(GeneralClassifierParameters):
    """Class to create the classifier parameters for DS packets"""

    classifier = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if IpPacketClassifier.name() in kwargs:
            self.classifier = IpPacketClassifier(**kwargs[IpPacketClassifier.name()])
        elif LLCPacketClassifier.__class__.__name__ in kwargs:
            self.classifier = LLCPacketClassifier(**kwargs[LLCPacketClassifier.name()])

    @classmethod
    def name(cls):
        return "DsPacketClass"

    def __str__(self):
        return self.to_str()

    def to_str(self):
        return dict_to_str(self.get_dict(), name=self.__class__.__name__)

    def get_dict(self):
        d = super().get_dict()
        if self.classifier:
            d.update(OrderedDict({self.classifier.name(): self.classifier.get_dict()}))
        return d


class UsPacketClass(GeneralClassifierParameters):
    """Class to create the classifier parameters for US packets"""

    classifier = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if IpPacketClassifier.name() in kwargs:
            self.classifier = IpPacketClassifier(**kwargs[IpPacketClassifier.name()])
        elif LLCPacketClassifier.__name__ in kwargs:
            self.classifier = LLCPacketClassifier(**kwargs[LLCPacketClassifier.name()])

    @classmethod
    def name(cls):
        return "UsPacketClass"

    def __str__(self):
        return super().__str__()

    def to_str(self):
        return dict_to_str(self.get_dict(), name=self.__class__.__name__)

    def get_dict(self):
        d = super().get_dict()
        if self.classifier:
            d.update(OrderedDict({self.classifier.name(): self.classifier.get_dict()}))
        return d


class UsServiceFlow(GeneralServiceFlow):
    """Class to create the service flow parameters for US service flow
    GeneralServiceFlow class is inherited
    """

    UsServiceFlow_dict = OrderedDict()

    UsServiceFlowRef = "UsServiceFlowRef"
    MaxConcatenatedBurst = "MaxConcatenatedBurst"
    SchedulingType = "SchedulingType"
    RequestOrTxPolicy = "RequestOrTxPolicy"
    IpTosOverwrite = "IpTosOverwrite"

    UsServiceFlow_defaults = {
        UsServiceFlowRef: 1,
        MaxConcatenatedBurst: 0,
        SchedulingType: None,
        RequestOrTxPolicy: None,
        IpTosOverwrite: None,
    }

    @classmethod
    def name(cls):
        return cls.__name__

    def __init__(self, **kwargs):
        """Constructor method to copy the US service flow params and update the dict of
        general service flow
        """
        super().__init__(**kwargs)
        self.UsServiceFlow_dict = copy.deepcopy(self.UsServiceFlow_defaults)
        update_dict(self.UsServiceFlow_dict, **kwargs)
        self.UsServiceFlow_dict.update(self.GeneralServiceFlow_dict)

    def __str__(self):
        """Method to get the US service flow params string format from method to_str

        :return : conversion of dict to string
        :rtype : string
        """
        return self.to_str()

    def to_str(self):
        """Method to get the string from dictionary of US service flow params

        :return : conversion of dict to string
        :rtype : string
        """
        return dict_to_str(self.UsServiceFlow_dict, name=self.__class__.__name__)

    def get_dict(self):
        """Method to get the param dictionary of US service flow

        :return : US service flow in dictionary format
        :rtype : dict
        """
        return self.UsServiceFlow_dict


class DsServiceFlow(GeneralServiceFlow):
    """Class to create the classifier parameters for DS service flow.
    GeneralServiceFlow is inherited
    """

    DsServiceFlow_dict = OrderedDict()

    DsServiceFlowRef = "DsServiceFlowRef"
    MaxDsLatency = "MaxDsLatency"

    DsServiceFlow_defaults = {DsServiceFlowRef: 3, MaxDsLatency: None}

    @classmethod
    def name(cls):
        return cls.__name__

    def __init__(self, **kwargs):
        """Constructor method to copy the DS service flow params and update the dict of
        general service flow
        """
        super().__init__(**kwargs)
        self.DsServiceFlow_dict = copy.deepcopy(self.DsServiceFlow_defaults)
        update_dict(self.DsServiceFlow_dict, **kwargs)
        self.DsServiceFlow_dict.update(self.GeneralServiceFlow_dict)

    def __str__(self):
        """Method to get the DS service flow params string format from method to_str

        :return : conversion of dict to string
        :rtype : string
        """
        return self.to_str()

    def to_str(self):
        """Method to get the string from dictionary of DS service flow params

        :return : conversion of dict to string
        :rtype : string
        """
        return dict_to_str(self.DsServiceFlow_dict, name=self.__class__.__name__)

    def get_dict(self):
        """Method to get the param dictionary of DS service flow

        :return : DS service flow in dictionary format
        :rtype : dict
        """
        return self.DsServiceFlow_dict


class BaselinePrivacy:
    """Class to create the baseline privacy parameters"""

    BaselinePrivacy_dict = OrderedDict()

    AuthTimeout = "AuthTimeout"
    ReAuthTimeout = "ReAuthTimeout"
    AuthGraceTime = "AuthGraceTime"
    OperTimeout = "OperTimeout"
    ReKeyTimeout = "ReKeyTimeout"
    TEKGraceTime = "TEKGraceTime"
    AuthRejectTimeout = "AuthRejectTimeout"
    SAMapWaitTimeout = "SAMapWaitTimeout"
    SAMapMaxRetries = "SAMapMaxRetries"

    BaselinePrivacy_defaults = {
        AuthTimeout: 10,
        ReAuthTimeout: 10,
        AuthGraceTime: 600,
        OperTimeout: 10,
        ReKeyTimeout: 10,
        TEKGraceTime: 600,
        AuthRejectTimeout: 60,
        SAMapWaitTimeout: None,
        SAMapMaxRetries: None,
    }

    @classmethod
    def name(cls):
        return cls.__name__

    def __init__(self, **kwargs):
        """Constructor method to copy the baseline privacy and update the dict"""
        self.BaselinePrivacy_dict = copy.deepcopy(self.BaselinePrivacy_defaults)
        update_dict(self.BaselinePrivacy_dict, **kwargs)

    def __str__(self):
        """Method to get the baseline privacy string format from method to_str

        :return : conversion of dict to string
        :rtype : string
        """
        return self.to_str()

    def to_str(self):
        """Method to get the string from dictionary of baseline privacy params

        :return : conversion of dict to string
        :rtype : string
        """
        return dict_to_str(self.BaselinePrivacy_dict, name=self.__class__.__name__)

    def get_dict(self):
        """Method to get the dictionary of baseline privacy

        :return : Baseline privacy in dictionary format
        :rtype : dict
        """
        return self.BaselinePrivacy_dict


class GlobalMTAParams:
    """
    This class fetches global mta mibs from the json file
    """

    global_mta_params_dict = OrderedDict
    snmp_mib_object = "SnmpMibObject"
    snmp_mta_CC = None
    global_mta_params_defaults = {snmp_mib_object: snmp_mta_CC}

    @classmethod
    def name(cls):
        """
        To get the class name
        """
        return cls.__name__

    @classmethod
    def snmp_mta_global(
        cls, line1="", line2="", global_mta_config_json="mta_config.json"
    ):
        """
        To create list of mta global mibs

        Parameters:
        line1(string): line number for line 1
        line2(string): line number for line 2
        """
        final_list = []
        global_mta_config_file = get_base_cfg(global_mta_config_json)
        for _key, val in global_mta_config_file.items():
            for sub_section, sub_value in val.items():
                tmp = sub_value
                line_suffix = ""
                if "line1" in sub_section:
                    line_suffix = "." + line1
                if "line2" in sub_section:
                    line_suffix = "." + line2
                snmp_mta_global = [
                    f"\t{k}{line_suffix}{v['suffix']}\t{v['data']}\t{v['data_type']}\t"
                    for k, v in tmp.items()
                ]
                final_list.extend(snmp_mta_global)
        return final_list

    def __init__(self, **kwargs):
        if not kwargs.get(self.snmp_mib_object, None):
            kwargs[self.snmp_mib_object] = GlobalMTAParams.snmp_mta_global()

        self.global_mta_params_dict = copy.deepcopy(self.global_mta_params_defaults)
        update_dict(self.global_mta_params_dict, **kwargs)

    def __str__(self):
        """Method to get the global mta params in string format from method to_str

        :return : conversion of dict to string
        :rtype : string
        """

        return self.to_str()

    def to_str(self):
        """Method to get the string from dictionary of global mta params

        :return : conversion of dict to string
        :rtype : string
        """

        return dict_to_str(self.global_mta_params_dict)

    def get_dict(self):
        """Method to get the global mta parameters

        :return : global params in dictionary format
        :rtype : dict
        """
        return self.global_mta_params_dict


class VendorSpecific:
    VendorSpecific_dict = OrderedDict()

    VendorIdentifier = "VendorIdentifier"
    GenericTLV = "GenericTLV"

    VendorSpecific_defaults = {VendorIdentifier: None, GenericTLV: None}

    @classmethod
    def name(cls):
        """
        To get the class name
        """
        return cls.__name__

    def __init__(self, **kwargs):
        self.VendorSpecific_dict = copy.deepcopy(self.VendorSpecific_defaults)
        update_dict(self.VendorSpecific_dict, **kwargs)

    def __str__(self):
        return self.to_str()

    def to_str(self):
        return dict_to_str(self.VendorSpecific_dict, name=self.__class__.__name__)

    def get_dict(self):
        return self.VendorSpecific_dict


class SNMPv1v2cCoexistenceConfig:
    SNMPv1v2cCoexistenceConfig_dict = OrderedDict()
    SNMPv1v2cCoexistenceConfig_defaults = {}

    @classmethod
    def name(cls):
        """
        To get the class name
        """
        return cls.__name__

    def __init__(self, **kwargs):
        self.SNMPv1v2cCoexistenceConfig_dict = copy.deepcopy(
            self.SNMPv1v2cCoexistenceConfig_defaults
        )
        self.SNMPv1v2cCoexistenceConfig_dict.update(**kwargs)

    def __str__(self):
        return self.to_str()

    def to_str(self):
        return dict_to_str(
            self.SNMPv1v2cCoexistenceConfig_dict, name=self.__class__.__name__
        )

    def get_dict(self):
        return self.SNMPv1v2cCoexistenceConfig_dict


class GlobalParameters:
    """
    This class groups the values found at the root level
    of the configuration file

    The SnmpMibObject is a list of values e.g.:

    dict['SnmpMibObject'] = ['docsDevNmAccessIp.10 IPAddress 172.20.0.1',
                             'docsDevNmAccessIp.20 IPAddress 172.20.0.1',
                             'docsDevNmAccessIpMask.10 IPAddress 255.255.255.255',
                             'docsDevNmAccessIpMask.20 IPAddress 255.255.255.255']

    and when the list is parsed/modified every element is split as:

    'docsDevNmAccessIp.10 IPAddress 172.20.0.1' --> 'docsDevNmAccessIp.10' and 'IPAddress 172.20.0.1'
    'docsDevNmAccessIp.10' is used as a key
    'IPAddress 172.20.0.1' is used as a value

    when updating the list:
    'docsDevNmAccessIp.10 IPAddress 255.255.255.255' will update the above
    'docsDevNmAccessIp.10 none' will remove it (it wil not be in the final config)

    NOTE: SnmpMibObject numeric are not allowed by defaul
    """

    GlobalParameters_dict = OrderedDict()

    NetworkAccess = "NetworkAccess"
    GlobalPrivacyEnable = "GlobalPrivacyEnable"
    DownstreamFrequency = "DownstreamFrequency"
    UpstreamChannelId = "UpstreamChannelId"
    MaxCPE = "MaxCPE"
    CpeMAcAddress = "CpeMAcAddress"
    MaxClassifiers = (
        "MaxClassifiers"  # default value 16 from Prasada (to avoid past config issue)
    )
    DocsisTwoEnable = "DocsisTwoEnable"
    GenericTLV = "GenericTLV"  # list
    SwUpgradeFilename = "SwUpgradeFilename"
    SwUpgradeServer = "SwUpgradeServer"
    SnmpMibObject = "SnmpMibObject"  # list
    SnmpWriteControl = "SnmpWriteControl"
    SNMPCPEAccessControl = "SNMPCPEAccessControl"
    MfgCVCData = "MfgCVCData"  # list
    CoSignerCVCData = "CoSignerCVCData"  # list?
    CoSignerCVC = "CoSignerCVC"  # list?
    MtaConfigDelimiter = "MtaConfigDelimiter"
    VendorSpecific = "VendorSpecific"  # dict

    # LLC filters
    snmpobjDocsLLC = [
        "docsDevFilterLLCUnmatchedAction.0 Integer 1",  # Default deny
        "docsDevFilterLLCIfIndex.1 Integer 0",  # all interfaces
        "docsDevFilterLLCProtocolType.1 Integer 1",  # ethertype
        "docsDevFilterLLCProtocol.1 Integer 2048",  # ipv4
        "docsDevFilterLLCStatus.1 Integer 4",  # createAndGo
        "docsDevFilterLLCIfIndex.2 Integer 0",  # all interfaces
        "docsDevFilterLLCProtocolType.2 Integer 1",  # ethertype
        "docsDevFilterLLCProtocol.2 Integer 2054",  # ARP
        "docsDevFilterLLCStatus.2 Integer 4",  # createAndGo
        "docsDevFilterLLCIfIndex.3 Integer 0",  # all interfaces
        "docsDevFilterLLCProtocolType.3 Integer 1",  # ethertype
        "docsDevFilterLLCProtocol.3 Integer 34525",  # ipv6
        "docsDevFilterLLCStatus.3 Integer 4",
    ]  # createAndGo
    snmpobjNmAcc = [
        "docsDevNmAccessIp.1 IPAddress 255.255.255.255",
        "docsDevNmAccessIpMask.1 IPAddress 255.255.255.255",
        'docsDevNmAccessCommunity.1 String "public"',
        "docsDevNmAccessControl.1 Integer 2",
        "docsDevNmAccessInterfaces.1 HexString 0xc0",
        "docsDevNmAccessStatus.1 Integer 4",
        "docsDevNmAccessIp.2 IPAddress 255.255.255.255",
        "docsDevNmAccessIpMask.2 IPAddress 255.255.255.255",
        'docsDevNmAccessCommunity.2 String "private"',
        "docsDevNmAccessControl.2 Integer 3",
        "docsDevNmAccessInterfaces.2 HexString 0xc0",
        "docsDevNmAccessStatus.2 Integer 4",
    ]

    GlobalParameters_defaults = {
        NetworkAccess: 1,
        GlobalPrivacyEnable: 1,
        DownstreamFrequency: None,
        UpstreamChannelId: None,
        MaxCPE: 16,
        CpeMAcAddress: None,
        MaxClassifiers: 16,
        DocsisTwoEnable: None,
        GenericTLV: None,
        SwUpgradeFilename: None,
        SwUpgradeServer: None,
        SnmpMibObject: [],
        SnmpWriteControl: None,
        SNMPCPEAccessControl: None,
        MfgCVCData: None,
        CoSignerCVCData: None,
        CoSignerCVC: None,
        MtaConfigDelimiter: None,
        VendorSpecific: None,
    }

    sys_log_ip = None

    @staticmethod
    def update_snmpobj(origlist, newvals, validate=True):
        """
        Helper function that attempts to update the SnmpMibObject list (origlist)
        with a given set of values (newvals)
        I.e.:

        origlist = ['docsDevNmAccessIp.1 IPAddress 255.255.255.255', 'docsDevNmAccessCommunity.1 String "private"', 'docsDevNmAccessControl.1 Integer 2', 'docsDevNmAccessCommunity.2 String "private"']

        newvals  = ['docsDevNmAccessIp.1 IPAddress 2.2.2.2', 'docsDevNmAccessCommunity.1 String "public"', 'docsDevNmAccessCommunity.2 none', 'docsDevNmAccessCommunity.3 String "unreal"']

        yields:
        ['docsDevNmAccessIp.1 IPAddress 2.2.2.2', 'docsDevNmAccessCommunity.1 String "public"', 'docsDevNmAccessControl.1 Integer 2', 'docsDevNmAccessCommunity.3 String "unreal"']
                    modified                                    modified                                    untouched                               added

        and 1 entry removed ('docsDevNmAccessControl.1 Integer 2')
        """
        newl = []
        tmplist = origlist[:]
        for newelem in newvals:
            name, val = newelem.split(" ", 1)
            for cfgelem in tmplist:
                if name == cfgelem.split(" ", 1)[0]:
                    if val == "none":
                        # skip this value (i.e. delete)
                        pass
                    else:
                        # modify the value
                        newl.append(name + " " + val)
                    name = None
                else:
                    newl.append(cfgelem)
            if name and val != "none":
                # not found in the original list, then add it
                newl.append(newelem)
            tmplist = newl[:]
            newl = []
            if validate:
                GlobalParameters._validate_SnmpMibObject(tmplist)
        return tmplist

    @staticmethod
    def _validate_SnmpMibObject(val_list):
        """Makes sure that there are no numberic oid in SnmpMibObject

        :raises assertion : If condition fails then assert
        """
        if len(val_list) == 0:
            return

        for i, v in enumerate(val_list):
            mib_name = v.split(" ", 1)[0]
            if mib_name.count(".") > 1:
                logger.error("No numeric OIDs allowed in SnmpMibObject")
                logger.debug(f"SnmpMibObject = {val_list}")
                assert 0, (
                    "SnmpMibObject at position "
                    + str(i)
                    + " has '"
                    + mib_name
                    + "' has numeric OID!!!!"
                )

    @classmethod
    def name(cls):
        return cls.__name__

    def __init__(self, **kwargs):
        if GlobalParameters.sys_log_ip is not None:
            # If a syslog ip is assigned might as well give some defautls
            # to its related attributes. These can then be overridden via
            # the kwargs received
            snmpobjlogs = [
                "docsDevEvSyslog.0 IPAddress " + str(GlobalParameters.sys_log_ip),
                "docsDevEvReporting.emergency HexString 0xe0",
                "docsDevEvReporting.alert HexString 0xe0",
                "docsDevEvReporting.critical HexString 0xe0",
                "docsDevEvReporting.error HexString 0xe0",
                "docsDevEvReporting.warning HexString 0xe0",
                "docsDevEvReporting.notice HexString 0xe0",
                "docsDevEvReporting.information HexString 0xe0",
                "docsDevEvReporting.debug HexString 0xe0",
            ]

            if kwargs == {} or self.SnmpMibObject not in kwargs:
                kwargs[self.SnmpMibObject] = []
            kwargs[self.SnmpMibObject].extend(snmpobjlogs)

        self.GlobalParameters_dict = copy.deepcopy(self.GlobalParameters_defaults)
        update_dict(self.GlobalParameters_dict, **kwargs)

        if self.GlobalParameters_dict[self.SnmpMibObject]:
            self._validate_SnmpMibObject(self.GlobalParameters_dict[self.SnmpMibObject])

    def __str__(self):
        """Method to get the global params in string format from method to_str

        :return : conversion of dict to string
        :rtype : string
        """
        return self.to_str()

    def to_str(self):
        """Method to get the string from dictionary of global params

        :return : conversion of dict to string
        :rtype : string
        """
        return dict_to_str(self.GlobalParameters_dict)

    def get_dict(self):
        """Method to get the global parameters

        :return : global params in dictionary format
        :rtype : dict
        """
        return self.GlobalParameters_dict


class eRouter:
    """Class to create the eRouter related parameters"""

    eRouter_dict = OrderedDict()
    InitializationMode = "InitializationMode"
    TR69ManagementServer = "TR69ManagementServer"
    InitializationModeOverride = "InitializationModeOverride"
    RATransmissionInterval = "RATransmissionInterval"
    TopologyModeEncoding = "TopologyModeEncoding"
    VendorSpecific = "VendorSpecific"  # dictionary
    GenericTLV = "GenericTLV"

    eRouter_defaults = {
        InitializationMode: None,
        TR69ManagementServer: None,
        InitializationModeOverride: None,
        RATransmissionInterval: None,
        TopologyModeEncoding: None,
        VendorSpecific: None,
        GenericTLV: None,
    }

    @classmethod
    def name(cls):
        return "eRouter"

    def __init__(self, **kwargs):
        """Constructor method to copy the erouter params and update the dict"""
        self.eRouter_dict = copy.deepcopy(self.eRouter_defaults)
        update_dict(self.eRouter_dict, **kwargs)

    def __str__(self):
        """Method to get the erouter params in string format from method to_str

        :return : conversion of dict to string
        :rtype : string
        """
        return self.to_str()

    def to_str(self):
        """Method to get the string from dictionary of service flow params

        :return : conversion of dict to string
        :rtype : string
        """
        return dict_to_str(self.eRouter_dict, name=self.__class__.__name__)

    def get_dict(self):
        """Method to get the dictionary of erouter

        :return : service flow in dictionary format
        :rtype : dict
        """
        return self.eRouter_dict


##############################################################################################


class CfgGenerator:
    """This class generates a docsis configuration file"""

    indent = 4
    cm_base_cfg = None
    mta_base_cfg = None

    def __init__(self, file_cfg=None):
        """maybe in the future can take swallow a cfg file"""
        if file_cfg is not None:
            assert 0, "Not yet implemented"

        self.additional_cfg = ""

        self.cm_base_cfg = None
        self.cm_base_cfg = [
            GlobalParameters(),
            DsServiceFlow(),
            UsServiceFlow(),
            BaselinePrivacy(),
            eRouter(),
        ]
        self.mta_base_cfg = [GlobalMTAParams()]

    def first(self, s):
        """Return the first element from an ordered collection
        or an arbitrary element from an unordered collection.
        Raise StopIteration if the collection is empty.
        """
        return next(iter(s))

    def update_cm_base_cfg(self, kwargs, flag="cm"):
        """
        Method to update cm or mta base config file with additional features
        based on the flag.

        :param flag : to mention whether cm or mta base cfg has to be created
        :type flag : string
        """
        if not kwargs:
            return

        while kwargs != {}:
            k = self.first(kwargs)
            base_cfg = self.mta_base_cfg if flag == "mta" else self.cm_base_cfg
            for elem in base_cfg:
                if elem.name() == k:
                    d = elem.get_dict()
                    d.update(kwargs[k])
                    break
            kwargs.pop(k)

    def _gen_cfg(self, erouter, kwargs):
        """This is quick way of appending a string at the end of the cfg
        file that can be used for config element that are not standard
        and/or testing new configs without major changes in the code

        :return : config file after appending the required erouter mode
        :rtype : string
        """
        if kwargs:
            self.additional_cfg = kwargs.pop("additional_cfg", "")
        if erouter:
            if eRouter.name() in kwargs:
                er = kwargs[eRouter.name()]
                er.update({eRouter.InitializationMode: erouter})
            else:
                er = {eRouter.InitializationMode: erouter}
            eRout = eRouter(**er)

        tmp_cfg = self.cm_base_cfg[:]
        # is this as bad as i think it is?
        if erouter:
            for i, elem in enumerate(self.cm_base_cfg):
                if elem.__class__.__name__ == eRout.__class__.__name__:
                    tmp_cfg[i] = eRout
        self.update_cm_base_cfg(kwargs)
        self.cm_base_cfg = tmp_cfg[:]
        return tmp_cfg

    def gen_dual_stack_cfg(self, kwargs=None):
        """Method to create dual stack as erouter mode in config file

        :return : config file with initialization mode 3 for dual
        :rtype : string
        """
        return self._gen_cfg("3", kwargs)

    def gen_ipv4_cfg(self, kwargs=None):
        """Method to create ipv4 as erouter mode in config file

        :param kwargs : Can give if any params required , defaults to None
        :type kwargs : string(, optional)
        :return : config file with initialization mode 1 for ipv4
        :rtype : string
        """
        return self._gen_cfg("1", kwargs)

    def gen_ipv6_cfg(self, kwargs=None):
        """Method to create ipv6 as erouter mode in config file

        :param kwargs : Can give if any params required , defaults to None
        :type kwargs : string(, optional)
        :return : config file with initialization mode 2 for ipv6
        :rtype : string
        """
        return self._gen_cfg("2", kwargs)

    def gen_bridge_cfg(self, kwargs=None):
        """Method to create bridge as erouter mode in config file

        :param kwargs : Can give if any params required , defaults to None
        :type kwargs : string(, optional)
        :return : config file with initialization mode 0 for bridge
        :rtype : string
        """
        return self._gen_cfg("0", kwargs)

    def gen_no_mode(self, kwargs=None):
        """Method to create no erouter mode in config file

        :param kwargs : Can give if any params required , defaults to None
        :type kwargs : string(, optional)
        :return : config file withiout any initialization mode
        :rtype : string
        """
        return self._gen_cfg(None, kwargs)

    def _gen_mta_cfg(self, kwargs):
        """Method to generate intermediate mta cfg

        :param kwargs : Can give if any params required
        :type kwargs : string(, optional)
        :return : mta config file
        :rtype : string
        """
        tmp_cfg = self.mta_base_cfg[:]
        self.update_cm_base_cfg(kwargs, flag="mta")
        self.mta_base_cfg = tmp_cfg[:]
        return tmp_cfg

    def generate_cfg(self, fname=None):
        """Finalise the config making it ready for use.

        :param fname : Filename to generate the config file, defaults to None
        :type fname : string(, optional)
        :return : Multiline string
        :rtype : string
        """
        cfg_file_str = "Main\n{\n"

        for i in self.cm_base_cfg:
            cfg_file_str += i.to_str()

        cfg_file_str += self.additional_cfg

        cfg_file_str += "}\n"
        """
        is this really needed? probably not
        if fname:
            # FIX ME: this should have a path too
            if not fname.endswith('.txt'):
                fname += '.txt'
            with open(fname, "w") as text_file:
                text_file.write("{}".format(cfg_file_str))
        """
        return cfg_file_str

    def gen_mta_cfg(self, fname=None):
        """
        This method generates final mta cfg and now its ready to use

        :param fname : Filename to generate the config file, defaults to None
        :type fname : string(, optional)
        :return : Multiline string
        :rtype : string
        """
        return "".join(i.to_str() for i in self.mta_base_cfg)


##############################################################################################

if __name__ == "__main__":
    """
    kwargs = {'DsServiceFlowRef':4}

    dsServiceFlow = DsServiceFlow(**kwargs)
    logger.info(dsServiceFlow)

    usServiceFlow = UsServiceFlow()
    logger.info(usServiceFlow)

    llcPacketClassifier = LLCPacketClassifier()
    logger.info(llcPacketClassifier)

    globalParams = GlobalParameters()
    logger.info(globalParams)

    baselinePrivacy = BaselinePrivacy()
    logger.info(baselinePrivacy)

    gbase_cfg = [GlobalParameters(), DsServiceFlow(**kwargs), UsServiceFlow(), BaselinePrivacy()]

    logger.info("From List:")
    for i in gbase_cfg:
        logger.info(i)
    """

    logger.info("Using: CfgGenerator")
    kwargs = {"GlobalPrivacyEnable": 0}
    c = CfgGenerator()

    GlobalParameters.sys_log_ip = "10.64.38.21"
    newGlobalParameters = copy.deepcopy(GlobalParameters(**kwargs))
    for i, elem in enumerate(c.cm_base_cfg):
        if type(elem) is GlobalParameters:
            c.cm_base_cfg[i] = newGlobalParameters
            break
    c.gen_dual_stack_cfg(kwargs)
    logger.info("=====================================================================")
    logger.info("Dual stack")
    logger.info(c.generate_cfg("dual-stack-config"))
    logger.info("=====================================================================")
    logger.info(
        UsServiceFlow(
            **{
                "UsServiceFlowRef": 1,
                "QosParamSetType": 7,
                "TrafficPriority": 1,
                "MaxRateSustained": 300000000,
                "SchedulingType": 2,
                "IpTosOverwrite": None,
                "MaxTrafficBurst": 42600,
                "MaxConcatenatedBurst": 42600,
            }
        )
    )
    k = UsPacketClass(
        **{
            "ClassifierRef": 21,
            "ServiceFlowRef": 2,
            "RulePriority": 64,
            "IpPacketClassifier": {
                "IpProto": 17,
                "SrcPortStart": 5060,
                "SrcPortEnd": 5060,
            },
        }
    )
    logger.info(k)
    k = UsPacketClass(
        **{
            "ClassifierRef": 132,
            "ServiceFlowRef": 103,
            "IpPacketClassifier": {
                "IpProto": 17,
                "SrcPortStart": 1812,
                "SrcPortEnd": 1813,
                "IpSrcAddr": "123.123.123.123",
                "IpSrcMask": "255.255.255.255",
            },
        }
    )
    logger.info(k)
    """
    GlobalParameters.sys_log_ip = None
    c = CfgGenerator()
    c.gen_bridge_cfg()
    logger.info('=====================================================================')
    logger.info('Bridge')
    logger.info(c.generate_cfg('bridge-config'))
    logger.info('=====================================================================')
    """
    """
    c = CfgGenerator()
    c.gen_ipv4_cfg()
    logger.info('=====================================================================')
    logger.info('IPv4')
    logger.info(c.generate_cfg('ipv4-stack-config'))
    logger.info('=====================================================================')

    c = CfgGenerator()
    c.gen_ipv6_cfg()

    logger.info('=====================================================================')
    logger.info('IPv6')
    logger.info(c.generate_cfg('ipv6-stack-config'))
    logger.info('=====================================================================')

    c = CfgGenerator()
    c.gen_bridge_cfg()

    logger.info('=====================================================================')
    logger.info('bridge')
    logger.info(c.generate_cfg('bridge-config'))
    logger.info('=====================================================================')
    """
    """
    configObj = CfgGenerator()
    # get the dict as is, not the generated string
    configObj.gen_dual_stack()

    # The following were generated randomly, they do not refer to any real certificate/signature
    cvc1 = "0x3c18f59d7a568327c"
    cvc2 = "0xab82b45cbca"
    cvc3 = "0xcfa536788aa410"

    # add to the dictionary as a list of vals
    configObj.add_multiline_values('MfgCVCData', [cvc1, cvc2, cvc3])

    cocvc1 = '0x0x30820311308201F9A003020102021079'
    cocvc2 = '0x0x040A13083830303030303039310F300D060355040B'
    configObj.add_multiline_values('CoSignerCVCData', [cocvc1, cocvc2])

    # the snmp mibs are multiline values too

    d = configObj.json_to_cfg()
    logger.info('##############################################')
    logger.info(d)
    logger.info('##############################################')
    """
    logger.info("Done.")
