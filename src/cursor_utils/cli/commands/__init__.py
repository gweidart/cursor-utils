"""
Command implementations for cursor-utils.

This package contains the implementations of the CLI commands.
Each command is implemented as a separate module.

Key Components:
    web: Web search command
    gemini: Gemini command
    github: GitHub command
    repo: Repository analysis command
    project: Project analysis command
    config: Configuration management command
    install: Installation command
    update: Update command

Project Dependencies:
    This file uses: None
    This file is used by: CLI parser
"""

# Import all commands to register them with the CLI
# The imports below will automatically register the commands with the CLI
# through the cli.add_command() calls in each module
from cursor_utils.cli.commands import (
    config,
    gemini,
    github,
    install,
    project,
    repo,
    update,
    web,
)
from cursor_utils.cli.parser import cli

# Register the commands with the CLI
cli.add_command(web.web_command)
cli.add_command(gemini.gemini_command)
cli.add_command(github.github_group)
cli.add_command(project.project_command)
cli.add_command(repo.repo_command)
cli.add_command(config.config_command)
cli.add_command(install.install_command)
cli.add_command(update.update_command)

__all__ = [
    "cli",
    "config",
    "gemini",
    "github",
    "install",
    "project",
    "repo",
    "update",
    "web",
]
