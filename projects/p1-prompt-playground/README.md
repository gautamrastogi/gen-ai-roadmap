# P1 — Prompt Playground

Compare four prompt strategies on any task — zero-shot, few-shot, system-role, and chain-of-thought — side by side in the terminal.

**Corporate networks:** uses HuggingFace Inference API (`router.huggingface.co`) — not blocked by corporate firewalls. Free tier, no OpenAI account needed.

## Quickstart

```bash
# 1. Copy env file and add your HuggingFace token
cp .env.example .env
# edit .env: set HF_TOKEN=hf_...
# Get one free at: huggingface.co/settings/tokens (no scopes needed)

# 2. Install dependencies
make install

# 3. Run a single strategy (saves rate-limit quota)
uv run python -m src.main --task "What is RAG?" --strategy zero_shot

# 4. Run all 4 strategies for side-by-side comparison
uv run python -m src.main --task "What is RAG?"
```

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--task` | required | Your question or task — plain text, nothing else needed |
| `--strategy` | all 4 | Run just one strategy: `zero_shot`, `few_shot`, `system_role`, `chain_of_thought` |
| `--model` | `Qwen/Qwen2.5-7B-Instruct` | Override model (HF org/name format) |
| `--temperature` | `0.7` | Sampling temperature (0 = deterministic, 1 = creative) |

## How it works

You provide **plain text only** — no examples, no formatting. Each strategy wraps your input differently before sending it to the model:

| Strategy | What it does to your input |
|----------|----------------------------|
| **zero_shot** | Sends it bare: `User: <your task>` — no guidance at all |
| **few_shot** | Prepends 2 hardcoded worked examples (neural net + gradient descent Q&A), then your task. The model mirrors the style of those examples |
| **system_role** | Adds a system message: *"You are a concise technical educator. Answer in exactly 3 sentences."* — constrains the format |
| **chain_of_thought** | Adds *"Think step by step"* system message + appends *"Walk through your reasoning..."* to your task — forces explicit reasoning |

The **few-shot examples are static** (hardcoded in `src/strategies.py`). The point is to observe how pre-seeding a conversation with examples shifts the model's tone and structure — not to generate examples dynamically (that comes in a later project).

## What to observe

- Does **zero-shot** ramble? Does **system-role** stay disciplined to 3 sentences?
- Does **few-shot** inherit the concise bullet style of the examples?
- Does **chain-of-thought** give longer, more structured reasoning?
- Try `--temperature 0.0` for deterministic answers vs `1.0` for creative ones

## Rate limits (HuggingFace free tier)

The quota line at the end of each run shows your remaining budget:

```
Quota: 198/100 requests remaining  |  33,333/33,333 tokens remaining  |  resets in 2s
```

- **Burst limit:** 2 requests per ~2s — `run_all` auto-paces with 1.5s gaps between strategies
- **Use `--strategy`** to burn 1 API call instead of 4 when you only need one result
- **`max_tokens` default is 256** — lower = faster + fewer tokens used; override with `OPENAI_MODEL` in `.env`

## Tests

```bash
make test    # unit tests only (no API calls)
make ci      # full: lint + type + test
```
