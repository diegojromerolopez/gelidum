import typing
from typing import Any, Callable, Optional, Sized, Union, Iterable, Reversible
from typing import TYPE_CHECKING, TypeVar

from frozendict import frozendict

if TYPE_CHECKING:  # pragma: no cover
    from gelidum.frozen import FrozenBase  # noqa
    from gelidum.collections import frozenlist  # noqa

try:
    _SpecialForm = getattr(typing, "_SpecialForm")

    @_SpecialForm
    def Final(self, parameters):  # noqa
        return typing.Final[parameters]

except AttributeError:  # pragma: no cover
    Final = typing.Final

FrozenList = Union["FrozenBase", Sized, Iterable, Reversible,  "frozenlist"]

T = TypeVar('T')

FrozenType = Optional[
    Union[
        bool, int, float, bytes, complex, str,
        bytes, frozendict, FrozenList, tuple, frozenset,
        "FrozenBase", T
    ]
]

OnUpdateFuncType = Callable[["FrozenBase", str, ...], None]


OnFreezeFuncType = Callable[[Any], Any]
