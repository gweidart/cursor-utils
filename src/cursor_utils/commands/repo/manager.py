"""
Orchestrates repository operations and manages state.

Key Components:
    RepoManager: Coordinates repository cloning, analysis, and Gemini queries

Project Dependencies:
    This file uses: rich: For console output
    This file uses: cursor_utils.commands.gemini: For Gemini API integration
    This file uses: cursor_utils.utils.file_rank_algo: For file ranking
    This file is used by: command: For CLI interface
"""

import os
import tempfile
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from cursor_utils.commands.gemini.manager import GeminiManager
from cursor_utils.errors import ErrorCodes, RepoError


class RepoManager:
    """Manages the repository analysis process."""

    def __init__(self) -> None:
        """Initialize the repo manager."""
        self.console: Console = Console()
        self.gemini_manager: GeminiManager = GeminiManager()
        self.temp_dir: Optional[tempfile.TemporaryDirectory[str]] = None

    def create_temp_dir(self) -> Path:
        """
        Create a temporary directory for cloning the repository.

        Returns:
            Path to the temporary directory

        """
        self.temp_dir = tempfile.TemporaryDirectory[str](prefix="cursor_utils_repo_")
        return Path(self.temp_dir.name)

    def cleanup(self) -> None:
        """Clean up temporary files and directories."""
        if self.temp_dir:
            try:
                self.temp_dir.cleanup()
            except Exception:  # noqa: S110
                # Best effort cleanup
                pass
            self.temp_dir = None

    def create_progress(self) -> Progress:
        """Create a rich progress display for long-running operations."""
        return Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            console=self.console,
        )

    def validate_repo_size(self, repo_path: Path, max_size_mb: int) -> int:
        """
        Validate that the repository size is within limits.

        Args:
            repo_path: Path to the repository
            max_size_mb: Maximum allowed size in MB

        Returns:
            Total size in bytes

        Raises:
            RepoError: If the repository is too large

        """
        total_size = 0
        max_size_bytes = max_size_mb * 1024 * 1024

        for dirpath, _, filenames in os.walk(repo_path):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(file_path)
                except OSError:
                    pass

        if total_size > max_size_bytes:
            raise RepoError(
                message=f"Repository is too large ({total_size // (1024 * 1024)} MB)",
                code=ErrorCodes.REPO_TOO_LARGE,
                causes=[f"Maximum allowed size is {max_size_mb} MB"],
                hint_stmt="Try again with a smaller repository or use --max-size to increase the limit.",
            )

        return total_size
