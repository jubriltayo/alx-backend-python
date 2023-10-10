#!/usr/bin/env python3
"""This module defines a function `sum_list`"""
from typing import List


def sum_list(input_list: List[float]) -> float:
    """returns the sum of list elements"""
    total = 0
    for n in input_list:
        total += n
    return total
