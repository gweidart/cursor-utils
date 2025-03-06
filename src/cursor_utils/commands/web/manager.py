"""
Manager module for web command configuration and client management.

Key Components:
    WebManager: Manages configuration and client lifecycle
    create_client: Factory function for client creation

Project Dependencies:
    This file uses: pyplexityai: For API client
    This file uses: types: For type definitions
    This file uses: errors: For standardized error handling
    This file is used by: actions: For client operations
"""

from typing import Optional

from pyplexityai import AsyncPerplexityClient
from rich.console import Console

from cursor_utils.config import Config
from cursor_utils.errors import ErrorCodes, WebError
from cursor_utils.types import ModelType, ModeType, SearchFocusType, WebConfig

console = Console()


class WebManager:
    """Manager for web command configuration and client lifecycle."""

    def __init__(self) -> None:
        """Initialize web manager."""
        self._client: Optional[AsyncPerplexityClient] = None
        self.config = Config()

    def load_config(self) -> Optional[WebConfig]:
        """Load web configuration from yaml file."""
        try:
            config = self.config.load_config()
            web_config = config.get("web", {})
            if not web_config or not all(
                k in web_config for k in ("model", "mode", "search_focus")
            ):
                return None
            return {
                "model": web_config["model"],
                "mode": web_config["mode"],
                "search_focus": web_config["search_focus"],
            }
        except Exception as e:
            raise WebError(
                message="Failed to load web configuration",
                code=ErrorCodes.WEB_CONFIG_ERROR,
                causes=[str(e)],
                hint_stmt="Check your configuration file permissions and format",
            ) from e

    def save_config(
        self, model: ModelType, mode: ModeType, search_focus: SearchFocusType
    ) -> None:
        """Save web configuration to yaml file."""
        try:
            # Load existing config
            config = self.config.load_config()

            # Update web section
            web_config: WebConfig = {
                "model": model,
                "mode": mode,
                "search_focus": search_focus,
            }
            config["web"] = web_config

            # Save updated config
            self.config.save_config(config)
        except Exception as e:
            raise WebError(
                message="Failed to save web configuration",
                code=ErrorCodes.WEB_CONFIG_ERROR,
                causes=[str(e)],
                hint_stmt="Check your configuration file permissions",
            ) from e

    def get_client(self, api_key: str) -> AsyncPerplexityClient:
        """Get or create Perplexity AI client."""
        try:
            # Always create a new client to ensure we're using the correct API key
            self._client = AsyncPerplexityClient(api_key=api_key)
            return self._client
        except Exception as e:
            raise WebError(
                message="Failed to create Perplexity AI client",
                code=ErrorCodes.WEB_API_ERROR,
                causes=[str(e)],
                hint_stmt="Check your API key and internet connection",
            ) from e


async def create_client(api_key: str) -> AsyncPerplexityClient:
    """Create a new Perplexity AI client."""
    try:
        return AsyncPerplexityClient(api_key=api_key)
    except Exception as e:
        raise WebError(
            message="Failed to create Perplexity AI client",
            code=ErrorCodes.WEB_API_ERROR,
            causes=[str(e)],
            hint_stmt="Check your API key and internet connection",
        ) from e
