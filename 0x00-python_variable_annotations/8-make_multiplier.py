#!/usr/bin/env python3
"""This module defines a function `make_multiplier`"""
from typing import Callable

Vector_Callable = Callable[[float], float]


def make_multiplier(multiplier: float) -> Vector_Callable:
    """Create a multiplier function based on the provided multiplier value"""
    def multiples(n: float) -> float:
        """Multiply the given number by the stored multiplier value."""
        return n * multiplier
    return multiples
