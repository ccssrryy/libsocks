import unittest

from libsocks.context import Socks5Context, Socks4Context
from libsocks.core.impl import Request, Response, HandshakeDoneState
from tests import socks_data


class TestSocks(unittest.TestCase):

    def test_socks5_handshake(self):
        req = iter(socks_data.socks5_no_auth_resp)
        context = Socks5Context(socks_data.proxy_ip, socks_data.proxy_port)
        self._test_handshake(context, req)

    def test_socks4_handshake(self):
        req = iter(socks_data.socks4_resp)
        context = Socks4Context(socks_data.proxy_ip, socks_data.proxy_port)
        self._test_handshake(context, req)

    def _test_handshake(self, context, req):
        h = context.handle()
        for action in h:
            self._process(h, req, action)
        self.assertIsInstance(context.state, HandshakeDoneState)

    def _process(self, handle, req, action):
        if isinstance(action, Request):
            pass
        elif isinstance(action, Response):
            l = action.length
            d = next(req)
            t = handle.send(d)
            if t:
                self._process(handle, req, t)
