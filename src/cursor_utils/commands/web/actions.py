"""
Actions module for web command operations.

Key Components:
    ensure_config: Ensures configuration exists
    stream_query: Streams query response
    format_response: Formats streaming response

Project Dependencies:
    This file uses: manager: For configuration and client management
    This file uses: types: For type definitions
    This file uses: errors: For standardized error handling
    This file is used by: command: For command execution
"""

import os
from collections.abc import AsyncGenerator

import rich_click as click
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from cursor_utils.commands.web.manager import WebManager
from cursor_utils.errors import ErrorCodes, WebError
from cursor_utils.types import (
    ModelType,
    ModeType,
    SearchFocusType,
    StreamResponse,
    WebConfig,
)

console = Console()

DEFAULT_MODEL: ModelType = "sonar"
DEFAULT_MODE: ModeType = "concise"
DEFAULT_SEARCH_FOCUS: SearchFocusType = "internet"


def ensure_config(manager: WebManager) -> WebConfig:
    """Ensure configuration exists or guide user to create it."""
    try:
        config = manager.load_config()
        if config is not None and "model" in config:
            return config

        console.print(
            "[#d7af00]No web configuration found. Let's create one![/#d7af00]"
        )

        model = DEFAULT_MODEL if not config else config["model"]
        mode = DEFAULT_MODE if not config else config["mode"]
        search_focus = DEFAULT_SEARCH_FOCUS if not config else config["search_focus"]
        manager.save_config(model, mode, search_focus)
        return {"model": model, "mode": mode, "search_focus": search_focus}
    except Exception as e:
        raise WebError(
            message="Failed to load or create web configuration",
            code=ErrorCodes.WEB_CONFIG_ERROR,
            causes=[str(e)],
            hint_stmt="Check your configuration file permissions and format",
        ) from e


def get_api_key() -> str:
    """Get API key from environment or prompt user."""
    api_key = os.getenv("PERPLEXITY_API_KEY", "")
    if not api_key:
        try:
            api_key = click.prompt(
                "Please enter your Perplexity API key (will be stored in environment)",
                type=str,
                hide_input=True,
            )
            # Suggest adding to environment
            console.print(
                "\n[#d7af00]Tip: Add this to your environment to avoid prompts:[/]"
                "\n[dim #5f87ff]export PERPLEXITY_API_KEY='your-api-key'[/]"
            )
        except click.Abort:
            raise
        except Exception as e:
            raise WebError(
                message="Failed to get API key",
                code=ErrorCodes.INVALID_API_KEY,
                causes=[str(e)],
                hint_stmt="Ensure you have set PERPLEXITY_API_KEY in your environment",
            ) from e

    if not api_key.strip():
        raise WebError(
            message="API key cannot be empty",
            code=ErrorCodes.INVALID_API_KEY,
            causes=["Empty API key provided"],
            hint_stmt="Set a valid PERPLEXITY_API_KEY in your environment",
        )

    return api_key


async def stream_query(
    query: str,
    model: ModelType,
    mode: ModeType,
    search_focus: SearchFocusType,
    api_key: str,
    manager: WebManager,
) -> AsyncGenerator[StreamResponse, None]:
    """Stream query response from Perplexity AI."""
    client = manager.get_client(api_key)

    try:
        # The client's async_search method returns chunks that can be str or dict
        async for chunk in client.async_search(  # type: ignore
            query,
            model=model,  # type: ignore
            mode=mode,
            search_focus=search_focus,
        ):
            # Validate chunk type
            if not isinstance(chunk, str | dict):  # type: ignore
                raise WebError(
                    message="Invalid response format from API",
                    code=ErrorCodes.WEB_API_ERROR,
                    causes=[f"Expected str or dict, got {type(chunk)}"],  # type: ignore
                    hint_stmt="This may be due to an API version mismatch",
                )

            # Extract text from chunk
            chunk_text = chunk if isinstance(chunk, str) else chunk.get("text", "")  # type: ignore
            yield {"text": chunk_text, "done": False}

        yield {"text": "", "done": True}
    except WebError:
        raise
    except Exception as e:
        raise WebError(
            message="Error during API call",
            code=ErrorCodes.WEB_API_ERROR,
            causes=[str(e)],
            hint_stmt="Check your internet connection and API key",
        ) from e


def format_response(response: str) -> Panel:
    """Format response for display."""
    return Panel(
        Markdown(response),
        title="[#af87ff]Perplexity AI's Response[/]",
        border_style="bold #d7af00",
        padding=(1, 2),
    )
