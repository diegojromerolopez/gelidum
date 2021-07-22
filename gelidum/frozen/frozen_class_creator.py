import sys
import threading
from typing import cast, Type, Dict, Optional, Set, Iterable
from gelidum.typing import OnUpdateFuncType
from gelidum.frozen.frozen_base import FrozenBase


def __create_frozen_class(
        klass: Type[object],
        attrs: Iterable[str],
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
                **{
                    "get_gelidum_hot_class_name": lambda _: klass.__name__,
                    "get_gelidum_hot_class_module": lambda _: klass.__module__,
                    "_gelidum_on_update":
                        lambda _self, *args, **kwargs:
                        on_update_func(*args, **kwargs),
                    **{attr: None for attr in attrs}
                }
            }
        )
    )
    __store_frozen_class(klass=klass, frozen_class=frozen_class)
    return frozen_class


def make_frozen_class(klass: Type[object], attrs: Iterable[str],
                      on_update: OnUpdateFuncType) -> Type[FrozenBase]:
    frozen_class = get_frozen_class(
        klass_key=f"{klass.__module__}.{klass.__qualname__}"
    )

    if not frozen_class:
        frozen_class = __create_frozen_class(
            klass=klass, attrs=attrs,
            on_update_func=on_update
        )

    return frozen_class


__FROZEN_CLASSES: Dict[str, Type[FrozenBase]] = dict()
__FROZEN_CLASSES_LOCK = threading.Lock()


def get_frozen_class(klass_key: str) -> Optional[Type[FrozenBase]]:
    with __FROZEN_CLASSES_LOCK:
        frozen_class = __FROZEN_CLASSES.get(klass_key)
    return frozen_class


def get_frozen_classes() -> Set[Type[FrozenBase]]:
    with __FROZEN_CLASSES_LOCK:
        return set(__FROZEN_CLASSES.values())


def __store_frozen_class(
        klass: Type[object], frozen_class: Type[FrozenBase]
) -> None:
    """
    Add a frozen class to this module.
    Required for pickle serialization as only objects of non-dynamic
    classes are allowed.
    This method is thread-safe.
    :param klass: the original class.
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

