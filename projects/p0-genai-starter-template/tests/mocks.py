"""Central fixture store for the GenAI Starter Template test suite.

All fixture data is defined as module-level constants here.
Test files import from this module instead of building data inline.

Example::

    from tests import mocks

    result = await complete(client, model, mocks.COMPLETION_REQUEST)
    assert result == mocks.COMPLETION_RESPONSE_EXPECTED
"""

import typing

# ---------------------------------------------------------------------------
# CompletionRequest fixtures
# ---------------------------------------------------------------------------

COMPLETION_REQUEST: dict[str, typing.Any] = {
    "prompt": "Summarise the following text in one sentence: FastAPI is a modern Python web framework.",
    "system": "You are a helpful assistant.",
    "max_tokens": 100,
    "temperature": 0.0,
}

COMPLETION_REQUEST_MINIMAL: dict[str, typing.Any] = {
    "prompt": "Say hello.",
}

# ---------------------------------------------------------------------------
# OpenAI API mock response shapes
# ---------------------------------------------------------------------------

OPENAI_CHAT_RESPONSE: dict[str, typing.Any] = {
    "id": "chatcmpl-test123",
    "object": "chat.completion",
    "model": "gpt-4o-mini",
    "choices": [
        {
            "index": 0,
            "message": {"role": "assistant", "content": "FastAPI is a modern Python web framework."},
            "finish_reason": "stop",
        }
    ],
    "usage": {
        "prompt_tokens": 20,
        "completion_tokens": 10,
        "total_tokens": 30,
    },
}

# ---------------------------------------------------------------------------
# Expected tool output shapes
# ---------------------------------------------------------------------------

COMPLETION_RESPONSE_EXPECTED: dict[str, typing.Any] = {
    "text": "FastAPI is a modern Python web framework.",
    "model": "gpt-4o-mini",
    "usage": {
        "prompt_tokens": 20,
        "completion_tokens": 10,
        "total_tokens": 30,
    },
}
