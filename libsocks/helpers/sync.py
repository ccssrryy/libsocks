from libsocks.core.impl import BaseContext, Request, Response
from libsocks.utils import send_all, recv_all

__all__ = ("sync_process",)


def sync_process(context, recv_func, send_func):
    # type: (BaseContext, callable, callable) -> None

    """

    :param context: socks context
    :param recv_func: sync recv callback, called by a length param, return bytes actually received
    :param send_func: sync send callback, called by a data param, return bytes sent
    :return: None
    """

    handler = context.handle()

    def _process(action):
        if isinstance(action, Request):
            send_all(send_func, action.msg)
        elif isinstance(action, Response):
            l = action.length
            d = recv_all(recv_func, l)
            t = handler.send(d)
            if t:
                _process(t)
    for h in handler:
        _process(h)
