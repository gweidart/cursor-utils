"""
Web search command for cursor-utils.

Key Components:
    web_command: Command to search the web using Perplexity AI

Project Dependencies:
    This file uses: parser: For command registration
                   perplexity: For web search
                   output: For rendering results including Rich formatting
    This file is used by: CLI commands package
"""

from typing import cast

import rich_click as click
from rich.progress import Progress, SpinnerColumn, TextColumn

from cursor_utils.cli.parser import (
    cli,
    command,
    option,
    print_error,
    print_info,
    validate_required_options,
)
from cursor_utils.core.errors import handle_command_errors
from cursor_utils.core.output import OutputFormat, get_renderer
from cursor_utils.services.perplexity import (
    PerplexityClient,
    PerplexityError,
    PerplexityResponse,
)


@command(
    name="web",
    help="Search the web using Perplexity AI",
    short_help="Search the web",
)
@click.argument(
    "query",
    required=True,
    metavar="QUERY",
)
@option(
    "--model",
    default="sonar",
    help="The model to use for search",
    show_default=False,
    callback=validate_required_options,
)
@option(
    "--format",
    default="rich",
    help="Output format (plain, markdown, json, rich)",
    show_default=False,
    type=click.Choice(["plain", "markdown", "json", "rich"], case_sensitive=False),
)
@handle_command_errors
async def web_command(query: str, model: str = "sonar", format: str = "rich") -> int:
    """
    Search the web using Perplexity AI and display the results.

    This command sends your query to the Perplexity AI search API and displays
    the results in your chosen format. It can stream the results as they're
    generated or wait for the complete response.

    Examples:
        cursor-utils web "What is rich-click?"

        cursor-utils web --model mixtral "Latest Python features" --format markdown


    """
    try:
        # Initialize the client
        client = PerplexityClient()

        # Initialize the renderer
        renderer = get_renderer(format)

        # Create a progress indicator for the search
        progress = None
        if format.upper() == OutputFormat.RICH.name:
            with Progress(
                SpinnerColumn(),
                TextColumn(
                    "[bold blue]Querying Perplexity: [bold cyan]{task.description}"
                ),
                transient=True,
            ) as progress:
                progress.add_task(description=query)

                try:
                    # Perform the search
                    result = await client.query_async(query, model=model)

                    response = cast(PerplexityResponse, result)
                    print_info(
                        f"Search results for: {query}", "Perplexity Search Results"
                    )
                    renderer.render(response.get_formatted_text())
                    progress.stop()
                except Exception as e:
                    print_error(f"Error searching the web: {e}")
                    return 1
        # Fallback if original attempt fails
        else:
            # Print a message before starting the search
            click.echo(f"Searching for: {query}\n")

            try:
                # Get the response
                result = await client.query_async(query, model=model)

                response = cast(PerplexityResponse, result)
                print_info(f"Search results for: {query}", "Perplexity Search Results")
                renderer.render(response.get_formatted_text())

            except Exception as e:
                print_error(f"Error searching the web: {e}")
                return 1
    except PerplexityError as e:
        print_error(f"{e.message}", "Perplexity API Error")
        if e.help_text:
            print_info(e.help_text, "Help")
        return e.exit_code
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        return 1

    return 0


# Register the command with the AI group
cli.add_command(web_command)
