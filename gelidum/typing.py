from typing import Any, Callable, Union


_GelidumOnUpdateWithMessageType = Callable[[str], None]
_GelidumOnUpdateWithFuncType = Callable[[str, ...], None]

GelidumOnUpdateType = Union[
    _GelidumOnUpdateWithMessageType,
    _GelidumOnUpdateWithFuncType
]

_OnUpdateFuncType = Callable[[str, Any], None]
OnUpdateType = Union[_OnUpdateFuncType, str]
