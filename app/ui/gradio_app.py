"""
Gradio presentation layer for the YouTube RAG Analyzer.
"""

import logging

import gradio as gr

from app.application.services import YouTubeAnalyzerService

logger = logging.getLogger(__name__)


def create_app():
    """
    Create and configure the Gradio application.

    Returns:
        Configured Gradio Blocks application.
    """

    logger.info("Configuring UI Components")

    service = YouTubeAnalyzerService()

    with gr.Blocks(title="YouTube Video Analyzer") as app:

        gr.Markdown("""
            # YouTube Video Analyzer

            Enter a YouTube URL to retrieve its transcript,
            generate a summary, and ask questions about the video.
            """)

        with gr.Row():

            youtube_url = gr.Textbox(
                label="YouTube URL",
                placeholder="Enter a YouTube video URL",
            )

            process_button = gr.Button(
                "Process Video",
            )

        transcript_status = gr.Textbox(
            label="Transcript Status",
        )

        transcript_output = gr.Textbox(
            label="Transcript",
            lines=10,
        )

        summary_button = gr.Button(
            "Generate Summary",
        )

        summary_output = gr.Textbox(
            label="Summary",
            lines=8,
        )

        question = gr.Textbox(
            label="Question",
            placeholder="Ask a question about the video...",
        )

        answer_button = gr.Button(
            "Ask Question",
        )

        answer_output = gr.Textbox(
            label="Answer",
            lines=8,
        )

        def process_video(url):
            """Process a YouTube video and return its transcript."""

            try:
                status = service.process_video(url)
                transcript = service.get_transcript()

                return status, transcript

            except Exception as exc:
                return f"Error: {exc}", ""

        def generate_summary():
            """Generate a summary for the currently loaded video."""

            try:
                return service.generate_summary()

            except Exception as exc:
                return f"Error: {exc}"

        def generate_answer(question_text):
            """Generate an answer for the user's question."""

            try:
                return service.answer_question(question_text)

            except Exception as exc:
                return f"Error: {exc}"

        process_button.click(
            fn=process_video,
            inputs=youtube_url,
            outputs=[
                transcript_status,
                transcript_output,
            ],
        )

        summary_button.click(
            fn=generate_summary,
            inputs=None,
            outputs=summary_output,
        )

        answer_button.click(
            fn=generate_answer,
            inputs=question,
            outputs=answer_output,
        )

    return app
