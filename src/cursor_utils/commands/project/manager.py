"""
Manages local project analysis for sending to Gemini.

Key Components:
    ProjectManager: Handles analysis of local project directories

Project Dependencies:
    This file uses: rich: For console output
    This file uses: cursor_utils.commands.gemini: For Gemini API integration
    This file uses: cursor_utils.utils.file_rank_algo: For file ranking
    This file is used by: command: For CLI interface
"""

import os
from pathlib import Path

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from cursor_utils.commands.gemini.manager import GeminiManager
from cursor_utils.errors import ErrorCodes, RepoError

# Use RepoError for now, we can create a ProjectError class later if needed
ProjectError = RepoError


class ProjectManager:
    """Manages the local project analysis process."""

    def __init__(self) -> None:
        """Initialize the project manager."""
        self.console: Console = Console()
        self.gemini_manager: GeminiManager = GeminiManager()

    def create_progress(self) -> Progress:
        """
        Create a progress display for the analysis process.

        Returns:
            Progress display

        """
        return Progress(
            SpinnerColumn(),
            TextColumn("[#afafd7]{task.description}[/]"),
            console=self.console,
        )

    def validate_project_size(self, project_path: Path, max_size_mb: int) -> int:
        """
        Validate that the project size is within limits.

        Args:
            project_path: Path to the project directory
            max_size_mb: Maximum allowed size in MB

        Returns:
            Project size in MB

        Raises:
            ProjectError: If the project is too large

        """
        total_size = 0
        for dirpath, _, filenames in os.walk(project_path):
            for filename in filenames:
                file_path = Path(dirpath) / filename
                if file_path.is_file():
                    total_size += file_path.stat().st_size

        project_size_mb = total_size // (1024 * 1024)

        if project_size_mb > max_size_mb:
            raise ProjectError(
                message=f"Project is too large ({project_size_mb} MB)",
                code=ErrorCodes.REPO_TOO_LARGE,
                causes=[f"Maximum allowed size is {max_size_mb} MB"],
                hint_stmt="Try again with a smaller project or use --max-size to increase the limit.",
            )

        return project_size_mb
