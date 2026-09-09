"""
YouTube transcript ingestion.

Responsible for extracting a YouTube video ID from a URL
and retrieving the video's English transcript.
"""

import re

from youtube_transcript_api import YouTubeTranscriptApi


def get_video_id(url: str) -> str | None:
    """
    Extract the YouTube video ID from a YouTube URL.

    Supports standard watch URLs and shortened youtu.be URLs.

    Args:
        url: YouTube video URL.

    Returns:
        The YouTube video ID if found, otherwise None.
    """

    pattern = r"(?:youtube\.com/watch\?v=|youtu\.be/)" r"([a-zA-Z0-9_-]{11})"

    match = re.search(pattern, url)

    if match:
        return match.group(1)

    return None


def get_transcript(video_id: str):
    """
    Retrieve the English transcript for a YouTube video.
    """

    try:
        api = YouTubeTranscriptApi()

        return api.fetch(
            video_id,
            languages=["en"],
        )

    except Exception as exc:
        raise RuntimeError(
            f"Unable to fetch transcript for video '{video_id}'."
        ) from exc
