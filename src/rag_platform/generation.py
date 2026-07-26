from __future__ import annotations

from dataclasses import dataclass
import json
import os

from .retrieval import SearchResult


@dataclass(frozen=True)
class Answer:
    answer: str
    citations: list[str]


class LocalGroundedGenerator:
    def answer(self, question: str, results: list[SearchResult]) -> Answer:
        if not results:
            return Answer(
                answer="I do not have enough retrieved context to answer this question.",
                citations=[],
            )
        top = results[:3]
        context = " ".join(result.chunk.text for result in top)
        answer = (
            f"Based on the retrieved project context: {context[:600]}"
            + ("..." if len(context) > 600 else "")
        )
        citations = [result.chunk.id for result in top]
        return Answer(answer=answer, citations=citations)


class BedrockGenerator:
    def __init__(self, model_id: str) -> None:
        self.model_id = model_id
        self.region = os.getenv("AWS_REGION", "us-east-1")
        import boto3

        self.client = boto3.client("bedrock-runtime", region_name=self.region)

    def answer(self, question: str, results: list[SearchResult]) -> Answer:
        if not results:
            return Answer(
                answer="I do not have enough retrieved context to answer this question.",
                citations=[],
            )
        context = "\n\n".join(
            f"[{result.chunk.id}] {result.chunk.text}" for result in results[:5]
        )
        prompt = (
            "Answer using only the retrieved context. Cite chunk ids inline.\n\n"
            f"Question: {question}\n\nContext:\n{context}"
        )
        response = self.client.invoke_model(
            modelId=self.model_id,
            body=json.dumps(
                {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 500,
                    "messages": [{"role": "user", "content": prompt}],
                }
            ),
        )
        payload = json.loads(response["body"].read())
        text_parts = [
            item.get("text", "")
            for item in payload.get("content", [])
            if item.get("type") == "text"
        ]
        return Answer(
            answer="\n".join(text_parts).strip(),
            citations=[result.chunk.id for result in results[:5]],
        )


def build_generator() -> LocalGroundedGenerator | BedrockGenerator:
    if os.getenv("RAG_GENERATOR", "local").lower() == "bedrock":
        return BedrockGenerator(
            os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0")
        )
    return LocalGroundedGenerator()
