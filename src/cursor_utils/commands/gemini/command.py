"""
Gemini command implementation for querying Google Gemini.

Key Components:
    gemini: Command function for querying Google Gemini

Project Dependencies:
    This file uses: actions: For command operations
    This file uses: manager: For configuration management
    This file uses: types: For type definitions
    This file uses: errors: For standardized error handling
    This file is used by: gemini.__init__: For command registration
"""

import asyncio
import pathlib
from typing import Optional

import rich_click as click
from rich.console import Console
from rich.live import Live
from rich.spinner import Spinner

from cursor_utils.commands.gemini.actions import (
    ensure_config,
    format_response,
    get_api_key,
    stream_query_with_context,
)
from cursor_utils.commands.gemini.manager import GeminiManager
from cursor_utils.errors import ErrorCodes, WebError

console = Console()

MODELS = [
    "gemini-2.0-flash-thinking-exp",
    "gemini-2.0-flash",
    "gemini-2.0-pro-exp-02-05",
]


@click.command()
@click.argument("query", nargs=-1, required=True)
@click.option(
    "--model",
    type=click.Choice(MODELS),
    help="Override the model specified in config",
)
@click.option(
    "-a",
    "--append",
    type=click.Path(exists=True, dir_okay=False, path_type=pathlib.Path),
    help="Path to a local file to append as context",
)
@click.pass_context
def gemini(
    ctx: click.Context,
    query: tuple[str, ...],
    model: Optional[str] = None,
    append: Optional[pathlib.Path] = None,
) -> None:
    """
    Query Google Gemini with your question.

    The query can be any text - it will be sent to Google Gemini for processing.
    Results are streamed back in real-time with markdown formatting.

    Examples:
        cursor-utils gemini "What is the capital of France?"
        cursor-utils gemini --model gemini-2.0-pro "Explain quantum computing"

    """
    asyncio.run(async_gemini(ctx, query, model, append))


async def async_gemini(
    ctx: click.Context,
    query: tuple[str, ...],
    model: Optional[str] = None,
    append: Optional[pathlib.Path] = None,
) -> None:
    """Async implementation of gemini command."""
    debug = ctx.obj.get("DEBUG", False)

    # Initialize manager
    manager = GeminiManager()

    # Get configuration
    try:
        config = ensure_config(manager)
    except WebError as e:
        console.print(str(e))
        if debug:
            console.print_exception()
        ctx.exit(1)
    except click.Abort:
        ctx.exit(1)
    except Exception as e:
        err = WebError(
            message="Unexpected error setting up configuration",
            code=ErrorCodes.WEB_CONFIG_ERROR,
            causes=[str(e)],
            hint_stmt="This is likely a bug, please report it",
        )
        console.print(str(err))
        if debug:
            console.print_exception()
        ctx.exit(1)

    # Get API key
    try:
        api_key = get_api_key()
    except WebError as e:
        console.print(str(e))
        if debug:
            console.print_exception()
        ctx.exit(1)
    except click.Abort:
        ctx.exit(1)
    except Exception as e:
        err = WebError(
            message="Unexpected error getting API key",
            code=ErrorCodes.INVALID_API_KEY,
            causes=[str(e)],
            hint_stmt="This is likely a bug, please report it",
        )
        console.print(str(err))
        if debug:
            console.print_exception()
        ctx.exit(1)

    # Use model from command line if specified
    model_to_use = model or config["model"]
    max_output_tokens = config["max_output_tokens"]
    temperature = config["temperature"]
    top_p = config["top_p"]
    top_k = config["top_k"]

    # Prepare query
    query_text = " ".join(query)
    if debug:
        console.print(f"[dim]Debug: Using model {model_to_use}[/]")
        console.print(f"[dim]Debug: Query: {query_text}[/]")
        if append:
            console.print(f"[dim]Debug: Using context file: {append}[/]")

    try:
        # Create spinner for initial connection
        with Live(
            Spinner("dots", text="Connecting to Google Gemini..."),
            console=console,
            refresh_per_second=10,
        ) as live:
            # Initialize response accumulator
            full_response = ""

            # Stream and update response
            async for chunk in stream_query_with_context(
                query=query_text,
                model=model_to_use,
                max_output_tokens=max_output_tokens,
                temperature=temperature,
                top_p=top_p,
                top_k=top_k,
                api_key=api_key,
                manager=manager,
                context_file=append,
            ):
                if chunk["done"]:
                    break
                full_response += chunk["text"]
                live.update(format_response(full_response))

    except asyncio.CancelledError:
        console.print("\n[yellow]Query cancelled by user[/]")
        ctx.exit(130)
    except WebError as e:
        console.print(str(e))
        if debug:
            console.print_exception()
        ctx.exit(1)
    except Exception as e:
        err = WebError(
            message="Unexpected error during query",
            code=ErrorCodes.WEB_API_ERROR,
            causes=[str(e)],
            hint_stmt="This is likely a bug, please report it",
        )
        console.print(str(err))
        if debug:
            console.print_exception()
        ctx.exit(1)
