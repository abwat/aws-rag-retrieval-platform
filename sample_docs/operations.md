# Operations

Missing secrets should fail deployment validation before production traffic reaches the service. Runtime readiness should report degraded status when required configuration is unavailable.

CloudWatch alarms should cover API error rate, Bedrock timeout rate, empty retrieval responses, and elevated p95 latency.

