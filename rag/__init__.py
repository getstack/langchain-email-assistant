"""RAG: load docs → split → embed → in-memory cosine retrieve.

Chunk storage (important):
  Chunks are NOT written to disk or Supabase.
  They live in process memory as module globals:
    - `_CHUNKS`: list of chunk texts (+ source path)
    - `_MATRIX`: numpy array of embedding vectors (one row per chunk)
  Rebuilt on first retrieve (or force_rebuild). Lost when the app restarts.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from utils import logger

load_dotenv()

KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent / "knowledge"

# In-memory vector store (not persisted)
_CHUNKS: list[dict[str, str]] = []  # {"text": "...", "source": "company_guide.md"}
_MATRIX: np.ndarray | None = None
_LAST_ERROR: str | None = None

# Working Gemini embedding model (text-embedding-004 returns 404 on current API)
EMBEDDING_MODEL = "models/gemini-embedding-001"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 80


def _embeddings() -> GoogleGenerativeAIEmbeddings:
    return GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)


def _load_documents() -> list[Document]:
    KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)
    docs: list[Document] = []
    for path in sorted(KNOWLEDGE_DIR.glob("*")):
        if path.suffix.lower() not in {".md", ".txt"}:
            continue
        loaded = TextLoader(str(path), encoding="utf-8").load()
        for doc in loaded:
            doc.metadata["source"] = path.name
        docs.extend(loaded)
    return docs


def index_stats() -> dict[str, Any]:
    """Inspect where chunks live right now (memory only)."""
    return {
        "knowledge_dir": str(KNOWLEDGE_DIR),
        "chunk_count": len(_CHUNKS),
        "matrix_shape": None if _MATRIX is None else list(_MATRIX.shape),
        "embedding_model": EMBEDDING_MODEL,
        "storage": "in-memory (module globals _CHUNKS + _MATRIX)",
        "last_error": _LAST_ERROR,
        "sources": sorted({c["source"] for c in _CHUNKS}),
    }


def build_index(force_rebuild: bool = False) -> bool:
    """Load knowledge files, chunk, embed, store vectors in memory."""
    global _CHUNKS, _MATRIX, _LAST_ERROR
    if _MATRIX is not None and not force_rebuild:
        return True

    docs = _load_documents()
    if not docs:
        _CHUNKS, _MATRIX = [], None
        _LAST_ERROR = f"No .md/.txt files found in {KNOWLEDGE_DIR}"
        logger.warning("rag_build_failed reason=%s", _LAST_ERROR)
        return False

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    split_docs = splitter.split_documents(docs)
    chunk_rows = [
        {
            "text": d.page_content,
            "source": str(d.metadata.get("source") or "unknown"),
        }
        for d in split_docs
        if (d.page_content or "").strip()
    ]
    if not chunk_rows:
        _CHUNKS, _MATRIX = [], None
        _LAST_ERROR = "Documents loaded but produced zero chunks"
        logger.warning("rag_build_failed reason=%s", _LAST_ERROR)
        return False

    try:
        vectors = _embeddings().embed_documents([c["text"] for c in chunk_rows])
        _CHUNKS = chunk_rows
        _MATRIX = np.array(vectors, dtype=np.float32)
        _LAST_ERROR = None
        logger.info(
            "rag_index_ready chunks=%s sources=%s model=%s storage=in-memory",
            len(_CHUNKS),
            sorted({c["source"] for c in _CHUNKS}),
            EMBEDDING_MODEL,
        )
        return True
    except Exception as exc:
        _CHUNKS, _MATRIX = [], None
        _LAST_ERROR = str(exc)
        logger.exception("rag_embed_failed model=%s", EMBEDDING_MODEL)
        return False


def retrieve(query: str, k: int = 3) -> dict[str, Any]:
    """Return ranked chunks + joined context text for Ask AI."""
    global _LAST_ERROR
    empty = {"context": "", "sources": [], "chunks": [], "error": _LAST_ERROR}
    try:
        if not build_index():
            return {**empty, "error": _LAST_ERROR}
        assert _MATRIX is not None

        q = np.array(_embeddings().embed_query(query), dtype=np.float32)
        denom = (np.linalg.norm(_MATRIX, axis=1) * (np.linalg.norm(q) + 1e-9)) + 1e-9
        scores = (_MATRIX @ q) / denom
        top_idx = np.argsort(scores)[::-1][:k]

        chunks = []
        for i in top_idx:
            row = _CHUNKS[int(i)]
            chunks.append(
                {
                    "text": row["text"],
                    "source": row["source"],
                    "score": float(scores[int(i)]),
                }
            )

        context = "\n\n".join(c["text"] for c in chunks)
        sources = list(dict.fromkeys(c["source"] for c in chunks))
        logger.info(
            "rag_retrieve_ok query_len=%s chunks=%s sources=%s",
            len(query),
            len(chunks),
            sources,
        )
        return {"context": context, "sources": sources, "chunks": chunks, "error": None}
    except Exception as exc:
        _LAST_ERROR = str(exc)
        logger.exception("rag_retrieve_failed")
        return {**empty, "error": _LAST_ERROR}


def retrieve_context(query: str, k: int = 3) -> str:
    """Back-compat helper used by LangGraph retrieve node."""
    return retrieve(query, k=k)["context"]
