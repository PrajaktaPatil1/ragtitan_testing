
from pathlib import Path

from rag_titan import RAGTitan, setup_logging


# --------------------------------------------------
# 1. Logging configuration
# --------------------------------------------------

setup_logging("INFO")


# --------------------------------------------------
# 2. Find documents inside docs folder
# --------------------------------------------------

DOCS_DIR = Path("docs")

SUPPORTED_EXTENSIONS = [
    "*.pdf",
    "*.docx",
    "*.txt",
    "*.md"
]

files = []

for extension in SUPPORTED_EXTENSIONS:
    files.extend(DOCS_DIR.glob(extension))

files = sorted(set(files))


# --------------------------------------------------
# 3. Check whether documents are available
# --------------------------------------------------

if not files:
    print("No documents found in the docs folder.")
    print("Please add PDF, DOCX, TXT or MD files.")
    raise SystemExit(1)


print("\nDocuments found:")

for file in files:
    print(f"- {file.name}")


# --------------------------------------------------
# 4. Initialize RAG-Titan
# --------------------------------------------------

print("\nInitializing RAG-Titan...")

rag = RAGTitan(rag_type="simple")


# --------------------------------------------------
# 5. Index documents
# --------------------------------------------------

print("\nIndexing documents...")

try:
    chunk_count = rag.index(
        [str(file) for file in files]
    )

    print(f"Successfully indexed {chunk_count} chunks.")

except Exception as error:
    print("\nDocument indexing failed.")
    print("Error:", error)
    raise SystemExit(1)


# --------------------------------------------------
# 6. Start interactive chatbot
# --------------------------------------------------

print("\n" + "=" * 50)
print("       LOCAL RAG CHATBOT IS READY")
print("=" * 50)

print("\nAsk questions based on your uploaded documents.")
print("Type 'trace' to inspect the RAG pipeline.")
print("Type 'exit' to close the chatbot.")


# --------------------------------------------------
# 7. Question and Answer Loop
# --------------------------------------------------

while True:

    question = input("\nYou: ").strip()

    # Exit chatbot
    if question.lower() in ["exit", "quit", "bye"]:
        print("\nChatbot stopped. Goodbye!")
        break

    # Ignore empty questions
    if not question:
        continue

    try:

        # Display pipeline execution details
        if question.lower() == "trace":

            question = input("Enter your question: ").strip()

            if not question:
                continue

            result = rag.run(question)

            print("\nAnswer:")
            print(result["answer"])

            print("\nSources:")
            print(result.get("sources", []))

            print("\nPipeline execution:")
            print(result["log"])

        else:

            # Normal RAG question
            answer = rag.ask(question)

            print("\nAssistant:")
            print(answer)

    except Exception as error:

        print("\nSomething went wrong.")
        print("Error:", error)
