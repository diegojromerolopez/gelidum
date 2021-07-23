from typing import Any, Callable, Optional, Sequence, Generator, Union

from gelidum.exceptions import FrozenException
from gelidum.frozen import FrozenBase
from gelidum.typing import FrozenType, FrozenList

__all__ = [
    "frozenlist"
]


_FrozenListParameterType = Optional[Union[Sequence, Generator]]


class frozenlist(tuple, FrozenBase): # noqa
    def __raise_immutable_exception(self, *args, **kwargs):
        raise FrozenException("'frozenlist' object is immutable")

    def __new__(
            cls, seq: Optional[_FrozenListParameterType] = None,
            freeze_func: Optional[Callable[[Any], FrozenBase]] = None
    ) -> "frozenlist":
        if freeze_func is None:
            def freeze_func(item: Any) -> FrozenType:
                from gelidum.freeze import freeze
                return freeze(item, on_update="exception", on_freeze="copy")
        if seq:
            self = tuple.__new__(cls, (freeze_func(arg) for arg in seq))
        else:
            self = tuple.__new__(cls, [])
        return self

    def __init__(
            self,  seq: Optional[_FrozenListParameterType] = None,
            freeze_func: Optional[Callable[[Any], FrozenBase]] = None
    ):
        pass

    @classmethod
    def _gelidum_on_update(cls, *args, **kwargs):
        raise FrozenException("'frozenlist' object is immutable")

    @classmethod
    def get_gelidum_hot_class_name(cls) -> str:
        return "tuple"

    @classmethod
    def get_gelidum_hot_class_module(cls) -> str:
        return "builtins.tuple"

    def __getitem__(self, key) -> Any:
        if type(key) is slice:
            return frozenlist(
                super().__getitem__(key)
            )
        try:
            return super().__getitem__(key)
        except IndexError:
            raise IndexError("frozenlist index out of range")

    def __add__(self, other: FrozenList) -> FrozenList:
        joined_list = []
        for item in self:
            joined_list.append(item)
        for item in other:
            joined_list.append(item)
        return frozenlist(joined_list)

    def __mul__(self, times: int) -> FrozenList:
        as_list = []
        for item in self:
            as_list.append(item)
        return frozenlist(as_list * times)

    def append(self, item) -> None:
        self.__raise_immutable_exception()

    def extend(self, iterable):
        self.__raise_immutable_exception()

    def insert(self, i, x):
        self.__raise_immutable_exception()

    def remove(self, x):
        self.__raise_immutable_exception()

    def pop(self, items):
        self.__raise_immutable_exception()

    def clear(self):
        self.__raise_immutable_exception()

    def index(self, x, start=None, end=None) -> int:
        args = [x]
        if start:
            args.append(start)
        if end:
            args.append(end)
        try:
            return super().index(*args)
        except ValueError:
            raise ValueError(f"{x} is not in frozenlist")

    def sort(self, *, key=None, reverse=False):
        self.__raise_immutable_exception()

    def reverse(self):
        self.__raise_immutable_exception()

    def copy(self) -> "frozenlist":
        """
        frozendlist objects are only shallow-copied.
        """
        return self

