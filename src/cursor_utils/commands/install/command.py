"""
CLI interface for the install command.

Key Components:
    install(): CLI command for installing Cursor Utils

Project Dependencies:
    This file uses: click: For CLI interface
    This file uses: manager: For installation orchestration
    This file is used by: cli: For command registration
"""

import click

from cursor_utils.commands.install.manager import InstallManager
from cursor_utils.errors import ErrorCodes, InstallError


@click.command()
@click.argument("project_path", type=click.Path(), default=".")
@click.option("--debug", is_flag=True, help="Enable debug output")
def install(project_path: str, debug: bool = False) -> None:
    """Install cursor-utils in a project."""
    manager = InstallManager()

    if debug:
        manager.console.print("[#d7af00]Debug mode enabled[/#d7af00]")

    try:
        manager.install_to_project(project_path)
    except InstallError as e:
        manager.console.print(f"[#d70000]✗[/#d70000] {e!s}")
        if debug:
            manager.console.print_exception()
        raise click.exceptions.Exit(1)
    except Exception as e:
        error = InstallError(
            message="An unexpected error occurred",
            code=ErrorCodes.UNKNOWN_ERROR,
            causes=[str(e)],
            hint_stmt="Check the logs for more details.",
        )
        manager.console.print(f"[#d70000]✗[/#d70000] {error!s}")
        if debug:
            manager.console.print_exception()
        raise click.exceptions.Exit(1)
