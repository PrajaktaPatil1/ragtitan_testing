import argparse
from pathlib import Path

from rag_titan import RAGTitan, setup_logging

from rag_utils import DEFAULT_PDF, configure_safe_loader


def resolve_files(explicit_files=None):
    """Return validated document paths, defaulting to the Machine Learning PDF."""
    files = [Path(p) for p in explicit_files] if explicit_files else [DEFAULT_PDF]
    missing = [str(p) for p in files if not p.is_file()]
    if missing:
        raise FileNotFoundError(f"File(s) not found: {', '.join(missing)}")
    return files


def run_chat(rag):
    """Start an interactive question-and-answer loop."""
    print("\n" + "=" * 55)
    print("       MACHINE LEARNING RAG CHATBOT IS READY")
    print("=" * 55)
    print("\nAsk questions about your Machine Learning book.")
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
    """Parse optional CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Machine Learning RAG chatbot powered by RAG-Titan."
    )
    parser.add_argument("--files", nargs="+", help="Optional custom document path(s) to index.")
    parser.add_argument("--rag-type", default="simple", choices=["simple", "adaptive", "parent_child"],
                        help="RAG strategy to use (default: simple).")
    parser.add_argument("--reindex", action="store_true",
                        help="Rebuild the vector index even if saved chunks already exist.")
    parser.add_argument("--question", help="Ask a single question and exit (non-interactive).")
    parser.add_argument("--trace", action="store_true", help="Print pipeline trace with --question.")
    parser.add_argument("--log-level", default="WARNING", choices=["DEBUG", "INFO", "WARNING"],
                        help="Logging level (default: WARNING).")
    return parser.parse_args()


def main():
    args = parse_args()
    setup_logging(args.log_level)

    files = resolve_files(args.files)
    print("Initializing Machine Learning RAG...")
    rag = configure_safe_loader(RAGTitan(rag_type=args.rag_type))

    persistent = getattr(rag.pipeline.store, "persistent", False)
    existing_chunks = rag.count() if persistent else 0

    if existing_chunks > 0 and not args.reindex and not args.files:
        print(f"Loaded {existing_chunks} existing chunk(s) from saved index.")
    else:
        print("Indexing document(s) (first run on the full book takes a few minutes)...")
        for file in files:
            print(f"- {file}")
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
