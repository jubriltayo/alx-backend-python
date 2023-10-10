#!/usr/bin/env python3
"""This module defines a function `sum_mixed_list`"""
from typing import List, Union

Vector_Union = Union[int, float]
Vector_List = List[Vector_Union]


def sum_mixed_list(mxd_ldt: Vector_List) -> float:
    """ Returns the total sum of elements in a list"""
    total = 0
    for n in mxd_ldt:
        total += n
    return total
