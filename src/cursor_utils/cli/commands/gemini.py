"""
Gemini command for cursor-utils.

Key Components:
    gemini_command: Command to generate content using Google's Gemini API

Project Dependencies:
    This file uses: parser: For command registration
                   gemini: For content generation
                   output: For rendering results including Rich formatting
    This file is used by: CLI commands package
"""

from typing import Optional

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
from cursor_utils.services.gemini import GeminiClient


@command(
    name="gemini",
    help="Generate content using Google's Gemini API",
    short_help="Generate content with Gemini",
)
@click.argument(
    "prompt",
    required=True,
    metavar="PROMPT",
)
@option(
    "--model",
    default="gemini-1.5-pro",
    help="The model to use (gemini-2.0-pro-exp, gemini-2.0-flash, gemini-2.0-flash-exp, gemini-2.0-flash-thinking-exp)",
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
@option(
    "--stream",
    default=False,
    help="Stream the response as it's generated (currently not supported)",
    show_default=False,
)
@option(
    "--temperature",
    default=0.7,
    help="The temperature for sampling (0.0 to 1.0)",
    show_default=False,
    type=float,
)
@option(
    "--max-tokens",
    default=None,
    help="The maximum number of tokens to generate",
    type=int,
)
@option(
    "--system",
    default=None,
    help="The system instruction to guide the model's behavior",
)
@handle_command_errors
async def gemini_command(
    prompt: str,
    model: str = "gemini-1.5-pro",
    format: str = "rich",
    stream: bool = False,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    system: Optional[str] = None,
) -> int:
    """
    Generate content using Google's Gemini API.

    This command sends your prompt to the Gemini API and displays the generated
    content in your chosen format.

    Examples:
        cursor-utils gemini "Explain quantum computing in simple terms"

        cursor-utils gemini --model gemini-1.5-flash "Write a Python function to sort a list"

        cursor-utils gemini --system "You are a helpful coding assistant" "How do I use asyncio in Python?"

        cursor-utils gemini --temperature 0.9 "Write a creative short story about robots"

    """
    # Initialize the client
    client = GeminiClient()

    # Initialize the renderer
    renderer = get_renderer(format)

    # Create a progress indicator for the generation
    if format.upper() == OutputFormat.RICH.name:
        with Progress(
            SpinnerColumn(),
            TextColumn(f"[bold blue]Generating content with [bold cyan]{model}"),
            transient=True,
        ) as progress:
            progress.add_task("generate")

            try:
                # Generate content
                result = await client.generate_content(
                    prompt=prompt,
                    model=model,
                    stream=False,  # Streaming is not supported
                    temperature=temperature,
                    max_tokens=max_tokens,
                    system_instruction=system,
                )

                # Render the result
                print_info(
                    f"Generated content for prompt: {prompt[:50]}...",
                    "Gemini Response",
                )
                renderer.render(str(result))
            except Exception as e:
                print_error(f"Error generating content: {e}")
                return 1
    else:
        # Print a message before starting the generation
        click.echo(f"Generating content with {model}...\n")

        try:
            # Get the full response
            result = await client.generate_content(
                prompt=prompt,
                model=model,
                stream=False,  # Streaming is not supported
                temperature=temperature,
                max_tokens=max_tokens,
                system_instruction=system,
            )

            # Render the result
            renderer.render(str(result))
        except Exception as e:
            print_error(f"Error generating content: {e}")
            return 1

    return 0


# Register the command with the CLI group
cli.add_command(gemini_command)
