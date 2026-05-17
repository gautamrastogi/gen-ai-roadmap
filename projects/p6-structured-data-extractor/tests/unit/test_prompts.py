"""Tests for prompt builders."""

from src import prompts, registry
from tests.fixtures.documents import SAMPLE_DOCUMENTS


def test_extraction_prompt_contains_schema_and_document() -> None:
    definition = registry.get_schema("invoice")
    messages = prompts.extraction_messages(definition, "Invoice INV-1 total EUR 10")

    joined = "\n".join(message["content"] for message in messages)
    assert "JSON Schema" in joined
    assert "Invoice INV-1" in joined
    assert "line_items" in joined


def test_schema_mode_prompt_is_shorter_than_prompt_mode() -> None:
    definition = registry.get_schema("support_ticket")
    prompt_messages = prompts.extraction_messages(definition, "INC-1 checkout down")
    schema_messages = prompts.schema_mode_messages(definition, "INC-1 checkout down")

    prompt_len = sum(len(message["content"]) for message in prompt_messages)
    schema_len = sum(len(message["content"]) for message in schema_messages)
    assert schema_len < prompt_len


def test_fixture_suite_has_ten_varied_documents() -> None:
    assert len(SAMPLE_DOCUMENTS) == 10
    assert {item["schema"] for item in SAMPLE_DOCUMENTS} == {
        "invoice",
        "support_ticket",
        "log_incident",
    }
