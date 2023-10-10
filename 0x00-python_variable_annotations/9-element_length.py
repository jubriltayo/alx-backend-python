#!/usr/bin/env python3
"""This module defines a function `element_length`"""
from typing import List, Tuple, Sequence, Iterable

Vector_Tuple = Tuple[Sequence, int]
Vector_List = List[Vector_Tuple]
Vector_Iterable = Iterable[Sequence]


def element_length(lst: Vector_Iterable) -> Vector_List:
    """
    Takes a list 'lst' as input and returns a new list of tuples.

    Args:
        lst (list): The input list containing elements of any data type.

    Returns:
        list: A list of tuples, where each tuple contains an item from the
        input list and its length.
    """
    return [(i, len(i)) for i in lst]
