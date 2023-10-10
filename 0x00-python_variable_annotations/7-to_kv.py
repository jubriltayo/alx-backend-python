#!/usr/bin/env python3
"""This module defines a function `to_kv`"""
from typing import Union, Tuple

Vector_Union = Union[int, float]
Vector_Tuple = Tuple[str, float]


def to_kv(k: str, v: Vector_Union) -> Vector_Tuple:
    """returns the sum of list elements"""
    return (k, v**2)
