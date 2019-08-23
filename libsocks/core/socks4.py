import socket
import struct

from libsocks.core import constants
from libsocks.core.decorators import gen
from libsocks.core.exceptions import socks4_raise_from_code
from libsocks.core.impl import BaseState, Request, Response, HandshakeDoneState


class Socks4StartState(BaseState):

    @gen
    def handle(self):
        self.set_state(Socks4CmdState(self.context))
        yield from self.context.handle()


class Socks4CmdState(BaseState):

    @gen
    def handle(self):
        msg = bytearray()
        msg.extend([4, self.context.ver])
        msg.extend(self.context.port_bytes)
        msg.extend(self.context.addr_bytes)
        if self.context.username:
            msg.extend(bytes(self.context.username, "utf8"))
        msg.append(0)
        yield Request(msg)
        resp = yield Response(8)
        if resp[1] != constants.CD_GRANTED:
            socks4_raise_from_code(resp[1])
        self.set_state(HandshakeDoneState(self.context))
        yield from self.context.handle()