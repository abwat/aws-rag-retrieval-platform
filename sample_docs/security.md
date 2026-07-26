# Security

The retrieval API should never log full prompts, raw customer documents, or unredacted retrieved context in production. Request logs should include request ids, latency, result counts, and error classes.

IAM permissions should be least privilege. The ECS task role needs permission to invoke the configured Bedrock model and read only the secrets required for that environment. It should not have wildcard Secrets Manager access.

Indexes containing sensitive documents should be encrypted at rest, scoped per environment, and rebuilt through a controlled ingestion job.

