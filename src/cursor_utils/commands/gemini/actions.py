"""
Actions module for gemini command operations.

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
import pathlib
from collections.abc import AsyncGenerator, Generator
from typing import Any, Optional, Union

import rich_click as click
from google.genai import types as genai_types
from google.genai.errors import ClientError
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from cursor_utils.commands.gemini.manager import GeminiManager
from cursor_utils.errors import ErrorCodes, WebError
from cursor_utils.types import GeminiConfig, StreamResponse

console = Console()

DEFAULT_MODEL = "gemini-2.0-flash"
DEFAULT_MAX_OUTPUT_TOKENS = 2048
DEFAULT_TEMPERATURE = 0.7
DEFAULT_TOP_P = 0.95
DEFAULT_TOP_K = 40


def ensure_config(manager: GeminiManager) -> GeminiConfig:
    """Ensure configuration exists or guide user to create it."""
    try:
        config = manager.load_config()
        if config is not None and all(
            k in config
            for k in ("model", "max_output_tokens", "temperature", "top_p", "top_k")
        ):
            return config

        console.print("[yellow]No gemini configuration found. Let's create one![/]")

        model = DEFAULT_MODEL if not config else config["model"]
        max_output_tokens = (
            DEFAULT_MAX_OUTPUT_TOKENS if not config else config["max_output_tokens"]
        )
        temperature = DEFAULT_TEMPERATURE if not config else config["temperature"]
        top_p = DEFAULT_TOP_P if not config else config["top_p"]
        top_k = DEFAULT_TOP_K if not config else config["top_k"]

        manager.save_config(model, max_output_tokens, temperature, top_p, top_k)
        return {
            "model": model,
            "max_output_tokens": max_output_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
        }
    except Exception as e:
        raise WebError(
            message="Failed to load or create gemini configuration",
            code=ErrorCodes.WEB_CONFIG_ERROR,
            causes=[str(e)],
            hint_stmt="Check your configuration file permissions and format",
        ) from e


def get_api_key() -> str:
    """Get API key from environment or prompt user."""
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        try:
            api_key = click.prompt(
                "Please enter your Google Gemini API key (will be stored in environment)",
                type=str,
                hide_input=True,
            )
            # Suggest adding to environment
            console.print(
                "\n[yellow]Tip: Add this to your environment to avoid prompts:[/]"
                "\n[dim]export GEMINI_API_KEY='your-api-key'[/]"
            )
        except click.Abort:
            raise
        except Exception as e:
            raise WebError(
                message="Failed to get API key",
                code=ErrorCodes.INVALID_API_KEY,
                causes=[str(e)],
                hint_stmt="Ensure you have set GEMINI_API_KEY in your environment",
            ) from e

    if not api_key.strip():
        raise WebError(
            message="API key cannot be empty",
            code=ErrorCodes.INVALID_API_KEY,
            causes=["Empty API key provided"],
            hint_stmt="Set a valid GEMINI_API_KEY in your environment",
        )

    return api_key


async def stream_query(
    query: str,
    model: str,
    max_output_tokens: int,
    temperature: float,
    top_p: float,
    top_k: int,
    api_key: str,
    manager: GeminiManager,
) -> AsyncGenerator[StreamResponse, None]:
    """Stream query response from Google Gemini."""
    # Input validation
    if not query.strip():
        raise WebError(
            message="Empty query is not allowed",
            code=ErrorCodes.WEB_API_ERROR,
            causes=["Query cannot be empty"],
            hint_stmt="Please provide a non-empty query",
        )

    client = manager.get_client(api_key)

    try:
        # Get streaming response from Gemini
        response: Generator[Any, None, None] = client.models.generate_content_stream(  # type: ignore
            model=model,
            contents=[query],
            config={
                "max_output_tokens": max_output_tokens,
                "temperature": temperature,
                "top_p": top_p,
                "top_k": top_k,
            },
        )

        # Convert regular generator to async generator
        for chunk in response:
            text = chunk.text if hasattr(chunk, "text") else ""
            if text is None:
                text = ""
            yield {"text": text, "done": False}

        yield {"text": "", "done": True}
    except WebError:
        raise
    except ClientError as e:
        if "NOT_FOUND" in str(e):
            raise WebError(
                message=f"Invalid model: {model}",
                code=ErrorCodes.GEMINI_MODEL_ERROR,
                causes=[str(e)],
                hint_stmt="Check the model name and try again",
            ) from e
        elif "RESOURCE_EXHAUSTED" in str(e):
            raise WebError(
                message="API rate limit exceeded",
                code=ErrorCodes.GEMINI_API_KEY_ERROR,
                causes=[str(e)],
                hint_stmt="Please try again later or reduce the number of concurrent requests",
            ) from e
        else:
            raise WebError(
                message="Error during API call",
                code=ErrorCodes.GEMINI_API_ERROR,
                causes=[str(e)],
                hint_stmt="Check your internet connection and API key",
            ) from e
    except Exception as e:
        raise WebError(
            message="Error during API call",
            code=ErrorCodes.GEMINI_API_ERROR,
            causes=[str(e)],
            hint_stmt="Check your internet connection and API key",
        ) from e


async def stream_query_with_context(
    query: str,
    model: str,
    max_output_tokens: int,
    temperature: float,
    top_p: float,
    top_k: int,
    api_key: str,
    manager: GeminiManager,
    context_file: Optional[pathlib.Path] = None,
) -> AsyncGenerator[StreamResponse, None]:
    """Stream query response from Google Gemini with optional file context."""
    # Input validation
    if not query.strip():
        raise WebError(
            message="Empty query is not allowed",
            code=ErrorCodes.WEB_API_ERROR,
            causes=["Query cannot be empty"],
            hint_stmt="Please provide a non-empty query",
        )

    client = manager.get_client(api_key)

    try:
        contents: list[Union[genai_types.Content, genai_types.File, str]] = []

        # Handle file context if provided
        if context_file:
            try:
                file_obj: genai_types.File = client.files.upload(file=context_file)  # type: ignore
                contents.append(file_obj)
            except Exception as e:
                raise WebError(
                    message="Failed to upload context file",
                    code=ErrorCodes.GEMINI_FILE_ERROR,
                    causes=[str(e)],
                    hint_stmt="Check file permissions and format",
                ) from e

        # Add query
        contents.append(query)

        # Get streaming response from Gemini
        response: Generator[genai_types.GenerateContentResponse, None, None] = (
            client.models.generate_content_stream(  # type: ignore
                model=model,
                contents=contents,
                config={
                    "max_output_tokens": max_output_tokens,
                    "temperature": temperature,
                    "top_p": top_p,
                    "top_k": top_k,
                },
            )
        )

        # Convert regular generator to async generator
        for chunk in response:
            text = chunk.text if hasattr(chunk, "text") else ""
            if text is None:
                text = ""
            yield {"text": text, "done": False}

        yield {"text": "", "done": True}
    except WebError:
        raise
    except ClientError as e:
        if "NOT_FOUND" in str(e):
            raise WebError(
                message=f"Invalid model: {model}",
                code=ErrorCodes.GEMINI_MODEL_ERROR,
                causes=[str(e)],
                hint_stmt="Check the model name and try again",
            ) from e
        elif "RESOURCE_EXHAUSTED" in str(e):
            raise WebError(
                message="API rate limit exceeded",
                code=ErrorCodes.GEMINI_API_KEY_ERROR,
                causes=[str(e)],
                hint_stmt="Please try again later or reduce the number of concurrent requests",
            ) from e
        else:
            raise WebError(
                message="Error during API call",
                code=ErrorCodes.GEMINI_API_ERROR,
                causes=[str(e)],
                hint_stmt="Check your internet connection and API key",
            ) from e
    except Exception as e:
        raise WebError(
            message="Error during API call",
            code=ErrorCodes.GEMINI_API_ERROR,
            causes=[str(e)],
            hint_stmt="Check your internet connection and API key",
        ) from e


def format_response(response: str) -> Panel:
    """Format response for display."""
    return Panel(
        Markdown(response),
        title="[#af87ff]Google Gemini's Response[/]",
        border_style="bold #d7af00",
        padding=(1, 2),
    )
