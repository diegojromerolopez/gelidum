import functools
from typing import Optional, Iterable

from gelidum import freeze


def freeze_params(params: Optional[Iterable[str]] = None):
    def inner_freeze_params(func):
        """Freeze all input params of a method"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func_args = tuple([freeze(arg, inplace=False)
                               for arg in args])
            func_kwargs = {
                kwarg_name: freeze(kwarg, inplace=False)
                if kwarg_name in params else kwarg
                for kwarg_name, kwarg in kwargs.items()
            }
            return func(*func_args, **func_kwargs)
        return wrapper
    return inner_freeze_params
