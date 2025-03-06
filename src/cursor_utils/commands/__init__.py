"""
Commands package for cursor-utils.

Key Components:
    config: Configuration management commands
    install: Installation commands
    update: Update commands
    web: Web search commands
    gemini: Google Gemini commands
    repo: Repository analysis commands
    project: Local project analysis commands
    github: GitHub repository management commands

Project Dependencies:
    This file uses: command modules: For command implementations
    This file is used by: cli: For command registration
"""

from cursor_utils.commands.config import config
from cursor_utils.commands.gemini import gemini
from cursor_utils.commands.github import github
from cursor_utils.commands.install import install
from cursor_utils.commands.project import project
from cursor_utils.commands.repo import repo
from cursor_utils.commands.update import update
from cursor_utils.commands.web import web

__all__ = ["config", "gemini", "github", "install", "project", "repo", "update", "web"]
