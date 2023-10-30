#!/usr/bin/env python3
"""This module defines github client"""

import unittest
from unittest.mock import patch, MagicMock, PropertyMock
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

    def test_public_repos_url(self) -> None:
        """test public repos url to give correct result"""
        with patch("client.GithubOrgClient.org",
                   new_callable=PropertyMock) as mock:
            mock.return_value = {
                "repos_url": "https://api.github.com/users/google/repos"
            }
            self.assertEqual(
                client.GithubOrgClient("google")._public_repos_url,
                "https://api.github.com/users/google/repos"
            )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json: MagicMock) -> None:
        """test public repos to give correct result"""
        test_payload = {
            "repos_url": "https://api.github.com/users/google/repos",
            "repos": [
                {
                    "id": 460600860,
                    "name": ".allstar",
                    "private": False,
                    "owner": {
                        "login": "google",
                        "id": 1342004,
                    },
                    "fork": False,
                    "url": "https://api.github.com/repos/google/.allstar",
                    "created_at": "2022-02-17T20:40:32Z",
                    "updated_at": "2023-04-03T17:58:33Z",
                    "has_issues": True,
                    "forks": 3,
                    "default_branch": "main"
                },
                {
                    "id": 91820777,
                    "name": "abpackage",
                    "private": False,
                    "owner": {
                        "login": "google",
                        "id": 1342004,
                    },
                    "fork": False,
                    "url": "https://api.github.com/repos/google/abpackage",
                    "created_at": "2017-05-19T15:38:35Z",
                    "updated_at": "2023-09-29T05:40:56Z",
                    "has_issues": False,
                    "forks": 18,
                    "default_branch": "master"
                }
            ]
        }
        mock_get_json.return_value = test_payload["repos"]
        with patch("client.GithubOrgClient._public_repos_url",
                   new_callable=PropertyMock) as mock_public_repos:
            mock_public_repos.return_value = test_payload["repos_url"]
            self.assertEqual(client.GithubOrgClient("google").public_repos(),
                            [".allstar",
                              "abpackage"
                            ])
            mock_public_repos.assert_called_once()
        mock_get_json.assert_called_once()
