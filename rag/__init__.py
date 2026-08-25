"""RAG: load docs → split → embed → simple vector retrieve (numpy).

Uses Google embeddings with an in-memory cosine search so we avoid
heavy FAISS wheels on some platforms while still teaching the RAG flow.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent / "knowledge"
_CHUNKS: list[str] = []
_MATRIX: np.ndarray | None = None


def _embeddings() -> GoogleGenerativeAIEmbeddings:
    return GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")


def _load_documents() -> list[Document]:
    KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)
    docs: list[Document] = []
    for path in sorted(KNOWLEDGE_DIR.glob("*")):
        if path.suffix.lower() not in {".md", ".txt"}:
            continue
        docs.extend(TextLoader(str(path), encoding="utf-8").load())
    return docs


def build_index(force_rebuild: bool = False) -> bool:
    global _CHUNKS, _MATRIX
    if _MATRIX is not None and not force_rebuild:
        return True

    docs = _load_documents()
    if not docs:
        _CHUNKS, _MATRIX = [], None
        return False

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=80)
    chunks = [c.page_content for c in splitter.split_documents(docs)]
    vectors = _embeddings().embed_documents(chunks)
    _CHUNKS = chunks
    _MATRIX = np.array(vectors, dtype=np.float32)
    return True


def retrieve_context(query: str, k: int = 3) -> str:
    try:
        if not build_index():
            return ""
        assert _MATRIX is not None
        q = np.array(_embeddings().embed_query(query), dtype=np.float32)
        # Cosine similarity
        denom = (np.linalg.norm(_MATRIX, axis=1) * (np.linalg.norm(q) + 1e-9)) + 1e-9
        scores = (_MATRIX @ q) / denom
        top_idx = np.argsort(scores)[::-1][:k]
        return "\n\n".join(_CHUNKS[i] for i in top_idx)
    except Exception:
        # RAG should never break Ask AI — fall back to empty context.
        return ""
