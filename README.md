# GenAI YouTube Analyzer

AI-powered YouTube content analyzer that extracts video transcripts, generates concise summaries, and answers natural-language questions using semantic retrieval, FAISS, Chroma, LangChain, and IBM watsonx.ai.

## ✨ Features

- 🎥 **YouTube Transcript Extraction**
  - Extracts English transcripts from YouTube videos.
  - Supports standard YouTube and shortened `youtu.be` URLs.

- 📝 **Transcript Summarization**
  - Generates concise summaries from processed video transcripts.
  - Supports configurable LLM providers.

- 💬 **Natural-Language Q&A**
  - Ask questions about the video content.
  - Retrieves semantically relevant transcript chunks before generating an answer.

- 🔎 **Pluggable Retrieval**
  - **Chroma** as the default vector store.
  - **FAISS** as an alternative retrieval provider.
  - Retrieval is abstracted behind a common interface.

- 🤖 **Pluggable AI Providers**
  - Local LLM and embedding models through Ollama.
  - IBM watsonx.ai for cloud-based generation and embeddings.

- ⚙️ **Environment-Based Configuration**
  - AI providers, retrieval providers, models, endpoints, and application settings are configured through environment variables.

- 🖥️ **Gradio Interface**
  - Provides a simple web-based interface for processing videos, generating summaries, and asking questions.

---

## 🏗️ Architecture

```text
                         ┌───────────────────────┐
                         │      Gradio UI        │
                         └───────────┬───────────┘
                                     │
                                     ▼
                       ┌─────────────────────────┐
                       │ YouTube Analyzer Service│
                       └────────────┬────────────┘
                                    │
                 ┌──────────────────┼──────────────────┐
                 │                  │                  │
                 ▼                  ▼                  ▼
        ┌────────────────┐  ┌────────────────┐  ┌─────────────────┐
        │ YouTube        │  │ Transcript     │  │ AI Capabilities │
        │ Ingestion      │  │ Processing     │  │                 │
        └───────┬────────┘  └───────┬────────┘  └───────┬─────────┘
                │                   │                   │
                ▼                   ▼                   │
        ┌────────────────┐  ┌────────────────┐          │
        │ Transcript     │  │ Text Chunking  │          │
        └────────────────┘  └───────┬────────┘          │
                                    │                   │
                                    ▼                   │
                         ┌────────────────────┐          │
                         │ Retriever Provider │◄─────────┘
                         └─────────┬──────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    │                             │
                    ▼                             ▼
             ┌─────────────┐               ┌─────────────┐
             │   Chroma    │               │    FAISS    │
             │   Default   │               │ Alternative │
             └─────────────┘               └─────────────┘
                    │
                    ▼
             ┌─────────────────┐
             │ Embedding       │
             │ Provider        │
             └────────┬────────┘
                      │
             ┌────────┴─────────┐
             │                  │
             ▼                  ▼
      ┌─────────────┐    ┌─────────────┐
      │ Local/Ollama│    │  watsonx.ai │
      └─────────────┘    └─────────────┘
```

---

## 🔄 Processing Flow

```text
YouTube URL
    │
    ▼
Extract Video ID
    │
    ▼
Fetch English Transcript
    │
    ▼
Process Transcript
    │
    ▼
Split into Chunks
    │
    ▼
Generate Embeddings
    │
    ▼
Index in Selected Vector Store
    │
    ├───────────────┐
    │               │
    ▼               ▼
  Chroma          FAISS
    │               │
    └───────┬───────┘
            │
            ▼
      User Question
            │
            ▼
   Semantic Similarity Search
            │
            ▼
    Relevant Transcript Chunks
            │
            ▼
       LLM Generation
            │
            ▼
        Final Answer
```

---

## 📁 Project Structure

```text
genai-youtube-analyzer/
│
├── app/
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
│   │   ├── base_retriever.py
│   │   ├── retriever_factory.py
│   │   │
│   │   └── providers/
│   │       ├── __init__.py
│   │       ├── chroma_retriever.py
│   │       └── faiss_retriever.py
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
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 🧩 Core Design

### Provider Abstraction

The application separates business capabilities from concrete AI implementations.

```text
                 ┌───────────────────┐
                 │   LLMProvider     │
                 └─────────┬─────────┘
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
     LocalLLMProvider          WatsonxLLMProvider
```

The same approach is used for embeddings:

```text
              ┌──────────────────────┐
              │  EmbeddingProvider   │
              └──────────┬───────────┘
                         │
             ┌───────────┴───────────┐
             │                       │
             ▼                       ▼
   LocalEmbeddingProvider   WatsonxEmbeddingProvider
```

Retrieval follows the same abstraction:

```text
              ┌──────────────────────┐
              │  RetrieverProvider   │
              └──────────┬───────────┘
                         │
             ┌───────────┴───────────┐
             │                       │
             ▼                       ▼
       ChromaRetriever        FAISSRetriever
```

This allows the application layer to remain independent of the underlying provider implementation.

---

## 🔎 Retrieval Architecture

The retrieval layer exposes a common interface:

```python
class RetrieverProvider(ABC):

    @abstractmethod
    def index(self, chunks: list[str]) -> None:
        ...

    @abstractmethod
    def search(
        self,
        query: str,
        k: int = 4,
    ) -> list[str]:
        ...
```

The application therefore does not need to know whether retrieval is backed by Chroma or FAISS.

```text
Application
     │
     ▼
RetrieverProvider
     │
     ├── ChromaRetriever
     │
     └── FAISSRetriever
```

---

## 🧠 RAG-Based Question Answering

Question answering follows a retrieval-augmented generation flow:

```text
User Question
      │
      ▼
Generate Query Embedding
      │
      ▼
Vector Similarity Search
      │
      ▼
Top-K Transcript Chunks
      │
      ▼
Build Context
      │
      ▼
LLM Prompt
      │
      ▼
Generated Answer
```

Only the most relevant transcript chunks are provided as context to the language model.

---

## 🛠️ Tech Stack

| Category | Technology |
|---|---|
| Language | Python 3.12 |
| Generative AI | IBM watsonx.ai / Local LLM |
| Local AI Runtime | Ollama |
| Embeddings | Local / IBM watsonx.ai |
| Vector Store | Chroma / FAISS |
| AI Framework | LangChain Core |
| Text Splitting | LangChain Text Splitters |
| YouTube Transcripts | youtube-transcript-api |
| UI | Gradio |
| Configuration | python-dotenv |
| HTTP Client | requests |

---

## ⚙️ Configuration

Create a local `.env` file based on `.env.example`.

### Provider Selection

```env
AI_PROVIDER=local
EMBEDDING_PROVIDER=local
RETRIEVAL_PROVIDER=chroma
```

### Local LLM

```env
LOCAL_LLM_BASE_URL=http://localhost:11434
LOCAL_LLM_MODEL=llama3.2:3b
LOCAL_LLM_TIMEOUT=120
```

### Local Embeddings

```env
LOCAL_EMBEDDING_MODEL=nomic-embed-text
```

### Chroma

```env
CHROMA_PERSIST_DIRECTORY=./chroma_data
CHROMA_COLLECTION_NAME=youtube_transcripts
```

### IBM watsonx.ai

```env
WATSONX_URL=
WATSONX_PROJECT_ID=
WATSONX_API_KEY=
WATSONX_MODEL_ID=
WATSONX_EMBEDDING_MODEL_ID=
```

### Generation

```env
MAX_NEW_TOKENS=900
DECODING_METHOD=greedy
```

### Application

```env
HOST=0.0.0.0
PORT=7860
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/mihirjha/genai-youtube-analyzer.git
cd genai-youtube-analyzer
```

### 2. Create a Virtual Environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Copy:

```text
.env.example
```

to:

```text
.env
```

Then configure the required provider settings.

### 5. Start the Application

```bash
python main.py
```

The Gradio application will start on the configured host and port.

---

## 🖥️ Example Usage

### Step 1 — Process a YouTube Video

Provide a YouTube URL through the application.

Example:

```text
https://www.youtube.com/watch?v=VIDEO_ID
```

The application:

1. Extracts the video ID.
2. Fetches the English transcript.
3. Processes the transcript.
4. Splits the transcript into chunks.
5. Generates embeddings.
6. Indexes the chunks in the configured vector store.

### Step 2 — Generate a Summary

The processed transcript is passed to the configured LLM provider to generate a concise summary.

### Step 3 — Ask Questions

Enter a natural-language question about the video.

The application retrieves relevant transcript chunks and uses them as context for the LLM.

---

## 🔄 Switching Vector Stores

The retrieval implementation can be changed through configuration without modifying application code.

### Chroma

```env
RETRIEVAL_PROVIDER=chroma
```

### FAISS

```env
RETRIEVAL_PROVIDER=faiss
```

The application uses the same `RetrieverProvider` interface for both implementations.

---

## 🧪 Testing

The project includes tests for core application areas:

```text
tests/
├── test_youtube.py
├── test_transcript.py
└── test_retrieval.py
```

Run the test suite with:

```bash
pytest
```

---

## 📦 Dependencies

Key direct dependencies include:

```text
youtube-transcript-api==1.2.1

langchain-core==1.6.2
langchain-text-splitters==1.1.2

langchain-chroma==1.1.0
chromadb==1.5.0
langchain-community==0.4.2
faiss-cpu==1.12.0
onnxruntime==1.24.3

ibm-watsonx-ai==1.7.1
langchain-ibm==1.1.0

gradio==6.26.0

python-dotenv==1.0.1
requests==2.32.3
```

See [`requirements.txt`](requirements.txt) for the complete dependency specification.

---

## 🔐 Security

Sensitive configuration should never be committed to source control.

The project uses environment variables for:

- IBM watsonx.ai API credentials
- Project identifiers
- Provider endpoints
- Model configuration
- Runtime configuration

The `.env` file should remain local.

```gitignore
.env
.env.*
!.env.example
```

Generated Chroma data is also excluded from version control:

```gitignore
chroma_data/
```

---

## 🎯 Design Principles

This project demonstrates several production-oriented software architecture principles:

- **Separation of concerns**
- **Provider abstraction**
- **Dependency inversion**
- **Configuration-driven behavior**
- **Pluggable vector stores**
- **Pluggable AI providers**
- **Reusable application services**
- **Retrieval-augmented generation**
- **Environment-based runtime configuration**
- **Clear separation between application capabilities and infrastructure**

The architecture allows the AI provider, embedding provider, and retrieval implementation to evolve independently.

---

## 💼 Portfolio Focus

This project demonstrates practical Generative AI engineering beyond a single-model prototype.

Key engineering concepts include:

- Generative AI application architecture
- Retrieval-Augmented Generation (RAG)
- Semantic search
- Vector databases
- Embedding providers
- LLM provider abstraction
- Local AI inference
- IBM watsonx.ai integration
- LangChain-based AI orchestration
- Configuration-driven architecture
- Modular Python application design
- Multiple interchangeable infrastructure providers

---

## 👤 Author

**Mihir Jha**

**Software Architect | AI Engineering | Multi-Cloud Solutions**

- GitHub: https://github.com/mihirjha
- LinkedIn: https://www.linkedin.com/in/mihirjha/
- Enterprise AI Engineering: https://enterpriseai.handbook.mihirkjha.com/

---

## 📄 License

This project is intended for educational and portfolio purposes.