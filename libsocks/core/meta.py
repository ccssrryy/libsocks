from abc import ABCMeta


class GenABCMeta(ABCMeta):

    def __new__(mcls, name, bases, namespace, **kwargs):
        for func_name, func in namespace.items():
            pass

        cls = super().__new__(mcls, name, bases, namespace, **kwargs)
        return cls
