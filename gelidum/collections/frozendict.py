from collections.abc import Mapping
from typing import Any, Callable, Dict, Hashable, Optional, Sequence, Tuple, Union

from gelidum.exceptions import FrozenException
from gelidum.frozen import FrozenBase
from gelidum.typing import FrozenDict

__all__ = ['frozendict']


class frozendict(dict, FrozenBase):  # noqa
    def __raise_immutable_exception(self, *args, **kwargs):
        raise FrozenException("'frozendict' object is immutable")

    def __init__(
        self,
        seq: Optional[Union[Mapping, Sequence, Tuple[Hashable, Any]]] = None,
        freeze_func: Optional[Callable[[Any], Any]] = None,
        **kwargs,
    ):
        if freeze_func is None:
            from gelidum.freeze import freeze

            def _freeze_func(item: Any) -> Any:
                return freeze(item, on_update='exception', on_freeze='copy')

            freeze_func = _freeze_func

        if seq is not None:
            if isinstance(seq, Mapping):
                super().__init__(
                    {key: freeze_func(value) for key, value in seq.items()},
                    **{key: freeze_func(value) for key, value in kwargs.items()},
                )
            elif isinstance(seq, Sequence):
                super().__init__(
                    {key: freeze_func(value) for key, value in seq},  # type: ignore[misc]
                    **{key: freeze_func(value) for key, value in kwargs.items()},
                )
            else:
                # Assume it's an iterable of key-value pairs
                super().__init__(
                    {key: freeze_func(value) for key, value in seq},  # type: ignore[misc]
                    **{key: freeze_func(value) for key, value in kwargs.items()},
                )
        elif kwargs:
            super().__init__({key: freeze_func(value) for key, value in kwargs.items()})
        else:
            super().__init__()

    @classmethod
    def _gelidum_on_update(cls, *args, **kwargs):
        raise FrozenException("'frozendict' object is immutable")

    @classmethod
    def get_gelidum_hot_class_name(cls) -> str:
        return 'dict'

    @classmethod
    def get_gelidum_hot_class_module(cls) -> str:
        return 'builtins.dict'

    def __hash__(self) -> int:  # type: ignore[override]
        return hash(tuple((k, v) for k, v in self.items()))

    def __getitem__(self, key) -> Any:
        if type(key) is slice:
            return frozendict(super().__getitem__(key))
        try:
            return super().__getitem__(key)
        except IndexError:
            raise IndexError('frozendict index out of range')

    def __add__(self, other: 'FrozenDict') -> 'frozendict':  # type: ignore[valid-type]
        joined_dict = self | other
        return frozendict(joined_dict)

    def __or__(self, other: FrozenDict) -> 'frozendict':  # type: ignore[override,valid-type]
        if hasattr(dict, '__or__'):
            joined: Dict[Any, Any] = dict.__or__(self, other)  # type: ignore[arg-type,operator]
            return frozendict(joined)
        # Python version < 3.9
        result_dict: Dict[Any, Any] = dict()
        result_dict.update(self)
        result_dict.update(other)  # type: ignore[arg-type]
        return frozendict(result_dict)

    def __sub__(self, other: FrozenDict) -> 'frozendict':  # type: ignore[valid-type]
        result = {k: v for k, v in self.items() if k not in other}  # type: ignore[attr-defined]
        return frozendict(result)  # type: ignore[arg-type,operator]

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

    def copy(self) -> 'frozendict':
        """
        frozendict objects are only shallow-copied.
        """
        return self
