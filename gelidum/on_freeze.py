import copy
from typing import Any, Optional, Union

from gelidum.typing import OnFreezeFuncType


class OnFreezeCopier:
    def __call__(self, obj: Any) -> Any:
        return copy.deepcopy(obj)


class OnFreezeIdentityFunc:
    def __call__(self, obj: Any) -> Any:
        return obj


class OnFreezeOriginalObjTracker(OnFreezeCopier):
    """
    A callable class that stores the first object that was
    frozen. Useful for keeping track of original "hot" objects.
    """
    def __init__(self):
        self.__original_obj: Optional[Any] = None

    def __call__(self, obj: Any) -> Any:
        if self.__original_obj is None:
            self.__original_obj = obj
        return super().__call__(obj=obj)

    @property
    def original_obj(self) -> Optional[Any]:
        return self.__original_obj


_ON_FREEZE_COPIER = OnFreezeCopier()
_ON_FREEZE_IDENTITY_FUNC = OnFreezeIdentityFunc()


def on_freeze_func_creator(on_freeze: Union[str, OnFreezeFuncType]) -> OnFreezeFuncType:
    if isinstance(on_freeze, str):
        if on_freeze == "copy":
            return _ON_FREEZE_COPIER
        elif on_freeze == "inplace":
            return _ON_FREEZE_IDENTITY_FUNC
        else:
            raise AttributeError(
                f"Invalid value for on_freeze parameter, '{on_freeze}' found, "
                f"only 'copy' and 'inplace' are valid options if passed a string"
            )

    elif callable(on_freeze):
        return on_freeze

    else:
        raise AttributeError(
            f"Invalid value for on_freeze parameter, '{on_freeze}' found, "
            f"only 'copy', 'inplace' or a callable are valid options"
        )
