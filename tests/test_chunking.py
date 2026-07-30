import unittest

from rag_platform.chunking import fixed_size_chunks, heading_aware_chunks
from rag_platform.ingestion import build_chunks


class ChunkingTest(unittest.TestCase):
    def test_fixed_size_chunks_reject_invalid_overlap(self) -> None:
        with self.assertRaises(ValueError):
            fixed_size_chunks("doc", "some text", size=10, overlap=10)

    def test_heading_aware_chunks_preserve_heading_context(self) -> None:
        chunks = heading_aware_chunks(
            "runbook",
            "# Deploy\nShip the service.\n# Rollback\nRestore the previous task definition.",
        )

        self.assertEqual([chunk.heading for chunk in chunks], ["Deploy", "Rollback"])
        self.assertEqual(chunks[0].id, "runbook:0")
        self.assertIn("previous task definition", chunks[1].text)

    def test_build_chunks_rejects_unknown_strategy(self) -> None:
        with self.assertRaises(ValueError):
            build_chunks({"doc": "text"}, strategy="semantic")


if __name__ == "__main__":
    unittest.main()
