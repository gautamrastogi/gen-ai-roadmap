# 🛠️ Environment Setup Guide
> GenAI Roadmap — M1 Mac (Apple Silicon) Edition

## Hardware
- **Mac**: Apple M1 Max, 32GB unified memory
- **Capability**: Runs 7B–30B models locally at production speed

---

## Reference Environment

These versions describe the machine this roadmap was built on. Exact patch versions are not required.
- ✅ Homebrew 5.1.7
- ✅ pyenv (Python version manager)
- ✅ Python 3.14.4 (global default)
- ✅ uv 0.11.7 (fast package installer)
- ✅ Docker 29.4.0
- ✅ Git 2.54.0
- ✅ Node.js v25.9.0
- ✅ Ollama.app + LM Studio.app
- ✅ GitHub CLI (`gh`)
- ✅ ffmpeg

---

## Step 1: Python Environment Strategy

> **Important:** Python 3.14 version is too new for MLX and some ML packages.
> Use **3.14 for API/web projects** and **3.12 for local model/ML projects**.

```bash
# Install Python 3.12 for ML work (Phase 8)
pyenv install 3.12.9

# Check available versions
pyenv versions
```

---

## Step 2: Project Virtual Environment

Most roadmap projects use their own `pyproject.toml` and `uv.lock`. Prefer per-project installs:

```bash
cd projects/p7-resume-vs-jd-analyzer
make install
make ci
```

Use the root virtual environment only for lightweight repo-level tooling.

```bash
cd ~/Documents/dev/gen\ ai\ roadmap

# Create venv (uses your current Python 3.14)
python -m venv .venv
source .venv/bin/activate

# Verify
which python
python --version
```

---

## Step 3: Install Packages by Phase

### Phase 2 — Python LLM App Development (Install Now)
```bash
pip install openai                    # OpenAI SDK (Responses API)
pip install fastapi uvicorn           # Web framework
pip install python-dotenv             # .env loading
pip install rich typer                # Beautiful CLI
pip install pydantic pydantic-settings httpx  # Already have, ensure latest
```

### Phase 3 — RAG (Install when starting Phase 3)
```bash
pip install langchain langchain-openai langchain-community
pip install chromadb                  # Local vector store
pip install sentence-transformers     # Open-source embeddings
pip install pypdf                     # PDF parsing
pip install tiktoken numpy            # Tokenization + math
pip install qdrant-client             # Production vector store
```

### Phase 5 — Evals & Observability
```bash
pip install deepeval                  # pytest-style LLM evals
pip install langsmith                 # LangChain tracing
pip install langfuse                  # Open-source observability
pip install dspy-ai                   # Programmatic prompt optimization
pip install litellm                   # Multi-LLM routing
```

### Phase 6 — Agents & MCP
```bash
pip install langgraph                 # Stateful agent graphs
pip install pydantic-ai               # Type-safe agents
pip install openai-agents             # OpenAI Agents SDK
pip install smolagents                # Code-first agent framework
pip install mcp                       # MCP Python SDK
pip install e2b-code-interpreter      # Sandboxed code execution for agents
```

### Phase 8 — Local Models & Fine-Tuning (Use Python 3.12!)
```bash
# Switch to 3.12 for this phase
pyenv local 3.12.9
python -m venv .venv-ml
source .venv-ml/bin/activate

pip install mlx-lm                    # Apple Silicon inference + fine-tuning
pip install huggingface-hub           # Model downloads from HF Hub
pip install datasets                  # HF datasets for fine-tuning data
```

---

## Step 4: Set Up Ollama Models

```bash
# Start Ollama server
ollama serve

# Pull the two roadmap models
ollama pull gemma4:latest
ollama pull nomic-embed-text-v2-moe:latest

# List pulled models
ollama list

# Test it
ollama run gemma4:latest "What is RAG in AI?"
```

---

## Step 5: Open WebUI (Local ChatGPT Interface)
> Uses your existing Docker installation.

```bash
docker run -d \
  -p 3000:8080 \
  --add-host=host.docker.internal:host-gateway \
  -v open-webui:/app/backend/data \
  --name open-webui \
  --restart always \
  ghcr.io/open-webui/open-webui:main
```

Then open: **http://localhost:3000**

Connect to Ollama: `http://host.docker.internal:11434`

---

## Step 6: Create Local Config Files

```bash
cp templates/config.env.template config.env
cp .env.example .env
```

Then edit only your local copies. Keep real API keys out of tracked files.

> `.env`, `config.env`, `.cursor/`, and project-level `.env` files are gitignored.

---

## Step 7: Useful Brew Additions

```bash
# Highly recommended
brew install jq          # JSON parsing in terminal
brew install graphviz    # Agent flow diagrams
brew install redis       # Session memory for agents

# Optional but helpful
brew install postgresql  # Local SQL for Phase 4 SQL assistant
```

---

## Verification Checklist

```bash
# Run this to verify your setup
python -c "import openai; print('openai OK')"
python -c "import fastapi; print('fastapi OK')"
ollama list                      # Should show pulled models
docker ps | grep open-webui      # Should show running container
curl http://localhost:3000       # Should return HTML
```

---

## Model Selection Quick Reference (32GB M1 Max)

| Task | Best Model | Command |
|------|-----------|---------|
| Chat, coding help, summaries, JSON prompting | Gemma 4 | `ollama run gemma4:latest` |
| Vision/image reasoning | Gemma 4 | `ollama run gemma4:latest` |
| Embeddings, semantic search, RAG retrieval | Nomic Embed Text v2 MoE | `ollama pull nomic-embed-text-v2-moe:latest` |
| Bigger experiments only | Check Ollama library first | https://ollama.com/library |

---

## Connect Local Model to Python (Drop-in for OpenAI)

```python
from openai import OpenAI

# Ollama — same code as OpenAI, different base_url
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)

response = client.chat.completions.create(
    model="gemma4:latest",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)
```
