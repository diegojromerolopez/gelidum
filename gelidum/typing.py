import typing
from platform import python_implementation
from typing import Any, Callable, TYPE_CHECKING, Generic
if TYPE_CHECKING:  # pragma: no cover
    from gelidum.frozen import FrozenBase  # noqa

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
        if hasattr(typing, "Final"):
            Final = typing.Final
        else:
            T = typing.TypeVar('T')
            class Final(Generic[T]):  # noqa
                pass

_FrozenBase = "FrozenBase"


try:
    OnUpdateFuncType = Callable[[_FrozenBase, str, ...], None]
except TypeError:
    OnUpdateFuncType = Callable


OnFreezeFuncType = Callable[[Any], Any]
