from freeze.exceptions import FrozenException


def frozen__setattr__(x, y, v):
    raise FrozenException(f"Can't assign \"{y}\" on immutable instance")


def frozen__set__(*args, **kwargs):
    raise FrozenException("Can't assign setter on immutable instance")


def frozen__delattr__(name):
    raise FrozenException(
        f"Can't delete attribute \"{name}\" on immutable instance")
