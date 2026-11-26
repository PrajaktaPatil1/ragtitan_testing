import argparse
from pathlib import Path

from rag_titan import RAGTitan, setup_logging
from rag_titan.evaluation import ReportManager, check_golden

from rag_utils import DEFAULT_PDF, configure_safe_loader, load_clean_documents

DEFAULT_FILES = [str(DEFAULT_PDF)]
DEFAULT_GOLDEN = "golden_questions.json"
DEFAULT_OUTPUT = "reports/eval_report.json"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run end-to-end stage evaluation for the Machine Learning RAG pipeline."
    )
    parser.add_argument("--files", nargs="+", default=DEFAULT_FILES,
                        help="Document paths to index and evaluate.")
    parser.add_argument("--questions", default=DEFAULT_GOLDEN,
                        help="Path to the golden questions JSON file.")
    parser.add_argument("--rag-type", default="simple", choices=["simple", "adaptive", "parent_child"],
                        help="RAG strategy to evaluate (default: simple).")
    parser.add_argument("--chunker", help="Optional chunker override (e.g. paragraph, word, heading).")
    parser.add_argument("--chunk-size", type=int, help="Optional chunk size override.")
    parser.add_argument("--k", type=int, default=5, help="Top-K cutoff for ranking metrics (default: 5).")
    parser.add_argument("--skip-embeddings", action="store_true",
                        help="Skip embedding stage scoring.")
    parser.add_argument("--output", default=DEFAULT_OUTPUT,
                        help="Output JSON report path (Markdown saved alongside it).")
    parser.add_argument("--baseline", help="Optional earlier JSON report path for regression check.")
    parser.add_argument("--log-level", default="WARNING", choices=["DEBUG", "INFO", "WARNING"],
                        help="Logging level (default: WARNING).")
    return parser.parse_args()


def main():
    args = parse_args()
    setup_logging(args.log_level)

    for path in args.files:
        if not Path(path).is_file():
            raise SystemExit(f"Document not found: {path}")

    documents = load_clean_documents(args.files)
    golden_status = check_golden(args.questions, documents)
    print(
        f"Golden dataset: {golden_status['validated_count']}/{golden_status['question_count']} "
        f"validated | Ready: {golden_status['ready']}"
    )
    if golden_status["problems"]:
        for problem in golden_status["problems"]:
            print(f"  Warning [{problem['id']}]: {problem['problem']}")

    overrides = {"vector_store": "memory"}
    if args.chunker:
        overrides["chunker"] = args.chunker
    if args.chunk_size is not None:
        overrides["chunk_size"] = args.chunk_size

    rag = configure_safe_loader(RAGTitan(rag_type=args.rag_type, settings=overrides))

    print(
        f"\nEvaluating {args.rag_type} ML RAG "
        f"(llm={rag.settings['llm_model']}, embed={rag.settings['embed_model']}, "
        f"chunker={rag.settings['chunker']}, chunk_size={rag.settings['chunk_size']})..."
    )

    report = rag.evaluate_stages(
        file_paths=args.files,
        questions=args.questions,
        k=args.k,
        include_embeddings=not args.skip_embeddings,
        show=True,
    )

    manager = ReportManager()
    if args.baseline:
        report["regressions"] = manager.regressions(report, manager.load_json(args.baseline))

    json_path = manager.save_json(report, args.output)
    md_path = manager.save_markdown(
        report,
        Path(args.output).with_suffix(".md"),
        title="Machine Learning RAG Pipeline Evaluation Report",
    )
    print(f"\nSaved reports:\n- JSON: {json_path}\n- Markdown: {md_path}")


if __name__ == "__main__":
    main()
