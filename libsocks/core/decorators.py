import functools, inspect


def gen(f):
    @functools.wraps(f)
    def _wrapper(*args, **kwargs):
        res = f(*args, **kwargs)
        if inspect.isgenerator(res):
            yield from res
        else:
            yield res
    return _wrapper
