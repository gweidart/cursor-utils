"""
CLI interface for the config command.

Key Components:
    config(): CLI command for managing configuration
    api_keys(): Subcommand for API key management

Project Dependencies:
    This file uses: click: For CLI interface
    This file uses: manager: For configuration orchestration
    This file uses: utils.command_helpers: For standardized command execution
"""

import rich_click as click

from cursor_utils.commands.config.manager import ConfigManager
from cursor_utils.errors import ConfigError, ErrorCodes
from cursor_utils.utils.command_helpers import safe_execute_sync


@click.group()
def config() -> None:
    """Manage cursor-utils configuration."""


@config.command()
@click.option(
    "--show",
    is_flag=True,
    help="Skip interactive prompts and only show current status.",
)
def api_keys(show: bool) -> None:
    """
    Configure API keys for enhanced features.

    Args:
        show: Whether to only show current status

    """
    manager = ConfigManager()
    execute_api_keys_config(manager, show)


@safe_execute_sync(ConfigError, ErrorCodes.CONFIG_FILE_ERROR)
def execute_api_keys_config(manager: ConfigManager, show: bool) -> None:
    """
    Execute API keys configuration with standardized error handling.

    Args:
        manager: Configuration manager
        show: Whether to only show current status

    Raises:
        ConfigError: If configuration fails

    """
    # Show current status
    manager.display_api_key_status()

    # Run interactive setup if requested
    if not show:
        manager.setup_api_keys()
