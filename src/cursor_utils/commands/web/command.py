"""
Web command implementation for querying Perplexity AI.

Key Components:
    web: Command function for querying Perplexity AI

Project Dependencies:
    This file uses: actions: For web operations
    This file uses: manager: For configuration and client management
    This file uses: errors: For standardized error handling
    This file is used by: cursor_utils.commands.web: For command registration
"""

import asyncio
from collections.abc import Coroutine
from typing import Any, Optional, cast

import rich_click as click
from rich.console import Console

from cursor_utils.commands.web.actions import (
    ensure_config,
    format_response as format_web_response,
    get_api_key,
    stream_query,
)
from cursor_utils.commands.web.manager import WebManager
from cursor_utils.errors import ErrorCodes, WebError
from cursor_utils.types import ModelType
from cursor_utils.utils.command_helpers import safe_execute

console = Console()


@click.command()
@click.argument("query", nargs=-1, required=True)
@click.option(
    "--model",
    type=click.Choice(["sonar", "sonar-pro", "sonar-reasoning", "sonar-pro-reasoning"]),
    help="Model to use for query (default: from config)",
)
@click.option(
    "--mode",
    type=click.Choice(["concise", "copilot"]),
    help="Response mode (default: from config)",
)
@click.option(
    "--focus",
    type=click.Choice(
        ["internet", "scholar", "writing", "wolfram", "youtube", "reddit"]
    ),
    help="Search focus (default: from config)",
)
@click.pass_context
def web(
    ctx: click.Context,
    query: tuple[str, ...],
    model: Optional[ModelType] = None,
    mode: Optional[str] = None,
    focus: Optional[str] = None,
) -> None:
    """
    Query Perplexity AI for real-time information from the web.

    QUERY: The search query to send to Perplexity AI

    Examples:
        cursor-utils web "What are the latest developments in AI?"
        cursor-utils web --model sonar-pro "Explain quantum computing"
        cursor-utils web --focus scholar "Recent research on climate change"

    """
    # Cast to Coroutine to satisfy type checker
    coro = cast(Coroutine[Any, Any, None], async_web(ctx, query, model, mode, focus))
    asyncio.run(coro)


@safe_execute(WebError, ErrorCodes.WEB_QUERY_ERROR)
async def async_web(
    ctx: click.Context,
    query: tuple[str, ...],
    model: Optional[ModelType] = None,
    mode: Optional[str] = None,
    focus: Optional[str] = None,
) -> None:
    """Async implementation of web command."""
    # Initialize manager
    manager = WebManager()

    # Get configuration
    config = ensure_config(manager)

    # Override config with command line options
    if model:
        config["model"] = model
    if mode and mode in ("concise", "copilot"):
        config["mode"] = mode
    if focus and focus in (
        "internet",
        "scholar",
        "writing",
        "wolfram",
        "youtube",
        "reddit",
    ):
        config["search_focus"] = focus

    # Get API key
    api_key = get_api_key()

    # Format query from tuple of strings
    formatted_query = " ".join(query)

    # Stream response from Perplexity
    console.print(f"[#afafd7]Querying Perplexity AI:[/] [#5f87ff]{formatted_query}[/]")

    response_text = ""
    async for chunk in stream_query(
        query=formatted_query,
        model=config["model"],
        mode=config["mode"],
        search_focus=config["search_focus"],
        api_key=api_key,
        manager=manager,
    ):
        if chunk["text"]:
            response_text += chunk["text"]
            console.clear()
            console.print(
                f"[#afafd7]Querying Perplexity AI:[/] [#5f87ff]{formatted_query}[/]"
            )
            console.print(response_text)

    # Final output with formatting
    if response_text:
        console.clear()
        console.print(
            f"[#afafd7]Perplexity AI response for:[/] [#5f87ff]{formatted_query}[/]"
        )
        console.print(format_web_response(response_text))
