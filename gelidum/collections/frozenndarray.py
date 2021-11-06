import numpy as np

from gelidum import FrozenException
from gelidum.frozen import FrozenBase


class frozenndarray(np.ndarray, FrozenBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.flags.writeable = False

    @classmethod
    def _gelidum_on_update(cls, *args, **kwargs):
        raise FrozenException("'ndarray' object is immutable")

    @classmethod
    def get_gelidum_hot_class_name(cls) -> str:
        return "ndarray"

    @classmethod
    def get_gelidum_hot_class_module(cls) -> str:
        return "numpy.ndarray"
