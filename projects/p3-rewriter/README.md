# P3 — Rewriter

Take any text and instantly rewrite it in four tones: professional, concise, technical, and friendly — one API call per tone, all from the CLI.

## Quickstart

```bash
cp .env.example .env
# Edit .env: set HF_TOKEN=<your token>

make install   # uv sync
make test      # pytest
make run       # python -m src.main --file sample.txt (all four tones)
```

## Usage

| Command | Description |
|---|---|
| `make run` | Rewrite `sample.txt` in all four tones |
| `make test` | Run all unit tests |
| `make lint` | Ruff + pyright |
| `make ci` | lint + test |

### CLI flags

```
python -m src.main --text "Your text here"
python -m src.main --file path/to/file.txt
python -m src.main --file draft.txt --tone professional
python -m src.main --file draft.txt --tone concise
python -m src.main --file draft.txt --tone technical
python -m src.main --file draft.txt --tone friendly
python -m src.main --file draft.txt --model Qwen/Qwen2.5-7B-Instruct --temperature 0.2
```

## Output tones

| Tone | Description |
|---|---|
| `professional` | Formal, authoritative business language — no contractions, precise vocabulary |
| `concise` | Maximum information density — all filler removed, every key fact kept |
| `technical` | Domain-accurate terminology, active voice, logical structure |
| `friendly` | Warm, conversational, short sentences — like explaining to a colleague |

## Environment variables

| Variable | Required | Description |
|---|---|---|
| `HF_TOKEN` | Yes (or `OPENAI_API_KEY`) | HuggingFace API token |
| `OPENAI_API_KEY` | Alt to HF_TOKEN | OpenAI key (uses openai.com endpoint) |
| `MODEL` | No | Override model name |
| `TEMPERATURE` | No | Sampling temperature (default `0.4`) |
| `MAX_TOKENS` | No | Max tokens per response (default `512`) |
