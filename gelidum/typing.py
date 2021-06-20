import typing
from typing import Any, Callable, Type, TYPE_CHECKING
if TYPE_CHECKING:  # pragma: no cover
    from gelidum.frozen import FrozenBase  # noqa

try:
    _SpecialForm = getattr(typing, "_SpecialForm")

    @_SpecialForm
    def Final(self, parameters):  # noqa
        return typing.Final[parameters]

except AttributeError:  # pragma: no cover
    Final = typing.Final

_FrozenBase = Type["FrozenBase"]


OnUpdateFuncType = Callable[[_FrozenBase, str, ...], None]


OnFreezeFuncType = Callable[[Any], Any]
