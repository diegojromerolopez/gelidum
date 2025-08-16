import typing
from platform import python_implementation, python_version_tuple
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


python_interpreter = python_implementation()
python_interpreter_version = tuple(int(number) for number in python_version_tuple()[:2])


if python_interpreter == 'PyPy' or (python_interpreter_version[0] == 3 and python_interpreter_version[1] < 9):
    try:
        T = typing.TypeVar('T')

        class Final(Generic[T]):  # noqa
            pass

    except AttributeError:  # pragma: no cover
        Final = typing.Final

else:
    try:
        _SpecialForm = getattr(typing, '_SpecialForm')

        @_SpecialForm
        def Final(self, parameters):  # noqa
            return typing.Final[parameters]

    except AttributeError:  # pragma: no cover
        Final = typing.Final

FrozenList = Union['FrozenBase', Sized, Iterable, Reversible, 'frozenlist']
FrozenDict = Union['FrozenBase', Mapping, 'frozendict']
FrozenZet = Union['FrozenBase', Sized, Iterable, 'frozenzet']
FrozenNdArray = Union['FrozenBase', Sized, Iterable, 'frozenndarray']

T = TypeVar('T')

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
