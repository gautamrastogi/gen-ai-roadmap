#!/usr/bin/env python3
"""
Local Agent MCP Server - Handles file operations, terminal commands, and web searches locally.
This server can be called by Copilot/Cursor to offload tasks and reduce cloud token usage.
"""

from __future__ import annotations

import json
import os
import shlex
import subprocess
from pathlib import Path
from urllib import parse, request

from mcp.server.fastmcp import FastMCP

# Workspace root can be overridden from Cursor mcp.json env.
WORKSPACE = Path(
    os.getenv("WORKSPACE_ROOT", Path(__file__).resolve().parent.parent)
).resolve()
LM_STUDIO_BASE_URL = os.getenv("LM_STUDIO_BASE_URL", "http://127.0.0.1:1234")
MAX_FILE_READ_CHARS = 20_000
MAX_COMMAND_OUTPUT_CHARS = 8_000
MAX_WEB_RESULTS = 5

# Initialize MCP server
app = FastMCP(
    "Local Agent Server",
    instructions="A local MCP server for file operations, terminal commands, and web searches. Use this to offload tasks from cloud AI assistants."
)

def resolve_workspace_path(path_str: str = ".") -> Path:
    """Resolve path relative to workspace root."""
    candidate = (WORKSPACE / path_str).resolve()
    try:
        candidate.relative_to(WORKSPACE)
        return candidate
    except ValueError:
        raise ValueError(f"Path {path_str} is outside workspace")


def _truncate(text: str, max_len: int) -> str:
    if len(text) <= max_len:
        return text
    return text[:max_len] + "...[truncated]"


def _json_response(ok: bool, **kwargs: object) -> str:
    payload = {"ok": ok, **kwargs}
    return json.dumps(payload, ensure_ascii=True, indent=2)

@app.tool()
def write_file(path: str, content: str) -> str:
    """
    Write content to a file in the workspace.

    Args:
        path: Relative path to the file (e.g., 'test.py')
        content: Content to write

    Returns:
        Success message
    """
    try:
        file_path = resolve_workspace_path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = file_path.with_suffix(file_path.suffix + ".tmp")
        temp_path.write_text(content, encoding="utf-8")
        temp_path.replace(file_path)
        return _json_response(
            True,
            message="File written successfully",
            path=str(file_path.relative_to(WORKSPACE)),
            bytes=len(content.encode("utf-8")),
        )
    except Exception as exc:
        return _json_response(False, error=f"write_file failed: {exc}")

@app.tool()
def read_file(path: str) -> str:
    """
    Read content from a file in the workspace.

    Args:
        path: Relative path to the file

    Returns:
        File content or error message
    """
    try:
        file_path = resolve_workspace_path(path)
        if not file_path.exists():
            return _json_response(False, error=f"File does not exist: {path}")
        content = file_path.read_text(encoding="utf-8")
        return _json_response(
            True,
            path=str(file_path.relative_to(WORKSPACE)),
            content=_truncate(content, MAX_FILE_READ_CHARS),
        )
    except Exception as exc:
        return _json_response(False, error=f"read_file failed: {exc}")


ALLOWED_COMMANDS: dict[str, set[str]] = {
    "ls": {"-a", "-la", "-l", "-lah", "-h"},
    "pwd": set(),
    "git": {"status", "log", "diff", "branch", "show"},
    "python": {"--version", "-V"},
}


def _validate_command(command: str) -> list[str]:
    parts = shlex.split(command)
    if not parts:
        raise ValueError("Command is empty")

    base = parts[0]
    if base not in ALLOWED_COMMANDS:
        raise ValueError(f"Command '{base}' is not allowed")

    if base == "git":
        if len(parts) < 2:
            raise ValueError("git subcommand is required")
        subcommand = parts[1]
        if subcommand not in ALLOWED_COMMANDS["git"]:
            raise ValueError(f"git subcommand '{subcommand}' is not allowed")
    elif base == "python":
        # python execution is intentionally blocked in run_command
        if any(flag not in ALLOWED_COMMANDS["python"] for flag in parts[1:]):
            raise ValueError("python only allows version flags here")
    elif base == "ls":
        for flag in parts[1:]:
            if flag.startswith("-") and flag not in ALLOWED_COMMANDS["ls"]:
                raise ValueError(f"ls flag '{flag}' is not allowed")

    return parts

@app.tool()
def run_command(command: str) -> str:
    """
    Run a safe terminal command in the workspace directory.
    Only allows read-only or workspace-safe commands.

    Args:
        command: Command to run (e.g., 'ls -la', 'git status')

    Returns:
        Command output or error
    """
    try:
        argv = _validate_command(command)
        result = subprocess.run(
            argv,
            shell=False,
            cwd=WORKSPACE,
            capture_output=True,
            text=True,
            timeout=20,
        )
        output = result.stdout + result.stderr
        return _json_response(
            result.returncode == 0,
            command=command,
            returncode=result.returncode,
            output=_truncate(output, MAX_COMMAND_OUTPUT_CHARS),
        )
    except subprocess.TimeoutExpired:
        return _json_response(False, error="Command timed out")
    except ValueError as exc:
        return _json_response(False, error=str(exc))
    except Exception as exc:
        return _json_response(False, error=f"run_command failed: {exc}")

@app.tool()
def web_search(query: str) -> str:
    """
    Perform a simple web search using DuckDuckGo instant answers.

    Args:
        query: Search query

    Returns:
        Search results summary
    """
    try:
        params = parse.urlencode(
            {"q": query, "format": "json", "no_html": "1", "no_redirect": "1"}
        )
        url = f"https://api.duckduckgo.com/?{params}"
        with request.urlopen(url, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        related_results: list[dict[str, str]] = []
        for item in data.get("RelatedTopics", []):
            if len(related_results) >= MAX_WEB_RESULTS:
                break
            if isinstance(item, dict) and item.get("Text"):
                related_results.append(
                    {"text": item["Text"][:240], "url": item.get("FirstURL", "")}
                )
            elif isinstance(item, dict) and item.get("Topics"):
                for nested in item["Topics"]:
                    if len(related_results) >= MAX_WEB_RESULTS:
                        break
                    if isinstance(nested, dict) and nested.get("Text"):
                        related_results.append(
                            {
                                "text": nested["Text"][:240],
                                "url": nested.get("FirstURL", ""),
                            }
                        )

        return _json_response(
            True,
            query=query,
            answer=data.get("Answer", ""),
            abstract=data.get("AbstractText", ""),
            related=related_results,
        )
    except Exception as exc:
        return _json_response(False, error=f"web_search failed: {exc}")


@app.tool()
def call_local_model(
    prompt: str,
    system_prompt: str = "You are a concise local coding assistant.",
    max_tokens: int = 400,
    temperature: float = 0.2,
) -> str:
    """
    Call the local LM Studio OpenAI-compatible API.

    Args:
        prompt: User prompt for the local model
        system_prompt: System instruction
        max_tokens: Max generation tokens
        temperature: Sampling temperature

    Returns:
        Model output or structured error payload
    """
    try:
        model_data = request.urlopen(
            f"{LM_STUDIO_BASE_URL}/v1/models", timeout=10
        ).read()
        models_payload = json.loads(model_data.decode("utf-8"))
        model_ids = [item["id"] for item in models_payload.get("data", []) if item.get("id")]
        if not model_ids:
            return _json_response(False, error="No model loaded in LM Studio server")

        selected_model = model_ids[0]
        payload = {
            "model": selected_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        body = json.dumps(payload).encode("utf-8")
        req = request.Request(
            f"{LM_STUDIO_BASE_URL}/v1/chat/completions",
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with request.urlopen(req, timeout=45) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        message = data.get("choices", [{}])[0].get("message", {})
        content = message.get("content", "")
        if isinstance(content, list):
            content = "".join(
                item.get("text", "")
                for item in content
                if isinstance(item, dict)
            )
        if not isinstance(content, str):
            content = str(content)

        # Some models return reasoning_content instead of content.
        if not content.strip():
            content = message.get("reasoning_content", "") or message.get("reasoning", "")
            if not isinstance(content, str):
                content = str(content)

        return _json_response(
            True,
            model=selected_model,
            output=content,
            finish_reason=data.get("choices", [{}])[0].get("finish_reason", ""),
        )
    except Exception as exc:
        return _json_response(False, error=f"call_local_model failed: {exc}")

if __name__ == "__main__":
    # Run the server
    import mcp.server.stdio
    mcp.server.stdio.stdio_server(app.to_server())