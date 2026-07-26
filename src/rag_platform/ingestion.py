from __future__ import annotations

from pathlib import Path

from .chunking import Chunk, fixed_size_chunks, heading_aware_chunks
from .retrieval import SparseRetrievalIndex


def load_documents(root: str | Path) -> dict[str, str]:
    base = Path(root)
    docs: dict[str, str] = {}
    for path in sorted(base.rglob("*.md")):
        docs[path.stem] = path.read_text(encoding="utf-8")
    for path in sorted(base.rglob("*.txt")):
        docs[path.stem] = path.read_text(encoding="utf-8")
    return docs


def build_chunks(docs: dict[str, str], strategy: str = "heading") -> list[Chunk]:
    chunks: list[Chunk] = []
    for document_id, text in docs.items():
        if strategy == "heading":
            chunks.extend(heading_aware_chunks(document_id, text))
        elif strategy == "fixed":
            chunks.extend(fixed_size_chunks(document_id, text))
        else:
            raise ValueError(f"unknown chunking strategy: {strategy}")
    return chunks


def build_index(root: str | Path, strategy: str = "heading") -> SparseRetrievalIndex:
    docs = load_documents(root)
    return SparseRetrievalIndex(build_chunks(docs, strategy))

