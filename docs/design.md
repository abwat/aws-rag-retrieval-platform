# Design Notes

The app separates document processing, retrieval, generation, and serving so each part can be tested without AWS credentials.

## Current Choices

- Local sparse retrieval keeps development deterministic and credential-free.
- Chunking strategies are explicit so latency and recall tradeoffs can be measured.
- Generation is behind an interface. The local generator is used for tests; Bedrock is enabled only when AWS credentials are configured.
- The API returns citations and retrieved context to make answers auditable.

## Follow-Up Work

- Replace sparse retrieval with OpenSearch Serverless, pgvector, or another managed vector store.
- Add ingestion jobs on ECS scheduled tasks or Lambda.
- Add CloudWatch metrics for empty-retrieval rate, p95 latency, Bedrock failures, and token usage.
- Add offline evals for recall, groundedness, and answer acceptance.
