import importlib.util
from importlib.machinery import ModuleSpec


def package_is_installed(package_name: str) -> bool:
    return isinstance(importlib.util.find_spec(package_name), ModuleSpec)


NUMPY_INSTALLED = package_is_installed("numpy")
