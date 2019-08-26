import unittest
import asyncio

from libsocks.context import Socks5Context, Socks4Context
from libsocks.helpers.asyncio import async_process
from tests import socks_data


class TestSocks(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()

    def _async_process(self, context, resp):
        req_data = []
        async def async_recv(l):
            return next(resp)
        async def async_send(d):
            req_data.append(d)
            return len(d)
        task = async_process(context, async_recv, async_send)
        self.loop.run_until_complete(task)

    def test_socks4_async_process(self):
        context = Socks4Context(socks_data.proxy_ip, socks_data.proxy_port)
        resp = iter(socks_data.socks4_resp)
        self._async_process(context, resp)

    def test_socks4_async_process_uid(self):
        context = Socks4Context(socks_data.proxy_ip, socks_data.proxy_port, username="test")
        resp = iter(socks_data.socks4_resp)
        self._async_process(context, resp)

    def test_socks5_async_process(self):
        context = Socks5Context(socks_data.proxy_ip, socks_data.proxy_port)
        resp = iter(socks_data.socks5_no_auth_resp)
        self._async_process(context, resp)

    def tearDown(self):
        self.loop.stop()
