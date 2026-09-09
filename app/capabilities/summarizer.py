"""
YouTube transcript summarization service.
"""

from app.ai.base_provider import LLMProvider
from app.prompts import SUMMARY_PROMPT


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

    return provider.generate(prompt)
