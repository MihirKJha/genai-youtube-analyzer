"""
Chroma retrieval provider.

Provides vector-based retrieval using Chroma and the configured
embedding provider.
"""

from langchain_chroma import Chroma

from app.ai.base_embedding import EmbeddingProvider
from app.config import (
    CHROMA_COLLECTION_NAME,
    CHROMA_PERSIST_DIRECTORY,
)
from app.retrieval.base_retriever import RetrieverProvider


class ChromaRetriever(RetrieverProvider):
    """Retriever implementation backed by Chroma."""

    def __init__(
        self,
        embeddings: EmbeddingProvider,
    ):
        self.embeddings = embeddings
        self.vector_store = None

    def index(self, chunks: list[str]) -> None:
        self.vector_store = Chroma.from_texts(
            texts=chunks,
            embedding=self.embeddings,
            collection_name=CHROMA_COLLECTION_NAME,
            persist_directory=CHROMA_PERSIST_DIRECTORY,
        )

    def search(
        self,
        query: str,
        k: int = 4,
    ) -> list[str]:
        if self.vector_store is None:
            raise RuntimeError("Retrieval index has not been created.")

        documents = self.vector_store.similarity_search(
            query,
            k=k,
        )

        return [document.page_content for document in documents]
