from freeze.exceptions import FrozenException


class FrozenBase(object):
    def __setattr__(self, key, value):
        raise FrozenException(f"Can't assign \"{key}\" on immutable instance")

    def __set__(self, *args, **kwargs):
        raise FrozenException("Can't assign setter on immutable instance")

    def __delattr__(self, name):
        raise FrozenException(
            f"Can't delete attribute \"{name}\" on immutable instance")

    def __setitem__(self, key, value):
        raise FrozenException("Can't set key on immutable instance")

    def __delitem__(self, key):
        raise FrozenException("Can't delete key on immutable instance")

    def __reversed__(self):
        raise FrozenException("Can't reverse on immutable instance")
