"""
Orchestrates update operations and manages state.

Key Components:
    UpdateManager: Coordinates update operations and state

Project Dependencies:
    This file uses: rich: For console output
    This file uses: actions: For update operations and version checking
    This file is used by: update.command: For CLI interface
"""

from rich.console import Console
from rich.panel import Panel

from cursor_utils import __version__
from cursor_utils.commands.update.actions import (
    UpdateOrchestrator,
    VersionChecker,
    run_update,
)
from cursor_utils.errors import ErrorCodes, UpdateError


class UpdateManager:
    """Manages the update process for Cursor Utils."""

    def __init__(self) -> None:
        """Initialize the update manager."""
        self.console: Console = Console()

    def check_version(self) -> tuple[bool, str | None]:
        """
        Check if an update is available.

        Returns:
            Tuple[bool, Optional[str]]: (is_update_available, latest_version)

        """
        try:
            update_available, latest_version = VersionChecker.is_update_available()
            if not update_available:
                self.console.print(
                    Panel(
                        f"[#00d700]Cursor Utils {__version__} is up to date![/#00d700]",
                        title="Update Status",
                    )
                )
                return False, None
            return True, latest_version
        except Exception as e:
            raise UpdateError(
                message="Failed to check for updates",
                code=ErrorCodes.UPDATE_FAILED,
                causes=[str(e)],
                hint_stmt="Check your internet connection and try again.",
            )

    def display_update_message(self, latest_version: str) -> None:
        """Display update availability message."""
        env_info = UpdateOrchestrator.get_environment_info()
        available_managers = env_info["available_managers"]

        message = (
            f"[yellow]Update available![/]\n"
            f"Current version: [red]{__version__}[/]\n"
            f"Latest version:  [green]{latest_version}[/]"
        )

        if available_managers != "None":
            message += f"\n\nAvailable package managers: [blue]{available_managers}[/]"

        self.console.print(message)

    def perform_update(self, version: str) -> None:
        """
        Perform the update operation.

        Args:
            version: Version to update to

        """
        self.console.print("[#5f87ff]Updating Cursor Utils...[/]")
        try:
            run_update(version)
            self.console.print(
                Panel(
                    f"[#00d700]Successfully updated to version {version}![/#00d700]",
                    title="Update Complete",
                )
            )
        except UpdateError as e:
            # Display the error with instructions
            self.console.print(
                Panel(
                    f"[#ff5f5f]{e.message}[/]\n\n"
                    f"[#ffff00]Cause:[/] {e.causes[0] if e.causes else 'Unknown'}\n\n"
                    f"[#00d7ff]Suggestion:[/] {e.hint_stmt}",
                    title=f"Update Failed (Error: {e.code})",
                )
            )
            raise
