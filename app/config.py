"""
Application configuration.

Loads runtime configuration from environment variables so that
local development and cloud deployments can use different AI
providers without changing application code.
"""

import os

from dotenv import load_dotenv

load_dotenv()


def get_required_setting(name: str) -> str:
    """
    Read a required environment variable.

    Args:
        name: Environment variable name.

    Returns:
        Configured environment variable value.

    Raises:
        RuntimeError: If the variable is missing or empty.
    """
    value = os.getenv(name)

    if not value:
        raise RuntimeError(f"Required environment variable '{name}' is not configured.")

    return value


AI_PROVIDER = get_required_setting("AI_PROVIDER")
EMBEDDING_PROVIDER = get_required_setting("EMBEDDING_PROVIDER")
RETRIEVAL_PROVIDER = get_required_setting("RETRIEVAL_PROVIDER")

LOCAL_LLM_BASE_URL = os.getenv("LOCAL_LLM_BASE_URL")
LOCAL_LLM_MODEL = os.getenv("LOCAL_LLM_MODEL")
LOCAL_LLM_TIMEOUT = int(os.getenv("LOCAL_LLM_TIMEOUT", "120"))

WATSONX_URL = os.getenv("WATSONX_URL")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_MODEL_ID = os.getenv("WATSONX_MODEL_ID")

LOCAL_EMBEDDING_MODEL = os.getenv("LOCAL_EMBEDDING_MODEL")
WATSONX_EMBEDDING_MODEL_ID = os.getenv("WATSONX_EMBEDDING_MODEL_ID")

MAX_NEW_TOKENS = int(os.getenv("MAX_NEW_TOKENS", "900"))
DECODING_METHOD = os.getenv("DECODING_METHOD", "greedy")

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "7860"))
SHARE = os.getenv("SHARE", "True").lower() == "true"

CHROMA_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "transcripts")
CHROMA_PERSIST_DIRECTORY = os.getenv("CHROMA_PERSIST_DIRECTORY", "chroma_persist")
