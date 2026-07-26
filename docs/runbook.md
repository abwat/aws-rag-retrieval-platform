# Runbook

## Empty Retrieval Responses

1. Confirm the index exists and has chunks.
2. Run the evaluation script.
3. Inspect recent ingestion changes.
4. Roll back chunking changes if recall dropped.

## Bedrock Timeout Or Throttling

1. Check CloudWatch metrics for timeout rate.
2. Confirm regional service health and quota limits.
3. Fall back to cached retrieval context where acceptable.
4. Increase retry budget only if user-facing latency SLOs still hold.

## Bad Or Missing Secrets

1. Run `scripts/validate_runtime.py`.
2. Confirm ECS task role can read only required secrets.
3. Check deployment events and task startup logs.

