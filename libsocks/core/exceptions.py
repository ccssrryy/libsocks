from libsocks.core import constants


class BaseSocksError(Exception):
    code = -1
    msg = "socks error"

    def __init__(self, code=None, msg=None):
        super().__init__()
        if code is None:
            self.code = code
            self.msg = msg

    def __str__(self):
        code = self.code if self.code is not None else '???'
        return '%s: %s' % (code, self.msg)

    def __repr__(self):
        code = self.code if self.code is not None else '???'
        return "<%s '%s: %s'>" % (self.__class__.__name__, code, self.msg)


class SocksError(BaseSocksError):
    def __init__(self, msg):
        super().__init__()
        self.msg = msg


class ServerFailError(BaseSocksError):
    code = constants.REP_FAILURE
    msg = "SOCKS server failure"


class NotAllowedError(BaseSocksError):
    code = constants.REP_NOT_ALLOWED
    msg = "connection not allowed by ruleset"


class NetworkUnreachableError(BaseSocksError):
    code = constants.REP_NETWORK_UNREACHABLE
    msg = "Network unreachable"


class HostUnreachableError(BaseSocksError):
    code = constants.REP_HOST_UNREACHABLE
    msg = "Host unreachable"


class ConnRefusedError(BaseSocksError):
    code = constants.REP_CONNECTION_REFUSED
    msg = "Connection refused"


class TtlExpireError(BaseSocksError):
    code = constants.REP_TTL_EXPIRED
    msg = "TTL expired"


class CmdNotSupportError(BaseSocksError):
    code = constants.REP_CMD_NOT_SUPPORT
    msg = "Command not supported"


class AddrNotSupportError(BaseSocksError):
    code = constants.REP_ADDR_NOT_SUPPORT
    msg = "Address type not supported"


class UnkownError(BaseSocksError):
    pass


class AuthError(BaseSocksError):
    msg = "auth fail"

code_map = {
    constants.REP_FAILURE: ServerFailError(),
    constants.REP_NOT_ALLOWED: NotAllowedError(),
    constants.REP_NETWORK_UNREACHABLE: NetworkUnreachableError(),
    constants.REP_HOST_UNREACHABLE: HostUnreachableError(),
    constants.REP_CONNECTION_REFUSED: ConnRefusedError(),
    constants.REP_TTL_EXPIRED:TtlExpireError(),
    constants.REP_CMD_NOT_SUPPORT: CmdNotSupportError(),
    constants.REP_ADDR_NOT_SUPPORT: AddrNotSupportError(),
}


def socks5_raise_from_code(code):
    raise code_map.get(code, UnkownError())


class Socks4RejectError(BaseSocksError):
    code = constants.CD_REJECTED
    msg = "request rejected or failed"


class Socks4ConnectError(BaseSocksError):
    code = constants.CD_CANNOT_CONNECT
    msg = "request rejected becasue SOCKS server " \
          "cannot connect to identd on the client"


class Socks4DiffUidsError(BaseSocksError):
    code = constants.CD_DIFF_UIDS
    msg = "request rejected because the client " \
          "program and identd report different user-ids."

socks4_code_map = {
    constants.CD_REJECTED: Socks4RejectError(),
    constants.CD_CANNOT_CONNECT: Socks4ConnectError(),
    constants.CD_DIFF_UIDS: Socks4DiffUidsError()
}


def socks4_raise_from_code(code):
    raise socks4_code_map.get(code, UnkownError())
