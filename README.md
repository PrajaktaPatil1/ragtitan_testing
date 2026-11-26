# Machine Learning RAG & Evaluation (RAG-Titan + Ollama)

A simple local Machine Learning RAG chatbot and end-to-end evaluation pipeline for *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow (2nd Edition)*, powered by [RAG-Titan](https://github.com/aion7891/rag-titan) and [Ollama](https://ollama.com/).

## Project Structure

- `app.py` — Machine Learning RAG Q&A and interactive chatbot (indexes the PDF into `rag_titan.db` on first run and reuses the saved SQLite index on subsequent runs).
- `create_golden.py` — Generate or validate (`--check`) the golden Q&A dataset against the Machine Learning PDF.
- `evaluate_rag.py` — Run end-to-end stage evaluation (chunking, embedding, retrieval, reranking, augmentation, generation, end-to-end) and save JSON + Markdown reports to `reports/`.
- `golden_questions.json` — 10 validated golden questions with verbatim evidence quotes from the Machine Learning PDF.
- `evaluation/questions.txt` — Source list of the 10 Machine Learning evaluation questions.
- `docs/` — Contains `Hands-On_Machine_Learning_with_Scikit-Learn-Keras-and-TensorFlow-2nd-Edition-Aurelien-Geron.pdf`.
- `requirements.txt` — Python dependencies.
- `.env.example` — Example environment configuration.

## 1. Prerequisites

1. **Python 3.10+**
2. **Ollama** running locally (`http://localhost:11434`) with the configured models pulled:

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

> By default `.env` uses `VECTOR_STORE=sqlite` so the 851-page book is indexed once into `rag_titan.db` and reused instantly afterward.

## 3. Execute End-to-End

### Step 1: Run the Machine Learning RAG Chatbot (`app.py`)

Ask a single question with pipeline tracing (the first run indexes the PDF into `rag_titan.db`; later runs reuse it immediately):

```bash
python app.py --question "What is gradient descent?" --trace
```

Or start the interactive chat loop:

```bash
python app.py
```

Inside interactive mode, type `trace` to inspect retrieval/reranking/generation steps, or `exit` to quit. Use `--reindex` if you change chunking or embedding settings in `.env`.

### Step 2: Validate Golden Questions (`create_golden.py`)

Verify all 10 golden questions and evidence quotes against the Machine Learning PDF:

```bash
python create_golden.py --check
```

### Step 3: Run End-to-End Evaluation (`evaluate_rag.py`)

```bash
python evaluate_rag.py
```

This validates `golden_questions.json`, evaluates every stage of the Machine Learning RAG pipeline, prints the scorecard summary, and saves:

- `reports/eval_report.json`
- `reports/eval_report.md`

Optional flags:

```bash
python evaluate_rag.py --rag-type adaptive --k 5 --output reports/adaptive_report.json --baseline reports/eval_report.json
```
