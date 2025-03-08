"""
Git utilities for cursor-utils.

Key Components:
    clone_repository: Clone a Git repository
    get_default_branch: Get the default branch of a repository
    get_repository_root: Get the root directory of a Git repository
    is_git_repository: Check if a directory is a Git repository

Project Dependencies:
    This file uses: errors: For Git-related errors
    This file is used by: CLI commands and service clients
"""

import subprocess
from pathlib import Path
from typing import Optional, Union

from cursor_utils.core.errors import CommandError
from cursor_utils.utils.fs import ensure_directory


class GitError(CommandError):
    """Error related to Git operations."""

    def __init__(
        self, message: str, exit_code: int = 6, help_text: Optional[str] = None
    ):
        super().__init__(message, exit_code, help_text)


def _run_git_command(
    args: list[str], cwd: Optional[Union[str, Path]] = None, capture_output: bool = True
) -> str:
    """
    Run a Git command.

    Args:
        args: The Git command arguments
        cwd: The working directory
        capture_output: Whether to capture the command output

    Returns:
        The command output

    Raises:
        GitError: If the command fails

    """
    try:
        cmd = ["git", *args]
        result = subprocess.run(
            cmd, cwd=cwd, capture_output=capture_output, text=True, check=True
        )
        return result.stdout.strip() if capture_output else ""
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.strip() if e.stderr else str(e)
        raise GitError(
            f"Git command failed: {error_message}",
            help_text=f"Command: git {' '.join(args)}",
        )
    except Exception as e:
        raise GitError(
            f"Failed to run Git command: {e}",
            help_text=f"Command: git {' '.join(args)}",
        )


def is_git_repository(path: Union[str, Path]) -> bool:
    """
    Check if a directory is a Git repository.

    Args:
        path: The directory path

    Returns:
        True if the directory is a Git repository, False otherwise

    """
    try:
        _run_git_command(["rev-parse", "--is-inside-work-tree"], cwd=path)
        return True
    except GitError:
        return False


def get_repository_root(path: Union[str, Path]) -> Path:
    """
    Get the root directory of a Git repository.

    Args:
        path: A path within the repository

    Returns:
        The repository root path

    Raises:
        GitError: If the path is not within a Git repository

    """
    if not is_git_repository(path):
        raise GitError(
            f"Not a Git repository: {path}",
            help_text="Ensure the path is within a Git repository.",
        )

    root = _run_git_command(["rev-parse", "--show-toplevel"], cwd=path)
    return Path(root)


def get_default_branch(path: Union[str, Path]) -> str:
    """
    Get the default branch of a repository.

    Args:
        path: A path within the repository

    Returns:
        The default branch name

    Raises:
        GitError: If the default branch cannot be determined

    """
    if not is_git_repository(path):
        raise GitError(
            f"Not a Git repository: {path}",
            help_text="Ensure the path is within a Git repository.",
        )

    try:
        # Try to get the default branch from the remote
        remote_head = _run_git_command(
            ["symbolic-ref", "refs/remotes/origin/HEAD"], cwd=path
        )
        return remote_head.split("/")[-1]
    except GitError:
        # Fall back to the current branch
        try:
            current_branch = _run_git_command(
                ["symbolic-ref", "--short", "HEAD"], cwd=path
            )
            return current_branch
        except GitError:
            # Fall back to "main" or "master"
            for branch in ["main", "master"]:
                try:
                    _run_git_command(["rev-parse", "--verify", branch], cwd=path)
                    return branch
                except GitError:
                    pass

            raise GitError(
                "Failed to determine default branch",
                help_text="Specify the branch explicitly.",
            )


def clone_repository(
    url: str,
    target_dir: Union[str, Path],
    branch: Optional[str] = None,
    depth: Optional[int] = None,
) -> Path:
    """
    Clone a Git repository.

    Args:
        url: The repository URL
        target_dir: The target directory
        branch: The branch to clone, or None for the default branch
        depth: The clone depth, or None for a full clone

    Returns:
        The repository path

    Raises:
        GitError: If the repository cannot be cloned

    """
    target_path = Path(target_dir)

    # Ensure the target directory exists
    ensure_directory(target_path.parent)

    # Build the clone command
    cmd = ["clone"]
    if branch:
        cmd.extend(["--branch", branch])
    if depth:
        cmd.extend(["--depth", str(depth)])
    cmd.extend([url, str(target_path)])

    # Clone the repository
    try:
        _run_git_command(cmd, capture_output=False)
        return target_path
    except GitError as e:
        raise GitError(
            f"Failed to clone repository: {e.message}", help_text=f"URL: {url}"
        )
