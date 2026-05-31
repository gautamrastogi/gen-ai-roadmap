"""Tests for JSON extraction helpers."""

import json

import pytest

from src import json_utils


def test_extracts_json_from_markdown_fence() -> None:
    text = '```json\n{"fit_score": 80}\n```'

    assert json_utils.extract_json_object(text) == '{"fit_score": 80}'


def test_extracts_first_balanced_object() -> None:
    text = 'Result: {"a": "brace } in text", "b": 2}. Done.'

    assert json_utils.extract_json_object(text) == '{"a": "brace } in text", "b": 2}'


def test_raises_when_object_missing() -> None:
    with pytest.raises(json.JSONDecodeError):
        json_utils.extract_json_object("no json")
