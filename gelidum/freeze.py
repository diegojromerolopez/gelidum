import io
import sys
import warnings
from typing import List, Set, Dict, Any, Optional, Union, Tuple

from gelidum.dependencies import NUMPY_INSTALLED
from gelidum.collections import frozendict, frozenlist, frozenzet
from gelidum.exceptions import FrozenException
from gelidum.frozen import make_frozen_class, FrozenBase
from gelidum.frozen.frozen_class_creator import make_unique_class
from gelidum.typing import OnFreezeFuncType, OnUpdateFuncType, T, FrozenType, FrozenList
from gelidum.utils import isbuiltin
from gelidum.on_freeze import on_freeze_func_creator, OnFreezeCopier

if NUMPY_INSTALLED:
    from gelidum.collections import frozenndarray

NpArrayType = Any


def freeze(
    obj: T,
    on_update: Union[str, OnUpdateFuncType] = "exception",
    on_freeze: Union[str, OnFreezeFuncType] = "copy",
    save_original_on_copy: bool = False,
    inplace: Optional[bool] = None,
) -> FrozenType:

    # inplace argument will be removed from freeze in the next major version (0.6.0)
    if isinstance(inplace, bool):
        warnings.warn(
            DeprecationWarning("Use of inplace is deprecated and will be removed in next major version (0.6.0)")
        )

        if hasattr(obj.__class__, "__slots__") and inplace:
            raise FrozenException("Objects of classes with __slots__ cannot be frozen inplace")

        on_freeze_func: OnFreezeFuncType = on_freeze_func_creator(on_freeze="inplace" if inplace else "copy")

    else:
        if hasattr(obj.__class__, "__slots__") and on_freeze == "inplace":
            raise FrozenException("Objects of classes with __slots__ cannot be frozen inplace")

        on_freeze_func: OnFreezeFuncType = on_freeze_func_creator(on_freeze=on_freeze)

    on_update_func: OnUpdateFuncType = __on_update_func(on_update=on_update)

    return __freeze(
        obj=obj, on_update=on_update_func, on_freeze=on_freeze_func, save_original_on_copy=save_original_on_copy
    )


def __freeze(
    obj: Any, on_update: OnUpdateFuncType, on_freeze: OnFreezeFuncType, save_original_on_copy: bool = False
) -> Any:

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

    if NUMPY_INSTALLED:
        import numpy as np

        if isinstance(obj, np.ndarray):
            return __freeze_ndarray(obj, on_update=on_update, on_freeze=on_freeze)

    if isinstance(obj, object):
        return __freeze_object(
            obj, on_update=on_update, on_freeze=on_freeze, save_original_on_copy=save_original_on_copy
        )

    # Actually, this code is unreachable
    raise ValueError(f"object of type {obj.__class__} not frozen")  # pragma: no cover


def __freeze_bytearray(obj: bytearray, *args, **kwargs) -> bytes:  # noqa
    return bytes(obj)


def __freeze_ndarray(obj: NpArrayType, on_update: OnUpdateFuncType, on_freeze: OnFreezeFuncType) -> FrozenList:
    def freeze_func(item: Any) -> FrozenType:
        return freeze(item, on_update=on_update, on_freeze=on_freeze)

    return frozenndarray(obj, freeze_func=freeze_func)


def __freeze_dict(obj: Dict, on_update: OnUpdateFuncType, on_freeze: OnFreezeFuncType) -> frozendict:
    def freeze_func(item: Any) -> FrozenType:
        return freeze(item, on_update=on_update, on_freeze=on_freeze)

    return frozendict(obj, freeze_func=freeze_func)


def __freeze_list(obj: List, on_update: OnUpdateFuncType, on_freeze: OnFreezeFuncType) -> FrozenList:
    def freeze_func(item: Any) -> FrozenType:
        return freeze(item, on_update=on_update, on_freeze=on_freeze)

    return frozenlist(obj, freeze_func=freeze_func)


def __freeze_tuple(obj: Tuple, on_update: OnUpdateFuncType, on_freeze: OnFreezeFuncType) -> Tuple:
    return tuple(freeze(item, on_update=on_update, on_freeze=on_freeze) for item in obj)


def __freeze_set(obj: Set, on_update: OnUpdateFuncType, on_freeze: OnFreezeFuncType) -> frozenzet:
    def freeze_func(item: Any) -> FrozenType:
        return freeze(item, on_update=on_update, on_freeze=on_freeze)

    return frozenzet(obj, freeze_func=freeze_func)


def __freeze_TextIOWrapper(*args, **kwargs) -> None:  # noqa
    raise io.UnsupportedOperation("Text file handlers can't be frozen")


def __freeze_BufferedWriter(*args, **kwargs) -> None:  # noqa
    raise io.UnsupportedOperation("Binary file handlers can't be frozen")


def __freeze_object(
    obj: object, on_update: OnUpdateFuncType, on_freeze: OnFreezeFuncType, save_original_on_copy: bool = False
) -> FrozenBase:

    # If the object has a class with __slots__ a unique class is created whose class attributes
    # are the object attributes that we want to freeze
    if hasattr(obj.__class__, "__slots__"):
        attrs = tuple(obj.__class__.__slots__)
        on_freeze: OnFreezeFuncType = on_freeze_func_creator(on_freeze="copy")
        frozen_class = make_unique_class(
            klass=obj.__class__,
            attrs={
                attr: freeze(getattr(obj, attr), on_update=on_update, on_freeze=on_freeze, save_original_on_copy=False)
                for attr in attrs
            },
            on_update=on_update,
        )
        return frozen_class()
    else:
        attrs = tuple(obj.__dict__.keys())

        frozen_obj = on_freeze(obj)
        for attr in attrs:
            attr_value = getattr(frozen_obj, attr)
            setattr(
                frozen_obj,
                attr,
                freeze(attr_value, on_update=on_update, on_freeze=on_freeze, save_original_on_copy=False),
            )

        # Only when the frozen method is copying the objects we can get the original object
        # save_original_on_copy is used to save only the original object (the first-level object whose
        # save_original_on_copy is set to True). Descendant attributes are not saved in other original_obj attributes,
        # i.e. there is no copy of hierarchy, only the first-level object is saved.
        if save_original_on_copy and on_freeze.__class__ == OnFreezeCopier:
            setattr(frozen_obj, "original_obj", obj)

        frozen_class = make_frozen_class(klass=obj.__class__, attrs=attrs, on_update=on_update)
        frozen_obj.__class__ = frozen_class
        return frozen_obj


def __on_update_exception(frozen_obj: FrozenBase, message: str, *args, **kwargs) -> None:  # noqa
    raise FrozenException(message)


def __on_update_warning(frozen_obj: FrozenBase, message: str, *args, **kwargs) -> None:  # noqa
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
