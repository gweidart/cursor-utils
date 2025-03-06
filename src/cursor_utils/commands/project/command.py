"""
CLI command for analyzing local projects with Gemini.

Key Components:
    project: Command for analyzing local projects

Project Dependencies:
    This file uses: click: For CLI
    This file uses: asyncio: For async execution
    This file uses: cursor_utils.commands.project.actions: For project analysis
    This file uses: cursor_utils.commands.project.manager: For project management
    This file is used by: cursor_utils.commands.project: For command registration
"""

import asyncio
from pathlib import Path

import rich_click as click

from cursor_utils.commands.project.actions import analyze_project
from cursor_utils.commands.project.manager import ProjectError, ProjectManager


@click.command()
@click.argument("query", nargs=-1, required=True)
@click.option(
    "--path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    default=".",
    help="Path to the project directory (default: current directory)",
)
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
def project(
    ctx: click.Context,
    query: tuple[str, ...],
    path: Path,
    max_size: int,
    type_weight: float,
    size_weight: float,
    time_weight: float,
) -> None:
    """
    Analyze the current project directory and query Gemini with the analysis.

    QUERY: Question to ask Gemini about the project

    Examples:
        cursor-utils project "Explain the architecture"
        cursor-utils project "Identify security issues"
        cursor-utils project --path /path/to/project "Document the API"

    """
    debug = ctx.obj.get("debug", False)

    try:
        asyncio.run(
            async_project(
                ctx=ctx,
                query=query,
                path=path,
                max_size=max_size,
                type_weight=type_weight,
                size_weight=size_weight,
                time_weight=time_weight,
                debug=debug,
            )
        )
    except ProjectError as e:
        manager = ProjectManager()
        manager.console.print(f"[#d70000]Error:[/] {e}")
    except Exception as e:
        manager = ProjectManager()
        manager.console.print(f"[#d70000]An unexpected error occurred:[/] {e}")


async def async_project(
    ctx: click.Context,
    query: tuple[str, ...],
    path: Path,
    max_size: int,
    type_weight: float,
    size_weight: float,
    time_weight: float,
    debug: bool = False,
) -> None:
    """
    Async implementation of the project command.

    Args:
        ctx: Click context
        query: Query to send to Gemini
        path: Path to the project directory
        max_size: Maximum size in MB of files to send to Gemini
        type_weight: Weight for file type importance
        size_weight: Weight for file size importance
        time_weight: Weight for file creation time importance
        debug: Whether to show debug information

    """
    manager = ProjectManager()

    # Resolve path to absolute path
    project_path = path.resolve()

    # Combine query parameters into a single string
    query_str = " ".join(query)

    # Analyze the project
    await analyze_project(
        project_path=project_path,
        query=query_str,
        max_size_mb=max_size,
        type_weight=type_weight,
        size_weight=size_weight,
        time_weight=time_weight,
        manager=manager,
        debug=debug,
    )
