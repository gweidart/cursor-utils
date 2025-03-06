"""
Orchestrates configuration operations and manages state.

Key Components:
    ConfigManager: Coordinates configuration operations and state

Project Dependencies:
    This file uses: rich: For console output
    This file uses: actions: For configuration operations
    This file is used by: config.command: For CLI interface
"""

from typing import Final

import rich_click as click
from rich.console import Console
from rich.table import Table

from cursor_utils.commands.config.actions import get_api_key_status, save_api_key
from cursor_utils.config import APIKeyType, Config
from cursor_utils.errors import ConfigError


class ConfigManager:
    """Manages the configuration process for Cursor Utils."""

    def __init__(self) -> None:
        """Initialize configuration manager."""
        self.console: Final[Console] = Console()
        self.config: Final[Config] = Config()

    def display_api_key_status(self) -> None:
        """Display status of all API keys."""
        status = get_api_key_status(self.config)

        # Create table
        table = Table(title="API Key Status", show_header=True)
        table.add_column("API Key", style="cyan")
        table.add_column("Status", style="green")

        # Add rows
        for key in status:
            table.add_row(
                key.key_type.description,
                "Set" if key.is_set else "Not Set",
            )

        # Display table
        self.console.print()
        self.console.print(table)
        self.console.print()

    def setup_api_keys(self) -> None:
        """Run interactive API key setup."""
        for key_type in APIKeyType:
            key_config = self.config.check_api_key(key_type)

            # Show key info
            self.console.print(f"\n[#00d700]{key_type.description}[/]")
            if not key_config.is_set:
                self.console.print(f"[#d7af00]Note:[/] {key_type.feature_impact}")

            # Prompt for key if not set or user wants to update
            if key_config.is_set:
                if not click.confirm(
                    "API key is already set. Would you like to update it?",
                    default=False,
                ):
                    continue

            # Get new key value
            value = click.prompt(
                "Enter API key",
                type=str,
                default="",
                show_default=False,
            )

            if value.strip():
                try:
                    save_api_key(self.config, key_type, value.strip())
                except ConfigError as e:
                    self.console.print(f"[#d70000]✗[/] {e}")
            else:
                self.console.print("[#d7af00]Skipped[/]")
