#!/usr/bin/env python3
from __future__ import annotations

import argparse

from rag_platform.ingestion import build_index


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--docs", default="sample_docs")
    parser.add_argument("--out", default="local_index.json")
    parser.add_argument("--strategy", choices=["heading", "fixed"], default="heading")
    args = parser.parse_args()

    index = build_index(args.docs, args.strategy)
    index.save(args.out)
    print({"indexed_chunks": len(index.chunks), "out": args.out, "strategy": args.strategy})


if __name__ == "__main__":
    main()

