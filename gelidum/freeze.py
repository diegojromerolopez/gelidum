import copy
import io
import sys
import warnings
from typing import (
    List, Tuple, Set, Dict, Any,
    Optional, Union, TypeVar
)
from frozendict import frozendict
from gelidum.exceptions import FrozenException
from gelidum.frozen import make_frozen_class, FrozenBase
from gelidum.utils import isbuiltin
from gelidum.typing import OnFreezeFuncType, OnUpdateFuncType

T = TypeVar('T')

_FrozenType = Optional[
    Union[
        bool, int, float, bytes, complex, str,
        bytes, frozendict, tuple, frozenset,
        FrozenBase, T
    ]
]


def freeze(
        obj: T,
        on_update: Union[str, OnUpdateFuncType] = "exception",
        on_freeze: Union[str, OnFreezeFuncType] = "copy",
        inplace: Optional[bool] = None,
        ) -> _FrozenType:

    # inplace argument will be removed from freeze in the next major version (0.5.0)
    if isinstance(inplace, bool):
        warnings.warn(
            DeprecationWarning(
                "Use of inplace is deprecated and will be removed in next major version (0.5.0)"
            )
        )
        if inplace:
            on_freeze_func: OnFreezeFuncType = __on_freeze_func(on_freeze="inplace")
        else:
            on_freeze_func: OnFreezeFuncType = __on_freeze_func(on_freeze="copy")

    else:
        on_freeze_func: OnFreezeFuncType = __on_freeze_func(on_freeze=on_freeze)

    on_update_func: OnUpdateFuncType = __on_update_func(on_update=on_update)

    return __freeze(obj=obj, on_update=on_update_func, on_freeze=on_freeze_func)


def __freeze(obj: Any, on_update: OnUpdateFuncType,
             on_freeze: OnFreezeFuncType) -> Any:

    if isbuiltin(obj):
        return obj

    if isinstance(obj, FrozenBase):
        return obj

    class_name = type(obj).__name__
    freeze_func_name = f"__freeze_{class_name}"
    this_module = sys.modules[__name__]
    if hasattr(this_module, freeze_func_name):
        freeze_func = getattr(this_module, freeze_func_name)
        return freeze_func(obj, on_update=on_update, on_freeze=on_freeze)

    if isinstance(obj, object):
        return __freeze_object(obj, on_update=on_update, on_freeze=on_freeze)

    # Actually, this code is unreachable
    raise ValueError(f"object of type {obj.__class__} not frozen")  # pragma: no cover


def __freeze_bytearray(obj: bytearray, *args, **kwargs) -> bytes:  # noqa
    return bytes(obj)


def __freeze_dict(obj: Dict, on_update: OnUpdateFuncType,
                  on_freeze: OnFreezeFuncType) -> frozendict:
    return frozendict({key: __freeze(value, on_update=on_update, on_freeze=on_freeze)
                       for key, value in obj.items()})


def __freeze_list(obj: List, on_update: OnUpdateFuncType,
                  on_freeze: OnFreezeFuncType) -> Tuple:
    return tuple(__freeze(item, on_update=on_update, on_freeze=on_freeze)
                 for item in obj)


def __freeze_tuple(obj: Tuple, on_update: OnUpdateFuncType,
                   on_freeze: OnFreezeFuncType) -> Tuple:
    return tuple(freeze(item, on_update=on_update, on_freeze=on_freeze)
                 for item in obj)


def __freeze_set(obj: Set, on_update: OnUpdateFuncType,
                 on_freeze: OnFreezeFuncType) -> frozenset:
    return frozenset([freeze(item, on_update=on_update, on_freeze=on_freeze)
                      for item in obj])


def __freeze_TextIOWrapper(*args, **kwargs) -> None:  # noqa
    raise io.UnsupportedOperation("Text file handlers can't be frozen")


def __freeze_BufferedWriter(*args, **kwargs) -> None:  # noqa
    raise io.UnsupportedOperation("Binary file handlers can't be frozen")


def __freeze_object(obj: object, on_update: OnUpdateFuncType,
                    on_freeze: OnFreezeFuncType) -> FrozenBase:

    frozen_obj = on_freeze(obj)
    for attr, value in frozen_obj.__dict__.items():
        attr_value = getattr(frozen_obj, attr)
        setattr(frozen_obj, attr, freeze(attr_value, on_update=on_update, on_freeze=on_freeze))
    frozen_obj.__class__ = make_frozen_class(
        klass=obj.__class__,
        attrs=list(obj.__dict__.keys()),
        on_update=on_update
    )
    return frozen_obj


def __on_freeze_func(on_freeze: Union[str, OnFreezeFuncType]) -> OnFreezeFuncType:
    if isinstance(on_freeze, str):
        if on_freeze == "copy":
            return lambda obj: copy.deepcopy(obj)
        elif on_freeze == "inplace":
            return lambda obj: obj
        else:
            raise AttributeError(
                f"Invalid value for on_freeze parameter, '{on_freeze}' found, "
                f"only 'copy' and 'inplace' are valid options if passed a string"
            )

    elif callable(on_freeze):
        return on_freeze

    else:
        raise AttributeError(
            f"Invalid value for on_freeze parameter, '{on_freeze}' found, "
            f"only 'copy', 'inplace' or a function are valid options"
        )


def __on_update_exception(
        frozen_obj: FrozenBase, message: str, *args, **kwargs  # noqa
) -> None:
    raise FrozenException(message)


def __on_update_warning(
        frozen_obj: FrozenBase, message: str, *args, **kwargs  # noqa
) -> None:
    warnings.warn(message)


def __on_update_func(on_update: OnUpdateFuncType) -> OnUpdateFuncType:
    if isinstance(on_update, str):
        if on_update == "exception":
            return __on_update_exception
        elif on_update == "warning":
            return __on_update_warning
        elif on_update == "nothing":
            return lambda message, *args, **kwargs: None
        else:
            raise AttributeError(
                f"Invalid value for on_update parameter, '{on_update}' found, "
                f"only 'exception', 'warning', and 'nothing' are valid options "
                f"if passed a string"
            )

    elif callable(on_update):
        return on_update

    else:
        raise AttributeError(
            f"Invalid value for on_update parameter, '{on_update}' found, "
            f"only 'exception', 'warning', 'nothing' or a function are "
            f"valid options"
        )
