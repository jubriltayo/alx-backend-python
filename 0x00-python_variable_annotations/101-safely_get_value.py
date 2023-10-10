#!/usr/bin/env python3
"""This module defines a function called `safely_get_value`
"""
from typing import TypeVar, Mapping, Any, Union

T = TypeVar('T')


def safely_get_value(dct: Mapping, key: Any,
                     default: Union[T, None] = None) -> Union[Any, T]:
    """Retrieves a value from a dictionary or returns the default value
    if the key is not present
    """
    if key in dct:
        return dct[key]
    else:
        return default
