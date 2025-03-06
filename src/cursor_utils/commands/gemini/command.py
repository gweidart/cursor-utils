"""
Gemini command implementation for interacting with Google's Gemini API.

Key Components:
    gemini: Command function for querying Google's Gemini API

Project Dependencies:
    This file uses: actions: For Gemini operations
    This file uses: manager: For configuration and client management
    This file uses: errors: For standardized error handling
    This file is used by: cursor_utils.commands.gemini: For command registration
"""

import asyncio
import pathlib
from collections.abc import Coroutine
from typing import Any, Optional, cast

import rich_click as click
from rich.console import Console

from cursor_utils.commands.gemini.actions import (
    ensure_config,
    format_response,
    get_api_key,
    stream_query,
    stream_query_with_context,
)
from cursor_utils.commands.gemini.manager import GeminiManager
from cursor_utils.errors import ErrorCodes, WebError
from cursor_utils.utils.command_helpers import safe_execute

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
    help="Model to use for query (default: from config)",
)
@click.option(
    "--append",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
    help="Append file content to query",
)
@click.pass_context
def gemini(
    ctx: click.Context,
    query: tuple[str, ...],
    model: Optional[str] = None,
    append: Optional[pathlib.Path] = None,
) -> None:
    """
    Query Google's Gemini API with your question.

    QUERY: The query to send to Gemini

    Examples:
        cursor-utils gemini "Explain quantum computing"
        cursor-utils gemini --model gemini-2.0-pro "Generate Python code for a web scraper"
        cursor-utils gemini --append ./src/main.py "Explain this code"

    """
    # Cast to Coroutine to satisfy type checker
    coro = cast(Coroutine[Any, Any, None], async_gemini(ctx, query, model, append))
    asyncio.run(coro)


@safe_execute(WebError, ErrorCodes.GEMINI_API_ERROR)
async def async_gemini(
    ctx: click.Context,
    query: tuple[str, ...],
    model: Optional[str] = None,
    append: Optional[pathlib.Path] = None,
) -> None:
    """Async implementation of gemini command."""
    # Initialize manager
    manager = GeminiManager()

    # Get configuration
    config = ensure_config(manager)

    # Override config with command line options
    if model:
        config["model"] = model

    # Get API key
    api_key = get_api_key()

    # Format query from tuple of strings
    formatted_query = " ".join(query)

    # Stream response from Gemini
    console.print(f"[#afafd7]Querying Gemini:[/] [#5f87ff]{formatted_query}[/]")

    response_text = ""

    # If append option is used, use stream_query_with_context
    if append:
        console.print(f"[#afafd7]Including file:[/] [#5f87ff]{append}[/]")
        async for chunk in stream_query_with_context(
            query=formatted_query,
            model=config["model"],
            max_output_tokens=config["max_output_tokens"],
            temperature=config["temperature"],
            top_p=config["top_p"],
            top_k=config["top_k"],
            api_key=api_key,
            manager=manager,
            context_file=append,
        ):
            if chunk["text"]:
                response_text += chunk["text"]
                console.clear()
                console.print(
                    f"[#afafd7]Querying Gemini:[/] [#5f87ff]{formatted_query}[/]"
                )
                console.print(response_text)
    else:
        # Use regular stream_query
        async for chunk in stream_query(
            query=formatted_query,
            model=config["model"],
            max_output_tokens=config["max_output_tokens"],
            temperature=config["temperature"],
            top_p=config["top_p"],
            top_k=config["top_k"],
            api_key=api_key,
            manager=manager,
        ):
            if chunk["text"]:
                response_text += chunk["text"]
                console.clear()
                console.print(
                    f"[#afafd7]Querying Gemini:[/] [#5f87ff]{formatted_query}[/]"
                )
                console.print(response_text)

    # Final output with formatting
    if response_text:
        console.clear()
        console.print(f"[#afafd7]Gemini response for:[/] [#5f87ff]{formatted_query}[/]")
        console.print(format_response(response_text))
