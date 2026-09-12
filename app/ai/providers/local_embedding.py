"""
Local embedding provider.

Provides text embeddings through a locally hosted embedding service.
"""

import logging

import requests

from app.ai.base_embedding import EmbeddingProvider
from app.config import (
    LOCAL_EMBEDDING_MODEL,
    LOCAL_LLM_BASE_URL,
    LOCAL_LLM_TIMEOUT,
)

logger = logging.getLogger(__name__)


class LocalEmbeddingProvider(EmbeddingProvider):
    """Embedding provider for a locally hosted embedding model."""

    def __init__(self):
        """Initialize the local embedding provider from configuration."""
        if not LOCAL_LLM_BASE_URL:
            logger.error("LOCAL_LLM_BASE_URL is not configured.")
            raise RuntimeError("LOCAL_LLM_BASE_URL is not configured.")

        if not LOCAL_EMBEDDING_MODEL:
            logger.error("LOCAL_EMBEDDING_MODEL is not configured.")
            raise RuntimeError("LOCAL_EMBEDDING_MODEL is not configured.")

        self.base_url = LOCAL_LLM_BASE_URL.rstrip("/")
        self.model = LOCAL_EMBEDDING_MODEL
        self.timeout = LOCAL_LLM_TIMEOUT

    def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple documents.

        Args:
            texts: Documents to embed.

        Returns:
            Embedding vectors for the supplied documents.
        """

        logger.info("Generating local embeddings for documents")

        return [self.embed_query(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        """
        Generate an embedding for a single text.

        Args:
            text: Text to embed.

        Returns:
            Embedding vector.

        Raises:
            RuntimeError: If the embedding service cannot be reached
                or returns an invalid response.
        """

        logger.info("Generating local embeddings for query")

        try:
            response = requests.post(
                f"{self.base_url}/api/embed",
                json={
                    "model": self.model,
                    "input": text,
                },
                timeout=self.timeout,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            logger.exception("Unable to communicate with the local embedding service.")
            raise RuntimeError(
                "Unable to communicate with the local embedding service."
            ) from exc

        try:
            data = response.json()
            embeddings = data["embeddings"]

            if not embeddings:
                logger.error("No embedding returned.")
                raise ValueError("No embedding returned.")

            return embeddings[0]

        except (ValueError, KeyError, TypeError) as exc:
            logger.exception("Local embedding service returned an invalid response.")
            raise RuntimeError(
                "Local embedding service returned an invalid response."
            ) from exc
