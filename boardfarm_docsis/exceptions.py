from boardfarm.exceptions import BftBaseException

class BftDocsisBaseException(BftBaseException):
    '''Base Docsis exception'''

class CfgEncodeFailed(BftBaseException):
    '''Encoding of Cfg file failed'''

class CMCfgEncodeFailed(CfgEncodeFailed):
    '''Exception that occurs when MTA encoding fails'''

class MTACfgEncodeFailed(CfgEncodeFailed):
    '''Exception that occurs when MTA encoding fails'''

class CfgUnknownType(CfgEncodeFailed):
    '''Unknown type of cfg'''

class VoiceSetupConfigureFailure(BftBaseException):
    '''Exception that occurs when Voice setup is not configured'''
