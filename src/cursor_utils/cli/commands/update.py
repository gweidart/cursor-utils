"""
Update command for cursor-utils.

Key Components:
    update_command: Command to check for updates and update the package

Project Dependencies:
    This file uses: parser: For command registration
                    updater: For checking for updates and updating the package
                    output: For rendering results including Rich formatting
    This file is used by: CLI commands package
"""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from cursor_utils.cli.parser import (
    command,
    option,
    print_error,
    print_info,
    print_success,
)
from cursor_utils.core.output import OutputFormat, get_renderer
from cursor_utils.services.updater import UpdateError, UpdaterService


@command(
    name="update",
    help="Check for updates and update cursor-utils",
    short_help="Update cursor-utils",
)
@option(
    "--check",
    is_flag=True,
    help="Only check for updates, don't update",
)
@option(
    "--force",
    is_flag=True,
    help="Force update even if already up to date",
)
def update_command(
    check: bool = False,
    force: bool = False,
) -> int:
    """
    Check for updates and update cursor-utils.

    Args:
        check: Only check for updates, don't update
        force: Force update even if already up to date
        format: Output format (plain, markdown, json, rich)

    Returns:
        Exit code

    """
    console = Console()
    # Initialize renderer for potential future use
    get_renderer(OutputFormat.RICH)
    updater = UpdaterService(console)

    try:
        # Check if an update is needed
        needs_update, current_version, latest_version = updater.needs_update()

        # Format the result for output
        if needs_update:
            if check:
                print_info(f"Update available: {current_version} → {latest_version}")
                print_info("Run 'cursor-utils update' to update")
                return 0
            else:
                print_info(
                    f"Updating cursor-utils from {current_version} to {latest_version}..."
                )

                # Update the package
                success = updater.update_package(force)

                if success:
                    console.print(
                        Panel(
                            Text(
                                f"cursor-utils has been updated to version {latest_version}!",
                                style="green",
                            ),
                            title="Update Complete",
                            title_align="center",
                            border_style="green",
                        )
                    )
                    return 0
                else:
                    print_error("Failed to update cursor-utils")
                    return 1
        else:
            if force:
                print_info("Forcing update even though already up to date...")
                success = updater.update_package(force=True)

                if success:
                    console.print(
                        Panel(
                            Text(
                                f"cursor-utils has been updated to version {latest_version}!",
                                style="green",
                            ),
                            title="Update Complete",
                            title_align="center",
                            border_style="green",
                        )
                    )
                    return 0
                else:
                    print_error("Failed to update cursor-utils")
                    return 1
            else:
                print_success(
                    f"cursor-utils is already up to date (version {current_version})"
                )
                return 0
    except UpdateError as e:
        print_error(f"Update error: {e}")
        if e.help_text:
            print_info(e.help_text)
        return e.exit_code
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        return 1
