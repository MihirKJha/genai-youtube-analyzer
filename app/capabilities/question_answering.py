"""
Question-answering service for YouTube transcript retrieval.
"""

import logging

from app.ai.base_provider import LLMProvider
from app.prompts import QA_PROMPT
from app.retrieval.base_retriever import RetrieverProvider

logger = logging.getLogger(__name__)


def answer_question(
    provider: LLMProvider,
    retriever: RetrieverProvider,
    question: str,
    k: int = 4,
) -> str:
    """
    Answer a question using relevant transcript context.

    Args:
        provider: Configured language-model provider.
        retriever: Configured retrieval provider.
        question: User's question.
        k: Number of relevant transcript chunks to retrieve.

    Returns:
        Generated answer based on retrieved transcript context.
    """
    documents = retriever.search(
        query=question,
        k=k,
    )

    context = "\n\n".join(documents)

    prompt = QA_PROMPT.format(
        context=context,
        question=question,
    )

    logger.info("Generating answer with prompt %s", prompt)

    return provider.generate(prompt)
