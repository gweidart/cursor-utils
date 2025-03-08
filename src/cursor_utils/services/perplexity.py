"""
Perplexity API client for cursor-utils.

Key Components:
    PerplexityClient: Client for the Perplexity API
    PerplexityModel: Enum of supported Perplexity models
    PerplexityResponse: Response from the Perplexity API

Project Dependencies:
    This file uses: errors: For API-related errors
                   config: For API key management
    This file is used by: Web search command
"""

import os
from collections.abc import AsyncIterator
from enum import Enum
from typing import Any, Optional, Union

import httpx

from cursor_utils.core.config import Configuration
from cursor_utils.core.errors import ServiceError


class PerplexityModel(str, Enum):
    """Supported Perplexity models."""

    SONAR = "sonar"
    MIXTRAL = "mixtral-8x7b-instruct"
    CODELLAMA = "codellama-70b-instruct"
    LLAMA3 = "llama-3-70b-instruct"


class PerplexityError(ServiceError):
    """Error related to the Perplexity API."""

    def __init__(
        self, message: str, exit_code: int = 10, help_text: Optional[str] = None
    ):
        super().__init__(message, "perplexity", exit_code, help_text)


class PerplexityResponse:
    """Response from the Perplexity API."""

    def __init__(self, data: dict[str, Any]):
        """
        Initialize the response.

        Args:
            data: The response data

        """
        self.data = data
        self.id = data.get("id", "")

        # Try to extract text from different possible response formats
        if "text" in data:
            self.text = data.get("text", "")
        elif "choices" in data and len(data["choices"]) > 0:
            choice = data["choices"][0]
            if "message" in choice and "content" in choice["message"]:
                self.text = choice["message"]["content"]
            elif "text" in choice:
                self.text = choice["text"]
            else:
                self.text = str(choice)
        else:
            self.text = str(data)

        self.sources = data.get("sources", [])

    def __str__(self) -> str:
        """
        Get the response as a string.

        Returns:
            The response text

        """
        return self.text

    def get_formatted_text(self) -> str:
        """
        Get the formatted response text with sources.

        Returns:
            The formatted response text

        """
        text = self.text

        if self.sources:
            text += "\n\nSources:\n"
            for i, source in enumerate(self.sources, 1):
                title = source.get("title", "Untitled")
                url = source.get("url", "")
                text += f"{i}. [{title}]({url})\n"

        return text


class PerplexityClient:
    """Client for the Perplexity API."""

    def __init__(
        self, api_key: Optional[str] = None, config: Optional[Configuration] = None
    ):
        """
        Initialize the client.

        Args:
            api_key: The API key, or None to use the configuration
            config: The configuration, or None to use the default

        Raises:
            PerplexityError: If the API key is not provided and not in the configuration

        """
        self.config = config or Configuration()

        # Try to get the API key from the provided parameter, config, or environment variables
        self.api_key = api_key

        # If no API key was provided directly, try the config
        if not self.api_key:
            self.api_key = self.config.get("perplexity_api_key")

        # If still no API key, try the environment variable directly
        if not self.api_key:
            self.api_key = os.environ.get("PERPLEXITY_API_KEY")

        # If we still don't have an API key, raise an error
        if not self.api_key:
            raise PerplexityError(
                "Perplexity API key not found",
                help_text="Set the PERPLEXITY_API_KEY environment variable or "
                "run 'cursor-utils config set perplexity_api_key YOUR_API_KEY'",
            )

        self.base_url = "https://api.perplexity.ai"

    async def query_async(
        self,
        query: str,
        model: Union[str, PerplexityModel] = PerplexityModel.SONAR,
    ) -> Union[PerplexityResponse, AsyncIterator[str]]:
        """
        Query the Perplexity API asynchronously.

        Args:
            query: The query text
            model: The model to use

        Returns:
            The response or a stream of response chunks

        Raises:
            PerplexityError: If the query fails

        """
        # Convert string model to enum
        model_value: str
        try:
            if isinstance(model, PerplexityModel):
                model_value = model.value
            else:
                model_enum = PerplexityModel(model.lower())
                model_value = model_enum.value
        except ValueError:
            raise PerplexityError(
                f"Unsupported model: {model}",
                help_text=f"Supported models: {', '.join(m.value for m in PerplexityModel)}",
            )

        # Prepare the request
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        data = {
            "model": model_value,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": query},
            ],
        }

        try:
            # Perform the query
            return await self._sync_query_async(url, headers, data)
        except httpx.HTTPStatusError as e:
            raise PerplexityError(
                f"Perplexity API error: {e.response.status_code} {e.response.reason_phrase}",
                help_text=f"API response: {e.response.text}",
            )
        except httpx.ConnectError as e:
            raise PerplexityError(
                f"Failed to connect to Perplexity API: {e}",
                help_text="Check your internet connection.",
            )
        except Exception as e:
            raise PerplexityError(f"Unexpected error: {e}")

    async def _sync_query_async(
        self, url: str, headers: dict[str, str], data: dict[str, Any]
    ) -> PerplexityResponse:
        """
        Perform a synchronous query asynchronously.

        Args:
            url: The API URL
            headers: The request headers
            data: The request data

        Returns:
            The response

        Raises:
            httpx.HTTPStatusError: If the request fails

        """
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, headers=headers, json=data)
            response.raise_for_status()
            return PerplexityResponse(response.json())
