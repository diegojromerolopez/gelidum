import typing
from typing import Any, Callable, Union

try:
    _SpecialForm = getattr(typing, "_SpecialForm")

    @_SpecialForm
    def Final(self, parameters):  # noqa
        return typing.Final[parameters]

except AttributeError:
    Final = typing.Final


_GelidumOnUpdateWithMessageType = Callable[[str], None]
_GelidumOnUpdateWithFuncType = Callable[[str, ...], None]

GelidumOnUpdateType = Union[
    _GelidumOnUpdateWithMessageType,
    _GelidumOnUpdateWithFuncType
]

_OnUpdateFuncType = Callable[[str, Any], None]
OnUpdateType = Union[_OnUpdateFuncType, str]
