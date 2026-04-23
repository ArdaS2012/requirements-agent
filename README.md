# ReqBot — Requirements Document Q&A System

ReqBot is a **Retrieval-Augmented Generation (RAG)** chatbot that lets you ask natural-language questions about PDF requirements documents. It ingests PDFs into a PostgreSQL vector database, retrieves the most relevant chunks for each query, reranks them with a cross-encoder, and answers through an LLM hosted on Groq.

---

## Table of Contents

1. [Core Concepts](#core-concepts)
2. [Architecture](#architecture)
3. [Project Layout](#project-layout)
4. [Prerequisites](#prerequisites)
5. [Installation](#installation)
6. [Configuration](#configuration)
7. [Usage](#usage)
8. [Security](#security)
9. [License](#license)

---

## Core Concepts

| Concept | Description |
|---|---|
| **RAG** | Retrieval-Augmented Generation — the LLM answers are grounded in text retrieved from your documents rather than the model's training data alone. |
| **Chunking** | Each PDF page is converted to Markdown and split at heading boundaries, producing small, semantically coherent chunks that fit within a context window. |
| **Vector Search** | Chunks are encoded with `all-MiniLM-L6-v2` into 384-dimensional vectors stored in PostgreSQL via `pgvector`. Queries are embedded with the same model and the nearest chunks are retrieved with cosine distance. |
| **Cross-Encoder Reranking** | The top-5 candidates from vector search are rescored by `ms-marco-MiniLM-L-6-v2`, a cross-encoder that jointly scores query + passage pairs for higher precision. |
| **Secure Pipeline** | All user input passes through prompt-injection detection and HITL (Human-in-the-Loop) risk scoring before reaching the LLM. Responses are validated before being returned. |

---

## Architecture

```
PDF files (data/raw/)
        │
        ▼
  pdf_processing.py  ── fitz / pymupdf4llm → Markdown per page
        │
        ▼
    chunking.py       ── heading-aware chunking
        │
        ▼
   embeddings.py      ── SentenceTransformer → float vectors
        │
        ▼
   ingestion.py       ── INSERT into PostgreSQL / pgvector
        │
        ▼
   retrieval.py       ── cosine search → cross-encoder rerank
        │
        ▼
    app.py (Flask)    ── /chat endpoint → Groq LLM (llama-3.3-70b)
        │
        ▼
  templates/index.html  ── browser UI
```

---

## Project Layout

```
requirement_project/
├── main.py                  # Entry point — starts the Flask web app
├── app.py                   # Flask routes: /chat, /reset, /conversations
├── src/
│   ├── chunking.py          # Heading-aware Markdown chunker
│   ├── config.py            # Shared clients, models, and constants
│   ├── embeddings.py        # SentenceTransformer embedding helpers
│   ├── ingestion.py         # PDF → chunks → PostgreSQL pipeline
│   ├── pdf_processing.py    # PDF page extraction and VLM image description
│   ├── retrieval.py         # Vector search + cross-encoder reranking
│   └── security.py          # Prompt-injection filter, HITL controller, output validator
├── data/
│   ├── raw/                 # Place your source PDF files here
│   └── extracted_images/    # Auto-generated page images
├── outputs/
│   ├── logs/                # Per-session conversation logs (text files)
│   ├── output.md            # Sample ingestion output
│   └── output_w_hf.md       # Sample output via HuggingFace router
└── templates/
    └── index.html           # Chat UI served by Flask
```

---

## Prerequisites

- Python 3.11+
- PostgreSQL 15+ with the [`pgvector`](https://github.com/pgvector/pgvector) extension enabled
- A [Groq](https://console.groq.com/) API key (for the LLM)
- A [HuggingFace](https://huggingface.co/settings/tokens) token (for the VLM image route, optional)
- `tesseract-ocr` installed on your system (used by `pytesseract` as a fallback OCR)

---

## Installation

```bash
# 1. Clone the repository
git clone <repo-url>
cd requirement_project

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Enable pgvector in PostgreSQL
psql -U postgres -c "CREATE EXTENSION IF NOT EXISTS vector;"

# 5. Create the database and table
psql -U postgres -d requirements -c "
CREATE TABLE IF NOT EXISTS rag_chunks (
    id          SERIAL PRIMARY KEY,
    document_id TEXT,
    chunk_index INTEGER,
    content     TEXT,
    metadata    JSONB,
    embedding   vector(384)
);"
```

---

## Configuration

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
HF_TOKEN=your_huggingface_token_here
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/requirements
```

`DATABASE_URL` falls back to a localhost default if not set, but you should always set it explicitly in `.env` to avoid committing credentials.

Place your PDF requirement documents in `data/raw/` before running ingestion.

---

## Usage

### 1. Ingest PDFs into the database

Open `main.py`, set `need_reset = True` on the first run (or whenever you want to re-ingest), then start the app:

```bash
python main.py
```

This will truncate the table, process all PDFs in `data/raw/`, embed every chunk, and insert the vectors into PostgreSQL. On subsequent runs, set `need_reset = False` to skip re-ingestion and go directly to the web UI.

### 2. Open the web UI

Navigate to **http://localhost:5000** in your browser. Type a question about your requirements document and press Enter or click **Send**.

### 3. Conversation logs

Every chat session is automatically saved to `outputs/logs/` as a plain-text file named `output_YYYYMMDD_HHMMSS.txt`. Past sessions can also be browsed and downloaded from the web UI.

---

## Security

- **Prompt injection filter** — regex + typoglycemia-aware fuzzy matching blocks common jailbreak patterns before input reaches the LLM.
- **HITL risk scoring** — inputs containing combinations of high-risk keywords are flagged for human review.
- **Output validation** — LLM responses are scanned for system-prompt leakage or API key exposure before being returned to the client.
- **Session isolation** — each browser session gets a random 16-byte ID; conversation histories are stored server-side and never shared across sessions.

---

## License

This project's own source code is released under the **MIT License** — see the [LICENSE](LICENSE) file for details.

> **Dependency notice:** This project uses [PyMuPDF](https://github.com/pymupdf/PyMuPDF) (`fitz` / `pymupdf4llm`), which is licensed under **AGPL-3.0**. If you distribute this software or run it as a public service, the AGPL-3.0 terms require you to make the full source code available. For commercial/closed-source use, a separate PyMuPDF commercial license is required from Artifex.
