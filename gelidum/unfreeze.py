import sys

from gelidum.frozen import FrozenBase
from gelidum.utils import isbuiltin


def unfreeze(frozen_obj: FrozenBase):
    if isbuiltin(frozen_obj):
        return frozen_obj

    hot_class = frozen_obj.get_hot_class()
    obj = hot_class(frozen_obj)
    if isinstance(frozen_obj, FrozenBase):
        for attr, value in frozen_obj.__dict__.items():
            attr_value = getattr(frozen_obj, attr)
            setattr(obj, attr, unfreeze(attr_value))

    return obj
