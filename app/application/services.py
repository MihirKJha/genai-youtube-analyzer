"""
Application services for the YouTube RAG Assistant.

This module orchestrates the end-to-end application workflows:
YouTube ingestion, transcript processing, vector-store creation,
summarization, and question answering.
"""

import logging

from app.ai.embedding_factory import create_embedding_provider
from app.ai.provider_factory import create_llm_provider
from app.capabilities.question_answering import answer_question
from app.capabilities.summarizer import summarize_transcript
from app.ingestion.youtube import get_transcript, get_video_id
from app.processing.transcript import chunk_transcript, process
from app.retrieval.retriever_factory import create_retriever

logger = logging.getLogger(__name__)


class YouTubeAnalyzerService:
    """
    Application-level service for YouTube transcript RAG workflows.

    Maintains the processed transcript and vector store for the
    currently loaded video.
    """

    def __init__(self):
        """Initialize the application service."""
        self.processed_transcript = None
        self.llm_provider = create_llm_provider()
        self.embedding_provider = create_embedding_provider()
        self.retriever = create_retriever(
            embeddings=self.embedding_provider,
        )

    def process_video(self, url: str) -> str:
        """
        Fetch and process a YouTube video's transcript.

        Args:
            url: YouTube video URL.

        Returns:
            Status message describing the processing result.
        """

        logger.info("Processing YouTube video: %s", url)

        video_id = get_video_id(url)

        if not video_id:
            logger.error("Invalid YouTube URL: %s", url)
            raise ValueError("Invalid YouTube URL.")

        transcript = get_transcript(video_id)

        self.processed_transcript = process(transcript)

        chunks = chunk_transcript(self.processed_transcript)

        self.retriever.index(chunks)

        return "Transcript successfully processed."

    def get_transcript(self) -> str:
        """
        Return the currently processed transcript.

        Returns:
            Processed transcript.

        Raises:
            RuntimeError: If no video has been processed.
        """

        if not self.processed_transcript:
            logger.error("Please process a YouTube video first.")
            raise RuntimeError("Please process a YouTube video first.")

        return self.processed_transcript

    def generate_summary(self) -> str:
        """
        Generate a summary of the processed YouTube transcript.

        Returns:
            Generated transcript summary.
        """
        transcript = self.get_transcript()

        return summarize_transcript(
            provider=self.llm_provider,
            transcript=transcript,
        )

    def answer_question(self, question: str) -> str:
        """
        Answer a question using the currently loaded video.

        Args:
            question: User's question.

        Returns:
            Generated answer.

        Raises:
            RuntimeError: If no video has been processed.
            ValueError: If the question is empty.
        """

        if self.processed_transcript is None:
            logger.error("Please process a YouTube video first.")
            raise RuntimeError("Please process a YouTube video first.")

        if not question.strip():
            logger.error("Empty question provided.")
            raise ValueError("Please enter a question.")

        return answer_question(
            provider=self.llm_provider,
            retriever=self.retriever,
            question=question,
        )
