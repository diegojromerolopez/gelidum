import typing
from typing import Any, Callable, Union


try:
    _SpecialForm = getattr(typing, "_SpecialForm")

    @_SpecialForm
    def Final(self, parameters):  # noqa
        return typing.Final[parameters]

except AttributeError:
    Final = typing.Final


_GelidumOnUpdateWithMessageType = Callable[[Any, str], None]
_GelidumOnUpdateWithFuncType = Callable[[Any, str, ...], None]

GelidumOnUpdateType = Union[
    _GelidumOnUpdateWithMessageType,
    _GelidumOnUpdateWithFuncType
]


OnUpdateFuncType = Callable[[str, Any], None]


OnFreezeFuncType = Callable[[Any], Any]
