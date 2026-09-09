"""
Embedding provider interface.

Defines the contract used by the application for generating
vector embeddings without coupling it to a specific provider.
"""

from abc import ABC, abstractmethod

from langchain_core.embeddings import Embeddings


class EmbeddingProvider(Embeddings, ABC):
    """Abstract interface for an embedding provider."""

    @abstractmethod
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """
        Generate embeddings for multiple text documents.

        Args:
            texts: Text documents to embed.

        Returns:
            Embedding vectors for the supplied documents.
        """
        raise NotImplementedError

    @abstractmethod
    def embed_query(self, text: str) -> list[float]:
        """
        Generate an embedding for a query.

        Args:
            text: Query text to embed.

        Returns:
            Embedding vector for the query.
        """
        raise NotImplementedError
