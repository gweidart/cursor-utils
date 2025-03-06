"""
GitHub manager for configuration and API access.

Key Components:
    GitHubManager: Manages GitHub configuration and API access

Project Dependencies:
    This file uses: PyGithub: For GitHub API integration
    This file uses: config: For configuration management
    This file uses: errors: For standardized error handling
    This file is used by: actions: For GitHub operations
"""

import os
from pathlib import Path
from typing import Optional, cast

from github import Github, GithubException
from github.Repository import Repository

from cursor_utils.config import Config
from cursor_utils.errors import ErrorCodes, GitHubError
from cursor_utils.types import GitHubConfig


class GitHubManager:
    """Manages GitHub configuration and API access."""

    def __init__(self) -> None:
        """Initialize the GitHub manager."""
        self.config = Config()
        self.github: Optional[Github] = None
        self.github_config: Optional[GitHubConfig] = None
        self._load_config()

    def _load_config(self) -> None:
        """Load GitHub configuration from config file."""
        config_dict = self.config.load_config()
        if "github" in config_dict:
            self.github_config = cast(GitHubConfig, config_dict["github"])  # type: ignore
        else:
            self.github_config = {
                "token_source": "env",
                "default_owner": "",
                "default_repo": "",
                "template_dir": str(Path.home() / ".cursor-utils" / "github-templates"),
            }
            # Save default config
            self.config.save_config({"github": self.github_config, **config_dict})

    def get_github_client(self) -> Github:
        """Get authenticated GitHub client."""
        if self.github is not None:
            return self.github

        token = self._get_token()
        if not token:
            raise GitHubError(
                message="GitHub token not found",
                code=ErrorCodes.GITHUB_AUTH_ERROR,
                causes=["GitHub token not found in environment or config"],
                hint_stmt="Set GITHUB_TOKEN environment variable or configure via 'cursor-utils config github'",
            )

        try:
            self.github = Github(token)
            # Test authentication
            self.github.get_user().login  # noqa: B018
            return self.github
        except GithubException as e:
            raise GitHubError(
                message="GitHub authentication failed",
                code=ErrorCodes.GITHUB_AUTH_ERROR,
                causes=[str(e)],
                hint_stmt="Check your GitHub token and permissions",
            )

    def _get_token(self) -> Optional[str]:
        """Get GitHub token from environment or config."""
        if not self.github_config:
            return os.getenv("GITHUB_TOKEN")

        if self.github_config["token_source"] == "env":
            return os.getenv("GITHUB_TOKEN")
        else:
            # Get from config
            return self.config.get_api_key("GITHUB_TOKEN")  # type: ignore

    def get_repository(self, owner: Optional[str], repo: Optional[str]) -> Repository:
        """Get GitHub repository."""
        github = self.get_github_client()

        # Use provided owner/repo or defaults
        final_owner = owner or (
            self.github_config and self.github_config.get("default_owner", "")
        )
        final_repo = repo or (
            self.github_config and self.github_config.get("default_repo", "")
        )

        if not final_owner or not final_repo:
            raise GitHubError(
                message="Repository owner and name required",
                code=ErrorCodes.GITHUB_REPO_NOT_FOUND,
                causes=["Owner or repository name not provided"],
                hint_stmt="Provide owner and repository name or set defaults via 'cursor-utils config github'",
            )

        try:
            return github.get_repo(f"{final_owner}/{final_repo}")
        except GithubException as e:
            raise GitHubError(
                message=f"Repository {final_owner}/{final_repo} not found",
                code=ErrorCodes.GITHUB_REPO_NOT_FOUND,
                causes=[str(e)],
                hint_stmt="Check repository name and your access permissions",
            )
