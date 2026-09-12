"""
IBM watsonx.ai LLM provider.

Provides text generation through IBM watsonx.ai while exposing
the application-level LLMProvider interface.
"""

import logging

from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import Model
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from langchain_ibm import WatsonxLLM

from app.ai.base_provider import LLMProvider
from app.config import (
    DECODING_METHOD,
    MAX_NEW_TOKENS,
    WATSONX_API_KEY,
    WATSONX_MODEL_ID,
    WATSONX_PROJECT_ID,
    WATSONX_URL,
)

logger = logging.getLogger(__name__)


class WatsonxLLMProvider(LLMProvider):
    """LLM provider backed by IBM watsonx.ai."""

    def __init__(self):
        """Initialize the Watsonx provider from application configuration."""
        required_settings = {
            "WATSONX_URL": WATSONX_URL,
            "WATSONX_API_KEY": WATSONX_API_KEY,
            "WATSONX_PROJECT_ID": WATSONX_PROJECT_ID,
            "WATSONX_MODEL_ID": WATSONX_MODEL_ID,
        }

        missing_settings = [
            name for name, value in required_settings.items() if not value
        ]

        if missing_settings:
            logger.error(
                "Missing Watsonx configuration: %s", ", ".join(missing_settings)
            )

            raise RuntimeError(
                "Missing Watsonx configuration: " + ", ".join(missing_settings)
            )

        credentials = Credentials(
            url=WATSONX_URL,
            api_key=WATSONX_API_KEY,
        )

        generate_params = {
            GenParams.DECODING_METHOD: DECODING_METHOD,
            GenParams.MAX_NEW_TOKENS: MAX_NEW_TOKENS,
        }

        model = Model(
            model_id=WATSONX_MODEL_ID,
            params=generate_params,
            credentials=credentials,
            project_id=WATSONX_PROJECT_ID,
        )

        self.llm = WatsonxLLM(watsonx_model=model)

    def generate(self, prompt: str) -> str:
        """
        Generate text using IBM watsonx.ai.

        Args:
            prompt: Input prompt sent to the language model.

        Returns:
            Generated text response.
        """
        logger.info("Invoking watsonx.ai llm with prompt: %s", prompt)

        return self.llm.invoke(prompt)
