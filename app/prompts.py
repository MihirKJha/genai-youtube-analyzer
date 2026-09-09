"""
Prompt templates used by the YouTube RAG Assistant.
"""

from langchain.prompts import PromptTemplate

# =============================================================================
# Summarization Prompt
# =============================================================================

SUMMARY_PROMPT = PromptTemplate(
    input_variables=["context"],
    template="""
Summarize the following YouTube video transcript.

Context:
{context}

Provide a clear and concise summary of the main points discussed in the video.
""",
)


# =============================================================================
# Question Answering Prompt
# =============================================================================

QA_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""
Answer the question based only on the provided YouTube video context.

Context:
{context}

Question:
{question}

Answer:
""",
)
