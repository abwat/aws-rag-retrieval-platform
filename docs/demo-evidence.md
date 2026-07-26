# Local Run Notes

## Verified Local Commands

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
PYTHONPATH=src python3 scripts/build_index.py --docs sample_docs --out local_index.json
PYTHONPATH=src python3 scripts/evaluate.py --index local_index.json --cases evals/regression_qa.json --json
PYTHONPATH=src python3 scripts/benchmark_chunking.py
PYTHONPYCACHEPREFIX=.pycache_tmp python3 -m compileall src tests scripts
```

## Current Retrieval Eval

- Cases: 14
- Metric: recall@3
- Result: 1.0 on the included regression set
- Indexed chunks: 7 with heading-aware chunking

## Compose Stack

`docker compose up --build` runs the API, Prometheus, and OpenTelemetry collector. Bedrock mode is off by default and must be enabled with environment variables in an AWS-authenticated deployment.

Validated locally:

- `/health` returned `{"status":"ok","indexed_chunks":7}`
- `/query` returned cited context for a cost-control question
- `/metrics` exposed query count, empty retrieval count, average latency, and chunk count
