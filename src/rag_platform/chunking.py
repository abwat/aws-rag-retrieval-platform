from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Chunk:
    id: str
    document_id: str
    text: str
    heading: str | None = None


def fixed_size_chunks(document_id: str, text: str, size: int = 700, overlap: int = 120) -> list[Chunk]:
    if size <= 0:
        raise ValueError("size must be positive")
    if overlap >= size:
        raise ValueError("overlap must be smaller than size")
    normalized = " ".join(text.split())
    chunks: list[Chunk] = []
    start = 0
    while start < len(normalized):
        end = min(start + size, len(normalized))
        chunk_text = normalized[start:end].strip()
        if chunk_text:
            chunks.append(Chunk(f"{document_id}:{len(chunks)}", document_id, chunk_text))
        if end == len(normalized):
            break
        start = end - overlap
    return chunks


def heading_aware_chunks(document_id: str, text: str, max_chars: int = 900) -> list[Chunk]:
    chunks: list[Chunk] = []
    current_heading: str | None = None
    buffer: list[str] = []

    def flush() -> None:
        nonlocal buffer
        joined = " ".join(" ".join(buffer).split()).strip()
        if joined:
            chunks.append(Chunk(f"{document_id}:{len(chunks)}", document_id, joined, current_heading))
        buffer = []

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("#"):
            flush()
            current_heading = line.lstrip("#").strip()
            continue
        if sum(len(part) for part in buffer) + len(line) > max_chars:
            flush()
        buffer.append(line)
    flush()
    return chunks

