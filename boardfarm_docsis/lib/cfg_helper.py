from collections import OrderedDict
import copy


def indent_str(string, indent, pad=' '):
    """Helper function to indent a string (padded with spaces by default)"""
    string_length=len(string)+indent
    indented_string = string.rjust(string_length, pad)
    return indented_string

def update_dict(d, **kwargs):
    """Helper function to update a config dictionary"""
    for k,v in kwargs.items():
        if k in d:
            d[k] = v
            kwargs.pop(k)

def dict_to_str(d, name=None, indent=4):
    """
    Helper function to convert a config dictionary to string.
    It takes care of the list elements (like SnmpMibObject).
    """
    s = ''
    for k,v in d.items():
        if v is None:
            continue
        if type(v) is list:
            # we need to unroll the list into a multiline sequence of values (like SnmpMibObject)
            for list_val in v:
                s +=  indent_str(k, indent) + ' ' + str(list_val) + ';\n'
        else:
            # single value string, append it to the rest
            s +=  indent_str(k, indent) + ' ' + str(v) + ';\n'

    if name and len(s):
        s = indent_str(name, indent) +\
            '\n' +\
            indent_str('{', indent) +\
            '\n' +\
            '\n'.join([indent_str(i, indent) for i in s.split('\n')]) +\
            '}\n'

    return s

#############################
#
# The following classes could take the default vals from json
# Or the whole obj could be jsonised maybe

class GeneralServiceFlow(object):

    GeneralServiceFlow_dict = OrderedDict()

    QosParamSetType  = 'QosParamSetType'
    TrafficPriority  = 'TrafficPriority'
    MaxRateSustained = 'MaxRateSustained'
    MaxTrafficBurst  = 'MaxTrafficBurst'
    MinReservedRate  = 'MinReservedRate'
    MinResPacketSize = 'MinResPacketSize'
    ActQosParamsTimeout = 'ActQosParamsTimeout'
    AdmQosParamsTimeout = 'AdmQosParamsTimeout'
    ServiceClassName = 'ServiceClassName'

    GeneralServiceFlow_dict_defaults = {\
                                         QosParamSetType:7,\
                                         TrafficPriority:1,\
                                         MaxRateSustained:0,\
                                         MaxTrafficBurst:None,\
                                         MinReservedRate:None,\
                                         MinResPacketSize:None,\
                                         ActQosParamsTimeout:None,\
                                         AdmQosParamsTimeout:None,\
                                         ServiceClassName:None\
                                       }

    def __init__(self, **kwargs):
        self.GeneralServiceFlow_dict = copy.deepcopy(self.GeneralServiceFlow_dict_defaults)
        update_dict(self.GeneralServiceFlow_dict, **kwargs)

    def __str__(self):
        return self.to_str()

    def to_str(self):
        return dict_to_str(self.GeneralServiceFlow_dict);

    def get_dict(self):
        return self.GeneralServiceFlow_dict

class GeneralClassifierParameters(object):

    GeneralClassifierParameters_dict = OrderedDict()

    ClassifierRef   = 'ClassifierRef'
    ServiceFlowRef  = 'ServiceFlowRef'
    RulePriority    = 'RulePriority'
    ActivationState = 'ActivationState'
    DscAction       = 'DscAction'

    GeneralClassifierParameters_defaults = {\
                                             ClassifierRef:None,\
                                             ServiceFlowRef:None,\
                                             RulePriority:None,\
                                             ActivationState:None,\
                                             DscAction:None
                                           }

    def __init__(self, **kwargs):
        self.GeneralClassifierParameters_dict = copy.deepcopy(self.GeneralClassifierParameters_defaults)
        update_dict(self.GeneralClassifierParameters_dict, **kwargs)

    def __str__(self):
        return self.to_str()

    def to_str(self):
        return dict_to_str(self.GeneralClassifierParameters_dict);

    def get_dict(self):
        return self.GeneralClassifierParameters_dict

class LLCPacketClassifier(GeneralClassifierParameters):

    LLCPacketClassifier_dict = OrderedDict()

    DstMacAddress = 'DstMacAddress'
    SrcMacAddress = 'SrcMacAddress'
    EtherType     = 'EtherType'

    LLCPacketClassifier_defaults = {\
                                     DstMacAddress:None,\
                                     SrcMacAddress:None,\
                                     EtherType:'0x030f16'\
                                   }
    @classmethod
    def name(cls):
        return 'LLCPacketClassifier'

    def __init__(self, **kwargs):
        super(LLCPacketClassifier, self).__init__(**kwargs)
        self.LLCPacketClassifier_dict = copy.deepcopy(self.LLCPacketClassifier_defaults)
        update_dict(self.LLCPacketClassifier_dict, **kwargs)
        self.LLCPacketClassifier_dict.update(self.GeneralClassifierParameters_dict)

    def __str__(self):
        return self.to_str()

    def to_str(self):
        return dict_to_str(self.LLCPacketClassifier_dict, name=self.__class__.__name__);

    def get_dict(self):
        return self.LLCPacketClassifier_dict

class IpPacketClassifier(GeneralClassifierParameters):

    IpPacketClassifier_dict = OrderedDict()

    IpSrcAddr = 'IpSrcAddr'
    IpSrcMask = 'IpSrcMask'
    SrcPortStart = 'SrcPortStart'
    SrcPortEnd = 'SrcPortEnd'
    IpDstAddr = 'IpDstAddr'
    IpDstMask = 'IpDstMask'
    DstPortStart = 'DstPortStart'
    DstPortEnd   = 'DstPortEnd'
    IpProto      = 'IpProto'

    IpPacketClassifier_dict_defaults = {\
                 IpSrcAddr:None,\
                 IpSrcMask:None,\
                 SrcPortStart:None,\
                 SrcPortEnd:None,\
                 IpDstAddr:None,\
                 IpDstMask:None,\
                 DstPortStart:None,\
                 DstPortEnd:None,\
                 IpProto:None
               }

    @classmethod
    def name(cls):
        return 'IpPacketClassifier'

    def __init__(self, **kwargs):
        super(IpPacketClassifier, self).__init__(**kwargs)
        self.IpPacketClassifier_dict = copy.deepcopy(self.IpPacketClassifier_dict_defaults)
        update_dict(self.IpPacketClassifier_dict, **kwargs)
        self.IpPacketClassifier_dict.update(self.GeneralClassifierParameters_dict)

    def __str__(self):
        return self.to_str()

    def to_str(self):
        return dict_to_str(self.IpPacketClassifier_dict, name=self.__class__.__name__);

    def get_dict(self):
        return self.IpPacketClassifier_dict

class DsPacketClass(GeneralClassifierParameters):

    classifier = None

    def __init__(self, **kwargs):
        pass

class UsPacketClass(GeneralClassifierParameters):

    classifier = None

    def __init__(self, **kwargs):
        pass

class UsServiceFlow(GeneralServiceFlow):

    UsServiceFlow_dict = OrderedDict()

    UsServiceFlowRef  = 'UsServiceFlowRef'
    MaxConcatenatedBurst = 'MaxConcatenatedBurst'
    SchedulingType    = 'SchedulingType'
    RequestOrTxPolicy = 'RequestOrTxPolicy'
    IpTosOverwrite    = 'IpTosOverwrite'

    UsServiceFlow_defaults = {\
                 UsServiceFlowRef:1,\
                 MaxConcatenatedBurst:0,\
                 SchedulingType:None,\
                 RequestOrTxPolicy:None,\
                 IpTosOverwrite:'0x0000'\
               }

    @classmethod
    def name(cls):
        return cls.__name__

    def __init__(self, **kwargs):
        super(UsServiceFlow, self).__init__(**kwargs)
        self.UsServiceFlow_dict = copy.deepcopy(self.UsServiceFlow_defaults)
        update_dict(self.UsServiceFlow_dict, **kwargs)
        self.UsServiceFlow_dict.update(self.GeneralServiceFlow_dict)

    def __str__(self):
        return self.to_str()

    def to_str(self):
        return dict_to_str(self.UsServiceFlow_dict, name=self.__class__.__name__);

    def get_dict(self):
        return self.UsServiceFlow_dict

class DsServiceFlow(GeneralServiceFlow):

    DsServiceFlow_dict = OrderedDict()

    DsServiceFlowRef = 'DsServiceFlowRef'
    MaxDsLatency     = 'MaxDsLatency'

    DsServiceFlow_dict_defaults = {\
                 DsServiceFlowRef:3,\
                 MaxDsLatency: None\
               }

    @classmethod
    def name(cls):
        return cls.__name__

    def __init__(self, **kwargs):
        super(DsServiceFlow, self).__init__(**kwargs)
        self.DsServiceFlow_dict = copy.deepcopy(self.DsServiceFlow_dict_defaults)
        update_dict(self.DsServiceFlow_dict, **kwargs)
        self.DsServiceFlow_dict.update(self.GeneralServiceFlow_dict)

    def __str__(self):
        return self.to_str()

    def to_str(self):
        return dict_to_str(self.DsServiceFlow_dict, name=self.__class__.__name__);

    def get_dict(self):
        return self.DsServiceFlow_dict

class BaselinePrivacy(object):
    BaselinePrivacy_dict = OrderedDict()

    AuthTimeout   = 'AuthTimeout'
    ReAuthTimeout = 'ReAuthTimeout'
    AuthGraceTime = 'AuthGraceTime'
    OperTimeout   = 'OperTimeout'
    ReKeyTimeout  = 'ReKeyTimeout'
    TEKGraceTime  = 'TEKGraceTime'
    AuthRejectTimeout = 'AuthRejectTimeout'
    SAMapWaitTimeout  = 'SAMapWaitTimeout'
    SAMapMaxRetries   = 'SAMapMaxRetries'


    BaselinePrivacy_defaults = {\
                                 AuthTimeout:10,\
                                 ReAuthTimeout:10,\
                                 AuthGraceTime:600,\
                                 OperTimeout:10,\
                                 ReKeyTimeout:10,\
                                 TEKGraceTime:600,\
                                 AuthRejectTimeout:60,\
                                 SAMapWaitTimeout:None,\
                                 SAMapMaxRetries:None\
                               }

    @classmethod
    def name(cls):
        return cls.__name__

    def __init__(self, **kwargs):
        self.BaselinePrivacy_dict = copy.deepcopy(self.BaselinePrivacy_defaults)
        update_dict(self.BaselinePrivacy_dict, **kwargs)

    def __str__(self):
        return self.to_str()

    def to_str(self):
        return dict_to_str(self.BaselinePrivacy_dict, name=self.__class__.__name__);

    def get_dict(self):
        return self.BaselinePrivacy_dict

class GlobalParameters(object):
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

    NetworkAccess       = 'NetworkAccess'
    GlobalPrivacyEnable = 'GlobalPrivacyEnable'
    DownstreamFrequency = 'DownstreamFrequency'
    UpstreamChannelId   = 'UpstreamChannelId'
    MaxCPE              = 'MaxCPE'
    CpeMAcAddress       = 'CpeMAcAddress'
    MaxClassifiers      = 'MaxClassifiers' # default value 16 from Prasada (to avoid past config issue)
    DocsisTwoEnable     = 'DocsisTwoEnable'
    GenericTLV          = 'GenericTLV'       # list
    SwUpgradeFilename   = 'SwUpgradeFilename'
    SwUpgradeServer     = 'SwUpgradeServer'
    SnmpMibObject       = 'SnmpMibObject'    # list
    SnmpWriteControl    = 'SnmpWriteControl'
    SNMPCPEAccessControl= 'SNMPCPEAccessControl'
    MfgCVCData          = 'MfgCVCData'       # list
    CoSignerCVCData     = 'CoSignerCVCData'  # list?
    CoSignerCVC         = 'CoSignerCVC'      # list?
    MtaConfigDelimiter  = 'MtaConfigDelimiter'


    # As requested always add the following
    snmpobjNmAcc = ['docsDevNmAccessIp.1 IPAddress 255.255.255.255',
                    'docsDevNmAccessIpMask.1 IPAddress 255.255.255.255',
                    'docsDevNmAccessCommunity.1 String "public"',
                    'docsDevNmAccessControl.1 Integer 2',
                    'docsDevNmAccessInterfaces.1 HexString 0xc0',
                    'docsDevNmAccessStatus.1 Integer 4',
                    'docsDevNmAccessIp.2 IPAddress 255.255.255.255',
                    'docsDevNmAccessIpMask.2 IPAddress 255.255.255.255',
                    'docsDevNmAccessCommunity.2 String "private"',
                    'docsDevNmAccessControl.2 Integer 3',
                    'docsDevNmAccessInterfaces.2 HexString 0xc0',
                    'docsDevNmAccessStatus.2 Integer 4']

    GlobalParameters_defaults = {\
                                  NetworkAccess:1,
                                  GlobalPrivacyEnable:1,
                                  DownstreamFrequency:None,
                                  UpstreamChannelId:None,
                                  MaxCPE:16,
                                  CpeMAcAddress:None,
                                  MaxClassifiers:16,
                                  DocsisTwoEnable:None,
                                  GenericTLV:None,
                                  SwUpgradeFilename:None,
                                  SwUpgradeServer:None,
                                  SnmpMibObject:snmpobjNmAcc,
                                  SnmpWriteControl:None,
                                  SNMPCPEAccessControl:None,
                                  MfgCVCData:None,
                                  CoSignerCVCData:None,
                                  CoSignerCVC:None,
                                  MtaConfigDelimiter:None
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
            name, val = newelem.split(' ',1)
            for cfgelem in tmplist:
                if name == cfgelem.split(' ',1)[0]:
                    if val == 'none':
                        # skip this value (i.e. delete)
                        pass
                    else:
                        # modify the value
                        newl.append(name + ' ' + val)
                    name = None
                else:
                    newl.append(cfgelem)
            if name and val != 'none':
                # not found in the original list, then add it
                newl.append(newelem)
            tmplist = newl[:]
            newl = []
            if validate:
                GlobalParameters._validate_SnmpMibObject(tmplist)
        return tmplist

    @staticmethod
    def _validate_SnmpMibObject(l):
        """
        Makes sure that there are no numberic oid in SnmpMibObject
        Asserts otherwise
        """
        if len(l) == 0:
            return

        for i,v in enumerate(l):
            mib_name =v.split(' ',1)[0]
            if mib_name.count('.') > 1:
                print("No numeric OIDs allowed in SnmpMibObject")
                print("SnmpMibObject = %s" % l)
                assert 0, "SnmpMibObject at position " + str(i) + " has '" + mib_name  + "' has numeric OID!!!!"
        pass

    @classmethod
    def name(cls):
        return cls.__name__

    def __init__(self, **kwargs):
        if GlobalParameters.sys_log_ip is not None:
            # If a syslog ip is assigned might as well give some defautls
            # to its related attributes. These can then be overridden via
            # the kwargs received
            snmpobjlogs = ['docsDevEvSyslog.0 IPAddress ' + str(GlobalParameters.sys_log_ip),\
                           'docsDevEvReporting.emergency HexString 0xe0',\
                           'docsDevEvReporting.alert HexString 0xe0',\
                           'docsDevEvReporting.critical HexString 0xe0',\
                           'docsDevEvReporting.error HexString 0xe0',\
                           'docsDevEvReporting.warning HexString 0xe0',\
                           'docsDevEvReporting.notice HexString 0xe0',\
                           'docsDevEvReporting.information HexString 0xe0',\
                           'docsDevEvReporting.debug HexString 0xe0']

            if kwargs == {} or self.SnmpMibObject not in kwargs:
                kwargs[self.SnmpMibObject] = []
            kwargs[self.SnmpMibObject].extend(snmpobjlogs)

        self.GlobalParameters_dict = copy.deepcopy(self.GlobalParameters_defaults)
        update_dict(self.GlobalParameters_dict, **kwargs)

        if self.GlobalParameters_dict[self.SnmpMibObject]:
            self._validate_SnmpMibObject(self.GlobalParameters_dict[self.SnmpMibObject])

    def __str__(self):
        return self.to_str()

    def to_str(self):
        return dict_to_str(self.GlobalParameters_dict)

    def get_dict(self):
        return self.GlobalParameters_dict

class eRouter(object):

    eRouter_dict = OrderedDict()
    InitializationMode    = 'InitializationMode'
    TR69ManagementServer  = 'TR69ManagementServer'
    InitializationModeOverride = 'InitializationModeOverride'
    RATransmissionInterval= 'RATransmissionInterval'
    TopologyModeEncoding  = 'TopologyModeEncoding'
    VendorSpecific        = 'VendorSpecific'

    eRouter_defaults = {\
                         InitializationMode:None,\
                         TR69ManagementServer:None,\
                         InitializationModeOverride:None,\
                         RATransmissionInterval:None,\
                         TopologyModeEncoding:None,\
                         VendorSpecific:None,\
                       }
    @classmethod
    def name(cls):
        return 'eRouter'

    def __init__(self, **kwargs):
        self.eRouter_dict = copy.deepcopy(self.eRouter_defaults)
        update_dict(self.eRouter_dict, **kwargs)

    def __str__(self):
        return self.to_str()

    def to_str(self):
        return dict_to_str(self.eRouter_dict, name=self.__class__.__name__);

    def get_dict(self):
        return self.eRouter_dict

##############################################################################################

class CfgGenerator():
    """This class generates a docsis configuration file"""

    indent = 4
    cm_base_cfg = None
    mta_base_cfg = None

    def __init__(self, file_cfg=None):
        """maybe in the future can take swallow a cfg file"""
        if file_cfg is not None:
            assert 0, "Not yet implemented"

        # For future used (if we want to get defaults from json file)
        #json_name = __file__.split('.')[0] + '.json'
        #default_json = os.path.abspath(os.path.realpath(os.path.dirname(__file__))) + json_name

        self.cm_base_cfg = None
        self.cm_base_cfg = [GlobalParameters(),\
                            DsServiceFlow(),\
                            UsServiceFlow(),\
                            BaselinePrivacy(),\
                            eRouter()]

    def first(self, s):
        '''Return the first element from an ordered collection
           or an arbitrary element from an unordered collection.
           Raise StopIteration if the collection is empty.
        '''
        return next(iter(s))

    def update_cm_base_cfg(self, kwargs):
        while kwargs != {}:
            k = self.first(kwargs)
            for elem in self.cm_base_cfg:
                if elem.name() == k:
                    d = elem.get_dict()
                    d.update(kwargs[k])
                    break
            kwargs.pop(k)

    def _gen_cfg(self, erouter, kwargs):
        er = {eRouter.InitializationMode:erouter}
        eRout = eRouter(**er)

        tmp_cfg = self.cm_base_cfg[:]
        # is this as bad as i think it is?
        for i,elem in enumerate(self.cm_base_cfg):
            if elem.__class__.__name__ == eRout.__class__.__name__:
                tmp_cfg[i] = eRout
        self.update_cm_base_cfg(kwargs)
        self.cm_base_cfg = tmp_cfg[:]
        return tmp_cfg

    def gen_dual_stack_cfg(self, kwargs):
        return self._gen_cfg('3', kwargs)

    def gen_ipv4_cfg(self, kwargs):
        return self._gen_cfg('1', kwargs)

    def gen_ipv6_cfg(self, kwargs):
        return self._gen_cfg('2', kwargs)

    def gen_bridge_cfg(self, kwargs):
        return self._gen_cfg('0', kwargs)

    def generate_cfg(self, fname = None):
        """
        Finalise the config making it ready for use.
        Returns a multiline string
        """
        cfg_file_str = 'Main\n{\n'

        for i in self.cm_base_cfg:
            cfg_file_str += i.to_str()

        cfg_file_str += '}\n'

        '''
        is this really needed? probably not
        if fname:
            # FIX ME: this should have a path too
            if not fname.endswith('.txt'):
                fname += '.txt'
            with open(fname, "w") as text_file:
                text_file.write("{}".format(cfg_file_str))
        '''
        return cfg_file_str


##############################################################################################

if __name__ == '__main__':

    '''
    kwargs = {'DsServiceFlowRef':4}

    dsServiceFlow = DsServiceFlow(**kwargs)
    print(dsServiceFlow)

    usServiceFlow = UsServiceFlow()
    print(usServiceFlow)

    llcPacketClassifier = LLCPacketClassifier()
    print(llcPacketClassifier)

    globalParams = GlobalParameters()
    print(globalParams)

    baselinePrivacy = BaselinePrivacy()
    print(baselinePrivacy)

    gbase_cfg = [GlobalParameters(), DsServiceFlow(**kwargs), UsServiceFlow(), BaselinePrivacy()]

    print("From List:")
    for i in gbase_cfg:
        print(i)
    '''

    print("Using: CfgGenerator")
    kwargs = {'GlobalPrivacyEnable':0}
    c = CfgGenerator()

    GlobalParameters.sys_log_ip = '10.64.38.21'
    newGlobalParameters = copy.deepcopy(GlobalParameters(**kwargs))
    for i,elem in enumerate(c.cm_base_cfg):
        if type(elem) is GlobalParameters:
            c.cm_base_cfg[i] = newGlobalParameters
            break
    c.gen_dual_stack_cfg()

    print('=====================================================================')
    print('Dual stack')
    print(c.generate_cfg('dual-stack-config'))
    print('=====================================================================')

    GlobalParameters.sys_log_ip = None
    c = CfgGenerator()
    c.gen_bridge_cfg()
    print('=====================================================================')
    print('Bridge')
    print(c.generate_cfg('bridge-config'))
    print('=====================================================================')


    '''
    c = CfgGenerator()
    c.gen_ipv4_cfg()
    print('=====================================================================')
    print('IPv4')
    print(c.generate_cfg('ipv4-stack-config'))
    print('=====================================================================')

    c = CfgGenerator()
    c.gen_ipv6_cfg()

    print('=====================================================================')
    print('IPv6')
    print(c.generate_cfg('ipv6-stack-config'))
    print('=====================================================================')

    c = CfgGenerator()
    c.gen_bridge_cfg()

    print('=====================================================================')
    print('bridge')
    print(c.generate_cfg('bridge-config'))
    print('=====================================================================')
    '''
    '''
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
    print('##############################################')
    print(d)
    print('##############################################')
    '''
    print('Done.')
