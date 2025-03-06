"""
Web command implementation for querying Perplexity AI.

Key Components:
    web: Command function for querying Perplexity AI

Project Dependencies:
    This file uses: actions: For command operations
    This file uses: manager: For configuration management
    This file uses: types: For type definitions
    This file uses: errors: For standardized error handling
    This file is used by: web.__init__: For command registration
"""

import asyncio
from typing import Optional

import rich_click as click
from rich.console import Console
from rich.live import Live
from rich.spinner import Spinner

from cursor_utils.commands.web.actions import (
    ensure_config,
    format_response,
    get_api_key,
    stream_query,
)
from cursor_utils.commands.web.manager import WebManager
from cursor_utils.errors import ErrorCodes, WebError
from cursor_utils.types import ModelType

console = Console()

MODELS = [
    "sonar",
    "sonar-pro",
    "sonar-reasoning",
    "sonar-pro-reasoning",
]


@click.command()
@click.argument("query", nargs=-1, required=True)
@click.option(
    "--model",
    type=click.Choice(MODELS),
    help="Override the model specified in config",
)
@click.pass_context
def web(
    ctx: click.Context, query: tuple[str, ...], model: Optional[ModelType] = None
) -> None:
    """
    Query Perplexity AI with your question.

    The query can be any text - it will be sent to Perplexity AI for processing.
    Results are streamed back in real-time with markdown formatting.

    Examples:
        cursor-utils web "What is the capital of France?"
        cursor-utils web --model sonar-pro "Explain quantum computing"

    """
    asyncio.run(async_web(ctx, query, model))


async def async_web(
    ctx: click.Context, query: tuple[str, ...], model: Optional[ModelType] = None
) -> None:
    """Async implementation of web command."""
    debug = ctx.obj.get("DEBUG", False)

    # Initialize manager
    manager = WebManager()

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
    mode_to_use = config["mode"]
    search_focus_to_use = config["search_focus"]

    # Prepare query
    query_text = " ".join(query)
    if debug:
        console.print(f"[dim]Debug: Using model {model_to_use}[/]")
        console.print(f"[dim]Debug: Query: {query_text}[/]")

    try:
        # Create spinner for initial connection
        with Live(
            Spinner("dots", text="Connecting to Perplexity AI..."),
            console=console,
            refresh_per_second=10,
        ) as live:
            # Initialize response accumulator
            full_response = ""

            # Stream and update response
            async for chunk in stream_query(
                query=query_text,
                model=model_to_use,
                mode=mode_to_use,
                search_focus=search_focus_to_use,
                api_key=api_key,
                manager=manager,
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
