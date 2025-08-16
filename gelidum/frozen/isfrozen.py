from typing import Any

from gelidum.frozen.frozen_base import FrozenBase

FROZEN_CLASSES = (FrozenBase, int, float, bool, tuple, None.__class__, complex, bytes, str)


def isfrozen(obj: Any) -> bool:
    return isinstance(obj, FROZEN_CLASSES)
