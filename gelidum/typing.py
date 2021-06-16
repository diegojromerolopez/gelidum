import typing
from typing import Any, Callable, Union

_SpecialForm = getattr(typing, "_SpecialForm")


@_SpecialForm
def Frozen(self, parameters):  # noqa
    return typing.Final[parameters]


_GelidumOnUpdateWithMessageType = Callable[[str], None]
_GelidumOnUpdateWithFuncType = Callable[[str, ...], None]

GelidumOnUpdateType = Union[
    _GelidumOnUpdateWithMessageType,
    _GelidumOnUpdateWithFuncType
]

_OnUpdateFuncType = Callable[[str, Any], None]
OnUpdateType = Union[_OnUpdateFuncType, str]
