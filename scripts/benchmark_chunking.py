#!/usr/bin/env python3
from __future__ import annotations

import argparse
import time

from rag_platform.evaluation import load_cases, recall_at_k
from rag_platform.ingestion import build_index


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--docs", default="sample_docs")
    parser.add_argument("--cases", default="evals/regression_qa.json")
    parser.add_argument("--k", type=int, default=3)
    args = parser.parse_args()

    cases = load_cases(args.cases)
    rows = []
    for strategy in ("heading", "fixed"):
        start = time.perf_counter()
        index = build_index(args.docs, strategy)
        build_seconds = time.perf_counter() - start
        score = recall_at_k(index, cases, args.k)
        rows.append(
            {
                "strategy": strategy,
                "chunks": len(index.chunks),
                "build_seconds": round(build_seconds, 4),
                "recall_at_k": round(score, 3),
            }
        )
    for row in rows:
        print(row)


if __name__ == "__main__":
    main()
