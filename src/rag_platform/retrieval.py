from __future__ import annotations

import json
import math
import re
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .chunking import Chunk


TOKEN_RE = re.compile(r"[a-zA-Z0-9_]+")
INDEX_SCHEMA_VERSION = 1


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_RE.findall(text)]


@dataclass(frozen=True)
class SearchResult:
    chunk: Chunk
    score: float


class SparseRetrievalIndex:
    def __init__(self, chunks: list[Chunk]) -> None:
        self.chunks = chunks
        self.term_freqs = [Counter(tokenize(chunk.text)) for chunk in chunks]
        self.chunk_lengths = [sum(terms.values()) for terms in self.term_freqs]
        self.avg_chunk_length = (
            sum(self.chunk_lengths) / len(self.chunk_lengths) if self.chunk_lengths else 0.0
        )
        doc_freq: dict[str, int] = defaultdict(int)
        for terms in self.term_freqs:
            for term in terms:
                doc_freq[term] += 1
        total = max(len(chunks), 1)
        self.idf = {
            term: math.log((1 + total) / (1 + count)) + 1.0
            for term, count in doc_freq.items()
        }

    def search(self, query: str, k: int = 5) -> list[SearchResult]:
        query_terms = Counter(tokenize(query))
        scores: list[SearchResult] = []
        for chunk, terms, chunk_length in zip(self.chunks, self.term_freqs, self.chunk_lengths):
            score = 0.0
            for term, q_count in query_terms.items():
                score += q_count * self._bm25_term_score(
                    term,
                    terms.get(term, 0),
                    chunk_length,
                )
            if score > 0:
                scores.append(SearchResult(chunk, round(score, 4)))
        return sorted(scores, key=lambda result: result.score, reverse=True)[:k]

    def _bm25_term_score(self, term: str, term_frequency: int, chunk_length: int) -> float:
        if term_frequency <= 0:
            return 0.0
        k1 = 1.5
        b = 0.75
        length_norm = chunk_length / self.avg_chunk_length if self.avg_chunk_length else 1.0
        numerator = term_frequency * (k1 + 1)
        denominator = term_frequency + k1 * (1 - b + b * length_norm)
        return self.idf.get(term, 0.0) * numerator / denominator

    def metadata(self) -> dict[str, object]:
        return {
            "schema_version": INDEX_SCHEMA_VERSION,
            "chunk_count": len(self.chunks),
            "document_ids": sorted({chunk.document_id for chunk in self.chunks}),
        }

    def save(self, path: str | Path) -> None:
        payload = {
            **self.metadata(),
            "chunks": [asdict(chunk) for chunk in self.chunks],
        }
        Path(path).write_text(json.dumps(payload, indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> "SparseRetrievalIndex":
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        chunks_payload = cls._validated_chunks_payload(payload)
        chunks = [Chunk(**item) for item in chunks_payload]
        return cls(chunks)

    @staticmethod
    def _validated_chunks_payload(payload: dict[str, Any]) -> list[dict[str, Any]]:
        chunks = payload.get("chunks")
        if not isinstance(chunks, list):
            raise ValueError("index payload must contain a chunks list")
        chunk_count = payload.get("chunk_count")
        if chunk_count is not None and chunk_count != len(chunks):
            raise ValueError("index chunk_count does not match chunks list")
        return chunks
