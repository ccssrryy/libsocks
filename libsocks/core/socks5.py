import socket
import struct

from libsocks.core import constants
from libsocks.core.decorators import gen
from libsocks.core.exceptions import SocksError, socks5_raise_from_code, AuthError
from libsocks.core.impl import BaseState, Request, Response, AddrPort, HandshakeDoneState


class Socks5StartState(BaseState):

    @gen
    def handle(self):
        if self.context.password and self.context.username:
            self.set_state(Socks5UsrPwdSelectState(self.context))
        else:
            self.set_state(Socks5NoAuthSelectState(self.context))
        yield from self.context.handle()


class Socks5NoAuthSelectState(BaseState):

    @gen
    def handle(self):
        req = bytearray()
        req.extend([self.context.ver, 1, constants.METHOD_NO_AUTH])
        yield Request(req)
        ver, method = yield Response(2)
        if method != constants.METHOD_NO_AUTH:
            raise SocksError("no acceptable methods")
        self.set_state(Socks5CmdState(self.context))
        yield from self.context.handle()


class Socks5CmdState(BaseState):

    @gen
    def handle(self):
        req = bytearray()
        req.extend([self.context.ver, self.context.cmd, constants.RSV,
                    self.context.atyp])
        if self.context.atyp == constants.ATYP_DOMAINNAME:
            req.append(len(self.context.addr_bytes))
        req.extend(self.context.addr_bytes)
        req.extend(self.context.port_bytes)
        yield Request(req)
        r = yield Response(3)
        if not r or r[1] != constants.REP_SUCCEED:
            raise socks5_raise_from_code(r[1])
        r = yield Response(1)
        atyp = r[0]
        if atyp == constants.ATYP_IPV4:
            t = yield Response(4)
            addr = socket.inet_ntoa(t)
        elif atyp == constants.ATYP_DOMAINNAME:
            length = yield Response(1)
            addr = yield Response(ord(length))
        elif atyp == constants.ATYP_IPV6:
            t = yield Response(16)
            addr = socket.inet_ntop(socket.AF_INET6, t)
        else:
            raise SocksError("SOCKS5 proxy server sent invalid data")
        t = yield Response(2)
        port = struct.unpack(">H", t)[0]
        self.set_state(HandshakeDoneState(self.context))
        yield AddrPort(addr, port)


class Socks5UsrPwdSelectState(BaseState):

    @gen
    def handle(self):
        """
           +----+------+----------+------+----------+
           |VER | ULEN |  UNAME   | PLEN |  PASSWD  |
           +----+------+----------+------+----------+
           | 1  |  1   | 1 to 255 |  1   | 1 to 255 |
           +----+------+----------+------+----------+
        """
        req = bytearray()
        req.extend([self.context.ver, 2, constants.METHOD_USERNAME_PASSWORD])
        yield Request(req)
        ver, method = yield Response(2)
        if method not in [constants.METHOD_NO_AUTH, constants.METHOD_USERNAME_PASSWORD]:
            raise SocksError("no acceptable methods")
        if method == constants.METHOD_USERNAME_PASSWORD:
            auth_req = bytearray()
            auth_req.append(1)  # VER
            auth_req.append(len(self.context.username))
            auth_req.extend(bytes(self.context.username, "utf8"))
            auth_req.append(len(self.context.password))
            auth_req.extend(bytes(self.context.password, "utf8"))
            yield Request(auth_req)
            _, status = yield Response(2)
            if status != 0:
                raise AuthError()
        self.set_state(Socks5CmdState(self.context))
        yield from self.context.handle()


