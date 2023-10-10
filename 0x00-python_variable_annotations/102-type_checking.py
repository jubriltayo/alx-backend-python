#!/usr/bin/env python3
"""This module defines a function `safe_first_element`"""
from typing import List, Tuple


def zoom_array(lst: Tuple, factor: int = 2) -> List:
    """
    zoom_array (repeats) the items in the tuple 'lst' by
        the specified 'factor'

    Args:
        lst (Tuple): The input tuple containing elements.
        factor (int): Determines how many times each item will be repeated.

    Returns:
        List: The new tuple containing zoomed elements based on the factor.
    """

    zoomed_in: List = [
        item for item in lst
        for i in range(factor)
    ]
    return zoomed_in


array = (12, 72, 91)

zoom_2x = zoom_array(array)

zoom_3x = zoom_array(array, 3)
