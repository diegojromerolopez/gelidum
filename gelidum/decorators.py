from __future__ import annotations

import functools
from typing import Optional, Iterable, Set, Any
from gelidum import freeze


def freeze_params(params: Optional[Iterable[str]] = None):
    def inner_freeze_params(func):
        """Freeze all input params of a method"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func_args = tuple([freeze(arg, on_freeze="copy")
                               for arg in args])
            func_kwargs = {
                kwarg_name: freeze(kwarg, on_freeze="copy")
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
            for i, (param_name, param_typing) in
            enumerate(func.__annotations__.items())
            if __param_is_final(param_typing)
        }
        named_params_to_freeze: Set[str] = {
            param_name
            for param_name, param_typing in
            func.__annotations__.items()
            if __param_is_final(param_typing)
        }
        func_args = tuple([
            (
                freeze(arg, on_freeze="copy")
                if arg_index in unnamed_params_to_freeze else
                arg
            )
            for arg_index, arg in enumerate(args)
            ])
        func_kwargs = {
            kwarg_name: (
                freeze(kwarg, on_freeze="copy")
                if kwarg_name in named_params_to_freeze else
                kwarg
            )
            for kwarg_name, kwarg in kwargs.items()
        }
        return func(*func_args, **func_kwargs)
    return wrapper


def __param_is_final(param_typing: Any) -> bool:
    param_typing_str = str(param_typing)
    return (
        param_typing_str.startswith("typing.Final") or
        param_typing_str.startswith("gelidum.typing.Final")
    )
