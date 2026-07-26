# Evaluation

The included evaluation starts with recall at k because it is easy to defend and automate.

## Current Metric

- `recall_at_k`: whether the expected source document appears in the top-k retrieved chunks.

## Next Metrics

- p50/p95 retrieval latency by corpus size.
- Empty result rate.
- Citation precision.
- Human acceptance rate for generated answers.
- Regression tests for chunking changes.

## Run

```bash
PYTHONPATH=src python3 scripts/build_index.py --docs sample_docs --out local_index.json
PYTHONPATH=src python3 scripts/evaluate.py --index local_index.json --cases evals/support_qa.json --json
PYTHONPATH=src python3 scripts/benchmark_chunking.py
```
