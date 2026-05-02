# Local Agent MCP Server + Roadmap Coach

This folder contains a local MCP server and a small LLM-backed roadmap coach:

- Cloud assistants can use MCP tools for local files, commands, git, web search, and model calls.
- `roadmap_coach.py` helps answer "What should I do next?" for this roadmap.
- LM Studio or Ollama can provide local OpenAI-compatible model inference.

## What You Built

`mcp_server.py` now includes:

- safe file tools: `write_file`, `read_file`
- guarded command tool: `run_command` (allowlist + no `shell=True`)
- git insight tool: `git_status_and_diff`
- roadmap coach tools: `roadmap_status`, `roadmap_next_task`, `roadmap_phase_details`
- web search tool: `web_search` (URL encoding + retries)
- local model tool: `call_local_model` (OpenAI-compatible local API)
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

### 1) Start or verify a local model

LM Studio:

```bash
./ensure_local_model.sh lmstudio
```

Ollama:

```bash
LOCAL_MODEL_NAME=qwen3 ./ensure_local_model.sh ollama
```

### 2) Ask the roadmap coach

The default `next` command uses the local model when available:

```bash
python roadmap_coach.py next
```

Use deterministic mode when you explicitly do not want an LLM call:

```bash
python roadmap_coach.py next --no-llm
```

### 3) Run checks

**macOS/Linux:**
```bash
./run_checks.sh
```

**Windows:**
```cmd
run_checks.bat
```

### 4) Start local MCP server manually

**macOS/Linux:**
```bash
./start_local_agent.sh
```

**Windows:**
```cmd
start_local_agent.bat
```

### 5) Verify in Cursor

Try prompts like:

- `Run health_check from local-agent and summarize issues.`
- `Use git_status_and_diff and summarize current changes.`
- `Use roadmap_next_task and tell me what to do next.`
- `Use call_local_model to summarize genai-roadmap.md into 5 bullets.`

## Roadmap Coach V1

The tiny roadmap coach is intentionally read-only. It gathers deterministic repo facts, sends a compact prompt to your local model, and falls back to deterministic output if the model is unavailable.

```bash
python roadmap_coach.py status
python roadmap_coach.py next          # local-model backed
python roadmap_coach.py next --no-llm # deterministic fallback only
python roadmap_coach.py phase --id 2
python roadmap_coach.py init --print-template
```

For personalized progress, create a local gitignored copy:

```bash
cp roadmap-progress.example.json roadmap-progress.local.json
```

## Local Model Requirements

The local model is optional for low-level deterministic tools, but the roadmap coach uses it by default for the richer `next` response.

Supported first-class local providers:

| Provider | Base URL | Example model |
|---|---|---|
| LM Studio | `http://127.0.0.1:1234` | `qwen/qwen3.5-9b` |
| Ollama | `http://127.0.0.1:11434/v1` | `qwen3` |

Use the generic helper:

```bash
./ensure_local_model.sh lmstudio
./ensure_local_model.sh ollama
```

Configure the provider with OpenAI-compatible environment variables:

```bash
export LOCAL_MODEL_BASE_URL="http://127.0.0.1:1234"      # LM Studio
export LOCAL_MODEL_NAME="qwen/qwen3.5-9b"

# or Ollama
export LOCAL_MODEL_BASE_URL="http://127.0.0.1:11434/v1"
export LOCAL_MODEL_NAME="qwen3"

local-agent/start_local_agent.sh
```

`./ensure_lm_studio.sh` is kept as an LM Studio-specific convenience wrapper.

## Known Notes

- `web_search` may fail in restricted environments where outbound web requests are blocked.
- Editor lints may show unresolved `mcp.server.*` imports even when runtime works in your venv.

## Daily Workflow

1. Keep LM Studio or Ollama running.
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
