import tempfile
import unittest
from pathlib import Path

from rag_platform.evaluation import EvalCase, recall_at_k
from rag_platform.ingestion import build_chunks
from rag_platform.retrieval import SparseRetrievalIndex


class RetrievalTest(unittest.TestCase):
    def test_search_returns_relevant_chunk(self) -> None:
        chunks = build_chunks(
            {
                "operations": "# Operations\nMissing secrets fail readiness checks and surface in runbooks.",
                "retrieval": "# Retrieval\nHeading-aware chunks preserve section context.",
            }
        )
        index = SparseRetrievalIndex(chunks)

        results = index.search("How are missing secrets detected?", k=1)

        self.assertEqual(results[0].chunk.document_id, "operations")

    def test_index_round_trip(self) -> None:
        chunks = build_chunks({"retrieval": "# Retrieval\nChunking benchmarks compare strategies."})
        index = SparseRetrievalIndex(chunks)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "index.json"
            index.save(path)
            loaded = SparseRetrievalIndex.load(path)

        self.assertEqual(loaded.search("chunking", k=1)[0].chunk.document_id, "retrieval")

    def test_recall_at_k(self) -> None:
        chunks = build_chunks({"aws_architecture": "# AWS\nBedrock is isolated behind an adapter."})
        index = SparseRetrievalIndex(chunks)

        score = recall_at_k(index, [EvalCase("Where is Bedrock isolated?", "aws_architecture")], k=1)

        self.assertEqual(score, 1.0)


if __name__ == "__main__":
    unittest.main()

