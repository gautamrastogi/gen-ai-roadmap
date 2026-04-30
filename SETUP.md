# 🛠️ Environment Setup Guide
> GenAI Roadmap — M1 Mac (Apple Silicon) Edition

## Hardware
- **Mac**: Apple M1 Max, 32GB unified memory
- **Capability**: Runs 7B–30B models locally at production speed

---

## Prerequisites (Already Installed)
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

## Step 4: Set Up Ollama (Already Installed, No Models)

```bash
# Start Ollama server
ollama serve

# Pull models (choose based on task)
ollama pull qwen3:14b           # Best everyday model (~9GB)
ollama pull qwen2.5-coder:14b   # Best for coding tasks (~9GB)
ollama pull deepseek-r1:14b     # Reasoning / chain-of-thought (~9GB)
ollama pull phi4:latest         # Tiny but capable (~5GB)
ollama pull llava:13b           # Vision + language (~8GB)

# List pulled models
ollama list

# Test it
ollama run qwen3:14b "What is RAG in AI?"
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

## Step 6: Create .env File

```bash
cat > .env << 'EOF'
# OpenAI
OPENAI_API_KEY=sk-your-key-here
OPENAI_ORG_ID=org-your-org-here

# Anthropic (optional)
ANTHROPIC_API_KEY=sk-ant-your-key

# LangSmith (Phase 5)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=lsv2_your-key
LANGCHAIN_PROJECT=genai-roadmap

# Local models (no key needed — just the URL)
OLLAMA_BASE_URL=http://localhost:11434/v1
EOF
```

> ⚠️ Add `.env` to `.gitignore` — never commit API keys!

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
| Everyday chat | Qwen3 14B | `ollama run qwen3:14b` |
| Coding | Qwen2.5-Coder 14B | `ollama run qwen2.5-coder:14b` |
| Reasoning | DeepSeek-R1 14B | `ollama run deepseek-r1:14b` |
| Vision | LLaVA 13B | `ollama run llava:13b` |
| Max quality (slow) | Qwen3 30B | `ollama run qwen3:30b` |
| Smallest/fastest | Phi-4 Mini | `ollama run phi4-mini:latest` |

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
    model="qwen3:14b",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)
```
