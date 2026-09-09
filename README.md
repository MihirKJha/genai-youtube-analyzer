# GenAI YouTube Analyzer

AI-powered YouTube content analyzer that extracts video transcripts, generates concise summaries, and answers natural-language questions using semantic retrieval and configurable AI providers.

The project is designed with a provider-agnostic AI architecture so that local AI runtimes and cloud AI services can be used without changing the application layer.

---

## 🚀 Features

- Extract English transcripts from YouTube videos
- Process and chunk transcripts for downstream AI workloads
- Generate concise transcript summaries
- Ask natural-language questions about video content
- Perform semantic retrieval using FAISS
- Generate answers using retrieved transcript context
- Support configurable LLM providers
- Support configurable embedding providers
- Local AI inference through a reusable local runtime
- IBM watsonx.ai integration
- Environment-based configuration
- Provider abstraction that allows future AI providers to be added without changing application capabilities
- Gradio-based web interface

---

## 🏗️ Architecture

The application separates business capabilities from AI infrastructure through provider interfaces.

```text
                         GenAI YouTube Analyzer
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │ Application Layer   │
                       │                     │
                       │ • Summarization     │
                       │ • Question Answering│
                       │ • Retrieval         │
                       └──────────┬──────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
             LLMProvider              EmbeddingProvider
                    │                           │
          ┌─────────┴─────────┐       ┌─────────┴─────────┐
          ▼                   ▼       ▼                   ▼
       Local AI           watsonx.ai  Local AI         watsonx.ai
       Runtime             IBM Cloud  Runtime           IBM Cloud
```

### Processing Flow

```text
YouTube URL
    │
    ▼
Transcript Extraction
    │
    ▼
Transcript Processing
    │
    ▼
Text Chunking
    │
    ├──────────────────────┐
    │                      │
    ▼                      ▼
Summary Generation     Embedding Generation
                           │
                           ▼
                      FAISS Vector Store
                           │
                           ▼
                     Similarity Search
                           │
                           ▼
                  Retrieved Transcript Context
                           │
                           ▼
                      LLM Generation
                           │
                           ▼
                         Answer
```

---

## 🔌 Provider Architecture

The application does not directly depend on a specific LLM or embedding implementation.

Instead, application capabilities depend on stable interfaces:

```text
LLMProvider
    │
    ├── LocalLLMProvider
    └── WatsonxLLMProvider


EmbeddingProvider
    │
    ├── LocalEmbeddingProvider
    └── WatsonxEmbeddingProvider
```

This allows the same application architecture to support:

- Local AI development
- IBM watsonx.ai
- Future cloud AI providers
- Alternative local AI runtimes
- Different LLMs
- Different embedding models

The goal is to treat AI models and runtimes as configurable infrastructure dependencies rather than application-level dependencies.

---

## 🤖 AI Capabilities

### Summarization

The summarization capability receives the processed transcript and delegates text generation to the configured `LLMProvider`.

```text
Transcript
    │
    ▼
Summary Prompt
    │
    ▼
LLMProvider
    │
    ▼
Generated Summary
```

### Question Answering

Question answering uses semantic retrieval before generation.

```text
User Question
      │
      ▼
Embedding / Similarity Search
      │
      ▼
Relevant Transcript Chunks
      │
      ▼
Question + Retrieved Context
      │
      ▼
LLMProvider
      │
      ▼
Answer
```

This keeps RAG as an implementation detail of the question-answering capability rather than making it the identity of the product.

---

## 🧠 Local AI Runtime

The project is designed to work with a reusable local AI runtime rather than coupling the application directly to a particular runtime.

The intended local architecture is:

```text
                    Local AI Runtime
                           │
                ┌──────────┴──────────┐
                ▼                     ▼
              Local LLM          Local Embeddings
                │                     │
                ▼                     ▼
          LLMProvider          EmbeddingProvider
```

A local runtime can therefore be reused across multiple AI projects, including:

- YouTube analysis
- PDF/RAG applications
- Semantic search
- AI agents
- Document intelligence
- Question-answering systems
- Future AI engineering experiments

The current configuration is prepared for a local runtime through environment variables.

---

## ☁️ IBM watsonx.ai

The project also includes IBM watsonx.ai implementations for both generation and embeddings.

```text
Application
     │
     ▼
Provider Interfaces
     │
     ├── WatsonxLLMProvider
     │
     └── WatsonxEmbeddingProvider
              │
              ▼
        IBM watsonx.ai
```

Switching providers is configuration-driven rather than requiring changes to application capabilities.

---

## 📁 Project Structure

```text
genai-youtube-analyzer/
│
├── app/
│   │
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── base_embedding.py
│   │   ├── factory.py
│   │   ├── embedding_factory.py
│   │   │
│   │   └── providers/
│   │       ├── __init__.py
│   │       ├── local.py
│   │       ├── local_embedding.py
│   │       ├── watsonx.py
│   │       └── watsonx_embedding.py
│   │
│   ├── application/
│   │   ├── __init__.py
│   │   └── services.py
│   │
│   ├── capabilities/
│   │   ├── __init__.py
│   │   ├── summarizer.py
│   │   └── qa.py
│   │
│   ├── ingestion/
│   │   ├── __init__.py
│   │   └── youtube.py
│   │
│   ├── processing/
│   │   ├── __init__.py
│   │   └── transcript.py
│   │
│   ├── retrieval/
│   │   ├── __init__.py
│   │   └── faiss_store.py
│   │
│   ├── ui/
│   │   ├── __init__.py
│   │   └── gradio_app.py
│   │
│   ├── __init__.py
│   ├── config.py
│   └── prompts.py
│
├── tests/
│   ├── test_youtube.py
│   ├── test_transcript.py
│   └── test_retrieval.py
│
├── run.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

### Architectural Responsibilities

| Component | Responsibility |
|---|---|
| `application/` | Application orchestration |
| `capabilities/` | User-facing AI capabilities |
| `ingestion/` | YouTube transcript extraction |
| `processing/` | Transcript processing and chunking |
| `retrieval/` | Vector storage and similarity search |
| `ai/` | AI provider abstractions and implementations |
| `ui/` | Gradio web interface |
| `config.py` | Environment-based runtime configuration |
| `tests/` | Automated tests |

---

## ⚙️ Configuration

Runtime configuration is managed through environment variables rather than hardcoded provider-specific values.

Create a local `.env` file based on `.env.example`.

Example local configuration:

```env
# =============================================================================
# AI Provider Selection
# =============================================================================

AI_PROVIDER=local
EMBEDDING_PROVIDER=local


# =============================================================================
# Local LLM Provider
# =============================================================================

LOCAL_LLM_BASE_URL=http://localhost:11434
LOCAL_LLM_MODEL=llama3.2:3b
LOCAL_LLM_TIMEOUT=120


# =============================================================================
# Local Embedding Provider
# =============================================================================

LOCAL_EMBEDDING_MODEL=


# =============================================================================
# IBM watsonx.ai Provider
# =============================================================================

WATSONX_URL=
WATSONX_PROJECT_ID=
WATSONX_API_KEY=
WATSONX_MODEL_ID=
WATSONX_EMBEDDING_MODEL_ID=


# =============================================================================
# Generation Configuration
# =============================================================================

MAX_NEW_TOKENS=900
DECODING_METHOD=greedy


# =============================================================================
# Application
# =============================================================================

HOST=0.0.0.0
PORT=7860
```

> Keep `.env` local and never commit credentials or other environment-specific secrets.

---

## 🛠️ Installation

Clone the repository:

```bash
git clone https://github.com/<your-username>/genai-youtube-analyzer.git
cd genai-youtube-analyzer
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure environment variables:

```bash
copy .env.example .env
```

On Linux/macOS:

```bash
cp .env.example .env
```

Update `.env` with the desired AI providers and model configuration.

---

## ▶️ Running the Application

Start the application with:

```bash
python run.py
```

The Gradio interface will be available at:

```text
http://localhost:7860
```

---

## 🔄 Typical Usage

1. Enter a YouTube video URL.
2. Process the video transcript.
3. Generate a summary.
4. Ask questions about the video.
5. The application retrieves relevant transcript chunks.
6. The configured LLM generates an answer using the retrieved context.

---

## 🧪 Testing

Run the test suite with:

```bash
pytest
```

The test structure covers key application components including:

- YouTube transcript extraction
- Transcript processing
- Retrieval behavior

---

## 📦 Dependencies

Key technologies used by the project:

- Python
- LangChain
- FAISS
- YouTube Transcript API
- IBM watsonx.ai
- Gradio
- Requests
- python-dotenv

See [`requirements.txt`](requirements.txt) for the pinned dependency versions.

---

## 🔐 Security & Configuration Practices

The project follows environment-based configuration for runtime and provider settings.

Sensitive values such as:

- IBM API keys
- Project identifiers
- Provider endpoints
- Model configuration

should be supplied through environment variables and must not be committed to source control.

The `.gitignore` configuration excludes local environment files while keeping `.env.example` available as a configuration template.

---

## 🧭 Architecture Evolution

The project is intentionally structured to evolve beyond a single AI provider.

### Phase 1 — Local Development

```text
Local AI Runtime
      │
      ├── Local LLM
      └── Local Embeddings
             │
             ▼
           FAISS
```

Goal: develop and debug AI application behavior locally without depending on paid inference APIs.

### Phase 2 — Provider Abstraction

Introduce stable interfaces:

```text
LLMProvider
EmbeddingProvider
```

Application capabilities no longer depend directly on specific AI providers.

### Phase 3 — Cloud AI

Add IBM watsonx.ai implementations:

```text
Application
    │
    ▼
Provider Interfaces
    │
    ├── Local
    └── IBM watsonx.ai
```

### Phase 4 — Deployment

The same application can be deployed with environment-specific configuration without changing the core application logic.

### Phase 5 — AI Infrastructure Experiments

The architecture provides a foundation for experimenting with:

- Different LLMs
- Different embedding models
- Different vector stores
- Different AI providers
- Local versus cloud inference
- Retrieval strategies
- Production deployment patterns

---

## 💡 Key Engineering Concepts

This project demonstrates several practical AI engineering and software architecture patterns:

- Provider abstraction
- Dependency inversion
- Factory pattern
- Configuration-driven architecture
- Semantic retrieval
- Vector search
- Retrieval-Augmented Generation
- LLM integration
- Embedding integration
- Application/service separation
- AI infrastructure decoupling
- Environment-based configuration
- Local-to-cloud portability

---

## 🎯 Learning Objectives

This project demonstrates how a traditional application can integrate modern generative AI capabilities while maintaining clean architectural boundaries.

The primary architectural goal is:

> **Keep application capabilities independent from AI infrastructure.**

This allows the same application design to evolve from local experimentation to cloud-based AI services without requiring a fundamental rewrite.

---

## 👤 Author

**Mihir Jha**

Software Architect | AI Engineering | Multi-Cloud Solutions

- GitHub: https://github.com/
- LinkedIn: https://www.linkedin.com/
- Enterprise AI Engineering: https://www.linkedin.com/

---

## 📄 License

This project is intended for educational and portfolio purposes.