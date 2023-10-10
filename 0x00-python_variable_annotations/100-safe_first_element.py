#!/usr/bin/env python3
"""This module defines a function `safe_first_element`
"""
from typing import Union, Any, Sequence

# Any - when type of element is unknown
Vector_Union = Union[Any, None]
Vector_Sequence = Sequence[Any]


def safe_first_element(lst: Vector_Sequence) -> Vector_Union:
    """
    Recieves the first element from the input list

    Args:
        lst (Sequence[Any]): The input list.

    Returns:
        Union[Any, None]: The first element of the list or 'None' if
        the list is empty.
    """
    if lst:
        return lst[0]
    else:
        return None
