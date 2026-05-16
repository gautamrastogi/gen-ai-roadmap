"""Persistent chat session storage."""

from __future__ import annotations

import dataclasses
import datetime as dt
import json
import uuid
from pathlib import Path
from typing import Literal

Role = Literal["user", "assistant"]


def _now() -> str:
    """Return an ISO-8601 UTC timestamp."""

    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat()


@dataclasses.dataclass
class ChatMessage:
    """A single persisted chat message."""

    role: Role
    content: str
    created_at: str = dataclasses.field(default_factory=_now)


@dataclasses.dataclass
class TurnStats:
    """Token stats for one user/assistant turn."""

    prompt_tokens: int
    completion_tokens: int

    @property
    def total_tokens(self) -> int:
        """Return prompt + completion tokens."""

        return self.prompt_tokens + self.completion_tokens


@dataclasses.dataclass
class ChatSession:
    """A persisted chatbot session."""

    session_id: str
    persona: str
    messages: list[ChatMessage]
    turns: list[TurnStats]
    created_at: str
    updated_at: str

    @property
    def total_prompt_tokens(self) -> int:
        """Return prompt tokens across all turns."""

        return sum(turn.prompt_tokens for turn in self.turns)

    @property
    def total_completion_tokens(self) -> int:
        """Return completion tokens across all turns."""

        return sum(turn.completion_tokens for turn in self.turns)

    @property
    def total_tokens(self) -> int:
        """Return total estimated tokens across all turns."""

        return self.total_prompt_tokens + self.total_completion_tokens


def new_session(persona: str = "default") -> ChatSession:
    """Create a fresh chat session."""

    timestamp = _now()
    return ChatSession(
        session_id=str(uuid.uuid4()),
        persona=persona,
        messages=[],
        turns=[],
        created_at=timestamp,
        updated_at=timestamp,
    )


def add_turn(
    session: ChatSession,
    user_text: str,
    assistant_text: str,
    stats: TurnStats,
) -> None:
    """Append a full user/assistant turn to the session."""

    session.messages.append(ChatMessage(role="user", content=user_text))
    session.messages.append(ChatMessage(role="assistant", content=assistant_text))
    session.turns.append(stats)
    session.updated_at = _now()


def undo_last_turn(session: ChatSession) -> bool:
    """Remove the latest user/assistant pair.

    :return: Whether a turn was removed.
    """

    if len(session.messages) < 2:
        return False
    session.messages = session.messages[:-2]
    if session.turns:
        session.turns = session.turns[:-1]
    session.updated_at = _now()
    return True


def clear_session(session: ChatSession) -> None:
    """Clear all messages and turn stats without changing session identity."""

    session.messages.clear()
    session.turns.clear()
    session.updated_at = _now()


def build_api_messages(session: ChatSession, system_prompt: str) -> list[dict[str, str]]:
    """Build OpenAI-compatible messages for the current session."""

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend({"role": msg.role, "content": msg.content} for msg in session.messages)
    return messages


def save_session(session: ChatSession, path: Path) -> None:
    """Write session JSON to disk."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(to_dict(session), indent=2) + "\n", encoding="utf-8")


def load_session(path: Path) -> ChatSession:
    """Load a session JSON file."""

    raw = json.loads(path.read_text(encoding="utf-8"))
    return from_dict(raw)


def to_dict(session: ChatSession) -> dict[str, object]:
    """Serialize a session to plain JSON-compatible data."""

    return {
        "session_id": session.session_id,
        "persona": session.persona,
        "messages": [dataclasses.asdict(message) for message in session.messages],
        "turns": [dataclasses.asdict(turn) for turn in session.turns],
        "created_at": session.created_at,
        "updated_at": session.updated_at,
        "totals": {
            "prompt_tokens": session.total_prompt_tokens,
            "completion_tokens": session.total_completion_tokens,
            "total_tokens": session.total_tokens,
        },
    }


def from_dict(raw: dict[str, object]) -> ChatSession:
    """Deserialize a session from plain JSON-compatible data."""

    messages_raw = raw.get("messages", [])
    turns_raw = raw.get("turns", [])
    if not isinstance(messages_raw, list) or not isinstance(turns_raw, list):
        raise ValueError("Invalid session file: messages and turns must be lists.")

    timestamp = _now()
    return ChatSession(
        session_id=str(raw.get("session_id") or uuid.uuid4()),
        persona=str(raw.get("persona") or "default"),
        messages=[
            ChatMessage(
                role=_parse_role(item),
                content=str(item.get("content") or ""),
                created_at=str(item.get("created_at") or timestamp),
            )
            for item in messages_raw
            if isinstance(item, dict)
        ],
        turns=[
            TurnStats(
                prompt_tokens=int(item.get("prompt_tokens") or 0),
                completion_tokens=int(item.get("completion_tokens") or 0),
            )
            for item in turns_raw
            if isinstance(item, dict)
        ],
        created_at=str(raw.get("created_at") or timestamp),
        updated_at=str(raw.get("updated_at") or timestamp),
    )


def _parse_role(item: dict[object, object]) -> Role:
    """Parse and validate a persisted role."""

    role = str(item.get("role") or "")
    if role not in {"user", "assistant"}:
        raise ValueError(f"Invalid message role: {role!r}")
    if role == "user":
        return "user"
    return "assistant"
