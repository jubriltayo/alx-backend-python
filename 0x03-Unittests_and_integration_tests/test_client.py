#!/usr/bin/env python3
"""This module defines github client"""

import unittest
from unittest.mock import patch, MagicMock, PropertyMock, Mock
import client
import fixtures
from typing import Dict
from parameterized import parameterized, parameterized_class
from requests import HTTPError


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
            self.assertEqual(
                client.GithubOrgClient("google").public_repos(),
                [
                    ".allstar",
                    "abpackage"
                ],
            )
            mock_public_repos.assert_called_once()
        mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "apache-2.0"}}, "apache-2.0", True),
        ({"license": {"key": "apache-2.0"}}, "other", False)
    ])
    def test_has_license(self, repo: Dict, key: str, expected: bool) -> None:
        """test that license key matches expected result"""
        client_org = client.GithubOrgClient("google")
        client_license = client_org.has_license(repo, key)
        self.assertEqual(client_license, expected)

    @parameterized_class([
        {
            "org_payload": fixtures.TEST_PAYLOAD[0][0],
            "repos_payload": fixtures.TEST_PAYLOAD[0][1],
            "expected_repos": fixtures.TEST_PAYLOAD[0][2],
            "apache2_repos": fixtures.TEST_PAYLOAD[0][3]
        }
    ])
    class TestIntegrationGithubOrgClient(unittest.TestCase):
        """provides functionality to perform integration test on
            GithubOrgClient class
        """
        @classmethod
        def setUpClass(cls) -> None:
            """set up initial class"""
            route_payload = {
                "https://api.github.com/orgs/google": cls.org_payload,
                "https://api.github.com/orgs/google/repos": cls.repos_payload,
            }

            def get_payload(url):
                if url in route_payload:
                    return Mock(**{"json.return_value": route_payload[url]})
                return HTTPError

            cls.get_patcher = patch("requests.get", side_effect=get_payload)
            cls.get_patcher.start()

        def test_public_repos(self) -> None:
            """test public repos to return expected result"""
            self.assertEqual(
                client.GithubOrgClient("google").public_repos(),
                self.expected_repos
            )

        def test_public_repos_with_license(self) -> None:
            """test that public repos with license returns expected result"""
            self.assertEqual(
                client.GithubOrgClient("google")
                .public_repos(license="apache-2.0"),
                self.apache2_repos
            )

        @classmethod
        def tearDownClass(cls) -> None:
            """tears down the initial class fixtures"""
            cls.get_patcher.stop()
