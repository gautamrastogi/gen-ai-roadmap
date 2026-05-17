"""Helpers for extracting JSON from model text."""

import json


def extract_json_object(text: str) -> str:
    """Extract the first complete JSON object from model text."""

    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = _strip_markdown_fence(stripped)
    if stripped.startswith("{") and stripped.endswith("}"):
        return stripped

    start = stripped.find("{")
    if start < 0:
        raise json.JSONDecodeError("No JSON object found", stripped, 0)

    depth = 0
    in_string = False
    escaped = False
    for index, char in enumerate(stripped[start:], start=start):
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if char == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return stripped[start : index + 1]

    raise json.JSONDecodeError("Unclosed JSON object", stripped, start)


def _strip_markdown_fence(text: str) -> str:
    """Remove a simple fenced code block wrapper."""

    lines = text.splitlines()
    if len(lines) >= 2 and lines[0].startswith("```") and lines[-1].strip() == "```":
        return "\n".join(lines[1:-1]).strip()
    return text
