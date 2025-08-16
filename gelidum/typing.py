from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Generic,
    Iterable,
    Mapping,
    Optional,
    Reversible,
    Sized,
    TypeVar,
    Union,
)

if TYPE_CHECKING:  # pragma: no cover
    from gelidum.collections import (  # noqa
        frozendict,
        frozenlist,
        frozenndarray,
        frozenzet,
    )
    from gelidum.frozen import FrozenBase  # noqa


T = TypeVar('T')


class Freezable(Generic[T]):  # noqa
    pass


FrozenList = Union['FrozenBase', Sized, Iterable, Reversible, 'frozenlist']
FrozenDict = Union['FrozenBase', Mapping, 'frozendict']
FrozenZet = Union['FrozenBase', Sized, Iterable, 'frozenzet']
FrozenNdArray = Union['FrozenBase', Sized, Iterable, 'frozenndarray']


FrozenType = Optional[
    Union[
        bool,
        int,
        float,
        bytes,
        complex,
        str,
        bytes,
        FrozenDict,
        FrozenList,
        FrozenZet,
        FrozenNdArray,
        tuple,
        frozenset,
        'FrozenBase',
        T,
    ]
]

try:
    OnUpdateFuncType = Callable[['FrozenBase', str, ...], None]
except TypeError:
    OnUpdateFuncType = Callable


OnFreezeFuncType = Callable[[Any], Any]
