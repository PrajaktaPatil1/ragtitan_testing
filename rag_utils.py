from pathlib import Path

from rag_titan.loaders import load_document

DEFAULT_PDF = (
    Path("docs")
    / "Hands-On_Machine_Learning_with_Scikit-Learn-Keras-and-TensorFlow-2nd-Edition-Aurelien-Geron.pdf"
)


def sanitize_text(text):
    """Replace lone UTF-16 surrogates from PDF extraction so UTF-8/SQLite writes succeed."""
    return text.encode("utf-8", "replace").decode("utf-8")


def load_clean_documents(file_paths):
    """Load documents into a {source: clean_text} mapping."""
    docs = {}
    for path in file_paths:
        doc = load_document(path)
        docs[doc["source"]] = sanitize_text(doc["text"])
    return docs


def configure_safe_loader(rag):
    """Wrap rag.pipeline.load_documents to sanitize extracted PDF text."""
    original_load = rag.pipeline.load_documents

    def safe_load_documents(file_paths):
        docs = original_load(file_paths)
        for doc in docs:
            doc["text"] = sanitize_text(doc["text"])
        return docs

    rag.pipeline.load_documents = safe_load_documents
    return rag
