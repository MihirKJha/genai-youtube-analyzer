"""
AI provider factory.

Creates the configured language-model provider without exposing
provider-specific implementation details to the application layer.
"""

from app.ai.base_provider import LLMProvider
from app.ai.providers.local_provider import LocalLLMProvider
from app.ai.providers.watsonx_provider import WatsonxLLMProvider
from app.config import AI_PROVIDER


def create_llm_provider() -> LLMProvider:
    """
    Create the configured LLM provider.

    Returns:
        Configured LLM provider instance.

    Raises:
        RuntimeError: If the configured provider is unsupported.
    """
    if AI_PROVIDER == "local":
        return LocalLLMProvider()

    if AI_PROVIDER == "watsonx":
        return WatsonxLLMProvider()

    raise RuntimeError(f"Unsupported AI provider: '{AI_PROVIDER}'.")
