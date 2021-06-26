from typing import Any, Callable, Optional
from gelidum import freeze
from gelidum.frozen import FrozenBase


class ImmutableList(object):
    def __init__(self, *args, freeze_func: Optional[Callable[[Any], FrozenBase]] = None):
        if freeze_func is None:
            def freeze_func(item: Any) -> FrozenBase:
                return freeze(item, on_update="exception", on_freeze="copy")
        self.__freeze = freeze_func

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
        frozen_other = self.__freeze(other)
        return ImmutableList(
            *(self.__items + (frozen_other,))
        )
