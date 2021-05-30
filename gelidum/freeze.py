import copy
from typing import List, Tuple, Set, Dict

from frozendict import frozendict

from gelidum.frozen import make_frozen_class
from gelidum.utils import isbuiltin


def freeze(obj: object, inplace: bool = False) -> object:
    if isbuiltin(obj):
        return obj

    if isinstance(obj, bytearray):
        return __freeze_bytes(obj, inplace=inplace)

    if isinstance(obj, dict):
        return __freeze_dict(obj, inplace=inplace)

    if isinstance(obj, list):
        return __freeze_list(obj, inplace=inplace)

    if isinstance(obj, tuple):
        return __freeze_tuple(obj, inplace=inplace)

    if isinstance(obj, set):
        return __freeze_set(obj, inplace=inplace)

    if isinstance(obj, object):
        return __freeze_object(obj, inplace=inplace)

    raise ValueError(f"object of type {obj.__class__} not frozen")


def __freeze_bytes(obj: bytearray, inplace: bool = False) -> bytes:
    return bytes(obj)


def __freeze_dict(obj: Dict, inplace: bool = False) -> frozendict:
    return frozendict({key: freeze(value, inplace=inplace)
                       for key, value in obj.items()})


def __freeze_list(obj: List, inplace: bool = False) -> Tuple:
    return tuple(freeze(item, inplace=inplace) for item in obj)


def __freeze_tuple(obj: Tuple, inplace: bool = False) -> Tuple:
    return tuple(freeze(item, inplace=inplace) for item in obj)


def __freeze_set(obj: Set, inplace: bool = False) -> frozenset:
    return frozenset([freeze(item, inplace=inplace) for item in obj])


def __freeze_object(obj: object, inplace: bool = False) -> object:
    if inplace:
        frozen_obj = obj
    else:
        frozen_obj = copy.deepcopy(obj)
    for attr, value in frozen_obj.__dict__.items():
        attr_value = getattr(frozen_obj, attr)
        setattr(frozen_obj, attr, freeze(attr_value, inplace=inplace))
    frozen_obj.__class__ = make_frozen_class(klass=obj.__class__, attrs=list(obj.__dict__.keys()))
    return frozen_obj
