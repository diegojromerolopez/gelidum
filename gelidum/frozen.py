import sys
from typing import Type, List, cast

import shortuuid as shortuuid

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


def __add_frozen_class_to_this_module(frozen_class: Type[FrozenBase]) -> None:
    """
    Add a frozen class to this module.
    Required for pickle serialization as only objects of non-dynamic
    classes are allowed.
    :param frozen_class: a class that inherits from FrozenBase.
    """
    setattr(sys.modules[__name__], frozen_class.__name__, frozen_class)


def make_frozen_class(klass: Type[object], attrs: List[str]) -> Type[FrozenBase]:
    klass_source_module = klass.__module__
    camel_case_module = klass.__module__.title().replace(".", "").replace("_", "")
    frozen_class_name = f"Frozen{klass.__name__}From{camel_case_module}UUID{shortuuid.uuid()}"
    frozen_class: Type[FrozenBase] = cast(
        Type[FrozenBase],
        type(
            frozen_class_name,
            (klass, FrozenBase),
            {
                "__slots__": tuple(),
                **{
                    'get_gelidum_hot_class_name': lambda _: klass.__name__,
                    'get_gelidum_hot_class_module': lambda _: klass_source_module,
                    **{attr: None for attr in attrs}
                }
            }
        )
    )
    __add_frozen_class_to_this_module(frozen_class=frozen_class)
    return frozen_class
