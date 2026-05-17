"""Tests for analyzer service."""

import asyncio
import json
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from pydantic import SecretStr

from src import errors
from src.service import ResumeJdAnalyzer
from src.settings import Settings


def test_analyze_with_mocked_llm() -> None:
    settings = Settings(
        analysis_mode="prompt",
        openai_base_url="http://127.0.0.1:11434/v1",
        openai_api_key=SecretStr("local-model"),
        openai_model="test-model",
    )
    analyzer = ResumeJdAnalyzer(settings, _mock_client(json.dumps(_model_payload())))

    result = asyncio.run(
        analyzer.analyze(
            "Python FastAPI Kafka Redis Postgres Docker OpenShift observability AWS",
            "Need Python FastAPI Kafka Redis PostgreSQL Docker Kubernetes AWS observability",
        )
    )

    assert result.fit_score >= 80
    assert result.score_breakdown.llm_fit_score == 84
    assert "python" in result.score_breakdown.matched_keywords
    assert result.usage.total_tokens_actual == 8


def test_analyze_raises_on_over_budget_input() -> None:
    settings = Settings(
        analysis_mode="prompt",
        openai_base_url="http://127.0.0.1:11434/v1",
        openai_api_key=SecretStr("local-model"),
        openai_model="test-model",
        max_input_tokens=1,
    )
    analyzer = ResumeJdAnalyzer(settings, _mock_client(json.dumps(_model_payload())))

    with pytest.raises(errors.BudgetExceededError):
        asyncio.run(analyzer.analyze("Python FastAPI", "Need Python"))


def test_analyze_raises_on_invalid_model_json() -> None:
    settings = Settings(
        analysis_mode="prompt",
        openai_base_url="http://127.0.0.1:11434/v1",
        openai_api_key=SecretStr("local-model"),
        openai_model="test-model",
    )
    analyzer = ResumeJdAnalyzer(settings, _mock_client("not json"))

    with pytest.raises(errors.LLMOutputError):
        asyncio.run(analyzer.analyze("Python FastAPI", "Need Python"))


def _mock_client(content: str) -> MagicMock:
    response = SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=content))],
        model="test-model",
        usage=SimpleNamespace(prompt_tokens=5, completion_tokens=3, total_tokens=8),
    )
    client = MagicMock()
    client.chat.completions.create = AsyncMock(return_value=response)
    return client


def _model_payload() -> dict[str, object]:
    return {
        "fit_score": 84,
        "recommendation": "strong_match",
        "matching_skills": ["Python", "FastAPI", "Kafka"],
        "partial_matches": ["Kubernetes"],
        "missing_skills": ["LangGraph"],
        "strengths": ["Backend platform engineering"],
        "risks": ["Limited GenAI production evidence"],
        "suggestions": ["Add a RAG/evals project to portfolio"],
        "evidence": [
            {
                "area": "Backend",
                "resume_evidence": "Built FastAPI services",
                "jd_evidence": "Requires Python backend services",
                "judgment": "strong_match",
            }
        ],
    }
