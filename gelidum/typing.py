import typing
from typing import Any, Callable, Union, Type, TYPE_CHECKING
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
_GelidumOnUpdateWithMessageType = Callable[[_FrozenBase, str], None]
_GelidumOnUpdateWithFuncType = Callable[[_FrozenBase, str, ...], None]

GelidumOnUpdateType = Union[
    _GelidumOnUpdateWithMessageType,
    _GelidumOnUpdateWithFuncType
]


OnUpdateFuncType = Callable[[_FrozenBase, str, ...], None]


OnFreezeFuncType = Callable[[Any], Any]
