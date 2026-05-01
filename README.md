# 🚀 GenAI Developer Roadmap 2026

> A structured, project-driven learning path for building production-grade Generative AI applications — from Python fundamentals through multi-agent orchestration, local model inference, and cloud certification.

[![GitHub Pages](https://img.shields.io/badge/Dashboard-Live-8b5cf6?style=flat-square&logo=github)](https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/)
[![Phases](https://img.shields.io/badge/Phases-12-ec4899?style=flat-square)](#roadmap-structure)
[![Projects](https://img.shields.io/badge/Projects-39-10b981?style=flat-square)](#roadmap-structure)
[![Courses](https://img.shields.io/badge/Courses-86+-3b82f6?style=flat-square)](#roadmap-structure)

---

## 📊 Interactive Dashboard

**[→ Open Dashboard](https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/)**

**Zenith demo pages:**

- [Master Dashboard](https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/docs/zenith-master-dashboard.html)
- [Advanced Curriculum](https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/docs/zenith-advanced-curriculum.html)

The dashboard is a fully client-side web app (no backend, no login) that lets you:

- ✅ Track progress per project and per course resource
- ⏱️ See estimated time remaining per phase and overall
- 📈 Watch your mastery percentage grow as you complete items
- ☁️ Sync progress across devices via a private GitHub Gist
- 🌙 Switch between dark and light themes
- 📤 Export / import progress as JSON backup

> **Tech stack:** Pure HTML + CSS + Vanilla JS — zero dependencies, zero build step.  
> **Data layer:** `localStorage` (primary) + GitHub Gist API (cloud sync, optional).

---

## 🗺️ Roadmap Structure

| Phase | Name | Projects | Est. Time |
|-------|------|----------|-----------|
| 0 | Software Baseline | 1 | ~2h |
| 1 | Foundations | 3 | ~15h |
| 2 | Python LLM Apps | 4 | ~20h |
| 3 | Embeddings & RAG | 5 | ~15h |
| 4 | Tool Calling & Workflows | 4 | ~12h |
| 5 | Evals & Observability | 5 | ~10h |
| 6 | MCP & Agentic Orchestration | 7 | ~20h |
| 7 | AI-Native Dev Productivity | 2 | ~6h |
| 8 | Multimodal, Real-Time & SLMs | 3 | ~12h |
| 9 | Portfolio & Job Prep | 1 | ~8h |
| 10 | Certification | 1 | ~15h |
| 11 | Capstone Projects | 3 | ~30h |

**Total: ~165 hours of structured learning + project building**

---

## 📚 Learning Resources

Curated resources from:
- **Pluralsight** — Structured video courses (paid)
- **DeepLearning.AI** — Short courses on cutting-edge topics (mostly free)
- **QA Platform** — Certification exam prep
- **Official Docs** — OpenAI, LangChain, LangGraph, MCP, Hugging Face, Anthropic

---

## ☁️ Cross-Device Sync Setup

The dashboard supports syncing your progress to a private GitHub Gist so it persists across browsers and devices.

**One-time setup:**
1. Go to [github.com/settings/tokens](https://github.com/settings/tokens) → **Tokens (classic)**
2. Generate a new token with only the **`gist`** scope → copy it
3. Open the dashboard → click **☁ Gist Sync** → paste the token
4. Leave Gist ID blank on first device (it auto-creates) — paste the returned ID on subsequent devices
5. Click **Save & Sync**

> The token is stored only in your browser's `localStorage`. It is never committed to this repository or sent anywhere other than the GitHub API.

---

## 🛠️ Setup

First, configure the repository for your personal use:

```bash
# Run the setup script to personalize URLs and create config files
./setup.sh
```

This will:
- Replace `YOUR_USERNAME` and `YOUR_REPO_NAME` placeholders with your GitHub details
- Create `config.env` from template for API keys
- Create `.cursor/mcp.json` for Cursor MCP integration
- Update all documentation with your information

## 🛠️ Local Development

```bash
# Clone
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd gen-ai-roadmap

# Serve locally (any static file server works)
npx serve docs/
# or
python3 -m http.server 8080 --directory docs/
```

Then open `http://localhost:8080`.

---

## 🤖 Local AI Setup (M1/M2/M3 Mac)

This roadmap is optimized for Apple Silicon. Recommended local model setup:

| Tool | Purpose |
|------|---------|
| [LM Studio](https://lmstudio.ai/) | GUI for running local LLMs (Llama, Mistral, Phi) |
| [Ollama](https://ollama.com/) | CLI-driven local model server |
| [MLX](https://github.com/ml-explore/mlx-examples) | Apple Silicon optimized fine-tuning |

**Recommended local models (runs well on M1 Max — updated April 2026):**
- `qwen3:14b` — ⭐ best everyday model: fast, smart, hybrid thinking/non-thinking modes, native MCP support
- `qwen3:30b-a3b` — ⭐ reasoning sweet spot: MoE architecture (only 3B active params), best quality/speed on 32GB
- `qwen2.5-coder:14b` — best dedicated coding model
- `deepseek-r1:14b` — reasoning model with transparent chain-of-thought logs
- `llava:13b` — vision/multimodal tasks

---

## 📁 Repository Structure

```
gen-ai-roadmap/
├── docs/
│   ├── index.html                      # Dashboard (single-file app, deployed to GitHub Pages)
│   ├── zenith-master-dashboard.html    # Zenith master dashboard demo
│   └── zenith-advanced-curriculum.html # Zenith advanced curriculum demo
├── projects/
│   ├── local-agent/            # FastMCP local Python MCP server
│   ├── p0-genai-starter-template/  # Phase 0: FastAPI + Pydantic starter template
│   ├── p1-prompt-playground/   # Phase 1: Prompt strategy comparison app
│   ├── p2-summarizer/          # Phase 1: FastAPI summarization service
│   └── p3-rewriter/            # Phase 1: Tone/style rewriter service
├── genai-roadmap.md            # Full roadmap content (source of truth)
├── .env                        # Local secrets (gitignored)
├── .gitignore
└── README.md
```

---

## 🔧 MCP Local Agent

The `projects/local-agent/` folder contains a **FastMCP Python server** that runs locally and provides deterministic execution tools to cloud AI assistants (Cursor, GitHub Copilot, Antigravity).

### Available Tools

| Tool | Description |
|------|-------------|
| `run_python` | Execute Python code in a sandboxed subprocess |
| `shell` | Run shell commands with output capture |
| `read_file` / `write_file` | Safe file I/O |
| `list_dir` | Directory listing |
| `lm_studio_chat` | Route prompts to a local LM Studio model |
| `search_web` | DuckDuckGo search without API key |

See `projects/local-agent/README.md` for setup instructions.

---

## 🎯 Philosophy

- **Build first, learn second** — every phase culminates in a real, deployable project
- **Local-first** — run models on your own hardware before paying for APIs
- **Agentic from day one** — tool-use, memory, and MCP show up early and throughout
- **Production mindset** — evals, observability, and security are first-class citizens

---

## � Cross-Device Usage

This roadmap supports seamless development across multiple devices:

### Progress Sync (GitHub Gist)
- Dashboard progress automatically syncs via private GitHub Gist
- Works across Mac, Windows, Linux devices
- No manual export/import needed

### Environment Setup
- **macOS/Linux**: Use `./setup.sh` and standard Python venv
- **Windows**: Use `setup.bat` (create from `setup.sh` template) and `python -m venv .venv`
- All scripts are designed to work on both Unix and Windows

### Local Agent Compatibility
- MCP server runs on all platforms (Python 3.8+)
- LM Studio available for macOS, Windows, Linux
- Cursor IDE supports MCP on all platforms

### Configuration
- `config.env` contains all environment-specific settings
- `.cursor/mcp.json` configures Cursor MCP integration
- Both are gitignored for personal customization

---

## �📝 License

MIT — use this roadmap however you like. If you find it useful, ⭐ the repo!
