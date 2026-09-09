"""
Local LLM provider.

Provides text generation through a locally hosted LLM service
using an HTTP API.
"""

import requests

from app.ai.base_provider import LLMProvider
from app.config import (
    LOCAL_LLM_BASE_URL,
    LOCAL_LLM_MODEL,
    LOCAL_LLM_TIMEOUT,
)


class LocalLLMProvider(LLMProvider):
    """LLM provider for a locally hosted model."""

    def __init__(self):
        """Initialize the local LLM provider from application configuration."""
        if not LOCAL_LLM_BASE_URL:
            raise RuntimeError("LOCAL_LLM_BASE_URL is not configured.")

        if not LOCAL_LLM_MODEL:
            raise RuntimeError("LOCAL_LLM_MODEL is not configured.")

        self.base_url = LOCAL_LLM_BASE_URL.rstrip("/")
        self.model = LOCAL_LLM_MODEL
        self.timeout = LOCAL_LLM_TIMEOUT

    def generate(self, prompt: str) -> str:
        """
        Generate text using the configured local LLM.

        Args:
            prompt: Input prompt sent to the language model.

        Returns:
            Generated text response.

        Raises:
            RuntimeError: If the local LLM service cannot be reached
                or returns an invalid response.
        """
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                },
                timeout=self.timeout,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            raise RuntimeError(
                "Unable to communicate with the local LLM service."
            ) from exc

        try:
            data = response.json()
            return data["response"]
        except (ValueError, KeyError) as exc:
            raise RuntimeError(
                "Local LLM service returned an invalid response."
            ) from exc
