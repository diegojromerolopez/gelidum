import typing
from platform import python_implementation
from typing import Any, Callable, TYPE_CHECKING, Generic
from typing import Optional, Sized, Union, Iterable, Reversible, Mapping
from typing import TypeVar

if TYPE_CHECKING:  # pragma: no cover
    from gelidum.frozen import FrozenBase  # noqa
    from gelidum.collections import frozendict, frozenlist  # noqa

if python_implementation() == "PyPy":
    try:
        T = typing.TypeVar('T')

        class Final(Generic[T]):  # noqa
            pass
    except AttributeError:  # pragma: no cover
        Final = typing.Final

else:
    try:
        _SpecialForm = getattr(typing, "_SpecialForm")

        @_SpecialForm
        def Final(self, parameters):  # noqa
            return typing.Final[parameters]
    except AttributeError:  # pragma: no cover
        Final = typing.Final

FrozenList = Union["FrozenBase", Sized, Iterable, Reversible,  "frozenlist"]
FrozenDict = Union["FrozenBase", Mapping, "frozendict"]

T = TypeVar('T')

FrozenType = Optional[
    Union[
        bool, int, float, bytes, complex, str,
        bytes, FrozenDict, FrozenList, tuple, frozenset,
        "FrozenBase", T
    ]
]

try:
    OnUpdateFuncType = Callable[["FrozenBase", str, ...], None]
except TypeError:
    OnUpdateFuncType = Callable


OnFreezeFuncType = Callable[[Any], Any]
