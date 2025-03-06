"""
Repository command implementation for analyzing GitHub repositories with Gemini.

Key Components:
    repo: Command function for cloning and analyzing GitHub repositories

Project Dependencies:
    This file uses: actions: For repository operations
    This file uses: manager: For clone and analysis orchestration
    This file uses: errors: For standardized error handling
    This file is used by: cursor_utils.commands.repo: For command registration
"""

import asyncio
import re

import rich_click as click
from rich.console import Console

from cursor_utils.commands.repo.actions import clone_and_analyze_repo
from cursor_utils.commands.repo.manager import RepoManager
from cursor_utils.errors import ErrorCodes, RepoError

console = Console()


def validate_repo_url(ctx: click.Context, param: click.Parameter, value: str) -> str:
    """Validate that the input is a GitHub repository URL."""
    if value:
        # Basic GitHub URL pattern validation
        pattern = r"^(https?:\/\/)?(www\.)?github\.com\/[\w-]+\/[\w.-]+\/?$"
        if not re.match(pattern, value):
            raise click.BadParameter(
                "Repository URL must be a valid GitHub repository URL"
            )
    return value


@click.command()
@click.argument("repo_url", callback=validate_repo_url)
@click.argument("query", nargs=-1, required=True)
@click.option(
    "--max-size",
    type=int,
    default=2048,
    help="Maximum total size in MB of files to send to Gemini (default: 2048)",
)
@click.option(
    "--type-weight",
    type=float,
    default=1.0,
    help="Weight for file type importance (default: 1.0)",
)
@click.option(
    "--size-weight",
    type=float,
    default=1.0,
    help="Weight for file size importance (default: 1.0)",
)
@click.option(
    "--time-weight",
    type=float,
    default=1.0,
    help="Weight for file creation time importance (default: 1.0)",
)
@click.pass_context
def repo(
    ctx: click.Context,
    repo_url: str,
    query: tuple[str, ...],
    max_size: int,
    type_weight: float,
    size_weight: float,
    time_weight: float,
) -> None:
    """
    Clone a GitHub repository, analyze it, and query Gemini with the analysis.

    REPO_URL: URL of the GitHub repository to clone
    QUERY: Question to ask Gemini about the repository

    Examples:
        cursor-utils repo https://github.com/user/repo "Explain the architecture"
        cursor-utils repo https://github.com/user/repo "Identify security issues"

    """
    asyncio.run(
        async_repo(
            ctx, repo_url, query, max_size, type_weight, size_weight, time_weight
        )
    )


async def async_repo(
    ctx: click.Context,
    repo_url: str,
    query: tuple[str, ...],
    max_size: int,
    type_weight: float,
    size_weight: float,
    time_weight: float,
) -> None:
    """Async implementation of repo command."""
    debug = ctx.obj.get("DEBUG", False)

    # Format query from tuple of strings
    formatted_query = " ".join(query)

    # Initialize manager
    manager = RepoManager()

    try:
        # Execute repo clone and analysis
        await clone_and_analyze_repo(
            repo_url,
            formatted_query,
            max_size,
            type_weight,
            size_weight,
            time_weight,
            manager,
            debug,
        )
    except RepoError as e:
        console.print(f"[red]✗[/red] {e!s}")
        if debug:
            console.print_exception()
        ctx.exit(1)
    except click.Abort:
        ctx.exit(1)
    except Exception as e:
        error = RepoError(
            message="An unexpected error occurred",
            code=ErrorCodes.UNKNOWN_ERROR,
            causes=[str(e)],
            hint_stmt="Check the logs for more details.",
        )
        console.print(f"[red]✗[/red] {error!s}")
        if debug:
            console.print_exception()
        ctx.exit(1)
