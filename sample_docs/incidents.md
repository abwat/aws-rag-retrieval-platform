# Incidents

If retrieval quality drops after a deployment, run the evaluation suite, compare recall at k by document, and inspect the chunk distribution. Roll back the index if the regression is tied to chunking or ingestion changes.

If Bedrock throttles requests, check regional quota, retry budget, average latency, and error rate. The service should return retrieved context or a graceful error instead of hallucinating an answer.

