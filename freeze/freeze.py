import copy
from frozendict import frozendict

from freeze.frozen import frozen__setattr__, frozen__delattr__, frozen__set__
from freeze.utils import isbuiltin


def freeze(obj: object) -> object:
    if isbuiltin(obj):
        return obj
    if isinstance(obj, bytearray):
        return bytes(obj)
    if isinstance(obj, dict):
        return frozendict({key: freeze(value) for key, value in obj.items()})
    if isinstance(obj, list) or isinstance(obj, tuple):
        return tuple(freeze(item) for item in obj)
    if isinstance(obj, set):
        return frozenset([freeze(item) for item in obj])
    if isinstance(obj, object):
        frozen_class = type(
            f"Frozen{obj.__class__.__name__}",
            (obj.__class__,),
            {
                "__slots__": tuple(),
                **{attr: None for attr in list(obj.__dict__.keys())},
                "__setattr__": frozen__setattr__,
                "__delattr__": frozen__delattr__,
                "__set__": frozen__set__,
            }
        )
        frozen_obj = copy.deepcopy(obj)
        for attr, value in frozen_obj.__dict__.items():
            setattr(frozen_obj, attr, freeze(getattr(frozen_obj, attr)))

        frozen_obj.__class__ = frozen_class
        return frozen_obj
    raise ValueError(f"object of type {obj.__class__} not frozen")
