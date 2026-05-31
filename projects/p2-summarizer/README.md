# P2 — Summarizer

Paste or pipe any long text and get three views back: a concise paragraph, 5 key bullet points, and a list of action items — all from a single HuggingFace-hosted LLM call per format.

## Quickstart

```bash
cp .env.example .env
# Edit .env: set HF_TOKEN=<your token>

make install   # uv sync
make test      # pytest
make run       # python -m src.main --file sample.txt (all three formats)
```

## Usage

| Command | Description |
|---|---|
| `make run` | Summarise `sample.txt` in all three formats |
| `make test` | Run all unit tests |
| `make lint` | Ruff + pyright |
| `make ci` | lint + test |

### CLI flags

```
python -m src.main --text "Your text here"
python -m src.main --file path/to/file.txt
python -m src.main --file doc.txt --format summary
python -m src.main --file doc.txt --format bullets
python -m src.main --file doc.txt --format action_items
python -m src.main --file doc.txt --model Qwen/Qwen2.5-7B-Instruct --temperature 0.1
```

## Output formats

| Format | Description |
|---|---|
| `summary` | Single prose paragraph (3-5 sentences) |
| `bullets` | Exactly 5 `• ` bullet points |
| `action_items` | Numbered list of concrete tasks |

## Environment variables

| Variable | Required | Description |
|---|---|---|
| `HF_TOKEN` | Yes (or `OPENAI_API_KEY`) | HuggingFace API token |
| `OPENAI_API_KEY` | Alt to HF_TOKEN | OpenAI key (uses openai.com endpoint) |
| `MODEL` | No | Override model name |
| `TEMPERATURE` | No | Sampling temperature (default `0.3`) |
| `MAX_TOKENS` | No | Max tokens per response (default `512`) |
