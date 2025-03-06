"""
CLI interface for the config command.

Key Components:
    config(): CLI command for managing configuration
    api_keys(): Subcommand for API key management

Project Dependencies:
    This file uses: click: For CLI interface
    This file uses: manager: For configuration orchestration
"""

import rich_click as click

from cursor_utils.commands.config.manager import ConfigManager


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
    """Configure API keys for enhanced features."""
    manager = ConfigManager()

    try:
        # Show current status
        manager.display_api_key_status()

        # Run interactive setup if requested
        if not show:
            manager.setup_api_keys()
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort() from e
