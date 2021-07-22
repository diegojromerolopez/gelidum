class FrozenBase(object):
    @classmethod
    def _gelidum_on_update(cls, *args, **kwargs):  # pragma: no cover
        raise NotImplementedError("Implement in derived class")

    @classmethod
    def get_gelidum_hot_class_name(cls) -> str:  # pragma: no cover
        raise NotImplementedError("Implement in derived class")

    @classmethod
    def get_gelidum_hot_class_module(cls) -> str:  # pragma: no cover
        raise NotImplementedError("Implement in derived class")

    def __setattr__(self, key, value):
        self._gelidum_on_update(
            frozen_obj=self,
            message=f"Can't assign attribute '{key}' on immutable instance",
            key=key, value=value
        )

    def __set__(self, obj, value):
        self._gelidum_on_update(
            frozen_obj=self,
            message=f"Can't assign setter on immutable instance",
            obj=obj, value=value
        )

    def __delattr__(self, name):
        self._gelidum_on_update(
            frozen_obj=self,
            message=f"Can't delete attribute '{name}' on immutable instance",
            name=name
        )

    def __setitem__(self, key, value):
        self._gelidum_on_update(
            frozen_obj=self,
            message=f"Can't set key '{key}' on immutable instance",
            key=key, value=value
        )

    def __delitem__(self, key):
        self._gelidum_on_update(
            frozen_obj=self,
            message=f"Can't delete key '{key}' on immutable instance",
            key=key)

    def __deepcopy__(self, *args, **kwargs) -> "FrozenBase":
        """
        No frozen object must need to be (deep) copied.
        Use structural sharing to improve performance when doing
        immutable data structures.
        :return: reference to self.
        """
        return self
