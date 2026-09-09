"""
FAISS retrieval provider.

Provides vector-based retrieval using FAISS and the configured
embedding provider.
"""

from langchain_community.vectorstores import FAISS

from app.ai.base_embedding import EmbeddingProvider
from app.retrieval.base_retriever import RetrieverProvider


class FAISSRetriever(RetrieverProvider):
    """Retriever implementation backed by FAISS."""

    def __init__(
        self,
        embeddings: EmbeddingProvider,
    ):
        """
        Initialize the FAISS retriever.

        Args:
            embeddings: Embedding provider used to generate vectors.
        """
        self.embeddings = embeddings
        self.vector_store = None

    def index(self, chunks: list[str]) -> None:
        """
        Create a FAISS index from text chunks.

        Args:
            chunks: Text chunks to index.
        """
        self.vector_store = FAISS.from_texts(
            texts=chunks,
            embedding=self.embeddings,
        )

    def search(
        self,
        query: str,
        k: int = 4,
    ) -> list[str]:
        """
        Retrieve relevant text chunks.

        Args:
            query: User's search query.
            k: Number of relevant chunks to retrieve.

        Returns:
            Relevant text chunks.

        Raises:
            RuntimeError: If the retrieval index has not been created.
        """
        if self.vector_store is None:
            raise RuntimeError("Retrieval index has not been created.")

        documents = self.vector_store.similarity_search(
            query,
            k=k,
        )

        return [document.page_content for document in documents]
