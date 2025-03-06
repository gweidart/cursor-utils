"""
Orchestrates installation operations and manages state.

Key Components:
    InstallManager: Coordinates installation operations and state

Project Dependencies:
    This file uses: rich: For console output
    This file uses: actions: For installation operations
    This file uses: config: For API key setup
    This file is used by: install.command: For CLI interface
"""

from pathlib import Path

import rich_click as click
from packaging.version import parse
from rich.console import Console

from cursor_utils import __version__
from cursor_utils.commands.config.manager import ConfigManager
from cursor_utils.commands.install.actions import (
    check_existing_installation,
    create_cursor_dir,
    find_mdc_file,
    format_template,
    get_template_content,
    write_mdc_file,
)
from cursor_utils.errors import ErrorCodes, InstallError


class InstallManager:
    """Manages the installation process for Cursor Utils."""

    def __init__(self) -> None:
        """Initialize the install manager."""
        self.console: Console = Console()

    def install_to_project(self, project_path: str) -> None:
        """
        Install cursor-utils in a project.

        Args:
            project_path: Path to the project root

        Raises:
            InstallError: If installation fails

        """
        project_dir = Path(project_path).resolve()
        mdc_file = find_mdc_file(project_dir)

        # Check if already installed
        current_version = parse(__version__)
        installed, current_version = check_existing_installation(mdc_file)
        if installed and current_version:
            # If installed but older version, offer to update
            if current_version != __version__:
                self.console.print(
                    f"[#d7af00]⚠[/#d7af00] cursor-utils is already installed (version {current_version})"
                )
                self.console.print(
                    f"[#d7af00]⚠[/#d7af00] Current version is {__version__}"
                )

                if click.confirm(
                    "Would you like to update to the latest version?", default=True
                ):
                    # Get template and write to file
                    cursor_dir = create_cursor_dir(project_dir)
                    template_content = get_template_content()
                    formatted_content = format_template(template_content, project_dir)
                    write_mdc_file(cursor_dir, formatted_content)
                    self.console.print(
                        f"[#00d700]✓[/#00d700] cursor-utils updated from {current_version} to {__version__}!"
                    )
                    return
                else:
                    self.console.print("[#d7af00]⚠[/#d7af00] Update cancelled")
                    return
            else:
                # Already installed with same version
                raise InstallError(
                    message="cursor-utils is already installed",
                    code=ErrorCodes.ALREADY_INSTALLED,
                    causes=[f"Current version: {current_version}"],
                    hint_stmt="No update needed as you already have the latest version.",
                )

        # Create .cursor directory
        cursor_dir = create_cursor_dir(project_dir)

        # Get template and write to file
        template_content = get_template_content()
        formatted_content = format_template(template_content, project_dir)
        write_mdc_file(cursor_dir, formatted_content)

        self.console.print(
            f"[#00d700]✓[/#00d700] cursor-utils {__version__} installed successfully!"
        )

        # Setup API keys
        if click.confirm(
            "\nWould you like to configure API keys for enhanced features?",
            default=True,
        ):
            ConfigManager().setup_api_keys()
