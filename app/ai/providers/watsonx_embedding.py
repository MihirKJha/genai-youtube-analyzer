"""
IBM watsonx.ai embedding provider.

Provides document and query embeddings through IBM watsonx.ai
while exposing the application-level EmbeddingProvider interface.
"""

from langchain_ibm import WatsonxEmbeddings

from app.ai.base_embedding import EmbeddingProvider
from app.config import (
    WATSONX_API_KEY,
    WATSONX_EMBEDDING_MODEL_ID,
    WATSONX_PROJECT_ID,
    WATSONX_URL,
)


class WatsonxEmbeddingProvider(EmbeddingProvider):
    """Embedding provider backed by IBM watsonx.ai."""

    def __init__(self):
        """Initialize the Watsonx embedding provider."""
        required_settings = {
            "WATSONX_URL": WATSONX_URL,
            "WATSONX_API_KEY": WATSONX_API_KEY,
            "WATSONX_PROJECT_ID": WATSONX_PROJECT_ID,
            "WATSONX_EMBEDDING_MODEL_ID": WATSONX_EMBEDDING_MODEL_ID,
        }

        missing_settings = [
            name for name, value in required_settings.items() if not value
        ]

        if missing_settings:
            raise RuntimeError(
                "Missing Watsonx embedding configuration: "
                + ", ".join(missing_settings)
            )

        self.embeddings = WatsonxEmbeddings(
            model_id=WATSONX_EMBEDDING_MODEL_ID,
            url=WATSONX_URL,
            project_id=WATSONX_PROJECT_ID,
        )

    def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple documents.

        Args:
            texts: Documents to embed.

        Returns:
            Embedding vectors.
        """
        return self.embeddings.embed_documents(texts)

    def embed_query(self, text: str) -> list[float]:
        """
        Generate an embedding for a query.

        Args:
            text: Query text.

        Returns:
            Embedding vector.
        """
        return self.embeddings.embed_query(text)
