"""
Google Gemini API client for cursor-utils.

Key Components:
    GeminiClient: Client for the Google Gemini API
    GeminiModel: Enum of supported Gemini models
    GeminiResponse: Response from the Gemini API

Project Dependencies:
    This file uses: errors: For API-related errors
                   config: For API key management
    This file is used by: Gemini command
"""

import os
from enum import Enum
from typing import Any, Optional, Union

import httpx

from cursor_utils.core.config import Configuration
from cursor_utils.core.errors import ServiceError


class GeminiModel(str, Enum):
    """Supported Gemini models."""

    GEMINI_1_5_PRO = "gemini-1.5-pro"
    GEMINI_1_5_FLASH = "gemini-1.5-flash"
    GEMINI_2_0_FLASH = "gemini-2.0-flash"
    GEMINI_PRO_VISION = "gemini-pro-vision"


class GeminiError(ServiceError):
    """Error related to the Gemini API."""

    def __init__(
        self, message: str, exit_code: int = 11, help_text: Optional[str] = None
    ):
        super().__init__(message, "gemini", exit_code, help_text)


class GeminiResponse:
    """Response from the Gemini API."""

    def __init__(self, data: dict[str, Any]):
        """
        Initialize the response.

        Args:
            data: The response data

        """
        self.data = data
        self.text = ""

        # Extract the text from the response
        if data.get("candidates"):
            candidate = data["candidates"][0]
            if candidate.get("content"):
                content = candidate["content"]
                if content.get("parts"):
                    part = content["parts"][0]
                    if "text" in part:
                        self.text = part["text"]

    def __str__(self) -> str:
        """
        Get the response as a string.

        Returns:
            The response text

        """
        return self.text


class GeminiClient:
    """Client for the Google Gemini API."""

    def __init__(
        self, api_key: Optional[str] = None, config: Optional[Configuration] = None
    ):
        """
        Initialize the client.

        Args:
            api_key: The API key, or None to use the configuration
            config: The configuration, or None to use the default

        Raises:
            GeminiError: If the API key is not provided and not in the configuration

        """
        self.config = config or Configuration()
        self.api_key = api_key or self.config.get("gemini_api_key")

        if not self.api_key:
            self.api_key = os.environ.get("GEMINI_API_KEY")

        if not self.api_key:
            raise GeminiError(
                "Gemini API key not found",
                help_text="Set the GEMINI_API_KEY environment variable or "
                "run 'cursor-utils config set gemini_api_key YOUR_API_KEY'",
            )

        self.base_url = "https://generativelanguage.googleapis.com/v1"

    async def generate_content(
        self,
        prompt: str,
        model: Union[str, GeminiModel] = GeminiModel.GEMINI_1_5_PRO,
        stream: bool = False,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        system_instruction: Optional[str] = None,
        debug: bool = False,
    ) -> GeminiResponse:
        """
        Generate content with the Gemini API asynchronously.

        Args:
            prompt: The prompt text
            model: The model to use
            stream: Whether to stream the response (currently not supported)
            temperature: The temperature for sampling
            max_tokens: The maximum number of tokens to generate
            system_instruction: The system instruction
            debug: Whether to print debug information

        Returns:
            The response

        Raises:
            GeminiError: If the generation fails

        """
        # Convert string model to enum if needed
        model_value: str
        if isinstance(model, GeminiModel):
            model_value = model.value
        else:
            # It's a string
            try:
                model_enum = GeminiModel(model)
                model_value = model_enum.value
            except ValueError:
                # Use the string value directly if it's not in our enum
                model_value = model

        # Prepare the request
        url = f"{self.base_url}/models/{model_value}:generateContent"
        # Note: Streaming is not currently implemented
        # if stream:
        #     url = f"{self.base_url}/models/{model_value}:streamGenerateContent"

        # We know this is a string
        api_key_str: str = str(self.api_key)
        params: dict[str, str] = {"key": api_key_str}

        data: dict[str, Any] = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": temperature,
            },
        }

        if max_tokens:
            data["generationConfig"]["maxOutputTokens"] = max_tokens

        if system_instruction:
            data["systemInstruction"] = {"parts": [{"text": system_instruction}]}

        try:
            return await self._sync_generate_async(url, params, data, debug)
        except httpx.HTTPStatusError as e:
            raise GeminiError(
                f"Gemini API error: {e.response.status_code} {e.response.reason_phrase}",
                help_text=f"Response: {e.response.text}",
            )
        except httpx.RequestError as e:
            raise GeminiError(
                f"Failed to connect to Gemini API: {e}",
                help_text="Check your internet connection.",
            )
        except Exception as e:
            raise GeminiError(f"Unexpected error: {e}")

    async def _sync_generate_async(
        self,
        url: str,
        params: dict[str, str],
        data: dict[str, Any],
        debug: bool = False,
    ) -> GeminiResponse:
        """
        Perform a synchronous content generation asynchronously.

        Args:
            url: The API URL
            params: The query parameters
            data: The request data
            debug: Whether to print debug information

        Returns:
            The response

        Raises:
            httpx.HTTPStatusError: If the request fails

        """
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(url, params=params, json=data)

                response.raise_for_status()

                return GeminiResponse(response.json())
            except httpx.HTTPStatusError:
                raise
            except Exception:
                raise
