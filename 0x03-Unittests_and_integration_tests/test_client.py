#!/usr/bin/env python3
"""This module defines github client"""

import unittest
from unittest.mock import patch, MagicMock
import client
from typing import Dict
from parameterized import parameterized


class TestGithubOrgClient(unittest.TestCase):
    """test github client"""

    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"}),
    ])
    @patch("client.get_json")
    def test_org(self, org: str, response: Dict,
                 mocked_fn: MagicMock) -> None:
        """test GithubOrgClient returns as expected"""
        mocked_fn.return_value = MagicMock(return_value=response)
        github_client = client.GithubOrgClient(org)
        self.assertEqual(github_client.org(), response)
        mocked_fn.assert_called_once_with(f"https://api.github.com/orgs/{org}")
