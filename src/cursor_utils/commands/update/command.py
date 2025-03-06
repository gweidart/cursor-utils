"""
CLI interface for the update command.

Key Components:
    update(): CLI command for updating Cursor Utils

Project Dependencies:
    This file uses: click: For CLI interface
    This file uses: manager: For update orchestration
    This file is used by: cli: For command registration
"""

import click

from cursor_utils.commands.update.manager import UpdateManager
from cursor_utils.errors import UpdateError, VersionError


@click.command()
@click.option(
    "--check",
    is_flag=True,
    help="Only check for updates without installing.",
)
def update(check: bool) -> None:
    """Update Cursor Utils to the latest version."""
    manager = UpdateManager()

    try:
        # Check for updates
        has_update, latest_version = manager.check_version()
        if not has_update:
            return

        # Show update message
        if latest_version:
            manager.display_update_message(latest_version)

        # If only checking, exit here
        if check:
            return

        # Ensure we have a version to update to
        if not latest_version:
            manager.console.print("[red]Error: No version available to update to.[/]")
            return

        # Confirm update
        if not click.confirm("Would you like to update now?", default=True):
            manager.console.print("[yellow]Update cancelled.[/]")
            return

        # Perform update
        manager.perform_update(latest_version)

    except (UpdateError, VersionError) as e:
        manager.console.print(str(e))
        raise click.exceptions.Exit(1)
    except Exception as e:
        error = UpdateError(
            message="Unexpected error during update",
            code="UPDATE-999",
            causes=[str(e)],
            hint_stmt="Try running with elevated permissions or in a virtual environment.",
        )
        manager.console.print(str(error))
        raise click.exceptions.Exit(1)
