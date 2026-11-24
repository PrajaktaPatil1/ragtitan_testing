# Local RAG & Evaluation (RAG-Titan + Ollama)

A minimal, ready-to-run local RAG chatbot and end-to-end evaluation pipeline built with [RAG-Titan](https://github.com/aion7891/rag-titan) and [Ollama](https://ollama.com/).

## Project Structure

- `app.py` — Local RAG Q&A and interactive chatbot (defaults to documents under `docs/`, skipping >10 MB files unless `--all` or `--files` is passed).
- `create_golden.py` — Generate a golden question template with suggested evidence quotes, or validate an existing golden dataset (`--check`).
- `evaluate_rag.py` — Run end-to-end stage evaluation (chunking, embedding, retrieval, reranking, augmentation, generation, end-to-end) and save JSON + Markdown reports to `reports/`.
- `golden_questions.json` — Validated golden Q&A dataset for `docs/handbook.md`.
- `pdf_chat.py` — Dedicated interactive chatbot for the large Machine Learning PDF in `docs/`.
- `docs/` — Sample documents (`handbook.md` and the ML PDF).
- `requirements.txt` — Python dependencies.
- `.env.example` — Example environment configuration.

## 1. Prerequisites

1. **Python 3.10+**
2. **Ollama** installed and running locally (`http://localhost:11434`) with the configured models pulled:

```bash
ollama pull gemma3:4b
ollama pull nomic-embed-text
```

## 2. Installation & Setup

Create and activate a virtual environment, install dependencies from `requirements.txt`, and configure `.env`:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

> Edit `.env` if you want to change models (`LLM_MODEL`, `EMBED_MODEL`), chunking (`CHUNKER`, `CHUNK_SIZE`), or vector store (`VECTOR_STORE`).

## 3. Execute End-to-End

### Step 1: Ask questions with the RAG chatbot (`app.py`)

Run a single question with pipeline tracing:

```bash
python app.py --question "How many days of annual leave do employees receive?" --trace
```

Or launch the interactive chat loop:

```bash
python app.py
```

Inside interactive mode, type `trace` to inspect retrieval/reranking/generation steps, or `exit` to quit.

### Step 2: Validate (or generate) golden questions (`create_golden.py`)

Validate `golden_questions.json` against `docs/handbook.md`:

```bash
python create_golden.py --check
```

To generate a fresh template for custom documents and questions:

```bash
python create_golden.py --files docs/handbook.md --questions evaluation/questions.txt --output my_golden.json
```

### Step 3: Run end-to-end evaluation (`evaluate_rag.py`)

```bash
python evaluate_rag.py
```

This validates `golden_questions.json`, indexes `docs/handbook.md`, evaluates every RAG pipeline stage, prints the scorecard summary, and saves:

- `reports/eval_report.json`
- `reports/eval_report.md`

Optional flags:

```bash
python evaluate_rag.py --rag-type adaptive --k 5 --output reports/adaptive_report.json --baseline reports/eval_report.json
```

## Optional: Chat with the Machine Learning PDF

```bash
python pdf_chat.py
```

