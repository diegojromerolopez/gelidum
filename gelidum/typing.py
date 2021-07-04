import typing
from platform import python_implementation, python_version_tuple
from typing import Any, Callable, TYPE_CHECKING, Generic
if TYPE_CHECKING:  # pragma: no cover
    from gelidum.frozen import FrozenBase  # noqa


python_interpreter = python_implementation()
python_interpreter_version = tuple(int(number) for number in python_version_tuple())


if (
        python_interpreter == "PyPy" or (
            python_interpreter_version[0] == 3 and python_interpreter_version[1] < 9
        )
):
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


_FrozenBase = "FrozenBase"


try:
    OnUpdateFuncType = Callable[[_FrozenBase, str, ...], None]
except TypeError:
    OnUpdateFuncType = Callable


OnFreezeFuncType = Callable[[Any], Any]
