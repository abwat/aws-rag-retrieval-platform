variable "service_name" {
  type    = string
  default = "aws-rag-retrieval-platform"
}

variable "bedrock_model_id" {
  type    = string
  default = "anthropic.claude-3-haiku-20240307-v1:0"
}

output "deployment_contract" {
  value = {
    service_name     = var.service_name
    compute          = "ecs-fargate"
    secrets          = ["BEDROCK_MODEL_ID", "RAG_INDEX_PATH"]
    observability    = ["cloudwatch-logs", "cloudwatch-alarms"]
    bedrock_model_id = var.bedrock_model_id
  }
}

