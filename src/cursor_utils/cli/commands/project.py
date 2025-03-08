"""
Project analysis command for cursor-utils.

Key Components:
    project_command: Command to analyze local project code

Project Dependencies:
    This file uses: parser: For command registration
                   fs: For filesystem operations
                   output: For rendering results including Rich formatting
                   gemini: For AI analysis
    This file is used by: CLI commands package
"""

import os

import rich_click as click

from cursor_utils.cli.parser import cli, command, option, print_info
from cursor_utils.core.errors import handle_command_errors
from cursor_utils.core.output import OutputFormat, RichProgressIndicator, get_renderer
from cursor_utils.services.gemini import GeminiClient
from cursor_utils.utils.file_rank_algo import FileRanker, build_file_list
from cursor_utils.utils.fs import read_file


@command(name="project", help="Analyze local project code")
@click.argument("project_path")
@click.argument("query")
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
async def project_command(
    project_path: str,
    query: str,
    format: str = "rich",
    model: str = "gemini-2.0-flash-thinking-exp",
    max_files: int = 10,
    debug: bool = False,
) -> int | None:
    """
    Analyze local project code.

    Args:
        project_path: The project path
        query: The query to run against the project
        format: The output format
        model: The model to use
        max_files: Maximum number of files to include in context
        debug: Enable debug output

    Returns:
        Exit code

    """
    # Simple print statement that should always show
    print("Project command started")

    # Debug print
    if debug:
        print(f"Starting project command with path: {project_path}, query: {query}")
        print(f"Format: {format}, Model: {model}, Max files: {max_files}")

    # Initialize the renderer
    renderer = get_renderer(format)
    if debug:
        print(f"Initialized renderer: {type(renderer)}")

    # Check if the project path exists
    if not os.path.exists(project_path):
        click.echo(f"Error: Project path does not exist: {project_path}", err=True)
        return 1

    # Create a progress indicator
    progress = None
    if format.upper() == OutputFormat.RICH.name:
        progress = RichProgressIndicator("Analyzing project files")
        progress.start()
    else:
        click.echo("Analyzing project files...")

    try:
        # Build the file list
        if debug:
            print(f"Building file list for path: {project_path}")
        file_list = build_file_list(project_path)
        if debug:
            print(f"Found {len(file_list)} files")

        # Rank the files
        ranker = FileRanker()
        ranked_files = ranker.rank_files(file_list)
        if debug:
            print(f"Ranked files: {len(ranked_files)}")

        if debug:
            click.echo(f"Found {len(file_list)} files, using top {len(ranked_files)}")
            for i, file_info in enumerate(ranked_files[:max_files]):
                click.echo(
                    f"{i + 1}. {file_info['path']} (score: {file_info['importance_score']:.2f})"
                )

        # Read the file contents
        file_contents: list[str] = []
        for file_info in ranked_files[:max_files]:
            try:
                if debug:
                    print(f"Reading file: {file_info['path']}")
                content = read_file(os.path.join(project_path, file_info['path']))
                file_contents.append(f"File: {file_info['path']}\n\n{content}")
            except Exception as e:
                if debug:
                    click.echo(f"Error reading file {file_info['path']}: {e}", err=True)

        # Create the prompt
        prompt = f"""
        Analyze the following project code and answer this query:
        
        {query}
        
        Here are the most relevant files from the project:
        
        {chr(10).join(file_contents)}
        """
        if debug:
            print(f"Created prompt with length: {len(prompt)}")

        # Initialize the client
        if debug:
            print("Initializing Gemini client")
        client = GeminiClient()
        if debug:
            print("Gemini client initialized")

        # Stop the progress indicator
        if progress:
            progress.stop()

        # Create a new progress indicator for the generation
        if format.upper() == OutputFormat.RICH.name:
            progress = RichProgressIndicator(f"Generating analysis with {model}")
            progress.start()
        else:
            click.echo(f"Generating analysis with {model}...")
        # Generate the analysis
        # Get the full response
        if debug:
            print(f"Generating non-streaming content with model: {model}")
        try:
            result = await client.generate_content(
                prompt=prompt,
                model=model,
                stream=False,
                debug=debug,
            )
            # We know this is a GeminiResponse since stream=False
            response = result
            print_info(f"Analysis of project: {project_path}", "Project Analysis")
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


# Register the command with the CLI
cli.add_command(project_command)
