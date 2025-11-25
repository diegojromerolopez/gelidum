from __future__ import annotations

import sys
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Generic,
    Optional,
    TypeVar,
    Union,
)

if TYPE_CHECKING:  # pragma: no cover
    from gelidum.collections.frozendict import frozendict  # noqa
    from gelidum.collections.frozenlist import frozenlist  # noqa
    from gelidum.collections.frozenndarray import frozenndarray  # noqa
    from gelidum.collections.frozenzet import frozenzet  # noqa
    from gelidum.frozen.frozen_base import FrozenBase  # noqa


T = TypeVar('T')


class Freezable(Generic[T]):  # noqa
    pass


class Frozen(Generic[T]):
    """
    Generic type representing a frozen (immutable) version of type T.

    This type preserves all attributes and methods of T while ensuring immutability.
    Use this for type hints to maintain type information through freeze operations.

    Example:
        person = Person('Alice', 30)
        frozen_person: Frozen[Person] = freeze(person)
    """

    pass


# TypeAlias is available in Python 3.10+, for 3.9 we use simple assignment
if sys.version_info >= (3, 10):
    from typing import TypeAlias

    FrozenList: TypeAlias = 'frozenlist'
    FrozenDict: TypeAlias = 'frozendict'
    FrozenZet: TypeAlias = 'frozenzet'
    FrozenNdArray: TypeAlias = 'frozenndarray'
else:
    FrozenList = 'frozenlist'  # type: ignore[misc]
    FrozenDict = 'frozendict'  # type: ignore[misc]
    FrozenZet = 'frozenzet'  # type: ignore[misc]
    FrozenNdArray = 'frozenndarray'  # type: ignore[misc]

FrozenType = Optional[
    Union[
        bool,
        int,
        float,
        bytes,
        complex,
        str,
        bytes,
        FrozenDict,  # type: ignore[valid-type]
        FrozenList,  # type: ignore[valid-type]
        FrozenZet,  # type: ignore[valid-type]
        FrozenNdArray,  # type: ignore[valid-type]
        tuple,
        frozenset,
        'FrozenBase',
        Frozen[T],
    ]
]

OnUpdateFuncType = Callable[..., None]


OnFreezeFuncType = Callable[[Any], Any]
