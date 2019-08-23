from libsocks.core import constants
from libsocks.core.impl import BaseContext
from libsocks.core.socks4 import Socks4StartState
from libsocks.core.socks5 import Socks5StartState


class Socks5Context(BaseContext):

    def __init__(self, dst_addr, dst_port, atyp=constants.ATYP_IPV4,
                 ver=5, username=None, password=None):
        super().__init__(dst_addr, dst_port, atyp=atyp,
                         ver=ver, username=username, password=password)
        self.set_state(Socks5StartState(self))


class Socks4Context(BaseContext):

    def __init__(self, dst_addr, dst_port, username=None, atyp=constants.ATYP_IPV4):
        super().__init__(dst_addr, dst_port, username=username, atyp=atyp, ver=constants.VER4)
        self.set_state(Socks4StartState(self))
