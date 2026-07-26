from __future__ import annotations

import os
import time
from pathlib import Path

from fastapi import FastAPI, Response
from pydantic import BaseModel, Field

from .generation import build_generator
from .ingestion import build_index
from .observability import configure_observability
from .retrieval import SparseRetrievalIndex


class QueryRequest(BaseModel):
    question: str = Field(min_length=1, max_length=500)
    k: int = Field(default=3, ge=1, le=10)


class RetrievedContext(BaseModel):
    chunk_id: str
    document_id: str
    score: float
    text: str


class QueryResponse(BaseModel):
    answer: str
    citations: list[str]
    retrieved_context: list[RetrievedContext]


def load_or_build_index() -> SparseRetrievalIndex:
    index_path = Path(os.getenv("RAG_INDEX_PATH", "local_index.json"))
    docs_path = Path(os.getenv("RAG_DOCS_PATH", "sample_docs"))
    if index_path.exists():
        return SparseRetrievalIndex.load(index_path)
    return build_index(docs_path)


def build_app() -> FastAPI:
    app = FastAPI(title="AWS RAG Retrieval Platform", version="0.1.0")
    index = load_or_build_index()
    generator = build_generator()
    metrics = {"queries_total": 0, "empty_retrievals_total": 0, "latency_seconds_total": 0.0}
    configure_observability(app, "aws-rag-retrieval-platform")

    @app.get("/health")
    def health() -> dict[str, int | str]:
        return {"status": "ok", "indexed_chunks": len(index.chunks)}

    @app.post("/query", response_model=QueryResponse)
    def query(payload: QueryRequest) -> QueryResponse:
        start = time.perf_counter()
        results = index.search(payload.question, payload.k)
        metrics["queries_total"] += 1
        if not results:
            metrics["empty_retrievals_total"] += 1
        answer = generator.answer(payload.question, results)
        metrics["latency_seconds_total"] += time.perf_counter() - start
        return QueryResponse(
            answer=answer.answer,
            citations=answer.citations,
            retrieved_context=[
                RetrievedContext(
                    chunk_id=result.chunk.id,
                    document_id=result.chunk.document_id,
                    score=result.score,
                    text=result.chunk.text,
                )
                for result in results
            ],
        )

    @app.get("/metrics")
    def app_metrics() -> Response:
        avg_latency = (
            metrics["latency_seconds_total"] / metrics["queries_total"]
            if metrics["queries_total"]
            else 0.0
        )
        lines = [
            "# HELP rag_queries_total Total query requests.",
            "# TYPE rag_queries_total counter",
            f"rag_queries_total {int(metrics['queries_total'])}",
            "# HELP rag_empty_retrievals_total Queries with no retrieved context.",
            "# TYPE rag_empty_retrievals_total counter",
            f"rag_empty_retrievals_total {int(metrics['empty_retrievals_total'])}",
            "# HELP rag_avg_query_latency_seconds Average in-process query latency.",
            "# TYPE rag_avg_query_latency_seconds gauge",
            f"rag_avg_query_latency_seconds {avg_latency:.6f}",
            "# HELP rag_indexed_chunks Indexed chunks loaded by the service.",
            "# TYPE rag_indexed_chunks gauge",
            f"rag_indexed_chunks {len(index.chunks)}",
        ]
        return Response("\n".join(lines) + "\n", media_type="text/plain")

    return app


app = build_app()
