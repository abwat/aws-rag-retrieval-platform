# Cost

Cost controls should cover Bedrock token usage, vector-store capacity, ECS task sizing, and log retention. The platform should emit query volume, empty retrieval rate, average latency, and model invocation failures.

For development, the local generator and sparse retrieval index avoid cloud spend. For production, deployments should set budget alarms and right-size ECS CPU and memory based on p95 latency tests.

