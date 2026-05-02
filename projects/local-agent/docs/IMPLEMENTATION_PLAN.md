# Hybrid Local-Agent Implementation Plan

## Goal
Ship a reliable daily-driver hybrid assistant where Cursor handles reasoning and the local MCP server handles deterministic execution with LM Studio.

## Phase 1 (Now): Solid Foundation
1. Harden existing tools (`write_file`, `read_file`, `run_command`, `web_search`).
2. Add `call_local_model` for LM Studio.
3. Standardize responses to JSON (`ok`, payload, `error`).
4. Configure Cursor MCP in `.cursor/mcp.json`.
5. Add and run smoke tests (`tests/test_mcp.py`).

## Phase 2 (Next): Reliability
1. Add request IDs and structured logging for every tool call.
2. Add per-tool timeout and retry policy.
3. Add explicit tool-level permissions (read/write/destructive labels).
4. Add better `run_command` policy (command + argument allowlists per command).
5. Add test cases for invalid paths, invalid commands, and timeout behavior.

## Phase 3: Expand Safely
1. Add `git_status_and_diff` (read-only).
2. Add `run_python_script` with explicit script allowlist.
3. Add optional `query_sqlite_readonly` with strict SQL validation.
4. Add caching for repeated web/model calls (small TTL cache).
5. Keep dangerous operations behind user confirmation.

## Phase 4: Production Readiness
1. Add startup script for server + health check.
2. Add docs for setup, troubleshooting, and expected workflows.
3. Add metrics report: tool latency, tool success rate, cloud-token reduction estimate.
4. Add fallback behavior when LM Studio is unavailable.

## Definition of Done
- Cursor auto-discovers the local server and can call tools in chat/agent mode.
- `run_command` cannot execute unsafe commands.
- LM Studio calls work consistently on local endpoint.
- Test script passes and includes failure-path checks.
- Docs are sufficient for reinstall/setup in under 10 minutes.
