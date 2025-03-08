"""
Updater service for cursor-utils.

Key Components:
    UpdaterService: Service for checking for updates and updating the package

Project Dependencies:
    This file uses: requests: For making HTTP requests to GitHub API
                    subprocess: For running shell commands
                    packaging.version: For comparing version strings
    This file is used by: update command
"""

import re
import subprocess
import sys
from pathlib import Path
from re import Match
from typing import Optional

import requests
from packaging import version
from rich.console import Console

from cursor_utils.core.errors import CommandError
from cursor_utils.utils.fs import ensure_directory, read_file, write_file


class UpdateError(CommandError):
    """Error related to updating cursor-utils."""

    def __init__(
        self,
        message: str,
        exit_code: int = 1,
        help_text: Optional[str] = None,
    ):
        super().__init__(message, exit_code, help_text)


class UpdaterService:
    """Service for checking for updates and updating the package."""

    def __init__(self, console: Optional[Console] = None):
        """
        Initialize the updater service.

        Args:
            console: Console for output, or None to create a new one

        """
        self.console = console or Console()
        self.repo_owner = "gweidart"
        self.repo_name = "cursor-utils"

    def get_current_version(self) -> str:
        """
        Get the current version of cursor-utils.

        Returns:
            The current version string

        Raises:
            UpdateError: If the version cannot be determined

        """
        try:
            # First try to get the version from the package
            from cursor_utils.version import __version__

            return __version__
        except ImportError:
            # If that fails, try to get it from the cursor-utils.mdc file
            try:
                rules_dir = Path.home() / ".cursor" / "rules"
                mdc_file = rules_dir / "cursor-utils.mdc"

                if not mdc_file.exists():
                    raise UpdateError(
                        "Could not find cursor-utils.mdc file. Please run 'cursor-utils install' first."
                    )

                content = read_file(mdc_file)
                if isinstance(content, bytes):
                    content = content.decode('utf-8')

                version_match: Optional[Match[str]] = re.search(
                    r'version:\s*"([^"]+)"', content
                )
                if version_match:
                    return version_match.group(1)

                # If no version is found in the file, use a default
                return "0.0.0"
            except Exception as e:
                raise UpdateError(f"Could not determine current version: {e}")

    def get_latest_version(self) -> str:
        """
        Get the latest version of cursor-utils from GitHub.

        Returns:
            The latest version string

        Raises:
            UpdateError: If the latest version cannot be determined

        """
        try:
            response = requests.get(
                f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/releases/latest",
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()
            return data["tag_name"].lstrip("v")
        except requests.RequestException as e:
            raise UpdateError(f"Could not fetch latest version: {e}")
        except (KeyError, ValueError) as e:
            raise UpdateError(f"Could not parse latest version: {e}")

    def needs_update(self) -> tuple[bool, str, str]:
        """
        Check if cursor-utils needs an update.

        Returns:
            A tuple of (needs_update, current_version, latest_version)

        Raises:
            UpdateError: If the version check fails

        """
        current_version = self.get_current_version()
        latest_version = self.get_latest_version()

        try:
            return (
                version.parse(latest_version) > version.parse(current_version),
                current_version,
                latest_version,
            )
        except Exception as e:
            raise UpdateError(f"Could not compare versions: {e}")

    def update_package(self, force: bool = False) -> bool:
        """
        Update cursor-utils to the latest version.

        Args:
            force: Force update even if already up to date

        Returns:
            True if the update was successful, False otherwise

        Raises:
            UpdateError: If the update fails

        """
        needs_update, _, latest_version = self.needs_update()

        if not needs_update and not force:
            return False

        # Determine the best way to update based on how cursor-utils was installed
        try:
            # Try to update using pip
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "--upgrade", "cursor-utils"],
                capture_output=True,
                text=True,
                check=False,
            )

            if result.returncode != 0:
                raise UpdateError(
                    f"Failed to update cursor-utils: {result.stderr}",
                    help_text="Try updating manually with 'pip install --upgrade cursor-utils'",
                )

            # Update the cursor-utils.mdc file with the new version
            self._update_mdc_file(latest_version)

            return True
        except Exception as e:
            raise UpdateError(f"Failed to update cursor-utils: {e}")

    def _update_mdc_file(self, new_version: str) -> None:
        """
        Update the cursor-utils.mdc file with the new version.

        Args:
            new_version: The new version string

        Raises:
            UpdateError: If the file cannot be updated

        """
        try:
            rules_dir = Path.home() / ".cursor" / "rules"
            mdc_file = rules_dir / "cursor-utils.mdc"

            if not mdc_file.exists():
                # Copy the new version from the package
                source_file = (
                    Path(__file__).parent.parent / "models" / "cursor-utils.mdc"
                )
                ensure_directory(rules_dir)
                content = read_file(source_file)
            else:
                content = read_file(mdc_file)

            # Ensure content is a string
            if isinstance(content, bytes):
                content = content.decode('utf-8')

            # Update the version in the file
            if "version:" in content:
                content = re.sub(
                    r'version:\s*"[^"]+"',
                    f'version: "{new_version}"',
                    content,
                )
            else:
                # Add version if it doesn't exist
                content = content.replace(
                    "description: cursor-utils",
                    f'description: cursor-utils\nversion: "{new_version}"',
                )

            write_file(mdc_file, content)
        except Exception as e:
            raise UpdateError(f"Failed to update cursor-utils.mdc file: {e}")
