# Prompt Templates for Automatic Local Delegation

Use these templates when you want predictable tool behavior.

## 1) Daily coding request

`Handle this task end-to-end. Use local MCP tools by default for file edits, shell commands, git checks, and local model calls. Only use cloud reasoning for planning/explanations.`

## 2) Debugging flow

`Debug this issue and verify the fix. Prefer local MCP execution for all deterministic steps, run health_check first, then run relevant commands/tests, and summarize root cause + fix.`

## 3) Refactor flow

`Refactor this safely. Use local MCP for reading/writing files and running checks. Keep changes minimal and run local-agent/run_checks.sh before finalizing.`

## 4) Fast review

`Review the current changes with local MCP git_status_and_diff, identify risks, and suggest fixes in priority order.`

## 5) Local model assist

`Use call_local_model to generate a concise answer, then verify against project files before final response.`

---

Because project hooks and rules are now configured, you should not need to explicitly mention local-agent in every prompt. These templates are optional for extra control.
