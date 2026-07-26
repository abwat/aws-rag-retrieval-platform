# AWS Architecture

Amazon Bedrock access is isolated behind a generation adapter so retrieval, indexing, and API behavior can be tested locally. Private deployments should call Bedrock through the AWS SDK with least-privilege IAM permissions.

The target AWS deployment uses ECS Fargate, ECR, Secrets Manager, IAM roles, CloudWatch logs, and alarms. Terraform should create environment-specific infrastructure with separate execution roles.

