"""
Application entry point.

Starts the Gradio web application using the configured
host, port and share settings.

Run the YouTube RAG Assistant with:

    python run.py
"""

import logging

from app.config import HOST, PORT, SHARE
from app.logging_config import configure_logging
from app.ui.gradio_app import create_app

configure_logging()

logger = logging.getLogger(__name__)


def main() -> None:
    """Start the YouTube Analyzer application."""

    logger.info("Application starting")

    app = create_app()

    app.launch(
        server_name=HOST,
        server_port=PORT,
        share=SHARE,
    )


if __name__ == "__main__":
    main()
