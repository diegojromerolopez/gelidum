from typing import Callable, Generator, Optional, Sequence, Union, TypeVar, SupportsIndex, List

from gelidum.exceptions import FrozenException
from gelidum.frozen import FrozenBase, Frozen

__all__ = ['frozenlist']


_FrozenListParameterType = Optional[Union[Sequence, Generator]]

T = TypeVar('T')

class frozenlist(tuple, FrozenBase, Generic[T]):  # noqa
    def __raise_immutable_exception(self, *args, **kwargs):
        raise FrozenException("'frozenlist' object is immutable")

    def __new__(
        cls, seq: Optional[_FrozenListParameterType] = None, freeze_func: Optional[Callable[[T], Frozen[T]]] = None
    ) -> 'frozenlist[T]':
        if freeze_func is None:

            def freeze_func(item: T) -> Frozen[T]:
                from gelidum.freeze import freeze

                return freeze(item, on_update='exception', on_freeze='copy')

        if seq:
            self = frozenlist.__new__(cls, (freeze_func(arg) for arg in seq))
        else:
            self = frozenlist.__new__(cls, [])
        return self

    def __init__(
        self, seq: Optional[_FrozenListParameterType] = None, freeze_func: Optional[Callable[[T], Frozen[T]]] = None
    ):
        pass

    @classmethod
    def _gelidum_on_update(cls, *args, **kwargs) -> None:
        raise FrozenException("'frozenlist' object is immutable")

    @classmethod
    def get_gelidum_hot_class_name(cls) -> str:
        return 'tuple'

    @classmethod
    def get_gelidum_hot_class_module(cls) -> str:
        return 'builtins.tuple'

    def __getitem__(self, key: int) -> 'frozenlist[T]' | Frozen[T]:
        if type(key) is slice:
            return frozenlist(super().__getitem__(key))
        try:
            return super().__getitem__(key)
        except IndexError:
            raise IndexError('frozenlist index out of range')

    def __add__(self, other: 'frozenlist[T]') -> 'frozenlist[T]':
        joined_list = []
        for item in self:
            joined_list.append(item)
        for item in other:
            joined_list.append(item)
        return frozenlist(joined_list)

    def __mul__(self, times: SupportsIndex) -> 'frozenlist[T]':
        as_list = []
        for item in self:
            as_list.append(item)
        return frozenlist(as_list * times)

    def append(self, item: T) -> None:
        self.__raise_immutable_exception()

    def extend(self, iterable) -> None:
        self.__raise_immutable_exception()

    def insert(self, i: int, x: T) -> None:
        self.__raise_immutable_exception()

    def remove(self, x: T) -> None:
        self.__raise_immutable_exception()

    def pop(self, items: Sequence[T]) -> None:
        self.__raise_immutable_exception()

    def clear(self) -> None:
        self.__raise_immutable_exception()

    def index(self, x: SupportsIndex, start=None, end=None) -> int:
        args = [x]
        if start:
            args.append(start)
        if end:
            args.append(end)
        try:
            return super().index(*args)
        except ValueError:
            raise ValueError(f'{x} is not in frozenlist')

    def sort(self, *, key=None, reverse=False) -> None:
        self.__raise_immutable_exception()

    def reverse(self) -> None:
        self.__raise_immutable_exception()

    def copy(self) -> 'frozenlist[T]':
        """
        frozendlist objects are only shallow-copied.
        """
        return self
