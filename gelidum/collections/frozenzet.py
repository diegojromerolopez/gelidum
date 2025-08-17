from typing import Any, Callable, Generic, Generator, Iterable, Optional, Sequence, Union, TypeVar

from gelidum.exceptions import FrozenException
from gelidum.frozen import FrozenBase, Frozen

__all__ = ['frozenzet']

T = TypeVar('T')

_FrozenZetParameterType = Optional[Union[Sequence[T], Generator[T], Iterable[T]]]


class frozenzet(frozenset, FrozenBase, Generic[T]):  # noqa
    def __raise_immutable_exception(self, *args, **kwargs):
        raise FrozenException("'frozenzet' object is immutable")

    def __new__(
        cls, seq: Optional[_FrozenZetParameterType] = None, freeze_func: Optional[Callable[[T], Frozen[T]]] = None
    ) -> 'frozenzet[T]':
        if freeze_func is None:

            def freeze_func(item: T) -> Frozen[T]:
                from gelidum.freeze import freeze

                return freeze(item, on_update='exception', on_freeze='copy')

        if seq:
            self = super().__new__(cls, (freeze_func(arg) for arg in seq))
        else:
            self = super().__new__(cls, [])
        return self

    def __init__(
        self, seq: Optional[_FrozenZetParameterType] = None, freeze_func: Optional[Callable[[Any], FrozenBase]] = None
    ):
        super().__init__()

    @classmethod
    def _gelidum_on_update(cls, *args, **kwargs):
        raise FrozenException("'frozenzet' object is immutable")

    @classmethod
    def get_gelidum_hot_class_name(cls) -> str:
        return 'frozenset'

    @classmethod
    def get_gelidum_hot_class_module(cls) -> str:
        return 'builtins.frozenset'

    def __hash__(self) -> int:
        return hash(tuple(v for v in self))

    def __add__(self, other: 'frozenzet[T]') -> 'frozenzet[T]':
        joined_set = set()
        for item in self:
            joined_set.add(item)
        for item in other:
            joined_set.add(item)
        return frozenzet(joined_set)

    def add(self, item: T) -> None:
        self.__raise_immutable_exception()

    def remove(self, item: T) -> None:
        self.__raise_immutable_exception()

    def discard(self, item: T) -> None:
        self.__raise_immutable_exception()

    def pop(self) -> None:
        self.__raise_immutable_exception()

    def clear(self) -> None:
        self.__raise_immutable_exception()

    def update(self, *others: T) -> None:
        self.__raise_immutable_exception()

    def __ior__(self, *others: T) -> None:
        self.__raise_immutable_exception()

    def intersection_update(self, *others: T) -> None:
        self.__raise_immutable_exception()

    def __iand__(self, *others: T) -> None:
        self.__raise_immutable_exception()

    def difference_update(self, *others: T) -> None:
        self.__raise_immutable_exception()

    def __isub__(self, *others: T) -> None:
        self.__raise_immutable_exception()

    def symmetric_difference_update(self, others: Sequence[T]) -> None:
        self.__raise_immutable_exception()

    def __ixor__(self, *others: T) -> None:
        self.__raise_immutable_exception()

    def copy(self) -> 'frozenzet[T]':
        """
        frozenzet objects are only shallow-copied.
        """
        return self

    def __or__(self, *others: T) -> 'frozenzet[T]':
        return frozenzet(super().__or__(*others))

