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

import asyncio
import pathlib
from collections.abc import AsyncGenerator, Generator
from typing import Any, Optional, Protocol, cast

from google.genai import types as genai_types
from google.genai.errors import ClientError
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from cursor_utils.commands.gemini.manager import GeminiManager
from cursor_utils.config import APIKeyType
from cursor_utils.errors import ErrorCodes, WebError
from cursor_utils.types import GeminiConfig, StreamResponse
from cursor_utils.utils.api_helpers import (
    get_api_key as get_api_key_helper,
    validate_api_key,
)
from cursor_utils.utils.config_helpers import ensure_config as ensure_config_helper

console = Console()

DEFAULT_MODEL = "gemini-2.0-flash"
DEFAULT_MAX_OUTPUT_TOKENS = 2048
DEFAULT_TEMPERATURE = 0.7
DEFAULT_TOP_P = 0.95
DEFAULT_TOP_K = 40


# Protocol for Gemini client to satisfy type checker
class GeminiClientProtocol(Protocol):
    """Protocol for Gemini client."""

    models: Any
    files: Any


# Protocol for Gemini models to satisfy type checker
class GeminiModelsProtocol(Protocol):
    """Protocol for Gemini models."""

    def generate_content_stream(
        self, *, model: str, contents: list[str], config: Any
    ) -> Generator[Any, None, None]:
        """Generate content stream."""
        ...


def ensure_config(manager: GeminiManager, silent: bool = False) -> GeminiConfig:
    """Ensure configuration exists or guide user to create it."""
    required_keys = ["model", "max_output_tokens", "temperature", "top_p", "top_k"]
    defaults = {
        "model": DEFAULT_MODEL,
        "max_output_tokens": DEFAULT_MAX_OUTPUT_TOKENS,
        "temperature": DEFAULT_TEMPERATURE,
        "top_p": DEFAULT_TOP_P,
        "top_k": DEFAULT_TOP_K,
    }

    try:
        config = ensure_config_helper(manager, required_keys, defaults, silent=silent)
        return cast(GeminiConfig, config)
    except Exception as e:
        raise WebError(
            message="Failed to load or create Gemini configuration",
            code=ErrorCodes.WEB_CONFIG_ERROR,
            causes=[str(e)],
            hint_stmt="Check your configuration file permissions and format",
        ) from e


def get_api_key() -> str:
    """
    Get Google Gemini API key from environment or prompt user.

    Returns:
        str: API key

    Raises:
        WebError: If API key is invalid or not provided

    """
    try:
        api_key = get_api_key_helper(APIKeyType.GEMINI, "GEMINI_API_KEY")
        validate_api_key(api_key, APIKeyType.GEMINI, "GEMINI_API_KEY")
        return api_key
    except Exception as e:
        raise WebError(
            message="Failed to get Google Gemini API key",
            code=ErrorCodes.INVALID_API_KEY,
            causes=[str(e)],
            hint_stmt="Set GEMINI_API_KEY environment variable or run 'cursor-utils config api_keys'",
        ) from e


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
    """Stream query response from Gemini API."""
    try:
        # Configure generation parameters
        generation_config = genai_types.GenerationConfig(
            max_output_tokens=max_output_tokens,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
        )

        # Import here to avoid circular imports
        from google.genai import genai  # type: ignore

        # Create a client with the API key
        gemini_client = cast(Any, genai.Client(api_key=api_key))  # type: ignore

        # Stream the response
        response = cast(
            Generator[genai_types.GenerateContentResponse, None, None],
            gemini_client.models.generate_content_stream(
                model=model,
                contents=[query],
                config=generation_config,
            ),
        )

        for chunk in response:
            if hasattr(chunk, "text") and chunk.text:
                yield {"text": chunk.text, "done": False}
                await asyncio.sleep(0)  # Yield control to event loop

        yield {"text": "", "done": True}
    except ClientError as e:
        if "API key not valid" in str(e):
            raise WebError(
                message="Invalid Gemini API key",
                code=ErrorCodes.GEMINI_API_KEY_ERROR,
                causes=[str(e)],
                hint_stmt="Please check your API key and try again. You can set a new API key with 'cursor-utils config set-api-key gemini'.",
            ) from e
        elif "model not found" in str(e).lower():
            raise WebError(
                message="Invalid Gemini model",
                code=ErrorCodes.GEMINI_MODEL_ERROR,
                causes=[str(e)],
                hint_stmt=f"The model '{model}' is not available. Please check the model name and try again.",
            ) from e
        elif "quota exceeded" in str(e).lower():
            raise WebError(
                message="Gemini API quota exceeded",
                code=ErrorCodes.GEMINI_API_ERROR,
                causes=[str(e)],
                hint_stmt="You have exceeded your Gemini API quota. Please try again later or upgrade your API plan.",
            ) from e
        else:
            raise WebError(
                message="Gemini API error",
                code=ErrorCodes.GEMINI_API_ERROR,
                causes=[str(e)],
                hint_stmt="An error occurred while calling the Gemini API. Please try again later.",
            ) from e
    except (ConnectionError, TimeoutError) as e:
        raise WebError(
            message="Connection error",
            code=ErrorCodes.GEMINI_API_ERROR,
            causes=[str(e)],
            hint_stmt="Could not connect to the Gemini API. Please check your internet connection and try again.",
        ) from e
    except Exception as e:
        raise WebError(
            message="Unexpected error",
            code=ErrorCodes.GEMINI_API_ERROR,
            causes=[str(e)],
            hint_stmt="An unexpected error occurred. Please try again later.",
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
        contents: genai_types.ContentListUnion | genai_types.ContentListUnionDict = []

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
