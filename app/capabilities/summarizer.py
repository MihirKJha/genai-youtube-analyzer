"""
YouTube transcript summarization service.
"""

import logging

from app.ai.base_provider import LLMProvider
from app.prompts import SUMMARY_PROMPT

logger = logging.getLogger(__name__)


def summarize_transcript(
    provider: LLMProvider,
    transcript: str,
) -> str:
    """
    Generate a summary of a YouTube transcript.

    Args:
        provider: Configured language-model provider.
        transcript: Processed YouTube transcript.

    Returns:
        Generated transcript summary.
    """
    prompt = SUMMARY_PROMPT.format(context=transcript)

    logger.info("Generating transcript summary with prompt %s", prompt)

    return provider.generate(prompt)
