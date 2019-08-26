from libsocks.core.impl import BaseContext, Request, Response
from libsocks.utils import async_send_all, async_recv_all

__all__ = ("async_process",)

async def async_process(context, recv_func, send_func):
    # type: (BaseContext, callable, callable) -> None

    """

    :param context: socks context
    :param recv_func: async recv callback, called by a length param, return bytes actually received
    :param send_func: async send callback, called by a data param, return bytes sent
    :return: None
    """

    handler = context.handle()
    async def _process(action):
        if isinstance(action, Request):
            await async_send_all(send_func, action.msg)
        elif isinstance(action, Response):
            l = action.length
            d = await async_recv_all(recv_func,l)
            t = handler.send(d)
            if t:
                await _process(t)
    for h in handler:
        await _process(h)

