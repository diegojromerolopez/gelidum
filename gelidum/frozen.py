from typing import Type, List
from gelidum.exceptions import FrozenException


class FrozenBase(object):
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


def make_frozen_class(klass: Type[object], attrs: List[str]):
    frozen_class = type(
        f"Frozen{klass.__name__}",
        (klass, FrozenBase),
        {
            "__slots__": tuple(),
            **{attr: None for attr in attrs}
        }
    )
    return frozen_class
