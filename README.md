# GenAI Roadmap for a Python Developer (2026)

> A structured, project-driven roadmap to transition from Python Software Engineer to **GenAI / LLM Application Engineer** — covering foundations through agentic systems, MCP, evals, security, and capstone deployments.

[![Last Updated](https://img.shields.io/badge/updated-April%202026-blue)](./genai-roadmap.md)
[![Stack](https://img.shields.io/badge/stack-Python%20%7C%20OpenAI%20%7C%20LangGraph%20%7C%20MCP-8b5cf6)](./genai-roadmap.md)
[![License](https://img.shields.io/badge/license-MIT-green)](#)

---

## 📖 The Roadmap

See [`genai-roadmap.md`](./genai-roadmap.md) for the full learning path — **10 phases, 29+ projects, 12-week fast-track plan, and a step-by-step action checklist.**

### Roadmap at a Glance

| Phase | Focus | Key Skills |
|-------|-------|-----------|
| 1 | GenAI Fundamentals | Prompting, tokens, LLM basics |
| 2 | Python LLM Dev | OpenAI API, Responses API, structured outputs, reasoning models |
| 3 | Embeddings & RAG | Vector DBs, Chroma, hybrid search, RAG pipelines |
| 4 | Tool Calling & Workflows | Function calling, agents SDK, tool schemas |
| 5 | Evals, Security & CI/CD | EDD, OWASP LLM Top 10, GitHub Actions, LangSmith |
| 6 | MCP + Agentic Orchestration | MCP, A2A protocol, LangGraph, HITL, persistence |
| 7 | AI-Native Dev Productivity | Copilot, local models (Ollama/LM Studio), dev agents |
| 8 | Portfolio & Job Prep | GitHub profile, READMEs, demos, architecture diagrams |
| 9 | Certifications | Azure AI-900/AI-901, AWS AIF-C01 |
| 10 | Capstone Projects | Unified AI Assistant, Multi-Agent Research Platform, Personal Copilot |

---

## 🗂 Repository Structure

```
gen-ai-roadmap/
├── genai-roadmap.md           # Main roadmap — phases, projects, step-by-step plan
├── README.md                  # This file
├── .gitignore
└── projects/
    ├── dashboard/             # Progress tracker dashboard (Python HTTP server + HTML)
    │   ├── app.py             # Backend: HTTP server + SQLite API
    │   ├── dashboard.html     # Frontend: dark-mode, glassmorphism UI
    │   ├── start_dashboard.command    # macOS double-click launcher
    │   └── install_launch_agent.sh   # Auto-start on login (macOS LaunchAgent)
    └── local-agent/           # Local Python MCP server for AI tool execution
        ├── mcp_server.py      # FastMCP server exposing shell/file/git tools
        ├── requirements.txt
        └── README.md
```

---

## 📊 Progress Dashboard

A self-hosted progress tracker — no cloud dependencies, runs locally.

**Start the dashboard:**

```bash
cd projects/dashboard
python app.py --open-browser
```

Opens at `http://127.0.0.1:8765` — click any checklist item to mark it complete. Progress is persisted in SQLite (`~/Library/Application Support/GenAIRoadmapDashboard/tracker.db`).

**Auto-start on macOS login:**

```bash
cd projects/dashboard
bash install_launch_agent.sh
```

---

## 🤖 Local Agent MCP Server

A [Model Context Protocol](https://modelcontextprotocol.io) server that gives AI assistants (Antigravity, Cursor, Claude Desktop) safe, local tool access:

- Shell command execution (scoped to workspace)
- File read/write operations
- Git status/diff/log tools
- Roadmap tracker integration

**Start the local agent:**

```bash
cd projects/local-agent
source .venv/bin/activate
python mcp_server.py
```

---

## 🛠 Tech Stack

| Layer | Tools |
|-------|-------|
| Language | Python 3.12+ |
| LLM APIs | OpenAI (Responses API), Anthropic Claude, Azure OpenAI |
| Local Models | Ollama, LM Studio |
| Agents | LangGraph, OpenAI Agents SDK, CrewAI |
| RAG | Chroma, FAISS, pgvector |
| MCP | Python MCP SDK (FastMCP), A2A Protocol |
| Evals | DeepEval, LangSmith, Arize Phoenix |
| Infra | Docker, GitHub Actions, Railway/Render |
| Dashboard | Python HTTP server, Vanilla HTML/CSS/JS, SQLite |

---

## 2026 GenAI Industry Trends Covered

| Trend | Phase |
|-------|-------|
| Agentic Systems (LangGraph, CrewAI, OpenAI Agents SDK) | 6 |
| Model Context Protocol (MCP) | 6 |
| A2A Agent-to-Agent Protocol | 6 |
| Reasoning Models (o1/o3, DeepSeek-R1) | 2 |
| Evals-as-Code (EDD) | 5 |
| AI Security & OWASP LLM Top 10 | 5 |
| CI/CD for AI Apps | 5 |
| Multimodal (Vision, Audio, Video) | 10 |
| Local Models (Ollama, LM Studio) | 2, 7 |

---

## 🚀 Getting Started

1. Read [`genai-roadmap.md`](./genai-roadmap.md) — start at **Step 1** in the action plan
2. Launch the dashboard to track your progress
3. Work through each phase in order — each phase builds on the previous
4. Build the projects — they are the portfolio, not the courses

---

*Maintained with Antigravity AI (Google DeepMind). Contributions welcome.*
