# P4 - CLI Chatbot

Stateful terminal chatbot with:

- streaming assistant responses
- local JSON session memory
- personas
- slash commands
- transcript/session export
- estimated token tracking
- OpenAI-compatible provider support: LM Studio, Ollama, HuggingFace router, GitHub Models, or OpenAI

## Quickstart

```bash
make install
make test

# Easiest local path
ollama pull qwen2.5:1.5b
make run-ollama
```

For LM Studio, OpenAI, HuggingFace Router, or GitHub Models:

```bash
cp .env.example .env
# Edit .env for your provider:
# - LM Studio: OPENAI_BASE_URL=http://127.0.0.1:1234/v1 and OPENAI_API_KEY=local-model
# - Hosted:    set HF_TOKEN, GITHUB_TOKEN, or OPENAI_API_KEY

make run
```

## Usage

```bash
python -m src.main
python -m src.main --persona senior-engineer
python -m src.main --session sessions/roadmap.json
python -m src.main --base-url http://127.0.0.1:11434/v1 --model qwen2.5:1.5b
python -m src.main --base-url http://127.0.0.1:1234/v1 --model local-model
python -m src.main --temperature 0.4 --max-tokens 500
```

## Slash Commands

| Command | Description |
|---|---|
| `/help` | Show commands |
| `/personas` | List personas |
| `/persona NAME` | Switch persona for future turns |
| `/stats` | Show token/session stats |
| `/undo` | Remove the last user/assistant turn |
| `/clear` | Clear this session |
| `/save [PATH]` | Save session JSON |
| `/export [PATH]` | Export transcript/session JSON |
| `/exit` | Save and quit |

## Personas

| Persona | Use Case |
|---|---|
| `default` | Balanced, practical assistant |
| `senior-engineer` | Implementation, tradeoffs, design review |
| `socratic` | Learning through guided questions |
| `concise` | Short answers with minimal ceremony |

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `OPENAI_BASE_URL` | Local/custom providers | OpenAI-compatible endpoint, e.g. LM Studio or Ollama |
| `OPENAI_API_KEY` | OpenAI direct, or dummy for local | API key |
| `HF_TOKEN` | Alt provider | HuggingFace router token |
| `GITHUB_TOKEN` | Alt provider | GitHub Models token |
| `MODEL` | No | Model name |
| `TEMPERATURE` | No | Sampling temperature |
| `MAX_TOKENS` | No | Max completion tokens |
| `SESSION_PATH` | No | Default session file path |

## Notes

- Session files are local runtime state. Keep them out of git if they contain personal or sensitive prompts.
- Token counts are estimates so the tool works with local models and OpenAI-compatible providers without adding a tokenizer dependency.
- This project uses Chat Completions because it is the most widely supported interface across local OpenAI-compatible servers.
