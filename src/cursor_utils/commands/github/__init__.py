"""
GitHub command for repository management.

Key Components:
    github: GitHub command for repository management

Project Dependencies:
    This file uses: PyGithub: For GitHub API integration
    This file is used by: cli: For command registration
"""

from cursor_utils.commands.github.command import github

__all__ = ["github"]
