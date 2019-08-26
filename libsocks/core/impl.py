import socket
from abc import abstractmethod, ABCMeta
from inspect import isgenerator

import struct

from libsocks.core.decorators import gen
from libsocks.core import constants
from libsocks.core.exceptions import SocksError


class Msg():
    pass


class Request(Msg):
    def __init__(self, msg):
        # type: (bytes or bytearray) -> None
        self.msg = msg


class Response(Msg):
    def __init__(self, length):
        # type: (int) -> None
        self.length = length


class AddrPort(Msg):

    def __init__(self, addr, port):
        self.addr = addr
        self.port = port


class Actions(metaclass=ABCMeta):
    @abstractmethod
    def handle(self):
        pass

    @abstractmethod
    def set_state(self, state):
        pass


class BaseContext(Actions):

    def __init__(self, dst_addr, dst_port, ver=5, cmd=constants.CMD_CONNECT,
                 atyp=constants.ATYP_IPV4, username=None, password=None):
        # type: (str, int, int, int, int, str, str) -> None

        self.dst_addr = dst_addr
        self.dst_port = dst_port
        self.atyp = atyp
        self.ver = ver
        self.username = username
        self.password = password
        self.cmd = cmd
        self._state = None
        if atyp == constants.ATYP_DOMAINNAME:
            self.addr_bytes = bytes(self.dst_addr, "utf8")
        else:
            self.addr_bytes = socket.inet_pton(socket.AF_INET if atyp == constants.ATYP_IPV4 else socket.AF_INET6,
                                               self.dst_addr)  # type: bytes
        self.port_bytes = struct.pack(">H", dst_port)  # type: bytes

    @gen
    def handle(self):
        if not self._state:
            raise SocksError("no state set!")
        yield from self._state.handle()

    def set_state(self, state):
        self._state = state

    @property
    def state(self):
        return self._state


class BaseState(Actions):
    def __init__(self, context):
        # type: (BaseContext) -> None
        self.context = context

    def set_state(self, state):
        self.context.set_state(state)


class StartState(BaseState):
    @gen
    def handle(self):
        pass


class HandshakeDoneState(BaseState):

    @gen
    def handle(self):
        pass
