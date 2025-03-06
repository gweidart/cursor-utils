"""
CLI interface for the install command.

Key Components:
    install(): CLI command for installing Cursor Utils

Project Dependencies:
    This file uses: click: For CLI interface
    This file uses: manager: For installation orchestration
    This file uses: utils.command_helpers: For standardized command execution
    This file is used by: cli: For command registration
"""

import click

from cursor_utils.commands.install.manager import InstallManager
from cursor_utils.errors import ErrorCodes, InstallError
from cursor_utils.utils.command_helpers import safe_execute_sync


@click.command()
@click.argument("project_path", type=click.Path(), default=".")
@click.option("--debug", is_flag=True, help="Enable debug output")
def install(project_path: str, debug: bool = False) -> None:
    """
    Install cursor-utils in a project.

    Args:
        project_path: Path to the project root
        debug: Whether to enable debug output

    """
    manager = InstallManager()

    if debug:
        manager.console.print("[#d7af00]Debug mode enabled[/#d7af00]")

    # Execute the installation with standardized error handling
    execute_install(manager, project_path, debug)


@safe_execute_sync(InstallError, ErrorCodes.INSTALL_FAILED)
def execute_install(
    manager: InstallManager, project_path: str, debug: bool = False
) -> None:
    """
    Execute the installation with standardized error handling.

    Args:
        manager: Installation manager
        project_path: Path to the project root
        debug: Whether to enable debug output

    Raises:
        InstallError: If installation fails

    """
    manager.install_to_project(project_path)
