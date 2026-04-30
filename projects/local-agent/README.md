# Local Agent MCP Server

This folder contains your local MCP server for a hybrid coding assistant:

- cloud model for planning/reasoning
- local MCP tools for deterministic execution
- LM Studio for local model inference

## What You Built

`mcp_server.py` now includes:

- safe file tools: `write_file`, `read_file`
- guarded command tool: `run_command` (allowlist + no `shell=True`)
- git insight tool: `git_status_and_diff`
- web search tool: `web_search` (URL encoding + retries)
- local model tool: `call_local_model` (LM Studio OpenAI-compatible API)
- diagnostics tool: `health_check`
- capability map tool: `list_tool_capabilities`
- structured JSON responses (`ok`, `request_id`, payload/error)
- request-level logging to `local-agent/logs/mcp_server.log`
- basic sensitive-value redaction in logs

## Cursor Integration

Project config is in `.cursor/mcp.json` and wires:

- `local-agent` (this Python MCP server)
- `filesystem-readonly` (official MCP server)
- `playwright` MCP server

After updates to `.cursor/mcp.json`, restart Cursor.

Project hooks are in `.cursor/hooks.json`:

- `preToolUse` hook provides MCP-first behavior with a safe default:
  - soft guidance for `Read`
  - hard block for built-in `Delete`
- Hook script: `.cursor/hooks/prefer-local-mcp.py`
- Toggle script: `.cursor/hooks/toggle-local-mcp-policy.sh`

Policy control:

```bash
.cursor/hooks/toggle-local-mcp-policy.sh status
.cursor/hooks/toggle-local-mcp-policy.sh off
.cursor/hooks/toggle-local-mcp-policy.sh on
```

## Quick Start

### 1) Run checks

**macOS/Linux:**
```bash
./run_checks.sh
```

**Windows:**
```cmd
run_checks.bat
```

### 2) Start local MCP server manually

**macOS/Linux:**
```bash
./start_local_agent.sh
```

**Windows:**
```cmd
start_local_agent.bat
```

### 3) Verify in Cursor

Try prompts like:

- `Run health_check from local-agent and summarize issues.`
- `Use git_status_and_diff and summarize current changes.`
- `Use call_local_model to summarize genai-roadmap.md into 5 bullets.`

## LM Studio Requirements

- LM Studio running at `http://127.0.0.1:1234`
- at least one loaded model (you already have `qwen/qwen3.5-9b`)

If needed, override base URL before startup:

```bash
export LM_STUDIO_BASE_URL="http://127.0.0.1:1234"
local-agent/start_local_agent.sh
```

## Known Notes

- `web_search` may fail in restricted environments where outbound web requests are blocked.
- Editor lints may show unresolved `mcp.server.*` imports even when runtime works in your venv.

## Daily Workflow

1. Keep LM Studio running.
2. Use Cursor agent/chat with local MCP tools.
3. Run `local-agent/run_checks.sh` after server changes.
4. Review `local-agent/logs/mcp_server.log` for request traces.

## Token Savings Tracking

Exact cloud-token savings depend on model/provider telemetry, but this setup typically reduces cloud usage because file/shell/git/web work runs locally.

Practical estimate bands for coding workflows:

- light delegation: 15-30% cloud token reduction
- medium delegation: 30-55% reduction
- heavy delegation (tool-heavy sessions): 50-70% reduction

How to measure in your workflow:

1. Baseline 20 tasks without local MCP delegation.
2. Repeat similar 20 tasks with this setup.
3. Compare cloud token counters from your provider/Cursor billing page.
4. Savings formula:

`savings_percent = (baseline_tokens - hybrid_tokens) / baseline_tokens * 100`

Use `local-agent/TOKEN_SAVINGS_TRACKER.csv` to log each baseline vs hybrid task pair.

Generate a quick report:

```bash
local-agent/.venv/bin/python local-agent/report_token_savings.py
```
