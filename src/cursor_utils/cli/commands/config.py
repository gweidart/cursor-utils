"""
Configuration command for cursor-utils.

Key Components:
    config_command: Command to manage configuration
    config_get_command: Command to get a configuration value
    config_set_command: Command to set a configuration value
    config_delete_command: Command to delete a configuration value

Project Dependencies:
    This file uses: parser: For command registration
                    config: For configuration management
                    output: For rendering results including Rich formatting
    This file is used by: CLI commands package
"""

from typing import Optional

import rich_click as click
from rich.table import Table

from cursor_utils.cli.parser import cli, command, option, print_error, print_info
from cursor_utils.core.config import Configuration, load_configuration
from cursor_utils.core.output import OutputFormat, OutputRenderer, get_renderer


@command(
    name="config",
    help="Manage configuration settings",
    short_help="Manage config",
)
@click.argument(
    "subcommand",
    type=click.Choice(["get", "set", "delete", "list"], case_sensitive=False),
)
@click.argument(
    "key",
    required=False,
)
@click.argument(
    "value",
    required=False,
)
@option(
    "--format",
    default="rich",
    help="Output format (plain, markdown, json, rich)",
    show_default=False,
    type=click.Choice(["plain", "markdown", "json", "rich"], case_sensitive=False),
)
def config_command(
    subcommand: str,
    key: Optional[str] = None,
    value: Optional[str] = None,
    format: str = "rich",
) -> int:
    """
    Manage cursor-utils configuration settings.

    This command allows you to get, set, delete, and list configuration values.
    Configuration values are stored in a local file and are used by other commands.

    Examples:
        cursor-utils config get gemini_api_key

        cursor-utils config set gemini_api_key your-api-key

        cursor-utils config delete gemini_api_key

        cursor-utils config list

    """
    # Initialize the configuration
    config = load_configuration()

    # Initialize the renderer
    renderer: OutputRenderer = get_renderer(format)

    # Execute the appropriate subcommand
    if subcommand == "get":
        if not key:
            print_error("Key is required for the 'get' subcommand")
            return 1
        return config_get_command(config, renderer, key)
    elif subcommand == "set":
        if not key:
            print_error("Key is required for the 'set' subcommand")
            return 1
        if not value:
            print_error("Value is required for the 'set' subcommand")
            return 1
        return config_set_command(config, renderer, key, value)
    elif subcommand == "delete":
        if not key:
            print_error("Key is required for the 'delete' subcommand")
            return 1
        return config_delete_command(config, renderer, key)
    elif subcommand == "list":
        return config_list_command(config, renderer)
    else:
        print_error(f"Unknown subcommand: {subcommand}")
        print_info("Available subcommands: get, set, delete, list")
        return 1


def config_get_command(
    config: Configuration, renderer: OutputRenderer, key: str
) -> int:
    """
    Get a configuration value.

    Args:
        config: The configuration
        renderer: The output renderer
        key: The configuration key

    Returns:
        Exit code

    """
    value = config.get(key)
    if value is None:
        print_error(f"Configuration key not found: {key}")
        return 1

    # Check if we're using Rich format
    if isinstance(renderer, type(get_renderer(OutputFormat.RICH))):
        # Create a table with the key and value
        table = Table(title=f"Configuration Value: {key}")
        table.add_column("Key", style="cyan")
        table.add_column("Value", style="green")
        table.add_row(key, value)
        print_info(f"Configuration value for {key}", "Configuration")
        # Use console to print the table directly
        from rich.console import Console

        console = Console()
        console.print(table)
    else:
        renderer.render(f"{key}: {value}")
    return 0


def config_set_command(
    config: Configuration, renderer: OutputRenderer, key: str, value: str
) -> int:
    """
    Set a configuration value.

    Args:
        config: The configuration
        renderer: The output renderer
        key: The configuration key
        value: The configuration value

    Returns:
        Exit code

    """
    if value == "":
        print_error("Value is required for set command")
        return 1

    config.set(key, value)

    # Check if we're using Rich format
    if isinstance(renderer, type(get_renderer(OutputFormat.RICH))):
        # Create a table with the key and status
        table = Table(title="Configuration Updated")
        table.add_column("Key", style="cyan")
        table.add_column("Value", style="green")
        table.add_row(key, value)
        print_info(f"Configuration key {key} set", "Configuration")
        # Use console to print the table directly
        from rich.console import Console

        console = Console()
        console.print(table)
    else:
        renderer.render(f"Configuration key {key} set to {value}")
    return 0


def config_delete_command(
    config: Configuration, renderer: OutputRenderer, key: str
) -> int:
    """
    Delete a configuration value.

    Args:
        config: The configuration
        renderer: The output renderer
        key: The configuration key

    Returns:
        Exit code

    """
    # Check if the key exists before deleting
    if config.get(key) is None:
        print_error(f"Configuration key not found: {key}")
        return 1

    # Delete the key
    config.delete(key)

    # Check if we're using Rich format
    if isinstance(renderer, type(get_renderer(OutputFormat.RICH))):
        # Create a table with the key and status
        table = Table(title="Configuration Deleted")
        table.add_column("Key", style="cyan")
        table.add_column("Status", style="yellow")
        table.add_row(key, "Deleted successfully")
        print_info(f"Configuration key {key} deleted", "Configuration")
        # Use console to print the table directly
        from rich.console import Console

        console = Console()
        console.print(table)
    else:
        renderer.render(f"Configuration key {key} deleted")
    return 0


def config_list_command(config: Configuration, renderer: OutputRenderer) -> int:
    """
    List all configuration values.

    Args:
        config: The configuration
        renderer: The output renderer

    Returns:
        Exit code

    """
    # Get all configuration values
    # Since there's no get_all method, we'll use the data attribute directly
    values = config.data if hasattr(config, 'data') else {}

    if not values:
        print_info("No configuration values found")
        return 0

    # Check if we're using Rich format
    if isinstance(renderer, type(get_renderer(OutputFormat.RICH))):
        # Create a table with all keys and values
        table = Table(title="Configuration Values")
        table.add_column("Key", style="cyan")
        table.add_column("Value", style="green")

        for key, value in values.items():
            # Mask sensitive values
            if (
                "api_key" in key.lower()
                or "token" in key.lower()
                or "password" in key.lower()
            ):
                masked_value = (
                    value[:4] + "*" * (len(value) - 4)
                    if len(value) > 4
                    else "*" * len(value)
                )
                table.add_row(key, masked_value)
            else:
                table.add_row(key, value)

        print_info("All configuration values", "Configuration")
        # Use console to print the table directly
        from rich.console import Console

        console = Console()
        console.print(table)
    else:
        for key, value in values.items():
            # Mask sensitive values
            if (
                "api_key" in key.lower()
                or "token" in key.lower()
                or "password" in key.lower()
            ):
                masked_value = (
                    value[:4] + "*" * (len(value) - 4)
                    if len(value) > 4
                    else "*" * len(value)
                )
                renderer.render(f"{key}: {masked_value}")
            else:
                renderer.render(f"{key}: {value}")

    return 0


# Register the command with the CLI
cli.add_command(config_command)
