"""
GitHub API client for cursor-utils.

Key Components:
    GitHubClient: Client for the GitHub API
    GitHubRepository: Representation of a GitHub repository
    GitHubIssue: Representation of a GitHub issue
    GitHubPullRequest: Representation of a GitHub pull request

Project Dependencies:
    This file uses: errors: For API-related errors
                   config: For API key management
    This file is used by: GitHub command
"""

import os
from dataclasses import dataclass
from typing import Any, Optional

import httpx

from cursor_utils.core.config import Configuration
from cursor_utils.core.errors import ServiceError


class GitHubError(ServiceError):
    """Error related to the GitHub API."""

    def __init__(
        self, message: str, exit_code: int = 12, help_text: Optional[str] = None
    ):
        super().__init__(message, "github", exit_code, help_text)


@dataclass
class GitHubRepository:
    """Representation of a GitHub repository."""

    name: str
    full_name: str
    description: str
    url: str
    html_url: str
    stars: int
    forks: int
    open_issues: int
    default_branch: str

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "GitHubRepository":
        """
        Create a repository from API data.

        Args:
            data: The API data

        Returns:
            The repository

        """
        return cls(
            name=data.get("name", ""),
            full_name=data.get("full_name", ""),
            description=data.get("description", ""),
            url=data.get("url", ""),
            html_url=data.get("html_url", ""),
            stars=data.get("stargazers_count", 0),
            forks=data.get("forks_count", 0),
            open_issues=data.get("open_issues_count", 0),
            default_branch=data.get("default_branch", "main"),
        )


@dataclass
class GitHubIssue:
    """Representation of a GitHub issue."""

    number: int
    title: str
    body: str
    url: str
    html_url: str
    state: str
    labels: list[str]
    created_at: str
    updated_at: str
    closed_at: Optional[str]

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "GitHubIssue":
        """
        Create an issue from API data.

        Args:
            data: The API data

        Returns:
            The issue

        """
        return cls(
            number=data.get("number", 0),
            title=data.get("title", ""),
            body=data.get("body", ""),
            url=data.get("url", ""),
            html_url=data.get("html_url", ""),
            state=data.get("state", ""),
            labels=[label.get("name", "") for label in data.get("labels", [])],
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", ""),
            closed_at=data.get("closed_at"),
        )


@dataclass
class GitHubPullRequest:
    """Representation of a GitHub pull request."""

    number: int
    title: str
    body: str
    url: str
    html_url: str
    state: str
    head: str
    base: str
    created_at: str
    updated_at: str
    closed_at: Optional[str]
    merged_at: Optional[str]

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "GitHubPullRequest":
        """
        Create a pull request from API data.

        Args:
            data: The API data

        Returns:
            The pull request

        """
        return cls(
            number=data.get("number", 0),
            title=data.get("title", ""),
            body=data.get("body", ""),
            url=data.get("url", ""),
            html_url=data.get("html_url", ""),
            state=data.get("state", ""),
            head=data.get("head", {}).get("ref", ""),
            base=data.get("base", {}).get("ref", ""),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", ""),
            closed_at=data.get("closed_at"),
            merged_at=data.get("merged_at"),
        )


class GitHubClient:
    """Client for the GitHub API."""

    def __init__(
        self, token: Optional[str] = None, config: Optional[Configuration] = None
    ):
        """
        Initialize the client.

        Args:
            token: The GitHub token, or None to use the configuration
            config: The configuration, or None to use the default

        Raises:
            GitHubError: If the token is not provided and not in the configuration

        """
        self.config = config or Configuration()
        self.token = token or self.config.get("github_token")

        if not self.token:
            self.token = os.environ.get("GITHUB_TOKEN")

        if not self.token:
            raise GitHubError(
                "GitHub token not found",
                help_text="Set the GITHUB_TOKEN environment variable or "
                "run 'cursor-utils config set github_token YOUR_TOKEN'",
            )

        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
        }

    async def get_repository_async(self, owner: str, repo: str) -> GitHubRepository:
        """
        Get a repository asynchronously.

        Args:
            owner: The repository owner
            repo: The repository name

        Returns:
            The repository

        Raises:
            GitHubError: If the repository cannot be retrieved

        """
        url = f"{self.base_url}/repos/{owner}/{repo}"

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, headers=self.headers)
                response.raise_for_status()
                return GitHubRepository.from_api(response.json())
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise GitHubError(
                    f"Repository not found: {owner}/{repo}",
                    help_text="Check the repository owner and name.",
                )
            else:
                raise GitHubError(
                    f"GitHub API error: {e.response.status_code} {e.response.reason_phrase}",
                    help_text=f"Response: {e.response.text}",
                )
        except httpx.RequestError as e:
            raise GitHubError(
                f"Failed to connect to GitHub API: {e}",
                help_text="Check your internet connection.",
            )
        except Exception as e:
            raise GitHubError(f"Unexpected error: {e}")

    def get_repository(self, owner: str, repo: str) -> GitHubRepository:
        """
        Get a repository.

        Args:
            owner: The repository owner
            repo: The repository name

        Returns:
            The repository

        Raises:
            GitHubError: If the repository cannot be retrieved

        """
        url = f"{self.base_url}/repos/{owner}/{repo}"

        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.get(url, headers=self.headers)
                response.raise_for_status()
                return GitHubRepository.from_api(response.json())
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise GitHubError(
                    f"Repository not found: {owner}/{repo}",
                    help_text="Check the repository owner and name.",
                )
            else:
                raise GitHubError(
                    f"GitHub API error: {e.response.status_code} {e.response.reason_phrase}",
                    help_text=f"Response: {e.response.text}",
                )
        except httpx.RequestError as e:
            raise GitHubError(
                f"Failed to connect to GitHub API: {e}",
                help_text="Check your internet connection.",
            )
        except Exception as e:
            raise GitHubError(f"Unexpected error: {e}")

    async def get_issues_async(
        self,
        owner: str,
        repo: str,
        state: str = "open",
        labels: Optional[list[str]] = None,
    ) -> list[GitHubIssue]:
        """
        Get issues for a repository asynchronously.

        Args:
            owner: The repository owner
            repo: The repository name
            state: The issue state (open, closed, all)
            labels: The issue labels

        Returns:
            The issues

        Raises:
            GitHubError: If the issues cannot be retrieved

        """
        url = f"{self.base_url}/repos/{owner}/{repo}/issues"
        params: dict[str, Any] = {"state": state}

        if labels:
            params["labels"] = ",".join(labels)

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                return [GitHubIssue.from_api(issue) for issue in response.json()]
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise GitHubError(
                    f"Repository not found: {owner}/{repo}",
                    help_text="Check the repository owner and name.",
                )
            else:
                raise GitHubError(
                    f"GitHub API error: {e.response.status_code} {e.response.reason_phrase}",
                    help_text=f"Response: {e.response.text}",
                )
        except httpx.RequestError as e:
            raise GitHubError(
                f"Failed to connect to GitHub API: {e}",
                help_text="Check your internet connection.",
            )
        except Exception as e:
            raise GitHubError(f"Unexpected error: {e}")

    def get_issues(
        self,
        owner: str,
        repo: str,
        state: str = "open",
        labels: Optional[list[str]] = None,
    ) -> list[GitHubIssue]:
        """
        Get issues for a repository.

        Args:
            owner: The repository owner
            repo: The repository name
            state: The issue state (open, closed, all)
            labels: The issue labels

        Returns:
            The issues

        Raises:
            GitHubError: If the issues cannot be retrieved

        """
        url = f"{self.base_url}/repos/{owner}/{repo}/issues"
        params: dict[str, Any] = {"state": state}

        if labels:
            params["labels"] = ",".join(labels)

        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                return [GitHubIssue.from_api(issue) for issue in response.json()]
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise GitHubError(
                    f"Repository not found: {owner}/{repo}",
                    help_text="Check the repository owner and name.",
                )
            else:
                raise GitHubError(
                    f"GitHub API error: {e.response.status_code} {e.response.reason_phrase}",
                    help_text=f"Response: {e.response.text}",
                )
        except httpx.RequestError as e:
            raise GitHubError(
                f"Failed to connect to GitHub API: {e}",
                help_text="Check your internet connection.",
            )
        except Exception as e:
            raise GitHubError(f"Unexpected error: {e}")

    async def get_pull_requests_async(
        self, owner: str, repo: str, state: str = "open", base: Optional[str] = None
    ) -> list[GitHubPullRequest]:
        """
        Get pull requests for a repository asynchronously.

        Args:
            owner: The repository owner
            repo: The repository name
            state: The pull request state (open, closed, all)
            base: The base branch

        Returns:
            The pull requests

        Raises:
            GitHubError: If the pull requests cannot be retrieved

        """
        url = f"{self.base_url}/repos/{owner}/{repo}/pulls"
        params: dict[str, Any] = {"state": state}

        if base:
            params["base"] = base

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                return [GitHubPullRequest.from_api(pr) for pr in response.json()]
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise GitHubError(
                    f"Repository not found: {owner}/{repo}",
                    help_text="Check the repository owner and name.",
                )
            else:
                raise GitHubError(
                    f"GitHub API error: {e.response.status_code} {e.response.reason_phrase}",
                    help_text=f"Response: {e.response.text}",
                )
        except httpx.RequestError as e:
            raise GitHubError(
                f"Failed to connect to GitHub API: {e}",
                help_text="Check your internet connection.",
            )
        except Exception as e:
            raise GitHubError(f"Unexpected error: {e}")

    def get_pull_requests(
        self, owner: str, repo: str, state: str = "open", base: Optional[str] = None
    ) -> list[GitHubPullRequest]:
        """
        Get pull requests for a repository.

        Args:
            owner: The repository owner
            repo: The repository name
            state: The pull request state (open, closed, all)
            base: The base branch

        Returns:
            The pull requests

        Raises:
            GitHubError: If the pull requests cannot be retrieved

        """
        url = f"{self.base_url}/repos/{owner}/{repo}/pulls"
        params: dict[str, Any] = {"state": state}

        if base:
            params["base"] = base

        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                return [GitHubPullRequest.from_api(pr) for pr in response.json()]
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise GitHubError(
                    f"Repository not found: {owner}/{repo}",
                    help_text="Check the repository owner and name.",
                )
            else:
                raise GitHubError(
                    f"GitHub API error: {e.response.status_code} {e.response.reason_phrase}",
                    help_text=f"Response: {e.response.text}",
                )
        except httpx.RequestError as e:
            raise GitHubError(
                f"Failed to connect to GitHub API: {e}",
                help_text="Check your internet connection.",
            )
        except Exception as e:
            raise GitHubError(f"Unexpected error: {e}")

    async def create_issue_async(
        self,
        owner: str,
        repo: str,
        title: str,
        body: str,
        labels: Optional[list[str]] = None,
    ) -> GitHubIssue:
        """
        Create an issue asynchronously.

        Args:
            owner: The repository owner
            repo: The repository name
            title: The issue title
            body: The issue body
            labels: The issue labels

        Returns:
            The created issue

        Raises:
            GitHubError: If the issue cannot be created

        """
        url = f"{self.base_url}/repos/{owner}/{repo}/issues"
        data: dict[str, Any] = {"title": title, "body": body}

        if labels:
            data["labels"] = labels

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, headers=self.headers, json=data)
                response.raise_for_status()
                return GitHubIssue.from_api(response.json())
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise GitHubError(
                    f"Repository not found: {owner}/{repo}",
                    help_text="Check the repository owner and name.",
                )
            else:
                raise GitHubError(
                    f"GitHub API error: {e.response.status_code} {e.response.reason_phrase}",
                    help_text=f"Response: {e.response.text}",
                )
        except httpx.RequestError as e:
            raise GitHubError(
                f"Failed to connect to GitHub API: {e}",
                help_text="Check your internet connection.",
            )
        except Exception as e:
            raise GitHubError(f"Unexpected error: {e}")

    def create_issue(
        self,
        owner: str,
        repo: str,
        title: str,
        body: str,
        labels: Optional[list[str]] = None,
    ) -> GitHubIssue:
        """
        Create an issue.

        Args:
            owner: The repository owner
            repo: The repository name
            title: The issue title
            body: The issue body
            labels: The issue labels

        Returns:
            The created issue

        Raises:
            GitHubError: If the issue cannot be created

        """
        url = f"{self.base_url}/repos/{owner}/{repo}/issues"
        data: dict[str, Any] = {"title": title, "body": body}

        if labels:
            data["labels"] = labels

        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.post(url, headers=self.headers, json=data)
                response.raise_for_status()
                return GitHubIssue.from_api(response.json())
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise GitHubError(
                    f"Repository not found: {owner}/{repo}",
                    help_text="Check the repository owner and name.",
                )
            else:
                raise GitHubError(
                    f"GitHub API error: {e.response.status_code} {e.response.reason_phrase}",
                    help_text=f"Response: {e.response.text}",
                )
        except httpx.RequestError as e:
            raise GitHubError(
                f"Failed to connect to GitHub API: {e}",
                help_text="Check your internet connection.",
            )
        except Exception as e:
            raise GitHubError(f"Unexpected error: {e}")

    async def create_pull_request_async(
        self, owner: str, repo: str, title: str, body: str, head: str, base: str
    ) -> GitHubPullRequest:
        """
        Create a pull request asynchronously.

        Args:
            owner: The repository owner
            repo: The repository name
            title: The pull request title
            body: The pull request body
            head: The head branch
            base: The base branch

        Returns:
            The created pull request

        Raises:
            GitHubError: If the pull request cannot be created

        """
        url = f"{self.base_url}/repos/{owner}/{repo}/pulls"
        data = {"title": title, "body": body, "head": head, "base": base}

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, headers=self.headers, json=data)
                response.raise_for_status()
                return GitHubPullRequest.from_api(response.json())
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise GitHubError(
                    f"Repository not found: {owner}/{repo}",
                    help_text="Check the repository owner and name.",
                )
            elif e.response.status_code == 422:
                raise GitHubError(
                    f"Invalid pull request: {e.response.text}",
                    help_text="Check the head and base branches.",
                )
            else:
                raise GitHubError(
                    f"GitHub API error: {e.response.status_code} {e.response.reason_phrase}",
                    help_text=f"Response: {e.response.text}",
                )
        except httpx.RequestError as e:
            raise GitHubError(
                f"Failed to connect to GitHub API: {e}",
                help_text="Check your internet connection.",
            )
        except Exception as e:
            raise GitHubError(f"Unexpected error: {e}")

    def create_pull_request(
        self, owner: str, repo: str, title: str, body: str, head: str, base: str
    ) -> GitHubPullRequest:
        """
        Create a pull request.

        Args:
            owner: The repository owner
            repo: The repository name
            title: The pull request title
            body: The pull request body
            head: The head branch
            base: The base branch

        Returns:
            The created pull request

        Raises:
            GitHubError: If the pull request cannot be created

        """
        url = f"{self.base_url}/repos/{owner}/{repo}/pulls"
        data = {"title": title, "body": body, "head": head, "base": base}

        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.post(url, headers=self.headers, json=data)
                response.raise_for_status()
                return GitHubPullRequest.from_api(response.json())
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise GitHubError(
                    f"Repository not found: {owner}/{repo}",
                    help_text="Check the repository owner and name.",
                )
            elif e.response.status_code == 422:
                raise GitHubError(
                    f"Invalid pull request: {e.response.text}",
                    help_text="Check the head and base branches.",
                )
            else:
                raise GitHubError(
                    f"GitHub API error: {e.response.status_code} {e.response.reason_phrase}",
                    help_text=f"Response: {e.response.text}",
                )
        except httpx.RequestError as e:
            raise GitHubError(
                f"Failed to connect to GitHub API: {e}",
                help_text="Check your internet connection.",
            )
        except Exception as e:
            raise GitHubError(f"Unexpected error: {e}")
