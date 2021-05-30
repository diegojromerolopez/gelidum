import copy
from frozendict import frozendict

from gelidum.frozen import make_frozen_class
from gelidum.utils import isbuiltin


def freeze(obj: object, inplace: bool = False) -> object:
    if isbuiltin(obj):
        return obj
    if isinstance(obj, bytearray):
        return bytes(obj)
    if isinstance(obj, dict):
        return frozendict({key: freeze(value, inplace=inplace)
                           for key, value in obj.items()})
    if isinstance(obj, list) or isinstance(obj, tuple):
        return tuple(freeze(item, inplace=inplace) for item in obj)
    if isinstance(obj, set):
        return frozenset([freeze(item, inplace=inplace)
                          for item in obj])
    if isinstance(obj, object):
        if inplace:
            frozen_obj = obj
        else:
            frozen_obj = copy.deepcopy(obj)
        for attr, value in frozen_obj.__dict__.items():
            attr_value = getattr(frozen_obj, attr)
            setattr(frozen_obj, attr, freeze(attr_value, inplace=inplace))
        frozen_obj.__class__ = make_frozen_class(klass=obj.__class__, attrs=list(obj.__dict__.keys()))
        return frozen_obj

    raise ValueError(f"object of type {obj.__class__} not frozen")
