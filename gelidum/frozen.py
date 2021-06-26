import sys
import threading
from typing import Type, List, cast, Dict
from gelidum.typing import OnUpdateFuncType


class FrozenBase(object):
    @classmethod
    def __gelidum_on_update(cls, *args, **kwargs):  # pragma: no cover
        raise NotImplementedError("Implement in derived class")

    @classmethod
    def get_gelidum_hot_class_name(cls) -> str:  # pragma: no cover
        raise NotImplementedError("Implement in derived class")

    @classmethod
    def get_gelidum_hot_class_module(cls) -> str:  # pragma: no cover
        raise NotImplementedError("Implement in derived class")

    def __setattr__(self, key, value):
        self.__gelidum_on_update(
            frozen_obj=self,
            message=f"Can't assign attribute '{key}' on immutable instance",
            key=key, value=value
        )

    def __set__(self, obj, value):
        self.__gelidum_on_update(
            frozen_obj=self,
            message=f"Can't assign setter on immutable instance",
            obj=obj, value=value
        )

    def __delattr__(self, name):
        self.__gelidum_on_update(
            frozen_obj=self,
            message=f"Can't delete attribute '{name}' on immutable instance",
            name=name
        )

    def __setitem__(self, key, value):
        self.__gelidum_on_update(
            frozen_obj=self,
            message=f"Can't set key '{key}' on immutable instance",
            key=key, value=value
        )

    def __delitem__(self, key):
        self.__gelidum_on_update(
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


__FROZEN_CLASSES: Dict[str, Type[FrozenBase]] = dict()
__FROZEN_CLASSES_LOCK = threading.Lock()


def __store_frozen_class(
        klass: Type[object], frozen_class: Type[FrozenBase]
) -> None:
    """
    Add a frozen class to this module.
    Required for pickle serialization as only objects of non-dynamic
    classes are allowed.
    This method is thread-safe.
    :param frozen_class: a class that inherits from FrozenBase.
    """
    with __FROZEN_CLASSES_LOCK:
        klass_key = f"{klass.__module__}.{klass.__qualname__}"
        __FROZEN_CLASSES[klass_key] = frozen_class
        # Required for pickling frozen objects (only classes defined in actual
        # modules can have their objects pickled)
        setattr(sys.modules[__name__], frozen_class.__name__, frozen_class)


def clear_frozen_classes() -> None:
    with __FROZEN_CLASSES_LOCK:
        __FROZEN_CLASSES.clear()


def __create_frozen_class(
        klass: Type[object],
        attrs: List[str],
        on_update_func: OnUpdateFuncType
) -> Type[FrozenBase]:
    camel_case_module = (
        klass.__module__.title().replace(".", "").replace("_", "")
    )
    frozen_class_name = f"Frozen{klass.__name__}From{camel_case_module}"
    frozen_class: Type[FrozenBase] = cast(
        Type[FrozenBase],
        type(
            frozen_class_name,
            (FrozenBase, klass),
            {
                "__slots__": tuple(),
                **{
                    "get_gelidum_hot_class_name": lambda _: klass.__name__,
                    "get_gelidum_hot_class_module": lambda _: klass.__module__,
                    "_FrozenBase__gelidum_on_update":
                        lambda _self, *args, **kwargs:
                        on_update_func(*args, **kwargs),
                    **{attr: None for attr in attrs}
                }
            }
        )
    )
    __store_frozen_class(klass=klass, frozen_class=frozen_class)
    return frozen_class


def make_frozen_class(klass: Type[object], attrs: List[str],
                      on_update: OnUpdateFuncType) -> Type[FrozenBase]:
    klass_key = f"{klass.__module__}.{klass.__qualname__}"
    with __FROZEN_CLASSES_LOCK:
        frozen_class = __FROZEN_CLASSES.get(klass_key)

    if not frozen_class:
        frozen_class = __create_frozen_class(
            klass=klass, attrs=attrs,
            on_update_func=on_update
        )

    return frozen_class
