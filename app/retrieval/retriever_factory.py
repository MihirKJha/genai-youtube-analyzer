"""
Retriever provider factory.

Creates the configured retrieval implementation without exposing
provider-specific details to the application layer.
"""

from app.ai.base_embedding import EmbeddingProvider
from app.config import RETRIEVAL_PROVIDER
from app.retrieval.base_retriever import RetrieverProvider
from app.retrieval.providers.faiss_retriever import FAISSRetriever


def create_retriever(
    embeddings: EmbeddingProvider,
) -> RetrieverProvider:
    """
    Create the configured retriever.

    Args:
        embeddings: Embedding provider used by the retriever.

    Returns:
        Configured retriever instance.

    Raises:
        RuntimeError: If the configured retriever is unsupported.
    """
    if RETRIEVAL_PROVIDER == "faiss":
        return FAISSRetriever(
            embeddings=embeddings,
        )

    if RETRIEVAL_PROVIDER == "chroma":
        return ChromaRetriever(
            embeddings=embeddings,
        )

    raise RuntimeError(f"Unsupported retrieval provider: '{RETRIEVAL_PROVIDER}'.")
