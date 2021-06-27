from typing import Any, Callable, Optional, Sized, Union, Iterable, Reversible, Iterator, Tuple
from gelidum import freeze, FrozenException
from gelidum.frozen import FrozenBase

__all__ = [
    "frozenlist"
]

FrozenList = Union[FrozenBase, Sized, Iterable, Reversible,  "_List"]

def frozenlist(  # noqa
        *args,
        freeze_func: Optional[Callable[[Any], FrozenBase]] = None
) -> FrozenList:
    if freeze_func is None:
        def freeze_func(item: Any) -> FrozenBase:
            return freeze(item, on_update="exception", on_freeze="copy")
    return freeze_func(_List(*args))


class _List(object): # noqa
    def __raise_immutable_exception(self):
        raise FrozenException("'frozenlist' object is immutable")

    def __init__(self, *args):
        self.__items: Tuple[Any] = tuple(args)

    def __getitem__(self, key) -> Any:
        try:
            return self.__items[key]
        except IndexError:
            raise IndexError("frozenlist index out of range")

    def __len__(self) -> int:
        return len(self.__items)

    def __add__(self, other) -> FrozenList:
        return frozenlist(
            *(self.__items + (other,))
        )

    def __mul__(self, times: int) -> FrozenList:
        return frozenlist(
            *(self.__items * times)
        )

    def __contains__(self, item) -> bool:
        return item in self.__items

    def __iter__(self) -> Iterator[FrozenBase]:
        return self.__items.__iter__()

    def __reversed__(self) -> FrozenList:
        return frozenlist(
            *(reversed(self.__items))
        )

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
            return self.__items.index(*args)
        except ValueError:
            raise ValueError(f"{x} is not in frozenlist")

    def count(self, x):
        pass

    def sort(self, *, key=None, reverse=False):
        self.__raise_immutable_exception()

    def reverse(self):
        self.__raise_immutable_exception()

    def copy(self) -> "_List":
        """
        frozenlist objects will only be
        """
        return self
