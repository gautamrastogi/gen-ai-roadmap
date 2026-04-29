#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib import error, request


DEFAULT_BASE_URL = "http://127.0.0.1:11434/v1"
DEFAULT_MODEL = "qwen3"
MAX_TOOL_ROUNDS = 6
WORKSPACE = Path(__file__).resolve().parent


SYSTEM_PROMPT = """You are a tiny local coding agent.

You are allowed to use tools when needed.
Be concise, practical, and honest.
If a tool is useful, call it instead of guessing.
Stay inside the provided workspace.
"""


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get the current local date and time.",
            "parameters": {"type": "object", "properties": {}, "additionalProperties": False},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List files in the workspace or a subdirectory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Optional relative path inside the workspace.",
                    }
                },
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a small text file from the workspace.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Relative file path inside the workspace.",
                    }
                },
                "required": ["path"],
                "additionalProperties": False,
            },
        },
    },
]


def resolve_workspace_path(path_str: str = ".") -> Path:
    candidate = (WORKSPACE / path_str).resolve()
    candidate.relative_to(WORKSPACE)
    return candidate


def tool_get_current_time(_: dict[str, Any]) -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def tool_list_files(args: dict[str, Any]) -> str:
    path = resolve_workspace_path(args.get("path") or ".")
    if not path.exists():
        return f"Path does not exist: {path.relative_to(WORKSPACE)}"
    if not path.is_dir():
        return f"Not a directory: {path.relative_to(WORKSPACE)}"

    entries = []
    for item in sorted(path.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))[:60]:
        marker = "/" if item.is_dir() else ""
        entries.append(f"{item.relative_to(WORKSPACE)}{marker}")
    return "\n".join(entries) if entries else "(empty directory)"


def tool_read_file(args: dict[str, Any]) -> str:
    raw_path = args.get("path") or ""
    if not raw_path:
        return "Missing required argument: path"
    path = resolve_workspace_path(raw_path)
    if not path.exists():
        return f"File does not exist: {raw_path}"
    if not path.is_file():
        return f"Not a file: {raw_path}"

    text = path.read_text(encoding="utf-8", errors="replace")
    max_chars = 4000
    if len(text) > max_chars:
        text = text[:max_chars] + "\n...[truncated]"
    return text


AVAILABLE_TOOLS = {
    "get_current_time": tool_get_current_time,
    "list_files": tool_list_files,
    "read_file": tool_read_file,
}


def post_json(url: str, payload: dict[str, Any]) -> dict[str, Any]:
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} from local model server: {body}") from exc
    except error.URLError as exc:
        raise RuntimeError(
            f"Could not reach local model server at {url}. Is Ollama or LM Studio running?"
        ) from exc


def call_model(base_url: str, model: str, messages: list[dict[str, Any]]) -> dict[str, Any]:
    payload = {
        "model": model,
        "messages": messages,
        "tools": TOOLS,
        "tool_choice": "auto",
        "stream": False,
        "temperature": 0.2,
    }
    return post_json(f"{base_url.rstrip('/')}/chat/completions", payload)


def extract_message(response: dict[str, Any]) -> dict[str, Any]:
    choices = response.get("choices") or []
    if not choices:
        raise RuntimeError(f"Unexpected response: {json.dumps(response, indent=2)}")
    return choices[0]["message"]


def run_tool_call(tool_call: dict[str, Any]) -> dict[str, Any]:
    fn = tool_call.get("function") or {}
    name = fn.get("name", "")
    raw_args = fn.get("arguments") or "{}"
    try:
        args = json.loads(raw_args)
    except json.JSONDecodeError:
        args = {}

    handler = AVAILABLE_TOOLS.get(name)
    if not handler:
        result = f"Unknown tool: {name}"
    else:
        try:
            result = handler(args)
        except Exception as exc:  # noqa: BLE001
            result = f"Tool error in {name}: {exc}"

    print(f"\n[tool] {name}({args})")
    print(result[:800] + ("..." if len(result) > 800 else ""))

    return {
        "role": "tool",
        "tool_call_id": tool_call.get("id", ""),
        "name": name,
        "content": result,
    }


def chat_loop(base_url: str, model: str) -> None:
    print("Tiny local agent demo")
    print(f"Workspace: {WORKSPACE}")
    print(f"Model server: {base_url}")
    print(f"Model: {model}")
    print("Try: 'list files here', 'read genai-roadmap.md', 'what time is it?'")
    print("Type 'quit' to exit.\n")

    messages: list[dict[str, Any]] = [{"role": "system", "content": SYSTEM_PROMPT}]

    while True:
        try:
            user_input = input("you> ").strip()
        except EOFError:
            print()
            return

        if not user_input:
            continue
        if user_input.lower() in {"quit", "exit"}:
            return

        messages.append({"role": "user", "content": user_input})

        for _ in range(MAX_TOOL_ROUNDS):
            response = call_model(base_url, model, messages)
            message = extract_message(response)

            assistant_text = (message.get("content") or "").strip()
            tool_calls = message.get("tool_calls") or []

            assistant_message = {"role": "assistant", "content": message.get("content", "")}
            if tool_calls:
                assistant_message["tool_calls"] = tool_calls
            messages.append(assistant_message)

            if assistant_text:
                print(f"agent> {assistant_text}")

            if not tool_calls:
                print()
                break

            for tool_call in tool_calls:
                messages.append(run_tool_call(tool_call))
        else:
            print("agent> Stopped after too many tool rounds.\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Tiny local agent demo for Ollama/LM Studio.")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="OpenAI-compatible base URL")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Local model name")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        chat_loop(args.base_url, args.model)
    except KeyboardInterrupt:
        print("\nbye")
        return 0
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
