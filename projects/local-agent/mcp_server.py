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
import time
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4
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
HTTP_RETRY_ATTEMPTS = 3
HTTP_RETRY_BACKOFF_SECONDS = 0.6
LOG_DIR = WORKSPACE / "local-agent" / "logs"
LOG_FILE = LOG_DIR / "mcp_server.log"
REDACT_KEYS = {"api_key", "token", "authorization", "password", "secret"}

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


def _request_id() -> str:
    return uuid4().hex[:12]


def _sanitize_for_logs(value: object) -> object:
    if isinstance(value, dict):
        sanitized: dict[str, object] = {}
        for key, item in value.items():
            if key.lower() in REDACT_KEYS:
                sanitized[key] = "[REDACTED]"
            else:
                sanitized[key] = _sanitize_for_logs(item)
        return sanitized
    if isinstance(value, list):
        return [_sanitize_for_logs(item) for item in value]
    if isinstance(value, str):
        lowered = value.lower()
        if "api_key=" in lowered or "token=" in lowered or "password=" in lowered:
            return "[REDACTED]"
    return value


def _log_event(tool: str, request_id: str, status: str, details: dict[str, object]) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    event = {
        "ts": datetime.now(UTC).isoformat(),
        "tool": tool,
        "request_id": request_id,
        "status": status,
        "details": _sanitize_for_logs(details),
    }
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=True) + "\n")


def _http_get_json(url: str, timeout: int, request_id: str, tool_name: str) -> dict[str, object]:
    last_error: Exception | None = None
    for attempt in range(1, HTTP_RETRY_ATTEMPTS + 1):
        try:
            with request.urlopen(url, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as exc:  # pragma: no cover - depends on runtime network
            last_error = exc
            _log_event(
                tool_name,
                request_id,
                "retry",
                {"attempt": attempt, "error": str(exc)},
            )
            if attempt < HTTP_RETRY_ATTEMPTS:
                time.sleep(HTTP_RETRY_BACKOFF_SECONDS * attempt)
    raise RuntimeError(f"GET failed after retries: {last_error}")


def _http_post_json(
    url: str,
    payload: dict[str, object],
    timeout: int,
    request_id: str,
    tool_name: str,
) -> dict[str, object]:
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    last_error: Exception | None = None
    for attempt in range(1, HTTP_RETRY_ATTEMPTS + 1):
        try:
            with request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as exc:  # pragma: no cover - depends on runtime network
            last_error = exc
            _log_event(
                tool_name,
                request_id,
                "retry",
                {"attempt": attempt, "error": str(exc)},
            )
            if attempt < HTTP_RETRY_ATTEMPTS:
                time.sleep(HTTP_RETRY_BACKOFF_SECONDS * attempt)
    raise RuntimeError(f"POST failed after retries: {last_error}")

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
    request_id = _request_id()
    try:
        file_path = resolve_workspace_path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = file_path.with_suffix(file_path.suffix + ".tmp")
        temp_path.write_text(content, encoding="utf-8")
        temp_path.replace(file_path)
        _log_event("write_file", request_id, "ok", {"path": path, "bytes": len(content.encode("utf-8"))})
        return _json_response(
            True,
            request_id=request_id,
            message="File written successfully",
            path=str(file_path.relative_to(WORKSPACE)),
            bytes=len(content.encode("utf-8")),
        )
    except Exception as exc:
        _log_event("write_file", request_id, "error", {"path": path, "error": str(exc)})
        return _json_response(False, request_id=request_id, error=f"write_file failed: {exc}")

@app.tool()
def read_file(path: str) -> str:
    """
    Read content from a file in the workspace.

    Args:
        path: Relative path to the file

    Returns:
        File content or error message
    """
    request_id = _request_id()
    try:
        file_path = resolve_workspace_path(path)
        if not file_path.exists():
            _log_event("read_file", request_id, "error", {"path": path, "error": "missing file"})
            return _json_response(False, request_id=request_id, error=f"File does not exist: {path}")
        content = file_path.read_text(encoding="utf-8")
        _log_event("read_file", request_id, "ok", {"path": path, "bytes": len(content.encode("utf-8"))})
        return _json_response(
            True,
            request_id=request_id,
            path=str(file_path.relative_to(WORKSPACE)),
            content=_truncate(content, MAX_FILE_READ_CHARS),
        )
    except Exception as exc:
        _log_event("read_file", request_id, "error", {"path": path, "error": str(exc)})
        return _json_response(False, request_id=request_id, error=f"read_file failed: {exc}")


@app.tool()
def list_tool_capabilities() -> str:
    """
    List tool capabilities for policy checks and auditing.
    """
    request_id = _request_id()
    capabilities = {
        "write_file": {"mode": "write", "network": False, "destructive": False},
        "read_file": {"mode": "read", "network": False, "destructive": False},
        "run_command": {"mode": "execute", "network": False, "destructive": False},
        "git_status_and_diff": {"mode": "read", "network": False, "destructive": False},
        "web_search": {"mode": "read", "network": True, "destructive": False},
        "call_local_model": {"mode": "read", "network": True, "destructive": False},
        "health_check": {"mode": "read", "network": False, "destructive": False},
        "list_tool_capabilities": {"mode": "read", "network": False, "destructive": False},
    }
    _log_event("list_tool_capabilities", request_id, "ok", {"tool_count": len(capabilities)})
    return _json_response(True, request_id=request_id, capabilities=capabilities)


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
    request_id = _request_id()
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
        _log_event(
            "run_command",
            request_id,
            "ok" if result.returncode == 0 else "error",
            {"command": command, "returncode": result.returncode},
        )
        return _json_response(
            result.returncode == 0,
            request_id=request_id,
            command=command,
            returncode=result.returncode,
            output=_truncate(output, MAX_COMMAND_OUTPUT_CHARS),
        )
    except subprocess.TimeoutExpired:
        _log_event("run_command", request_id, "error", {"command": command, "error": "timeout"})
        return _json_response(False, request_id=request_id, error="Command timed out")
    except ValueError as exc:
        _log_event("run_command", request_id, "error", {"command": command, "error": str(exc)})
        return _json_response(False, request_id=request_id, error=str(exc))
    except Exception as exc:
        _log_event("run_command", request_id, "error", {"command": command, "error": str(exc)})
        return _json_response(False, request_id=request_id, error=f"run_command failed: {exc}")


@app.tool()
def git_status_and_diff(max_lines: int = 300) -> str:
    """
    Return branch/status summary and a shortened diff preview.

    Args:
        max_lines: Maximum number of diff lines to return.
    """
    request_id = _request_id()
    if max_lines < 1 or max_lines > 1200:
        return _json_response(
            False,
            request_id=request_id,
            error="max_lines must be between 1 and 1200",
        )
    try:
        status = subprocess.run(
            ["git", "status", "--short", "--branch"],
            shell=False,
            cwd=WORKSPACE,
            capture_output=True,
            text=True,
            timeout=20,
        )
        diff = subprocess.run(
            ["git", "diff", "--", ".", ":(exclude).env", ":(exclude).env.*"],
            shell=False,
            cwd=WORKSPACE,
            capture_output=True,
            text=True,
            timeout=30,
        )
        diff_lines = (diff.stdout + diff.stderr).splitlines()
        _log_event(
            "git_status_and_diff",
            request_id,
            "ok" if status.returncode == 0 and diff.returncode == 0 else "error",
            {
                "status_returncode": status.returncode,
                "diff_returncode": diff.returncode,
                "max_lines": max_lines,
            },
        )
        return _json_response(
            status.returncode == 0 and diff.returncode == 0,
            request_id=request_id,
            status_output=_truncate(status.stdout + status.stderr, MAX_COMMAND_OUTPUT_CHARS),
            diff_preview="\n".join(diff_lines[:max_lines]),
            diff_total_lines=len(diff_lines),
        )
    except Exception as exc:
        _log_event("git_status_and_diff", request_id, "error", {"error": str(exc)})
        return _json_response(False, request_id=request_id, error=f"git_status_and_diff failed: {exc}")

@app.tool()
def web_search(query: str) -> str:
    """
    Perform a simple web search using DuckDuckGo instant answers.

    Args:
        query: Search query

    Returns:
        Search results summary
    """
    request_id = _request_id()
    try:
        params = parse.urlencode(
            {"q": query, "format": "json", "no_html": "1", "no_redirect": "1"}
        )
        url = f"https://api.duckduckgo.com/?{params}"
        data = _http_get_json(url, timeout=10, request_id=request_id, tool_name="web_search")

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
            request_id=request_id,
            query=query,
            answer=data.get("Answer", ""),
            abstract=data.get("AbstractText", ""),
            related=related_results,
        )
    except Exception as exc:
        _log_event("web_search", request_id, "error", {"query": query, "error": str(exc)})
        return _json_response(False, request_id=request_id, error=f"web_search failed: {exc}")


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
    request_id = _request_id()
    try:
        models_payload = _http_get_json(
            f"{LM_STUDIO_BASE_URL}/v1/models",
            timeout=10,
            request_id=request_id,
            tool_name="call_local_model",
        )
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
        data = _http_post_json(
            f"{LM_STUDIO_BASE_URL}/v1/chat/completions",
            payload=payload,
            timeout=45,
            request_id=request_id,
            tool_name="call_local_model",
        )

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
            request_id=request_id,
            model=selected_model,
            output=content,
            finish_reason=data.get("choices", [{}])[0].get("finish_reason", ""),
        )
    except Exception as exc:
        _log_event("call_local_model", request_id, "error", {"error": str(exc)})
        return _json_response(False, request_id=request_id, error=f"call_local_model failed: {exc}")


@app.tool()
def health_check() -> str:
    """
    Return diagnostic information for local MCP server readiness.
    """
    request_id = _request_id()
    checks: dict[str, object] = {}
    ok = True
    try:
        workspace_writable = False
        probe_path = WORKSPACE / ".mcp_write_probe.tmp"
        try:
            probe_path.write_text("ok", encoding="utf-8")
            workspace_writable = True
        finally:
            if probe_path.exists():
                probe_path.unlink()

        checks["workspace"] = {
            "path": str(WORKSPACE),
            "exists": WORKSPACE.exists(),
            "is_dir": WORKSPACE.is_dir(),
            "writable": workspace_writable,
        }
        if not checks["workspace"]["exists"] or not checks["workspace"]["is_dir"]:
            ok = False

        LOG_DIR.mkdir(parents=True, exist_ok=True)
        checks["logging"] = {
            "log_dir": str(LOG_DIR),
            "log_file": str(LOG_FILE),
            "writable": os.access(LOG_DIR, os.W_OK),
        }
        if not checks["logging"]["writable"]:
            ok = False

        git_probe = subprocess.run(
            ["git", "--version"],
            shell=False,
            cwd=WORKSPACE,
            capture_output=True,
            text=True,
            timeout=10,
        )
        checks["git"] = {
            "ok": git_probe.returncode == 0,
            "output": _truncate(git_probe.stdout + git_probe.stderr, 200),
        }
        if git_probe.returncode != 0:
            ok = False

        try:
            models_payload = _http_get_json(
                f"{LM_STUDIO_BASE_URL}/v1/models",
                timeout=8,
                request_id=request_id,
                tool_name="health_check",
            )
            model_ids = [
                item["id"] for item in models_payload.get("data", []) if isinstance(item, dict) and item.get("id")
            ]
            checks["lm_studio"] = {
                "base_url": LM_STUDIO_BASE_URL,
                "reachable": True,
                "loaded_models": model_ids,
            }
        except Exception as lm_exc:
            ok = False
            checks["lm_studio"] = {
                "base_url": LM_STUDIO_BASE_URL,
                "reachable": False,
                "error": str(lm_exc),
            }

        _log_event("health_check", request_id, "ok" if ok else "error", checks)
        return _json_response(ok, request_id=request_id, checks=checks)
    except Exception as exc:
        _log_event("health_check", request_id, "error", {"error": str(exc)})
        return _json_response(False, request_id=request_id, error=f"health_check failed: {exc}")

if __name__ == "__main__":
    # Run the server
    import mcp.server.stdio
    mcp.server.stdio.stdio_server(app.to_server())