from typing import Any, Callable, Optional

import numpy as np

from gelidum.exceptions import FrozenException
from gelidum.frozen import FrozenBase


__all__ = ["frozenndarray"]


class frozenndarray(np.ndarray, FrozenBase):  # noqa
    """
    Read https://numpy.org/devdocs/user/basics.subclassing.html for more
    information about numpy.ndarray subclassing.
    """

    def __new__(cls, ndarray: np.ndarray, freeze_func: Optional[Callable[[Any], FrozenBase]] = None, *args, **kwargs):
        obj = ndarray.copy().view(cls)
        obj.flags.writeable = False
        return obj

    @classmethod
    def _gelidum_on_update(cls, *args, **kwargs):
        raise FrozenException("'ndarray' object is immutable")

    @classmethod
    def get_gelidum_hot_class_name(cls) -> str:
        return "ndarray"

    @classmethod
    def get_gelidum_hot_class_module(cls) -> str:
        return "numpy.ndarray"
