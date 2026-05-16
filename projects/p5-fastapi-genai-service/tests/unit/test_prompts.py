"""Tests for prompt builders."""

from src import prompts, schemas


def test_summarize_prompt_mentions_requested_format() -> None:
    messages = prompts.summarize_messages("Long text", "bullets")

    assert messages[0]["role"] == "system"
    assert "five bullet points" in messages[1]["content"].lower()


def test_rewrite_prompt_uses_tone() -> None:
    messages = prompts.rewrite_messages("hello", "friendly")

    assert "warm" in messages[1]["content"].lower()


def test_classify_prompt_contains_labels_and_json_contract() -> None:
    messages = prompts.classify_messages("text", ["incident", "request"], "Prefer incidents.")

    content = messages[1]["content"]
    assert "incident" in content
    assert "request" in content
    assert "Return JSON" in content


def test_extract_prompt_contains_all_fields() -> None:
    messages = prompts.extract_messages(
        "Server abc failed.",
        [
            schemas.FieldDefinition(name="server", description="Host name"),
            schemas.FieldDefinition(name="error"),
        ],
    )

    content = messages[1]["content"]
    assert "server: Host name" in content
    assert "error" in content
