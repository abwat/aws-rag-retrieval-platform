from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .retrieval import SparseRetrievalIndex


@dataclass(frozen=True)
class EvalCase:
    question: str
    expected_document: str


DEFAULT_CASES = [
    EvalCase("How are missing secrets handled?", "operations"),
    EvalCase("What chunking strategies are supported?", "retrieval"),
    EvalCase("How is Bedrock isolated from the core service?", "aws_architecture"),
]


@dataclass(frozen=True)
class EvalResult:
    question: str
    expected_document: str
    hit: bool
    retrieved_documents: list[str]


def load_cases(path: str | Path) -> list[EvalCase]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    return [
        EvalCase(question=item["question"], expected_document=item["expected_document"])
        for item in payload["cases"]
    ]


def evaluate_cases(index: SparseRetrievalIndex, cases: list[EvalCase], k: int = 3) -> list[EvalResult]:
    results: list[EvalResult] = []
    for case in cases:
        search_results = index.search(case.question, k=k)
        retrieved_documents = [result.chunk.document_id for result in search_results]
        results.append(
            EvalResult(
                question=case.question,
                expected_document=case.expected_document,
                hit=case.expected_document in retrieved_documents,
                retrieved_documents=retrieved_documents,
            )
        )
    return results


def recall_at_k(index: SparseRetrievalIndex, cases: list[EvalCase], k: int = 3) -> float:
    if not cases:
        return 0.0
    results = evaluate_cases(index, cases, k)
    return sum(1 for result in results if result.hit) / len(cases)
