import copy
import io
import sys
from io import TextIOWrapper, BufferedWriter
from typing import List, Tuple, Set, Dict, Any
from frozendict import frozendict
from gelidum.frozen import make_frozen_class
from gelidum.utils import isbuiltin
from gelidum.typing import OnUpdateType


def freeze(obj: Any, on_update: OnUpdateType = "exception", inplace: bool = False) -> Any:
    if isbuiltin(obj):
        return obj

    class_name = type(obj).__name__
    freeze_func_name = f"__freeze_{class_name}"
    this_module = sys.modules[__name__]
    if hasattr(this_module, freeze_func_name):
        freeze_func = getattr(this_module, freeze_func_name)
        return freeze_func(obj, on_update=on_update, inplace=inplace)

    if isinstance(obj, object):
        return __freeze_object(obj, on_update=on_update, inplace=inplace)

    raise ValueError(f"object of type {obj.__class__} not frozen")


def __freeze_bytearray(obj: bytearray, *args, **kwargs) -> bytes:
    return bytes(obj)


def __freeze_dict(obj: Dict, on_update: OnUpdateType = "exception",
                  inplace: bool = False) -> frozendict:
    return frozendict({key: freeze(value, on_update=on_update, inplace=inplace)
                       for key, value in obj.items()})


def __freeze_list(obj: List, on_update: OnUpdateType = "exception",
                  inplace: bool = False) -> Tuple:
    return tuple(freeze(item, on_update=on_update, inplace=inplace)
                 for item in obj)


def __freeze_tuple(obj: Tuple, on_update: OnUpdateType = "exception",
                   inplace: bool = False) -> Tuple:
    return tuple(freeze(item, on_update=on_update, inplace=inplace)
                 for item in obj)


def __freeze_set(obj: Set, on_update: OnUpdateType = "exception",
                 inplace: bool = False) -> frozenset:
    return frozenset([freeze(item, on_update=on_update, inplace=inplace)
                      for item in obj])


def __freeze_TextIOWrapper(obj: TextIOWrapper, on_update: OnUpdateType = "exception",
                           inplace: bool = False):
    raise io.UnsupportedOperation("Text file handlers can't be frozen")


def __freeze_BufferedWriter(obj: BufferedWriter, on_update: OnUpdateType = "exception",
                            inplace: bool = False):
    raise io.UnsupportedOperation("Binary file handlers can't be frozen")


def __freeze_object(obj: object, on_update: OnUpdateType = "exception",
                    inplace: bool = False) -> object:
    if inplace:
        frozen_obj = obj
    else:
        frozen_obj = copy.deepcopy(obj)
    for attr, value in frozen_obj.__dict__.items():
        attr_value = getattr(frozen_obj, attr)
        setattr(frozen_obj, attr, freeze(attr_value, on_update=on_update, inplace=inplace))
    frozen_obj.__class__ = make_frozen_class(
        klass=obj.__class__,
        attrs=list(obj.__dict__.keys()),
        on_update=on_update
    )
    return frozen_obj
