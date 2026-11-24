import argparse
import json
from pathlib import Path

from rag_titan.evaluation import check_golden, make_golden_template
from rag_titan.loaders import load_document

DEFAULT_FILES = ["docs/handbook.md"]
DEFAULT_OUTPUT = "golden_questions.json"
DEFAULT_QUESTIONS = [
    "How many days of annual leave do employees receive?",
    "How many sick leave days are employees given per year?",
    "How many days per week can employees work from home?",
    "What is the standard notice period for employees?",
    "How much internet reimbursement do employees receive per month?",
]


def load_questions(path):
    """Load questions from a .txt file (one per line) or a JSON list of strings."""
    file_path = Path(path)
    if not file_path.is_file():
        raise FileNotFoundError(f"Questions file not found: {file_path}")
    text = file_path.read_text(encoding="utf-8")
    if file_path.suffix.lower() == ".json":
        return json.loads(text)
    return [line.strip() for line in text.splitlines() if line.strip()]


def load_documents_map(file_paths):
    """Load documents into a {source: text} dictionary for quote matching."""
    loaded = [load_document(path) for path in file_paths]
    return {doc["source"]: doc["text"] for doc in loaded}


def validate_golden(golden_path, file_paths):
    """Check whether golden questions are complete and match source documents."""
    documents = load_documents_map(file_paths)
    status = check_golden(golden_path, documents)
    print(
        f"Golden check ({golden_path}): "
        f"{status['validated_count']}/{status['question_count']} validated | "
        f"Ready: {status['ready']}"
    )
    for problem in status["problems"]:
        print(f"  - [{problem['id']}] {problem['problem']}")
    return status


def parse_args():
    parser = argparse.ArgumentParser(
        description="Create or validate a golden questions JSON file."
    )
    parser.add_argument("--files", nargs="+", default=DEFAULT_FILES,
                        help="Document paths used for evidence quote matching.")
    parser.add_argument("--questions", help="Optional .txt or .json file of questions.")
    parser.add_argument("--output", default=DEFAULT_OUTPUT,
                        help="Path for the golden questions JSON file.")
    parser.add_argument("--check", action="store_true",
                        help="Validate an existing golden file instead of generating a template.")
    parser.add_argument("--force", action="store_true",
                        help="Overwrite --output if it already exists.")
    return parser.parse_args()


def main():
    args = parse_args()

    if args.check:
        status = validate_golden(args.output, args.files)
        raise SystemExit(0 if status["ready"] else 1)

    output_path = Path(args.output)
    if output_path.exists() and not args.force:
        print(
            f"{output_path} already exists. Run with --check to validate it, "
            "or --force to overwrite it with a fresh template."
        )
        validate_golden(str(output_path), args.files)
        return

    questions = load_questions(args.questions) if args.questions else DEFAULT_QUESTIONS
    documents = load_documents_map(args.files)
    golden = make_golden_template(questions, documents)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(golden, indent=4, ensure_ascii=False) + "\n", encoding="utf-8")

    suggested = sum(bool(item["expected_evidence"]) for item in golden)
    print(f"Created {output_path} ({len(golden)} questions, {suggested} suggested evidence quotes).")
    print("Next: fill in expected_answer and required_facts, then set validated to true.")


if __name__ == "__main__":
    main()
