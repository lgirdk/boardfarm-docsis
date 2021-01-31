class BftBaseException(Exception):
    pass


class CodeError(BftBaseException):
    pass


class DeviceDoesNotExistError(BftBaseException):
    pass


class BootFail(BftBaseException):
    pass


class NoTFTPServer(BftBaseException):
    pass


class BftEnvExcKeyError(BftBaseException):
    pass


class BftEnvMismatch(BftBaseException):
    pass


class BftSysExit(BftBaseException):
    pass
