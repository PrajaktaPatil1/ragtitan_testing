import argparse
import json
from pathlib import Path

from rag_titan.evaluation import check_golden, make_golden_template

from rag_utils import DEFAULT_PDF, load_clean_documents

DEFAULT_FILES = [str(DEFAULT_PDF)]
DEFAULT_QUESTIONS = "evaluation/questions.txt"
DEFAULT_OUTPUT = "golden_questions.json"


def load_questions(path):
    """Load questions from a .txt file (one per line) or a JSON list of strings."""
    file_path = Path(path)
    if not file_path.is_file():
        raise FileNotFoundError(f"Questions file not found: {file_path}")
    text = file_path.read_text(encoding="utf-8")
    if file_path.suffix.lower() == ".json":
        return json.loads(text)
    return [line.strip() for line in text.splitlines() if line.strip()]


def validate_golden(golden_path, file_paths):
    """Check whether golden questions are complete and match source documents."""
    documents = load_clean_documents(file_paths)
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
        description="Create or validate the Machine Learning golden questions JSON file."
    )
    parser.add_argument("--files", nargs="+", default=DEFAULT_FILES,
                        help="Document paths used for evidence quote matching.")
    parser.add_argument("--questions", default=DEFAULT_QUESTIONS,
                        help="Path to a .txt or .json file of questions.")
    parser.add_argument("--output", default=DEFAULT_OUTPUT,
                        help="Path for the golden questions JSON file.")
    parser.add_argument("--check", action="store_true",
                        help="Validate an existing golden file against the source document.")
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

    questions = load_questions(args.questions)
    golden = make_golden_template(questions)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(golden, indent=4, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Created {output_path} with {len(golden)} questions.")
    print("Next: fill in expected_answer, expected_evidence, required_facts, then set validated to true.")


if __name__ == "__main__":
    main()
