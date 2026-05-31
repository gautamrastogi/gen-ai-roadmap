"""Tests for session persistence and state updates."""

from pathlib import Path

import pytest

from src import session_store


def test_new_session_defaults() -> None:
    session = session_store.new_session()

    assert session.persona == "default"
    assert session.messages == []
    assert session.turns == []


def test_add_turn_updates_messages_and_totals() -> None:
    session = session_store.new_session()

    session_store.add_turn(
        session,
        user_text="hello",
        assistant_text="hi",
        stats=session_store.TurnStats(prompt_tokens=10, completion_tokens=3),
    )

    assert [message.role for message in session.messages] == ["user", "assistant"]
    assert session.total_prompt_tokens == 10
    assert session.total_completion_tokens == 3
    assert session.total_tokens == 13


def test_undo_last_turn_removes_pair_and_stats() -> None:
    session = session_store.new_session()
    session_store.add_turn(
        session,
        user_text="hello",
        assistant_text="hi",
        stats=session_store.TurnStats(prompt_tokens=10, completion_tokens=3),
    )

    assert session_store.undo_last_turn(session) is True

    assert session.messages == []
    assert session.turns == []


def test_undo_empty_session_returns_false() -> None:
    assert session_store.undo_last_turn(session_store.new_session()) is False


def test_build_api_messages_includes_system_prompt() -> None:
    session = session_store.new_session()
    session_store.add_turn(
        session,
        user_text="hello",
        assistant_text="hi",
        stats=session_store.TurnStats(prompt_tokens=10, completion_tokens=3),
    )

    messages = session_store.build_api_messages(session, "system prompt")

    assert messages[0] == {"role": "system", "content": "system prompt"}
    assert messages[1]["role"] == "user"
    assert messages[2]["role"] == "assistant"


def test_save_and_load_session_round_trip(tmp_path: Path) -> None:
    path = tmp_path / "session.json"
    session = session_store.new_session(persona="concise")
    session_store.add_turn(
        session,
        user_text="hello",
        assistant_text="hi",
        stats=session_store.TurnStats(prompt_tokens=4, completion_tokens=2),
    )

    session_store.save_session(session, path)
    loaded = session_store.load_session(path)

    assert loaded.session_id == session.session_id
    assert loaded.persona == "concise"
    assert loaded.messages[0].content == "hello"
    assert loaded.total_tokens == 6


def test_invalid_role_raises() -> None:
    with pytest.raises(ValueError):
        session_store.from_dict(
            {
                "messages": [{"role": "system", "content": "bad"}],
                "turns": [],
            }
        )
