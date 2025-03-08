"""
Repository analysis command for cursor-utils.

Key Components:
    repo_command: Command to analyze and query code repositories

Project Dependencies:
    This file uses: parser: For command registration
                   git: For repository access
                   output: For rendering results including Rich formatting
                   gemini: For AI analysis
    This file is used by: CLI commands package
"""

import atexit
import contextlib
import os
import shutil
import tempfile
from collections.abc import Generator
from typing import Any, Optional

import rich_click as click

from cursor_utils.cli.parser import cli, command, option, print_info
from cursor_utils.core.errors import handle_command_errors
from cursor_utils.core.output import OutputFormat, RichProgressIndicator, get_renderer
from cursor_utils.services.gemini import GeminiClient
from cursor_utils.utils.file_rank_algo import FileRanker, build_file_list
from cursor_utils.utils.fs import read_file
from cursor_utils.utils.git import (
    clone_repository,
    get_repository_root,
    is_git_repository,
)

# Track temporary directories for cleanup
_temp_dirs: list[str] = []


def _cleanup_temp_dirs() -> None:
    """Clean up temporary directories created by the repo command."""
    global _temp_dirs
    dirs_to_clean = _temp_dirs.copy()
    _temp_dirs = []

    for temp_dir in dirs_to_clean:
        try:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception:
            # Log but don't fail if cleanup fails
            pass


# Register the cleanup function to run at exit
atexit.register(_cleanup_temp_dirs)


@contextlib.contextmanager
def temp_directory(prefix: str = "cursor_utils_repo_") -> Generator[str, None, None]:
    """
    Context manager for temporary directories.

    Creates a temporary directory and ensures it's cleaned up when done,
    even if an exception occurs.

    Args:
        prefix: Prefix for the temporary directory name

    Yields:
        The path to the temporary directory

    """
    temp_dir = tempfile.mkdtemp(prefix=prefix)
    try:
        _temp_dirs.append(temp_dir)
        yield temp_dir
    finally:
        # Try to clean up immediately
        try:
            if temp_dir in _temp_dirs:
                _temp_dirs.remove(temp_dir)
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception:
            # If immediate cleanup fails, it will be cleaned up at exit
            pass


@command(name="repo", help="Analyze and query code repositories")
@click.argument("repo_url")
@click.argument("query")
@option(
    "--branch",
    default=None,
    help="The branch to analyze",
)
@option(
    "--depth",
    default=1,
    help="The clone depth",
    type=int,
)
@option(
    "--format",
    default="rich",
    help="The output format (plain, markdown, json, rich)",
)
@option(
    "--model",
    default="gemini-1.5-pro",
    help="The model to use",
)
@option(
    "--max-files",
    default=10,
    help="Maximum number of files to include in context",
    type=int,
)
@option("--debug/--no-debug", default=False, help="Enable debug output")
@handle_command_errors
async def repo_command(
    repo_url: str,
    query: str,
    branch: Optional[str] = None,
    depth: int = 1,
    format: str = "rich",
    model: str = "gemini-1.5-pro",
    max_files: int = 10,
    debug: bool = False,
) -> int:
    """
    Analyze and query code repositories.

    Args:
        repo_url: The repository URL or local path
        query: The query to run against the repository
        branch: The branch to analyze
        depth: The clone depth
        format: The output format
        model: The model to use
        max_files: Maximum number of files to include in context
        debug: Enable debug output

    Returns:
        Exit code

    """
    # Initialize the renderer
    renderer = get_renderer(format)

    # Create a progress indicator
    progress = None
    if format.upper() == OutputFormat.RICH.name:
        progress = RichProgressIndicator("Checking repository")
        progress.start()
    else:
        click.echo("Checking repository...")

    try:
        # Check if the repository is a local path or a URL
        if os.path.exists(repo_url) and is_git_repository(repo_url):
            # Local repository
            repo_path = get_repository_root(repo_url)
            if debug:
                click.echo(f"Using local repository: {repo_path}")

            # Process the repository
            if progress:
                progress.stop()
            return await _process_repository(
                str(repo_path),
                repo_url,
                query,
                branch,
                format,
                model,
                max_files,
                debug,
                renderer,
            )
        else:
            # Remote repository
            if debug:
                click.echo(f"Cloning repository: {repo_url}")

            # Create a temporary directory for the clone
            with temp_directory() as temp_dir:
                if progress:
                    progress.update(description=f"Cloning {repo_url}")
                else:
                    click.echo(f"Cloning {repo_url}...")

                # Clone the repository
                repo_path = clone_repository(
                    repo_url, temp_dir, branch=branch, depth=depth
                )

                if debug:
                    click.echo(f"Cloned to: {repo_path}")

                # Process the repository
                if progress:
                    progress.stop()
                return await _process_repository(
                    str(repo_path),
                    repo_url,
                    query,
                    branch,
                    format,
                    model,
                    max_files,
                    debug,
                    renderer,
                )
    except Exception as e:
        if progress:
            progress.stop()
        click.echo(f"Error: {e}", err=True)
        return 1


async def _process_repository(
    repo_path: str,
    repo_url: str,
    query: str,
    branch: Optional[str],
    format: str,
    model: str,
    max_files: int,
    debug: bool,
    renderer: Any,
) -> int:
    """
    Process a repository.

    Args:
        repo_path: The path to the repository
        repo_url: The repository URL or local path
        query: The query to run against the repository
        branch: The branch to analyze
        format: The output format
        model: The model to use
        max_files: Maximum number of files to include in context
        debug: Enable debug output
        renderer: The output renderer

    Returns:
        Exit code

    """
    # Build the file list
    file_list = build_file_list(repo_path)

    # Rank the files
    ranker = FileRanker()
    ranked_files = ranker.rank_files(file_list)

    if debug:
        click.echo(f"Found {len(file_list)} files, using top {len(ranked_files)}")
        for i, file_info in enumerate(ranked_files[:max_files]):
            click.echo(
                f"{i + 1}. {file_info['path']} (score: {file_info['importance_score']:.2f})"
            )

    # Read the top-ranked files
    file_contents: list[str] = []
    for file_info in ranked_files[:max_files]:
        try:
            content = read_file(os.path.join(repo_path, file_info['path']))
            file_contents.append(f"File: {file_info['path']}\n\n{content}")
        except Exception as e:
            if debug:
                click.echo(f"Error reading file {file_info['path']}: {e}", err=True)

    # Create the prompt
    prompt = f"""
    Analyze this repository and answer the following question:
    {query}

    Here are the most relevant files from the repository:
    
    {chr(10).join(file_contents)}
    """

    # Initialize the client
    client = GeminiClient()

    # Initialize the renderer
    renderer = get_renderer(format)

    # Create a progress indicator
    progress = None
    if format.upper() == OutputFormat.RICH.name:
        progress = RichProgressIndicator("Analyzing repository")
        progress.start()
    else:
        click.echo("Analyzing repository...")

    try:
        try:
            # Get the full response
            result = await client.generate_content(
                prompt=prompt,
                model=model,
            )

            # Stop the progress indicator
            if progress:
                progress.stop()

            # We know this is a GeminiResponse since stream=False
            response = result
            print_info(f"Analysis of repository: {repo_url}", "Repository Analysis")
            renderer.render(response.text)
        except Exception as e:
            print(f"DEBUG: Error generating content: {e}")
            if progress:
                progress.stop()
            click.echo(f"Error generating content: {e}", err=True)
            return 1
    except Exception as e:
        # Make sure to stop the progress indicator if there's an error
        if progress:
            progress.stop()
        click.echo(f"Error: {e}", err=True)
        return 1

    return 0


# Register the command with the CLI
cli.add_command(repo_command)
