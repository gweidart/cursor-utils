"""
Command-line interface parser for cursor-utils using rich-click.

Key Components:
    cli: Main Click group for all commands
    command: Decorator for registering commands
    group: Decorator for creating command groups
    argument: Decorator for adding arguments to commands
    option: Decorator for adding options to commands
    parse_args: Parse command-line arguments

Project Dependencies:
    This file uses: rich_click: For enhanced CLI interface
    This file is used by: CLI commands and main entry point
"""

import asyncio
import inspect
from typing import Any, Optional

import rich_click as click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# Set up rich-click styling
click.rich_click.USE_RICH_MARKUP = True
click.rich_click.USE_MARKDOWN = True
click.rich_click.SHOW_ARGUMENTS = True
click.rich_click.GROUP_ARGUMENTS_OPTIONS = True
click.rich_click.STYLE_ERRORS_SUGGESTION = "bold italic"
click.rich_click.ERRORS_SUGGESTION = (
    "Try running the '--help' flag for more information."
)
click.rich_click.STYLE_OPTION = "bold cyan"
click.rich_click.STYLE_ARGUMENT = "bold cyan"
click.rich_click.STYLE_COMMAND = "bold green"
click.rich_click.STYLE_SWITCH = "bold blue"
click.rich_click.STYLE_METAVAR = "italic cyan"
click.rich_click.STYLE_USAGE = "bold"
click.rich_click.STYLE_USAGE_COMMAND = "bold green"
click.rich_click.STYLE_HELPTEXT = ""
click.rich_click.MAX_WIDTH = 100
click.rich_click.SHOW_METAVARS_COLUMN = False
click.rich_click.APPEND_METAVARS_HELP = False

# Add styling for panel borders and headers
click.rich_click.STYLE_OPTIONS_PANEL_BORDER = "yellow"
click.rich_click.STYLE_COMMANDS_PANEL_BORDER = "yellow"
click.rich_click.STYLE_ERRORS_PANEL_BORDER = "red"
click.rich_click.STYLE_FOOTER_TEXT = "bold"
click.rich_click.STYLE_HEADER_TEXT = "bold yellow"

# Create console for rich output
console = Console()

# Create the main CLI group with rich formatting
cli = click.RichGroup(
    name="cursor-utils",
    help="Cursor IDE utility tools for enhancing your development workflow",
    context_settings={
        "help_option_names": ["-h", "--help"],
        "color": True,  # Ensure color output is enabled
        # "terminal_width": 100,  # Set terminal width
    },
)

# Export Click's decorators directly
command = click.command
group = click.group
argument = click.argument
option = click.option
pass_context = click.pass_context

# Command groups

github_group = click.RichGroup(
    name="github",
    help="GitHub integration tools for repository management",
)

# Register command groups with the main CLI
cli.add_command(github_group)


def print_error(message: str, title: str = "Error") -> None:
    """
    Print an error message in a styled panel.

    Args:
        message: The error message to display
        title: The title of the error panel

    """
    console.print(
        Panel(
            Text(message, style="bold red"),
            title=title,
            title_align="left",
            border_style="red",
        )
    )


def print_success(message: str, title: str = "Success") -> None:
    """
    Print a success message in a styled panel.

    Args:
        message: The success message to display
        title: The title of the success panel

    """
    console.print(
        Panel(
            Text(message, style="bold green"),
            title=title,
            title_align="left",
            border_style="green",
        )
    )


def print_info(message: str, title: str = "Info") -> None:
    """
    Print an info message in a styled panel.

    Args:
        message: The info message to display
        title: The title of the info panel

    """
    console.print(
        Panel(
            Text(message, style="bold blue"),
            title=title,
            title_align="left",
            border_style="blue",
        )
    )


def print_warning(message: str, title: str = "Warning") -> None:
    """
    Print a warning message in a styled panel.

    Args:
        message: The warning message to display
        title: The title of the warning panel

    """
    console.print(
        Panel(
            Text(message, style="bold yellow"),
            title=title,
            title_align="left",
            border_style="yellow",
        )
    )


def validate_required_options(ctx: Any, param: Any, value: Any) -> Any:
    """
    Validate that required options are provided.

    Args:
        ctx: The Click context
        param: The parameter being validated
        value: The value of the parameter

    Returns:
        The value if valid

    Raises:
        click.BadParameter: If the parameter is required but not provided

    """
    if param.required and value is None:
        raise click.BadParameter(f"{param.name} is required")
    return value


def parse_args(args: Optional[list[str]] = None) -> int:
    """
    Parse command-line arguments and execute the appropriate command.

    Args:
        args: Command-line arguments, or None to use sys.argv

    Returns:
        Exit code

    """
    try:
        # Run the command using Click's built-in parsing
        result = cli(args)

        # Handle async commands
        if inspect.iscoroutine(result):
            try:
                result = asyncio.run(result)
            except Exception as e:
                print_error(f"Error in async execution: {e}")
                return 1

        # Return the result if it's an integer, otherwise 0
        return result if isinstance(result, int) else 0
    except Exception as e:
        # Handle unexpected exceptions
        print_error(f"Unexpected error: {e}")
        return 1


def get_commands() -> list[str]:
    """
    Get the list of registered commands.

    Returns:
        The list of command names

    """
    command_names = [cmd.name for cmd in cli.commands.values() if cmd.name is not None]
    return sorted(command_names)
