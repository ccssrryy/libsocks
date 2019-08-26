
def send_all(send_func, data, *args, **kwargs):
    # type: (callable, bytes or bytearray) -> int
    sent = 0
    while sent < len(data):
        sent += send_func(data[sent:], *args, **kwargs)
    return sent

def recv_all(recv_func, nbytes, *args, **kwargs):
    # type: (callable, int) -> bytes
    data = bytearray()
    while len(data) < nbytes:
        d = recv_func(nbytes - len(data), *args, **kwargs)
        if not d:
            break
        data.extend(d)
    return bytes(data)

async def async_send_all(send_func, data, *args, **kwargs):
    # type: (callable, bytes or bytearray) -> int
    sent = 0
    while sent < len(data):
        sent += await send_func(data[sent:], *args, **kwargs)
    return sent


async def async_recv_all(recv_func, nbytes, *args, **kwargs):
    # type: (callable, int) -> bytes
    data = bytearray()
    while len(data) < nbytes:
        d = await recv_func(nbytes - len(data), *args, **kwargs)
        if not d:
            break
        data.extend(d)
    return bytes(data)
