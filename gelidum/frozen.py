import sys
import threading
import warnings
from typing import Type, List, cast, Dict
from gelidum.exceptions import FrozenException
from gelidum.typing import OnUpdateType, GelidumOnUpdateType


class FrozenBase(object):
    @classmethod
    def __gelidum_on_update(cls, *args, **kwargs):
        raise NotImplementedError("Implement in derived class")

    def __setattr__(self, key, value):
        self.__gelidum_on_update(
            message=f"Can't assign '{key}' on immutable instance",
            key=key, value=value
        )

    def __set__(self, *args, **kwargs):
        self.__gelidum_on_update(
            message="Can't assign setter on immutable instance",
            *args, **kwargs
        )

    def __delattr__(self, name):
        self.__gelidum_on_update(
            message=f"Can't delete attribute '{name}' on immutable instance",
            name=name
        )

    def __setitem__(self, key, value):
        self.__gelidum_on_update(
            message="Can't set key on immutable instance",
            key=key, value=value
        )

    def __delitem__(self, key):
        self.__gelidum_on_update(
            message="Can't delete key on immutable instance",
            key=key)

    def __reversed__(self):
        self.__gelidum_on_update(message="Can't reverse on immutable instance")


__FROZEN_CLASSES: Dict[str, Type[FrozenBase]] = dict()
__FROZEN_CLASSES_LOCK = threading.Lock()


def __store_frozen_class(klass: Type[object], frozen_class: Type[FrozenBase]) -> None:
    """
    Add a frozen class to this module.
    Required for pickle serialization as only objects of non-dynamic
    classes are allowed.
    This method is thread-safe.
    :param frozen_class: a class that inherits from FrozenBase.
    """
    with __FROZEN_CLASSES_LOCK:
        klass_key = f"{klass.__module__}.{klass.__qualname__}"
        __FROZEN_CLASSES[klass_key] = frozen_class
        # Required for pickling frozen objects (only classes defined in actual
        # modules can have their objects pickled)
        setattr(sys.modules[__name__], frozen_class.__name__, frozen_class)


def clear_frozen_classes() -> None:
    with __FROZEN_CLASSES_LOCK:
        __FROZEN_CLASSES.clear()


def __create_frozen_class(klass: Type[object], attrs: List[str],
                          on_update_func: GelidumOnUpdateType) -> Type[FrozenBase]:
    camel_case_module = klass.__module__.title().replace(".", "").replace("_", "")
    frozen_class_name = f"Frozen{klass.__name__}From{camel_case_module}"
    frozen_class: Type[FrozenBase] = cast(
        Type[FrozenBase],
        type(
            frozen_class_name,
            (klass, FrozenBase),
            {
                "__slots__": tuple(),
                **{
                    'get_gelidum_hot_class_name': lambda _: klass.__name__,
                    'get_gelidum_hot_class_module': lambda _: klass.__module__,
                    '_FrozenBase__gelidum_on_update':
                        lambda _self, *args, **kwargs: on_update_func(*args, **kwargs),
                    **{attr: None for attr in attrs}
                }
            }
        )
    )
    __store_frozen_class(klass=klass, frozen_class=frozen_class)
    return frozen_class


def __on_update_exception(message: str, *args, **kwargs) -> None:
    raise FrozenException(message)


def __on_update_warning(message: str, *args, **kwargs) -> None:
    warnings.warn(message)


def __on_update_func(on_update: OnUpdateType) -> GelidumOnUpdateType:
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
                f"only 'exception', 'warning', and 'nothing' are valid options"
                f"if passed a string."
            )

    elif callable(on_update):
        return on_update

    else:
        raise AttributeError(
            f"Invalid value for on_update parameter, '{on_update}' found, "
            f"only 'exception', 'warning', 'nothing' or a function are valid options"
        )


def make_frozen_class(klass: Type[object], attrs: List[str],
                      on_update: OnUpdateType) -> Type[FrozenBase]:
    klass_key = f"{klass.__module__}.{klass.__qualname__}"
    with __FROZEN_CLASSES_LOCK:
        frozen_class = __FROZEN_CLASSES.get(klass_key)

    if not frozen_class:
        frozen_class = __create_frozen_class(
            klass=klass, attrs=attrs,
            on_update_func=__on_update_func(on_update=on_update)
        )

    return frozen_class

