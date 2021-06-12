import sys
import threading
from typing import Type, List, cast, Dict
from gelidum.exceptions import FrozenException


class FrozenBase(object):
    @property
    def gelidum_hot_class_module(self):
        raise NotImplementedError("Implement in derived class")

    def __setattr__(self, key, value):
        raise FrozenException(f"Can't assign '{key}' on immutable instance")

    def __set__(self, *args, **kwargs):
        raise FrozenException("Can't assign setter on immutable instance")

    def __delattr__(self, name):
        raise FrozenException(
            f"Can't delete attribute '{name}' on immutable instance")

    def __setitem__(self, key, value):
        raise FrozenException("Can't set key on immutable instance")

    def __delitem__(self, key):
        raise FrozenException("Can't delete key on immutable instance")

    def __reversed__(self):
        raise FrozenException("Can't reverse on immutable instance")


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


def clear_frozen_classes():
    with __FROZEN_CLASSES_LOCK:
        __FROZEN_CLASSES.clear()


def __create_frozen_class(klass: Type[object], attrs: List[str]) -> Type[FrozenBase]:
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
                    **{attr: None for attr in attrs}
                }
            }
        )
    )
    __store_frozen_class(klass=klass, frozen_class=frozen_class)
    return frozen_class


def make_frozen_class(klass: Type[object], attrs: List[str]) -> Type[FrozenBase]:
    klass_key = f"{klass.__module__}.{klass.__qualname__}"
    with __FROZEN_CLASSES_LOCK:
        frozen_class = __FROZEN_CLASSES.get(klass_key)

    if not frozen_class:
        frozen_class = __create_frozen_class(klass=klass, attrs=attrs)

    return frozen_class

