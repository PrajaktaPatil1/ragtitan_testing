
from pathlib import Path
from rag_titan import RAGTitan

# ----------------------------------
# 1. Project configuration
# ----------------------------------

BASE_DIR = Path(__file__).resolve().parent

PDF_PATH = (
    BASE_DIR
    / "docs"
    / "Hands-On_Machine_Learning_with_Scikit-Learn-Keras-and-TensorFlow-2nd-Edition-Aurelien-Geron.pdf"
)

# ----------------------------------
# 2. Verify PDF
# ----------------------------------

print("\nChecking PDF document...")

if not PDF_PATH.exists():
    raise FileNotFoundError(
        f"PDF not found: {PDF_PATH}"
    )

print(f"PDF Found: {PDF_PATH.name}")
print(f"PDF Size: {PDF_PATH.stat().st_size / (1024 * 1024):.2f} MB")

# ----------------------------------
# 3. Initialize RAG-Titan
# ----------------------------------

print("\nInitializing RAG-Titan...")

rag = RAGTitan(rag_type="simple")

# ----------------------------------
# 4. Index PDF document
# ----------------------------------

print("\nIndexing PDF document...")
print("This may take some time for a large book.")

rag.index([str(PDF_PATH)])

print("\nPDF indexing completed!")

# ----------------------------------
# 5. Start chatbot
# ----------------------------------

print("\n" + "=" * 55)
print("       MACHINE LEARNING PDF CHATBOT")
print("=" * 55)

print("\nAsk questions about your Machine Learning book.")
print("Type 'trace' to inspect the RAG pipeline.")
print("Type 'exit' to close the chatbot.")

# ----------------------------------
# 6. Question-answering loop
# ----------------------------------

while True:

    question = input("\nYou: ").strip()

    if question.lower() == "exit":
        print("\nChatbot closed.")
        break

    if not question:
        continue

    try:

        if question.lower() == "trace":

            question = input("Enter your question: ").strip()

            if not question:
                continue

            result = rag.run(question)

            print("\nPipeline trace:")
            print(result["log"])

            continue

        answer = rag.ask(question)

        print("\nAssistant:", answer)

    except Exception as e:

        print("\nError:", str(e))
