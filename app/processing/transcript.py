"""
Transcript processing utilities.

Responsible for converting YouTube transcript entries into a
retrieval-friendly text representation and splitting the transcript
into overlapping chunks.
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter


def process(transcript):
    """
    Convert transcript entries into a formatted text string.

    Each transcript entry is represented as:

        Text: <spoken text> Start: <start time>

    Args:
        transcript: Transcript entries returned by the YouTube
                    transcript API.

    Returns:
        A single formatted transcript string.
    """

    processed_transcript = ""

    for entry in transcript:
        processed_transcript += f"Text: {entry.text} Start: {entry.start}\n"

    return processed_transcript


def chunk_transcript(
    processed_transcript,
    chunk_size=200,
    chunk_overlap=20,
):
    """
    Split a processed transcript into overlapping text chunks.

    Args:
        processed_transcript: Formatted transcript string.
        chunk_size: Maximum size of each chunk.
        chunk_overlap: Number of overlapping characters between chunks.

    Returns:
        A list of transcript chunks.
    """

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    return text_splitter.split_text(processed_transcript)
