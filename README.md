# libsocks

a socks5/socks/http proxy client module, easy to work with your code

# Feature

* socks4 `CONNECT` command support

* socks5 `CONNECT` command support

* Username/Password Authentication support for SOCKS V5

* TCP supported

* work with sync/asyncio

# Requirements

* Python3.5+ support

# Usage

## blocking socket example

```
import socket

from libsocks import constants
from libsocks import Socks5Context
from libsocks import sync_process


def test_socks5():
    proxy_ip = "127.0.0.1"
    proxy_port = 1080
    dst_addr = "www.test.com"
    dst_port = 80
    s = socket.socket()

    # connect to socks5 server
    s.connect((proxy_ip, proxy_port))

    # handshake with socks5 server and tell it the dst_addr and dst_port
    context = Socks5Context(dst_addr, dst_port, constants.ATYP_DOMAINNAME,
                            username="user", password="password")
    # or context = Socks4Context(dst_addr, dst_port, constants.ATYP_DOMAINNAME)
    sync_process(context, s.recv, s.send)

    # now, all data on s will be sent to (dst_addr, dst_port) via socks5 server
    s.send(b"GET / HTTP/1.1\r\n\r\n")
    print(s.recv(1024))


test_socks5()
```

## asyncio example

```
import socket
import asyncio

from libsocks import async_process
from libsocks import constants
from libsocks import Socks5Context


async def test_socks5(loop):
    proxy_ip = "127.0.0.1"
    proxy_port = 1080
    dst_addr = "www.test.com"
    dst_port = 80
    s = socket.socket()
    s.setblocking(False)

    async def async_recv(nbytes):
        return await loop.sock_recv(s, nbytes)

    async def async_send(data):
        await loop.sock_sendall(s, data)
        return len(data)

    # connect to socks5 server
    await loop.sock_connect(s, (proxy_ip, proxy_port))

    # handshake with socks5 server and tell it the dst_addr and dst_port
    context = Socks5Context(dst_addr, dst_port, constants.ATYP_DOMAINNAME,
                            username="user", password="password")
    await async_process(context, async_recv, async_send)

    # now, all data on s will be sent to (dst_addr, dst_port) via socks5 server
    await loop.sock_sendall(s, b"GET / HTTP/1.1\r\n\r\n")
    print(await loop.sock_recv(s, 1024))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_socks5(loop))
```

# License

BSD