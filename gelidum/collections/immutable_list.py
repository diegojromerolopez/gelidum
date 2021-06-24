from typing import Any
from gelidum import freeze
from gelidum.frozen import FrozenBase


class ImmutableList(object):
    @staticmethod
    def __freeze(item: Any) -> FrozenBase:
        return freeze(item, on_update="exception", on_freeze="copy")

    def __init__(self, *args):
        if len(args) > 0:
            self.__items = tuple(
                self.__freeze(arg_i) for arg_i in args
            )
        else:
            self.__items = tuple()

    def __getitem__(self, key) -> Any:
        return self.__items[key]

    def __len__(self) -> int:
        return len(self.__items)

    def __add__(self, other) -> "ImmutableList":
        frozen_other = freeze(other, on_update="exception", on_freeze="copy")
        return ImmutableList(
            *(self.__items + (frozen_other,))
        )
