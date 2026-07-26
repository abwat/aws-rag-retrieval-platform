#!/usr/bin/env python3
from __future__ import annotations

import os
from pathlib import Path


def main() -> None:
    checks = {
        "sample_docs_present": Path("sample_docs").exists(),
        "index_present": Path(os.getenv("RAG_INDEX_PATH", "local_index.json")).exists(),
        "bedrock_model_configured": bool(os.getenv("BEDROCK_MODEL_ID")),
        "aws_region_configured": bool(os.getenv("AWS_REGION")),
    }
    status = "ready-local" if checks["sample_docs_present"] else "degraded"
    print({"status": status, "checks": checks})


if __name__ == "__main__":
    main()

