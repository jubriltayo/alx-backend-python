#!/usr/bin/env python3
"""This module defines unit testing for test cases"""

from utils import access_nested_map
import unittest
from parameterized import parameterized
from typing import Mapping, Tuple, Union


class TestAccessNestedMap(unittest.TestCase):
    """ Class for Unit Tests using parameterization"""
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map: Mapping, path: Tuple[str],
                               expected: Union[Mapping, int]) -> None:
        """Unit Test for different test cases"""
        self.assertEqual(access_nested_map(nested_map, path), expected)
