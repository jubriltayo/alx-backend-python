#!/usr/bin/env python3
"""This module defines unit testing for test cases"""

from utils import access_nested_map, get_json
import unittest
from unittest.mock import patch
from parameterized import parameterized
from typing import Mapping, Tuple, Union, Type, Dict


class TestAccessNestedMap(unittest.TestCase):
    """ Tests for nested map function using parameterization"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map: Mapping, path: Tuple[str],
                               expected: Union[Mapping, int]) -> None:
        """Unit Test for different test cases"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError),
    ])
    def test_access_nested_map_exception(self, nested_map: Mapping,
                                         path: Tuple[str],
                                         expected: Type[Exception]) -> None:
        """Unit test for different test cases"""
        with self.assertRaises(expected):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Tests for get jdon function using parameterization"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(self, test_url: str, test_payload: Dict[str, bool]):
        """tests for HTTP request using mock"""
        # create mock with patch (as context manager)
        with patch("requests.get") as mock:
            mock.return_value.json.return_value = test_payload
            self.assertEqual(get_json(test_url), test_payload)

            # test that `get` method was called once
            mock.assert_called_once_with(test_url)
