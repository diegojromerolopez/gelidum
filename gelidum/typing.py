from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Annotated,
    Any,
    Callable,
    Generic,
    TypeAlias,
    TypeVar,
)

if TYPE_CHECKING:  # pragma: no cover
    from gelidum.collections.frozendict import frozendict  # noqa
    from gelidum.collections.frozenlist import frozenlist  # noqa
    from gelidum.collections.frozenndarray import frozenndarray  # noqa
    from gelidum.collections.frozenzet import frozenzet  # noqa
    from gelidum.frozen.frozen_base import FrozenBase  # noqa


T = TypeVar('T')


FrozenList: TypeAlias = 'frozenlist'
FrozenDict: TypeAlias = 'frozendict'
FrozenZet: TypeAlias = 'frozenzet'
FrozenNdArray: TypeAlias = 'frozenndarray'

if TYPE_CHECKING:
    Frozen = Annotated[T, "Frozen"]
    Freezable = Annotated[T, "Freezable"]
else:
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

from typing import Union

FrozenType = Union[
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
    None,
]

OnUpdateFuncType = Callable[..., None]


OnFreezeFuncType = Callable[[Any], Any]
