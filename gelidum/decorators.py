from __future__ import annotations

import functools
from typing import Optional, Iterable, Set
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


def freeze_final(func):
    """Freeze all final params of a method"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        unnamed_params_to_freeze: Set[str] = {
            i
            for i, (param_name, param_typing) in enumerate(func.__annotations__.items())
            if str(param_typing).startswith("typing.Final")
        }
        named_params_to_freeze: Set[str] = {
            param_name
            for param_name, param_typing in func.__annotations__.items()
            if str(param_typing).startswith("typing.Final")
        }
        func_args = tuple([
            (
                freeze(arg, inplace=False)
                if arg_index in unnamed_params_to_freeze else
                arg
            )
            for arg_index, arg in enumerate(args)
            ])
        func_kwargs = {
            kwarg_name: (
                freeze(kwarg, inplace=False)
                if kwarg_name in named_params_to_freeze else
                kwarg
            )
            for kwarg_name, kwarg in kwargs.items()
        }
        return func(*func_args, **func_kwargs)
    return wrapper
