import argparse
from pathlib import Path

from rag_titan import RAGTitan, setup_logging

DOCS_DIR = Path("docs")
SUPPORTED_EXTENSIONS = ("*.pdf", "*.docx", "*.txt", "*.md")
MAX_DEFAULT_MB = 10


def find_documents(explicit_files=None, include_all=False):
    """Collect document paths to index, skipping very large files by default."""
    if explicit_files:
        files = [Path(p) for p in explicit_files]
        missing = [str(p) for p in files if not p.is_file()]
        if missing:
            raise FileNotFoundError(f"File(s) not found: {', '.join(missing)}")
        return files

    if not DOCS_DIR.is_dir():
        return []

    all_files = sorted({p for ext in SUPPORTED_EXTENSIONS for p in DOCS_DIR.glob(ext)})
    if include_all:
        return all_files

    selected, skipped = [], []
    for path in all_files:
        size_mb = path.stat().st_size / (1024 * 1024)
        if size_mb > MAX_DEFAULT_MB:
            skipped.append((path, size_mb))
        else:
            selected.append(path)

    for path, size_mb in skipped:
        print(
            f"Skipping large file '{path.name}' ({size_mb:.1f} MB). "
            "Use --all or pdf_chat.py to index it."
        )
    return selected


def run_chat(rag):
    """Start an interactive question-and-answer loop."""
    print("\n" + "=" * 50)
    print("       LOCAL RAG CHATBOT IS READY")
    print("=" * 50)
    print("\nAsk questions based on your documents.")
    print("Type 'trace' to inspect pipeline steps, or 'exit' to quit.")

    while True:
        try:
            question = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nChatbot stopped. Goodbye!")
            break

        if question.lower() in {"exit", "quit", "bye"}:
            print("\nChatbot stopped. Goodbye!")
            break

        if not question:
            continue

        try:
            if question.lower() == "trace":
                question = input("Enter your question: ").strip()
                if not question:
                    continue
                result = rag.run(question)
                print("\nAnswer:\n" + result["answer"])
                print("\nSources:", [s.get("source") for s in result.get("sources", [])])
                print("\nPipeline execution:\n" + result["log"])
            else:
                print("\nAssistant:\n" + rag.ask(question))
        except Exception as error:
            print(f"\nSomething went wrong: {error}")


def parse_args():
    """Parse optional CLI arguments for one-shot or custom runs."""
    parser = argparse.ArgumentParser(description="Simple local RAG chatbot powered by RAG-Titan.")
    parser.add_argument("--files", nargs="+", help="Specific document paths to index.")
    parser.add_argument("--all", action="store_true", help="Include large files (>10 MB) in docs/.")
    parser.add_argument("--rag-type", default="simple", choices=["simple", "adaptive", "parent_child"],
                        help="RAG strategy to use (default: simple).")
    parser.add_argument("--question", help="Ask a single question and exit (non-interactive).")
    parser.add_argument("--trace", action="store_true", help="Print pipeline trace with --question.")
    parser.add_argument("--log-level", default="WARNING", choices=["DEBUG", "INFO", "WARNING"],
                        help="Logging level (default: WARNING).")
    return parser.parse_args()


def main():
    args = parse_args()
    setup_logging(args.log_level)

    files = find_documents(explicit_files=args.files, include_all=args.all)
    if not files:
        print("No documents found in docs/. Add PDF, DOCX, TXT, or MD files (or pass --files).")
        raise SystemExit(1)

    print("Documents selected:")
    for file in files:
        print(f"- {file}")

    print(f"\nInitializing RAG-Titan ({args.rag_type})...")
    rag = RAGTitan(rag_type=args.rag_type)

    print("Indexing documents...")
    chunk_count = rag.index([str(file) for file in files])
    print(f"Indexed {chunk_count} chunk(s).")

    if args.question:
        if args.trace:
            result = rag.run(args.question)
            print("\nAnswer:\n" + result["answer"])
            print("\nPipeline execution:\n" + result["log"])
        else:
            print("\nAnswer:\n" + rag.ask(args.question))
        return

    run_chat(rag)


if __name__ == "__main__":
    main()
