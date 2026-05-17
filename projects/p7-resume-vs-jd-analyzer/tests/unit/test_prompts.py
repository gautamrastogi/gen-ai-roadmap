"""Tests for prompt builders."""

from src import prompts


def test_analysis_prompt_contains_schema_resume_and_jd() -> None:
    messages = prompts.analysis_messages("Resume with Python", "JD needs FastAPI")
    joined = "\n".join(message["content"] for message in messages)

    assert "Target JSON Schema" in joined
    assert "Resume with Python" in joined
    assert "JD needs FastAPI" in joined
    assert "fit_score" in joined


def test_schema_mode_prompt_is_shorter() -> None:
    prompt_messages = prompts.analysis_messages("Resume with Python", "JD needs FastAPI")
    schema_messages = prompts.schema_mode_messages("Resume with Python", "JD needs FastAPI")

    prompt_len = sum(len(message["content"]) for message in prompt_messages)
    schema_len = sum(len(message["content"]) for message in schema_messages)
    assert schema_len < prompt_len
