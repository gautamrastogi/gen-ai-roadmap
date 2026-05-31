"""Tests for JSON extraction helpers."""

import json

import pytest

from src import json_utils


def test_extracts_plain_json_object() -> None:
    assert json_utils.extract_json_object('{"a": 1}') == '{"a": 1}'


def test_extracts_json_from_markdown_fence() -> None:
    text = '```json\n{"a": {"b": 2}}\n```'

    assert json_utils.extract_json_object(text) == '{"a": {"b": 2}}'


def test_extracts_first_balanced_object_from_text() -> None:
    text = 'Here is the JSON: {"a": "brace } inside string", "b": 2}. Done.'

    assert json_utils.extract_json_object(text) == '{"a": "brace } inside string", "b": 2}'


def test_raises_when_json_missing() -> None:
    with pytest.raises(json.JSONDecodeError):
        json_utils.extract_json_object("no object here")
