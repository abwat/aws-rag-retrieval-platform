#!/usr/bin/env python3
from __future__ import annotations

import argparse

from dataclasses import asdict
import json

from rag_platform.evaluation import DEFAULT_CASES, evaluate_cases, load_cases, recall_at_k
from rag_platform.retrieval import SparseRetrievalIndex


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", default="local_index.json")
    parser.add_argument("--cases", default="")
    parser.add_argument("--k", type=int, default=3)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    index = SparseRetrievalIndex.load(args.index)
    cases = load_cases(args.cases) if args.cases else DEFAULT_CASES
    score = recall_at_k(index, cases, k=args.k)
    results = evaluate_cases(index, cases, k=args.k)
    payload = {
        "cases": len(cases),
        "k": args.k,
        "recall_at_k": round(score, 3),
        "results": [asdict(result) for result in results],
    }
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print({key: payload[key] for key in ("cases", "k", "recall_at_k")})


if __name__ == "__main__":
    main()
