from typing import (
    Any,
    Callable,
    Generic,
    Optional,
    TypeVar,
    Union,
)

from gelidum.collections.frozendict import frozendict
from gelidum.collections.frozenlist import frozenlist
from gelidum.collections.frozenndarray import frozenndarray
from gelidum.collections.frozenzet import frozenzet
from gelidum.frozen import FrozenBase, Frozen  # noqa


K = TypeVar('K')
V = TypeVar('V')
T = TypeVar('T')


class Freezable(Generic[T]):  # noqa
    pass


FrozenType = Optional[
    Union[
        bool,
        int,
        float,
        bytes,
        complex,
        str,
        bytes,
        frozendict,
        frozenlist,
        frozenzet,
        frozenndarray,
        tuple,
        frozenset,
        FrozenBase,
        Frozen[T],
    ]
]

try:
    OnUpdateFuncType = Callable[[Frozen[T], str], None]
except TypeError:
    OnUpdateFuncType = Callable


OnFreezeFuncType = Callable[[Any], Any]
