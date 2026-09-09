"""
Retriever provider interface.

Defines the contract used by the application for indexing and
retrieving text without coupling it to a specific retrieval
implementation.
"""

from abc import ABC, abstractmethod


class RetrieverProvider(ABC):
    """Abstract interface for a text retrieval provider."""

    @abstractmethod
    def index(self, chunks: list[str]) -> None:
        """
        Index text chunks for retrieval.

        Args:
            chunks: Text chunks to index.
        """
        raise NotImplementedError

    @abstractmethod
    def search(
        self,
        query: str,
        k: int = 4,
    ) -> list[str]:
        """
        Retrieve relevant text chunks for a query.

        Args:
            query: User's search query.
            k: Number of relevant chunks to retrieve.

        Returns:
            Relevant text chunks.
        """
        raise NotImplementedError
