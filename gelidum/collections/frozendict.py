from typing import Generic, Callable, Optional, Sequence, Tuple, Union, TypeVar

try:
    from collections import Mapping
except ImportError:
    # For python > 3.10
    from collections.abc import Mapping

from gelidum.exceptions import FrozenException
from gelidum.frozen import FrozenBase, Frozen

__all__ = ['frozendict']


K = TypeVar('K')
V = TypeVar('V')

class frozendict(dict, FrozenBase, Generic[K, V]):  # noqa
    def __raise_immutable_exception(self, *args, **kwargs):
        raise FrozenException("'frozendict' object is immutable")

    def __init__(
        self,
        seq: Optional[Union[Mapping[K, V], Sequence[Tuple[K, V]]]] = None,
        freeze_func: Optional[Callable[[V], Frozen[V]]] = None,
        **kwargs,
    ):
        if freeze_func is None:

            def freeze_func(item: V) -> Frozen[V]:
                from gelidum.freeze import freeze

                return freeze(item, on_update='exception', on_freeze='copy')

        if seq is not None:
            items = None
            if isinstance(seq, Mapping):
                items = seq.items()
            elif isinstance(seq, Sequence):
                items = seq

            if items is not None:
                super().__init__(
                    {key: freeze_func(value) for key, value in items},
                    **{key: freeze_func(value) for key, value in kwargs.items()},
                )
            else:
                super().__init__({key: freeze_func(value) for key, value in seq})
        elif kwargs:
            super().__init__({key: freeze_func(value) for key, value in kwargs.items()})
        else:
            super().__init__()

    @classmethod
    def _gelidum_on_update(cls, *args, **kwargs) -> None:
        raise FrozenException("'frozendict' object is immutable")

    @classmethod
    def get_gelidum_hot_class_name(cls) -> str:
        return 'dict'

    @classmethod
    def get_gelidum_hot_class_module(cls) -> str:
        return 'builtins.dict'

    def __hash__(self) -> int:
        return hash(tuple((k, v) for k, v in self.items()))

    def __getitem__(self, key: K) -> 'frozendict[K, V]':
        if type(key) is slice:
            return frozendict(super().__getitem__(key))
        try:
            return super().__getitem__(key)
        except IndexError:
            raise IndexError('frozendict index out of range')

    def __add__(self, other: 'frozendict[K, V]') -> 'frozendict[K, V]':
        joined_dict = self | other
        return frozendict(joined_dict)

    def __or__(self, other: 'frozendict[K, V]') -> 'frozendict[K, V]':
        if hasattr(super, '__or__'):
            return super().__or__(other)
        # Python version < 3.9
        result_dict = dict()
        result_dict.update(self)
        result_dict.update(other)
        return frozendict(result_dict)

    def __sub__(self, other: 'frozendict[K, V]') -> 'frozendict[K, V]':
        return frozendict({k: v for k, v in self.items() if k not in other})

    def remove(self, x) -> None:
        self.__raise_immutable_exception()

    def pop(self, items) -> None:
        self.__raise_immutable_exception()

    def popitem(self, *args, **kwarg) -> None:
        self.__raise_immutable_exception()

    def __setitem__(self, key, val, *args, **kwargs) -> None:
        self.__raise_immutable_exception()

    def __delitem__(self, key, *args, **kwargs) -> None:
        self.__raise_immutable_exception()

    def clear(self) -> None:
        self.__raise_immutable_exception()

    def update(self, *args, **kwarg) -> None:
        self.__raise_immutable_exception()

    def copy(self) -> 'frozendict[K, V]':
        """
        frozendict objects are only shallow-copied.
        """
        return self
