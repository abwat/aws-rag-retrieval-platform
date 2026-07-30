import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient


class RagApiTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmpdir = tempfile.TemporaryDirectory()
        docs = Path(self.tmpdir.name) / "docs"
        docs.mkdir()
        docs.joinpath("operations.md").write_text(
            "# Operations\nMissing secrets fail readiness checks and surface in runbooks.",
            encoding="utf-8",
        )
        self.env = patch.dict(
            os.environ,
            {
                "RAG_DOCS_PATH": str(docs),
                "RAG_INDEX_PATH": str(Path(self.tmpdir.name) / "missing-index.json"),
                "RAG_GENERATOR": "local",
            },
        )
        self.env.start()
        from rag_platform.main import build_app

        self.client = TestClient(build_app())

    def tearDown(self) -> None:
        self.client.close()
        self.env.stop()
        self.tmpdir.cleanup()

    def test_query_returns_grounded_context_and_metrics(self) -> None:
        response = self.client.post(
            "/query",
            json={"question": "How are missing secrets handled?", "k": 1},
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["citations"], ["operations:0"])
        self.assertEqual(payload["retrieved_context"][0]["document_id"], "operations")

        metrics = self.client.get("/metrics")
        self.assertIn("rag_queries_total 1", metrics.text)
        self.assertIn("rag_empty_retrievals_total 0", metrics.text)

    def test_query_validation_rejects_invalid_k(self) -> None:
        response = self.client.post("/query", json={"question": "hello", "k": 99})

        self.assertEqual(response.status_code, 422)

    def test_empty_retrieval_returns_no_citations_and_updates_metrics(self) -> None:
        response = self.client.post(
            "/query",
            json={"question": "zzzz unmatched token", "k": 1},
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["citations"], [])
        self.assertEqual(payload["retrieved_context"], [])
        self.assertIn("not have enough retrieved context", payload["answer"])

        metrics = self.client.get("/metrics")
        self.assertIn("rag_queries_total 1", metrics.text)
        self.assertIn("rag_empty_retrievals_total 1", metrics.text)


if __name__ == "__main__":
    unittest.main()
