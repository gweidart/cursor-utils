"""Command line interface for Cursor Utils.

Key Components:
    main: Main CLI entry point
    print_version: Prints version information

Project Dependencies:
    This file uses: click, rich: For CLI and output formatting
    This file uses: commands: For command implementations
"""

import rich_click as click
from rich.console import Console
from rich.traceback import install as install_rich_traceback

from cursor_utils.commands import (
    config,
    gemini,
    github,
    install,
    project,
    repo,
    update,
    web,
)

# Install rich traceback handler
install_rich_traceback()

# Initialize rich console
console: Console = Console()


def print_version(ctx: click.Context, param: click.Parameter, value: bool) -> None:
    """Print the version and exit."""
    if not value or ctx.resilient_parsing:
        return
    from cursor_utils import __version__

    console.print(
        f"[bold #00d700]Cursor Utils[/] [#afafd7] version[/]: [#5f87ff]{__version__}[/]"
    )
    ctx.exit()


@click.group()
@click.option(
    "--version",
    is_flag=True,
    callback=print_version,
    expose_value=False,
    is_eager=True,
    help="Show the version and exit.",
)
@click.option(
    "--debug/--no-debug",
    default=False,
    help="Enable debug mode.",
)
@click.pass_context
def main(ctx: click.Context, debug: bool) -> None:
    """Cursor Utils.

    Give your Cursor Agents superpowers.
    """
    ctx.ensure_object(dict)
    ctx.obj["debug"] = debug
    if debug:
        console.print("[#af87ff]Debug mode enabled[/]")


# Register commands
main.add_command(config)
main.add_command(gemini)
main.add_command(github)
main.add_command(install)
main.add_command(project)
main.add_command(repo)
main.add_command(update)
main.add_command(web)


if __name__ == "__main__":
    main()
