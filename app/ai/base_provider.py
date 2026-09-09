"""
AI provider interfaces.

Defines the contracts that application capabilities use for
text generation without depending on a specific AI provider.
"""

from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """Abstract interface for a text-generation provider."""

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Generate a text response from the supplied prompt.

        Args:
            prompt: Input prompt sent to the language model.

        Returns:
            Generated text response.
        """
        raise NotImplementedError
