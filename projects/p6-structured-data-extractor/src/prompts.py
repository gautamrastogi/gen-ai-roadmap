"""Prompt builders for structured extraction."""

import json

from src import registry

Message = dict[str, str]


def extraction_messages(definition: registry.SchemaDefinition, text: str) -> list[Message]:
    """Build messages for prompt-and-validate extraction."""

    schema_json = json.dumps(definition.model.model_json_schema(), indent=2, sort_keys=True)
    return [
        {
            "role": "system",
            "content": (
                "You extract structured data from messy operational and business text. "
                "Return valid JSON only. Do not include markdown fences, commentary, or extra keys. "
                "Use null when a required nullable field is missing. Preserve evidence from the text. "
                "Every required top-level and nested key from the schema must be present. "
                "For invoice line_items, each item must include description, quantity, unit_price, "
                "and line_total."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Target schema: {definition.title}\n"
                f"Schema purpose: {definition.description}\n\n"
                f"JSON Schema:\n{schema_json}\n\n"
                f"Document:\n{text}\n\n"
                "Return one JSON object matching the schema."
            ),
        },
    ]


def schema_mode_messages(definition: registry.SchemaDefinition, text: str) -> list[Message]:
    """Build shorter messages when provider-level schema enforcement is enabled."""

    return [
        {
            "role": "system",
            "content": (
                "You extract structured data from messy operational and business text. "
                "Follow the provided response schema exactly and preserve facts from the source text. "
                "Every required top-level and nested key from the schema must be present."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Extract a {definition.title} object.\n"
                f"Schema purpose: {definition.description}\n\n"
                f"Document:\n{text}"
            ),
        },
    ]
