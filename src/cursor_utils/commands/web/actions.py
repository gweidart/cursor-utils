"""
Actions for web command implementation.

Key Components:
    ensure_config: Ensures configuration exists
    get_api_key: Gets API key from environment or prompts user
    stream_query: Streams query response from Perplexity API
    format_response: Formats response for display

Project Dependencies:
    This file uses: pyplexityai: For Perplexity API integration
    This file uses: cursor_utils.config: For configuration management
    This file is used by: command: For CLI interface
"""

from collections.abc import AsyncGenerator, AsyncIterable
from typing import Protocol, cast

from httpx import ConnectTimeout, ReadTimeout, RequestError
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from cursor_utils.commands.web.manager import WebManager
from cursor_utils.config import APIKeyType
from cursor_utils.errors import ErrorCodes, WebError
from cursor_utils.types import (
    ModelType,
    ModeType,
    SearchFocusType,
    StreamResponse,
    WebConfig,
)
from cursor_utils.utils.api_helpers import (
    get_api_key as get_api_key_helper,
    validate_api_key,
)
from cursor_utils.utils.config_helpers import ensure_config as ensure_config_helper

# Constants
DEFAULT_MODEL = "sonar"
DEFAULT_MODE = "copilot"
DEFAULT_SEARCH_FOCUS = "internet"

console = Console()


# Protocol for AsyncPerplexityClient to satisfy type checker
class AsyncPerplexityClientProtocol(Protocol):
    """Protocol for AsyncPerplexityClient."""

    def query(
        self,
        query: str,
        model: ModelType,
        mode: ModeType,
        search_focus: SearchFocusType,
    ) -> AsyncIterable[str]:
        """Query the Perplexity API."""
        ...


def ensure_config(manager: WebManager) -> WebConfig:
    """Ensure configuration exists or guide user to create it."""
    required_keys = ["model", "mode", "search_focus"]
    defaults = {
        "model": DEFAULT_MODEL,
        "mode": DEFAULT_MODE,
        "search_focus": DEFAULT_SEARCH_FOCUS,
    }

    try:
        config = ensure_config_helper(manager, required_keys, defaults)
        return cast(WebConfig, config)
    except Exception as e:
        raise WebError(
            message="Failed to load or create web configuration",
            code=ErrorCodes.WEB_CONFIG_ERROR,
            causes=[str(e)],
            hint_stmt="Check your configuration file permissions and format",
        ) from e


def get_api_key() -> str:
    """
    Get Perplexity API key from environment or prompt user.

    Returns:
        str: API key

    Raises:
        WebError: If API key is invalid or not provided

    """
    try:
        api_key = get_api_key_helper(APIKeyType.PERPLEXITY, "PERPLEXITY_API_KEY")
        validate_api_key(api_key, APIKeyType.PERPLEXITY, "PERPLEXITY_API_KEY")
        return api_key
    except Exception as e:
        raise WebError(
            message="Failed to get Perplexity API key",
            code=ErrorCodes.INVALID_API_KEY,
            causes=[str(e)],
            hint_stmt="Set PERPLEXITY_API_KEY environment variable or run 'cursor-utils config api_keys'",
        ) from e


async def stream_query(
    query: str,
    model: ModelType,
    mode: ModeType,
    search_focus: SearchFocusType,
    api_key: str,
    manager: WebManager,
) -> AsyncGenerator[StreamResponse, None]:
    """Stream query response from Perplexity AI."""
    try:
        client = cast(AsyncPerplexityClientProtocol, manager.get_client(api_key))

        # Stream the response
        # The client.query method returns an AsyncIterable of strings
        response_stream = client.query(
            query=query,
            model=model,
            mode=mode,
            search_focus=search_focus,
        )

        async for response_text in response_stream:
            yield {"text": response_text, "done": False}

        yield {"text": "", "done": True}
    except (ConnectTimeout, ReadTimeout) as e:
        raise WebError(
            message="Connection to Perplexity API timed out",
            code=ErrorCodes.WEB_TIMEOUT_ERROR,
            causes=[str(e)],
            hint_stmt="Check your internet connection and try again",
        ) from e
    except RequestError as e:
        raise WebError(
            message="Error connecting to Perplexity API",
            code=ErrorCodes.WEB_CONNECTION_ERROR,
            causes=[str(e)],
            hint_stmt="Check your internet connection and try again",
        ) from e
    except Exception as e:
        raise WebError(
            message="Error querying Perplexity API",
            code=ErrorCodes.WEB_API_ERROR,
            causes=[str(e)],
            hint_stmt="Check your API key and try again",
        ) from e


def format_response(response: str) -> Panel:
    """Format response for display."""
    return Panel(
        Markdown(response),
        title="[#af87ff]Perplexity AI's Response[/]",
        border_style="bold #d7af00",
        padding=(1, 2),
    )
