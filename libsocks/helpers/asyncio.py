from libsocks.core.impl import BaseContext, Request, Response

__all__ = ("async_process",)

async def async_process(context, recv_func, send_func):
    # type: (BaseContext, callable, callable) -> None

    handler = context.handle()
    async def _process(action):
        if isinstance(action, Request):
            await send_func(action.msg)
        elif isinstance(action, Response):
            l = action.length
            d = await recv_func(l)
            t = handler.send(d)
            if t:
                await _process(t)
    for h in handler:
        await _process(h)

