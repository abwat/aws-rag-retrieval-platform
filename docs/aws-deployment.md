# AWS Deployment

## Target Components

- ECS Fargate for the API container.
- ECR for image storage.
- Secrets Manager for model and data-store configuration.
- IAM task role scoped to Bedrock invocation and required secrets.
- CloudWatch logs, metrics, dashboards, and alarms.
- Optional OpenSearch Serverless or RDS PostgreSQL with pgvector for retrieval storage.

## Bedrock Mode

Local runs use `RAG_GENERATOR=local`. An AWS deployment can enable Bedrock:

```bash
RAG_GENERATOR=bedrock
BEDROCK_MODEL_ID=anthropic.claude-3-haiku-20240307-v1:0
AWS_REGION=us-east-1
```

The adapter calls `bedrock-runtime:InvokeModel`. Retrieval and indexing still run without AWS credentials.

## Security Notes

- The API task role should not have wildcard Bedrock or Secrets Manager access.
- Secrets should be environment-specific.
- Retrieval indexes should not contain raw confidential customer data in checked-in sample files.
- Logs should avoid full prompt/context payloads unless explicitly redacted.
