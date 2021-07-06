from typing import Any, Callable, Optional, Dict

from gelidum.exceptions import FrozenException
from gelidum.frozen import FrozenBase
from gelidum.typing import FrozenType, FrozenDict

__all__ = [
    "frozendict"
]


class frozendict(dict, FrozenBase): # noqa
    def __raise_immutable_exception(self, *args, **kwargs):
        raise FrozenException("'frozendict' object is immutable")

    def __init__(
            self,
            mapping: Optional[Dict] = None,
            freeze_func: Optional[Callable[[Any], FrozenBase]] = None):
        if freeze_func is None:
            def freeze_func(item: Any) -> FrozenType:
                from gelidum.freeze import freeze
                return freeze(item, on_update="exception", on_freeze="copy")
        if mapping:
            super().__init__(
                {key: freeze_func(value) for key, value in mapping.items()}
            )
        else:
            super().__init__()

    @classmethod
    def _gelidum_on_update(cls, *args, **kwargs):
        raise FrozenException("'frozendict' object is immutable")

    @classmethod
    def get_gelidum_hot_class_name(cls) -> str:
        return "dict"

    @classmethod
    def get_gelidum_hot_class_module(cls) -> str:
        return "builtins.dict"

    def __getitem__(self, key) -> Any:
        if type(key) is slice:
            return frozendict(
                super().__getitem__(key)
            )
        try:
            return super().__getitem__(key)
        except IndexError:
            raise IndexError("frozendict index out of range")

    def __add__(self, other: FrozenDict) -> FrozenDict:
        joined_dict = {}
        joined_dict.update(self)
        joined_dict.update(other)
        return frozendict(joined_dict)

    def __ior__(self, other: FrozenDict) -> FrozenDict:
        joined_dict = {}
        joined_dict.update(self)
        joined_dict.update(other)
        return frozendict(joined_dict)

    def remove(self, x):
        self.__raise_immutable_exception()

    def pop(self, items):
        self.__raise_immutable_exception()

    def popitem(self, *args, **kwarg):
        self.__raise_immutable_exception()

    def __setitem__(self, key, val, *args, **kwargs):
        self.__raise_immutable_exception()
    
    def __delitem__(self, key, *args, **kwargs):
        self.__raise_immutable_exception()

    def clear(self):
        self.__raise_immutable_exception()

    def update(self, *args, **kwarg):
        self.__raise_immutable_exception()

    def copy(self) -> "frozendict":
        """
        frozendict objects are only shallow-copied.
        """
        return self

