# GenAI Developer Roadmap 2026

<!--
  CONTEXT FOR LLMs READING THIS FILE
  ===================================
  This is the primary roadmap document for a structured self-study program
  to transition from Python Software Engineer to GenAI / Agentic Systems Engineer,
  with a portfolio angle around enterprise workflow intelligence, platform automation, observability, and safe agentic systems.

  Owner:        gautamrastogi
  Hardware:     Apple Silicon Mac, 32 GB-class unified memory recommended
  OS:           macOS (Apple Silicon)
  Primary IDE:  VS Code/Cursor-compatible AI coding workflow
  Python:       3.14.4 (global), 3.12 (ML/MLX workloads)
  Package mgr:  uv + pip inside project .venv
  Local models: LM Studio (GUI) + Ollama (API), both installed
  Cloud models: OpenAI (GPT-4o, o3), Anthropic (Claude Sonnet)
  Repo:         https://github.com/gautamrastogi/gen-ai-roadmap
  Dashboard:    https://gautamrastogi.github.io/gen-ai-roadmap/

  HOW TO READ THIS FILE
  ─────────────────────
  • Phases 0–11 are sequential — do not skip ahead
  • Each phase has: Goal → Skills → Courses → Projects → Resources
  • Projects are the primary deliverables — each one should be a polished public project folder in this repo
  • "Learn" sections = theory to understand before building
  • Project Checklist = quick progress tracker
  • Phase Summary table = high-level status at a glance
  • Current focus is Phase 3 (Embeddings, Vector Search, and RAG)

  TECH STACK CONVENTIONS
  ──────────────────────
  • LLM SDK:         openai (Responses API + OpenAI-compatible Chat Completions — NOT Assistants API, deprecated Aug 2026)
  • Orchestration:   LangGraph (stateful graphs), PydanticAI (type-safe)
  • Evals:           DeepEval, LangSmith, Langfuse
  • Vector DB:       ChromaDB (local dev), Qdrant (production)
  • Embeddings:      text-embedding-3-small (OpenAI), or sentence-transformers (local)
  • Agents:          smolagents (code-first), LangGraph (stateful), OpenAI Agents SDK
  • Local inference: Ollama (API), LM Studio (GUI), MLX (peak Mac performance)
  • Local models:    Qwen3-14B (everyday), Qwen3-30B-A3B MoE (reasoning sweet spot), DeepSeek-R1-14B (reasoning)
  • Inference server: SGLang / vLLM (production), Ollama (dev)
  • AI coding agents: Gemini CLI (open-source, terminal), Cursor, Aider
  • Prompt opt:      DSPy (compiled prompts, replaces hand-tuning)
  • Multi-LLM:       LiteLLM (swap providers with one line)
  • Observability:   Arize Phoenix (open-source), LangSmith
  • CI/CD:           GitHub Actions with eval-gated deploys
  • Security:        OWASP LLM Top 10, prompt injection guards

  KEY DECISIONS
  ─────────────
  • Use OpenAI Responses API for hosted OpenAI projects; keep OpenAI-compatible Chat Completions adapters for Ollama/LM Studio/local-first work
  • Assistants API is sunset Aug 26, 2026 — do NOT build on it
  • Prefer code-first/type-safe frameworks (PydanticAI) over black-box wrappers
  • MCP (Model Context Protocol) is the standard tool integration layer
  • All projects should have evals and observability from day one
  • Security is integrated (OWASP LLM Top 10), not bolted on later
-->

> **Last updated:** 2026-05-17 | **Current phase:** Phase 3 — Embeddings + Vector Search + RAG
>
> Verified May 2026. Key changes: roadmap is now aligned to an AI backend/platform path for enterprise workflow intelligence, observability, and safe automation; inaccessible paid training was removed and replaced by Microsoft Learn free paths + DLAI; course lists trimmed to essentials only (build-first approach); every doc resource now has specific sections to read. Responses API is primary interface; Assistants API deprecated Aug 26, 2026.

## Goal
Transition from Python Software Engineer to:
- GenAI Engineer
- LLM Application Developer
- Applied AI Engineer
- AI Backend Engineer
- GenAI Platform Engineer
- Agentic Systems Engineer
- AI Workflow Automation Engineer
- AI for Observability / Operational Intelligence Engineer

## Target Career Lane
The roadmap is now intentionally aimed at the role shape that best matches the current background:

**Senior Backend / Platform Engineer → GenAI Platform Engineer for enterprise workflow intelligence.**

This means projects should not be random AI demos. They should increasingly look like safe, production-minded systems that can:
- triage workflow items such as alerts, tickets, change requests, bug reports, and support escalations
- search internal knowledge such as runbooks, support docs, API docs, architecture notes, and policies
- summarize evidence, timelines, decisions, and handoffs
- enrich work items with citations and suggested next actions
- integrate safely with tools through MCP, function calling, and HITL approval gates
- prove reliability through evals, snapshots, traces, and CI gates

Portfolio theme:
1. **RAG for enterprise knowledge**
2. **Tool calling for workflow automation**
3. **Agent orchestration with human approvals for critical actions**
4. **Production reliability: tracing, evals, regression tests, security, rollback**
5. **A capstone that feels like a workflow intelligence platform, not a toy chatbot**

## 2026 GenAI Industry Trends
> These are the high-signal topics the industry is actively hiring and building around in 2026. Prioritize them.

| Trend | Why It Matters | Covered In |
|-------|---------------|------------|
| **Agentic Systems** (LangGraph, CrewAI, PydanticAI) | The dominant engineering paradigm — agents planning and executing multi-step tasks autonomously | Phase 6 |
| **Model Context Protocol (MCP)** | Industry-standard "USB-C for AI" — standardizes how agents connect to tools, files, and databases | Phase 6 |
| **A2A (Agent-to-Agent Protocol)** | Google/Linux Foundation standard for agents collaborating cross-framework (LangGraph ↔ CrewAI ↔ ADK) | Phase 6 |
| **Reasoning-First Models** (o1/o3, DeepSeek-R1) | Chain-of-thought deliberation loops — know when to use expensive reasoning vs fast generalist models | Phase 2 |
| **GraphRAG & Knowledge Fabrics** | Moving beyond flat vector search to handle multi-hop reasoning and entity relationships | Phase 3 |
| **Enterprise Workflow Intelligence** | LLMs summarizing work items, docs, tickets, logs, changes, and service context for faster operational decisions | Phases 3-6, 11 |
| **Programmatic Prompting** (DSPy) | Replacing manual prompt engineering with compiled, metric-optimized prompt weights | Phase 5 |
| **Evals-as-Code (EDD)** | AI is non-deterministic — treat prompts like code with CI-integrated test suites (DeepEval, LangSmith) | Phase 5 |
| **AI Security & Prompt Injection** | OWASP LLM Top 10 — every production AI app needs guardrails | Phase 5 |
| **CI/CD for AI Apps** | Automated eval pipelines on every PR, LLM-as-a-Judge regression checks | Phase 5 |
| **Multimodal** (Vision, Audio, Video) | GPT-4o vision, Whisper STT, TTS — first-class in capstone projects | Phase 8 |
| **Local Models** (Ollama, LM Studio, llama.cpp) | Cost/privacy/air-gap — know when open-weights beats hosted | Phases 2, 7 |
| **Qwen3 & Hybrid Reasoning** | New open-weights SOTA: switchable thinking/non-thinking modes per prompt, native MCP support, 128K context, Apache 2.0 — replaces Qwen2.5 as default local recommendation | Phases 2, 7 |
| **Vibe Coding & Spec-Driven Dev** | Write clear specs / prompts → let coding agents (Gemini CLI, Cursor, Aider) generate and iterate — shift from line-by-line coding to intent-driven engineering | Phase 7 |
| **Sandboxed Code Execution** (E2B) | Agents that safely write and run code in isolated cloud sandboxes — mandatory for any autonomous coding agent | Phase 6 |

## What gets you hired after this roadmap:
1. 2-3 polished GitHub repos that work end-to-end (not half-finished)
2. One live deployed app (not just localhost) with a real URL
3. Can explain your RAG architecture, chunking strategy, evaluation approach
4. Can build and expose a tool/function-calling flow from scratch
5. Understands agents, state, HITL — can talk about tradeoffs

**What this roadmap does NOT teach (and that's fine):**
- Pre-training / fine-tuning large models from scratch (that's ML research, not applied AI engineering)
- Deep ML maths (not needed for most GenAI roles)
- Deep Kubernetes/SRE administration from scratch. You already have platform exposure; this roadmap uses that experience as domain leverage rather than turning into a pure infra syllabus.

**Bottom line:** Complete Phases 1–8, have 3 public repos, and you will pass screening for applied AI/GenAI engineer roles at top tech companies.

## Core principle
Do not optimize for certificates first.
Optimize for:
1. foundations
2. Python LLM app development
3. RAG systems
4. tool calling and workflow automation
5. evals, safety, observability, production reliability
6. MCP + agentic orchestration
7. strong portfolio
8. one certificate only if useful

---

# PROGRESS TRACKER
> Last updated: 2026-05-17

## Current Focus
**Phase:** Phase 3 — Embeddings + Vector Search + RAG
**Working on:** Project 8 — Semantic Search Prototype
**Status:** 🟡 In Progress — start embeddings and retrieval projects

## ⚡ Next Action — Do This Now
1. ✅ ~~Generative AI Foundations~~ — DONE
2. ✅ ~~Prompt Engineering & Generative AI~~ — DONE
3. ✅ ~~Large Language Models (LLM)~~ — DONE
4. ✅ ~~Intro to Generative AI~~ — DONE
5. ✅ ~~ChatGPT Prompt Engineering for Developers~~ — DONE
6. ✅ ~~Generative AI for Everyone~~ — DONE
7. ✅ ~~P1: Prompt Playground~~ — DONE
8. ✅ ~~P2: Summarizer~~ — DONE
9. ✅ ~~P3: Rewriter~~ — DONE
10. ✅ ~~Phase 2: Python LLM App Development~~ — DONE
    - ✅ ~~OpenAI for Developers~~ — DONE
    - ✅ ~~Generative AI for Developers~~ — DONE
    - ✅ ~~Generative AI Integration for Developers~~ — DONE
    - ✅ ~~Project 4 — CLI Chatbot~~ — DONE
    - ✅ ~~Project 5 — FastAPI GenAI Service~~ — DONE
    - ✅ ~~Project 6 — Structured Data Extractor~~ — DONE
    - ✅ ~~Project 7 — Resume vs JD Analyzer~~ — DONE
11. 🟡 **NOW → Phase 3: Embeddings + Vector Search + RAG** ← *you are here*
    - 🔨 **NOW → Build: Project 8 — Semantic Search Prototype**

## Phase Summary
| Phase | Name | Status |
|-------|------|--------|
| 0 | Software Baseline | ✅ Done |
| 1 | Foundations | ✅ Done |
| 2 | Python LLM App Development | ✅ Done |
| 3 | Embeddings + Vector Search + RAG | 🟡 In Progress |
| 4 | Tool Calling + Workflow Automation | ⬜ Not Started |
| 5 | Evals + Safety + Observability | ⬜ Not Started |
| 6 | MCP + Agentic Orchestration | ⬜ Not Started |
| 7 | AI-Native Developer Productivity | ⬜ Not Started |
| 8 | Multimodal, Real-Time AI, & SLMs | ⬜ Not Started |
| 9 | Portfolio + Job Prep | ⬜ Not Started |
| 10 | Certifications | ⬜ Not Started |
| 11 | Capstone: Resume-Grade Projects | ⬜ Not Started |

**Overall: 8 / 37 projects done**

## Project Checklist

### Phase 0 — Software Baseline
- [x] Project 0: GenAI Python starter template

### Phase 1 — Foundations
- [x] Project 1: Prompt Playground
- [x] Project 2: Summarizer
- [x] Project 3: Rewriter

### Phase 2 — Python LLM App Development
- [x] Project 4: CLI Chatbot
- [x] Project 5: FastAPI GenAI Service
- [x] Project 6: Structured Data Extractor
- [x] Project 7: Resume vs JD Analyzer

### Phase 3 — Embeddings + Vector Search + RAG
- [ ] Project 8: Semantic Search Prototype
- [ ] Project 9: PDF Q&A Assistant
- [ ] Project 10: Docs Knowledge Assistant
- [ ] Project 11: Enterprise Knowledge Bot
- [ ] Project 11a: GraphRAG Document Explorer

### Phase 4 — Tool Calling + Workflow Automation
- [ ] Project 12: Tool-Using Assistant
- [ ] Project 13: Research Assistant
- [ ] Project 14: SQL / Reporting Assistant
- [ ] Project 15: Workflow Triage Assistant

### Phase 5 — Evals + Safety + Observability
- [ ] Project 16: Eval Suite
- [ ] Project 17: Productionize a Workflow AI App
- [ ] Project 17a: DSPy Prompt Optimizer
- [ ] Project 17b: CI/CD Pipeline for AI
- [ ] Project 17c: OWASP LLM Security Scanner

### Phase 6 — MCP + Agentic Orchestration
- [ ] Project 18: Simple Workflow Context MCP Server
- [ ] Project 19: Workflow MCP Utility Server
- [ ] Project 20: MCP-Powered Workflow Agent Integration
- [ ] Project 21: HITL SQL Assistant
- [ ] Project 22: HITL File Action Agent
- [ ] Project 23: Stateful Workflow Automation
- [ ] Project 24: Orchestration & Multi-Agent

### Phase 7 — AI-Native Developer Productivity
- [ ] Project 25: Personal Dev Productivity Agent
- [ ] Project 26: Local AI Coding Utility

### Phase 8 — Multimodal, Real-Time AI, & SLMs
- [ ] Project 27: Vision-Based Data Extractor
- [ ] Project 28: Real-Time Voice Assistant
- [ ] Project 29: Local SLM Fine-Tuning

### Phase 11 — Capstone: Resume-Grade Projects
- [ ] Project 30: Workflow Intelligence Command Center
- [ ] Project 31: Multi-Agent Review + Knowledge Platform
- [ ] Project 32: Personal AI Dev/Workflow Copilot

---

# FINAL ROADMAP ORDER

1. Foundations
2. Python LLM apps
3. Embeddings + vector search + RAG
4. Tool calling + workflow automation
5. Evals + safety + observability + production reliability
6. MCP + agentic orchestration + HITL + persistence
7. AI-native developer productivity
8. Multimodal, Real-Time AI, & SLMs
9. Portfolio + job prep
10. One certification
11. Capstone: 3 big resume-grade projects that combine everything

---

# PHASE 0 - SOFTWARE BASELINE

## Goal
Have a strong software base so GenAI work is easy to execute.

## Skills
- Python
- FastAPI
- Pydantic
- REST APIs
- JSON
- SQL basics
- Git/GitHub
- logging
- testing
- Docker
- environment variables
- async basics
- CLI basics

## Project
### Project 0: GenAI Python starter template
Include:
- FastAPI
- Pydantic schemas
- env config
- logging
- health check
- sample endpoint
- README
- Dockerfile

## Completion goal
You can spin up a small Python AI service quickly.

---

# PHASE 1 - FOUNDATIONS

## Resources

> **Build-first rule:** Watch only what you need to unblock a project. For this phase, that's 2-3 hours max. Then build the 3 projects.

### 🟡 Pluralsight (paid)
- **Generative AI Foundations** (4 courses · 2h) — What GenAI is, prompting basics, ethics, GenAI in action. **Watch this. Skip the rest.**  
  https://www.pluralsight.com/paths/generative-ai-foundations  
  → What to watch: all 4 courses — they're short (30min each)

### 🟢 DeepLearning.AI (free)
- **ChatGPT Prompt Engineering for Developers** (1h · Andrew Ng + OpenAI) — Zero-shot, few-shot, CoT. Do this back-to-back with projects 1-3.  
  https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/

### 🔵 Microsoft Learn (free)
- **AI concepts for developers and technology professionals** (3h17m · Beginner · free, interactive modules with sandboxes)  
  https://learn.microsoft.com/en-us/training/paths/ai-concepts/  
  → What to do: complete all modules — they're interactive, not just reading. Takes ~3h. Covers what you need for AI-900 too.

### 📘 Docs — what to actually read
- **OpenAI Prompt Engineering Guide** (~20min read) — read completely, it's one page  
  https://platform.openai.com/docs/guides/prompt-engineering  
  → Read: all 6 strategies. This is the definitive reference, bookmark it.
- **OpenAI Models page** (~10min) — understand what's available and pricing  
  https://platform.openai.com/docs/models  
  → Read: GPT-4o, GPT-4o-mini, o1/o3 entries. Skip fine-tuned and legacy.
- **OpenAI Platform Docs Overview** (~10min) — just get oriented  
  https://platform.openai.com/docs/  
  → Read: "Overview" and "Quickstart" only. Don't go deeper yet.

## Learn
- AI vs ML vs LLM vs GenAI
- tokens
- context windows
- prompting basics
- hallucinations
- temperature
- limitations
- responsible AI
- privacy and bias basics

## Projects
### Project 1: Prompt Playground
Compare:
- zero-shot
- few-shot
- role/system prompting
- structured prompts

### Project 2: Summarizer
Input long text, output:
- summary
- bullets
- action items

### Project 3: Rewriter
Rewrite in:
- professional
- concise
- technical
- friendly tone

## Completion goal
You understand practical LLM behavior and failure modes.

---

# PHASE 2 - PYTHON LLM APP DEVELOPMENT

## Resources

> **Build-first rule:** Watch "OpenAI for Developers" (Pluralsight) while building — watch a module, then immediately code the same thing. Skip the other Pluralsight paths until you need them.

### 🟡 Pluralsight (paid)
- **OpenAI for Developers** (13 courses · 12h) — Full OpenAI API: Chat Completions, Responses API, function calling, Agents SDK, embeddings, streaming, evals, multimodal. **This is the main course for this phase.**  
  https://www.pluralsight.com/paths/openai-for-developers  
  → Watch in order. Key modules: "Chat Completions", "Function Calling", "Responses API & Agents SDK", "Embeddings", "Security and Moderation"

### 🟢 DeepLearning.AI (free)
- **LangChain for LLM Application Development** (1h38m · Harrison Chase) — Models, prompts, memory, chains, Q&A, agents. Good overview before Phase 3.  
  https://www.deeplearning.ai/short-courses/langchain-for-llm-application-development/

### 🎓 LangChain Academy (free)
- **Introduction to LangChain: Build AI Agents with Python** (~1.5h · free) — Modern LangChain: tools, short-term memory, MCP, multi-agent, HITL.  
  https://academy.langchain.com/courses/foundation-introduction-to-langchain-python

### 🔵 Microsoft Learn (free)
- **Get started with AI applications and agents on Azure** (4h59m · Beginner · free, hands-on labs)  
  https://learn.microsoft.com/en-us/training/paths/get-started-ai-apps-agents/  
  → Do this if you want Azure-specific context (Azure OpenAI, AI Foundry). Optional but useful for the day job.

### 📘 Docs — what to actually read
- **OpenAI API Reference: Chat Completions** (~30min) — the core endpoint you'll live in  
  https://platform.openai.com/docs/api-reference/chat  
  → Read: "Create chat completion", parameters (temperature, max_tokens, stream, tool_choice). Skip the deprecated `/completions` endpoint.
- **OpenAI Responses API vs Chat Completions** (~15min) — understand when/why to use each  
  https://platform.openai.com/docs/guides/migrate-to-responses  
  → Read the whole page. New projects should default to Responses API.
- **OpenAI Structured Outputs** (~20min)  
  https://platform.openai.com/docs/guides/structured-outputs  
  → Read: "How to use", "Supported schemas", "Refusals". Skip "Legacy JSON mode".
- **OpenAI Cookbook** — practical code examples  
  https://cookbook.openai.com/  
  → Read: "How to format inputs to ChatGPT models", "Function calling with a weather API", "How to count tokens with tiktoken". Skip fine-tuning examples for now.
- **openai-python library README** (~10min)  
  https://github.com/openai/openai-python  
  → Read: README and examples/ folder. Just get familiar with the client patterns.
- **Real Python async guide** (~30min, optional) — if async feels unfamiliar  
  https://realpython.com/async-io-python/  
  → Read: "The asyncio package and async/await", "Async IO in Context". Skip the deep OS-level sections.

## Learn
- Python API integration
- Responses API concepts
- why new OpenAI work should default to `Responses API`
- Chat Completions is still supported, but `Assistants API` is deprecated and currently scheduled to sunset on **August 26, 2026**
- local OpenAI-compatible servers: **Ollama** and **LM Studio** can expose localhost APIs so you can swap between hosted and local models with similar client code
- prompts and system instructions
- structured outputs
- JSON schema outputs
- streaming responses (stream=True, SSE)
- retries
- timeouts
- rate limits
- moderation basics
- token/cost awareness
- model selection basics
- **Reasoning Models (2026 critical skill):**
  - When to use reasoning models (OpenAI o1/o3, DeepSeek-R1) vs fast generalist models (GPT-4o, Claude Sonnet 3.5)
  - **DeepSeek-R1** — open-weights, MIT license, ~96% cheaper than o1, transparent chain-of-thought logs; ideal for cost-sensitive production and self-hosting
  - **OpenAI o3/o1** — best for complex multi-file agentic coding and general-purpose reasoning with managed infrastructure
  - Chain-of-Thought (CoT) and deliberation loops — understand how reasoning models "think before answering"
- **Open source models: Llama 3.x, Mistral, Gemma, Phi-3** — run locally via Ollama; understand cost/privacy/quality tradeoffs vs OpenAI
- when to use open source (data privacy, cost at scale, air-gapped) vs OpenAI (quality, ease, multimodal)
- learn the split between **model runtime** and **agent runtime**:
  - model runtime = Ollama / LM Studio serving the local model
  - agent runtime = your Python app / LangGraph loop / OpenAI Agents SDK handling tools, memory, approvals, and orchestration

## 🖥️ Local Models on Apple Silicon (M1 Max 32GB)
> **Your hardware advantage:** M1 Max with 32GB unified memory is a serious local AI machine. The unified memory architecture means your GPU and CPU share the same pool — models that would choke an NVIDIA RTX 4090 (24GB VRAM) run comfortably here.

### Why M1 Max is Good for Local AI
- **32GB unified memory** = GPU and CPU share it, no VRAM bottleneck
- **400 GB/s memory bandwidth** = fast token generation even on large models
- **Apple Neural Engine (ANE)** = hardware ML acceleration baked in
- **Energy-efficient** = run 7B–30B models for hours without fan noise or heat

### Framework Choice for Apple Silicon

| Framework | Best For | Speed |
|-----------|----------|-------|
| **MLX** ⭐ | Apple Silicon native — zero-copy tensors, fastest throughput | Fastest generation |
| **Ollama** | OpenAI-compatible API, easy setup, developer-friendly | Very fast |
| **LM Studio** | GUI exploration, visual parameter tuning, no terminal | Same as Ollama (same backend) |
| **llama.cpp** | Low-level control, custom quantization experiments | Same as Ollama |

> **Rule**: Use **Ollama** for development/agent integration. Use **MLX** when you want maximum speed or local fine-tuning on Mac.

### What Can You Run on 32GB M1 Max?

| Model Size | Examples | Q4 Memory | Speed |
|-----------|----------|-----------|-------|
| **7–8B** | Qwen3-8B, Llama 3.1 8B, Mistral 7B | ~5GB | ~60–80 tok/s — instant |
| **14B** | Qwen3-14B, Phi-4, Gemma 3 12B | ~9GB | ~40–50 tok/s — very fast |
| **27–30B** ⭐ Sweet spot | Qwen3-30B-A3B (MoE), Mistral Small 22B | ~18–22GB | ~20–30 tok/s — smooth |
| **70B (quantized)** | Llama 3.3 70B Q4, DeepSeek-R1-Distill 70B | ~42GB | ~8–12 tok/s — usable |

> ⚠️ **70B warning**: With 32GB, 70B Q4 models will exceed RAM and swap to SSD. Stick to 30B or less for a smooth experience. Use 70B only for experiments.

### Recommended Models to Try First (2026)

> **Qwen3 is now the top recommendation.** Released April 2025, it features hybrid thinking/non-thinking modes (switchable per prompt), native MCP tool support, 128K context, and Apache 2.0 license. On M1 Max, Qwen3-14B is the best everyday model — fast, smart, and MCP-aware out of the box.

```bash
# Install Ollama first: https://ollama.com
brew install ollama

# ⭐ Best everyday model — fast + smart (Qwen3, hybrid thinking)
ollama run qwen3:14b

# ⭐ Best reasoning/coding sweet spot (MoE — only 3B active params!)
ollama run qwen3:30b-a3b

# Best dedicated coding model
ollama run qwen2.5-coder:14b

# Reasoning model (like a local o1) — transparent CoT
ollama pull deepseek-r1:14b

# Tiny but surprisingly capable
ollama run qwen3:4b

# Vision model (multimodal)
ollama run llava:13b
```

> **Qwen3 hybrid thinking tip:** By default, Qwen3 thinks step-by-step. Add `/no_think` to your prompt for instant responses, or `/think` to force deep reasoning. This eliminates the need for a separate reasoning model in most cases.

### MLX Setup (Fastest for Mac)
```bash
pip install mlx-lm

# Run Qwen3 14B via MLX (faster than Ollama)
python -m mlx_lm.chat --model mlx-community/Qwen2.5-14B-Instruct-4bit

# Fine-tune locally (Phase 8 skill)
python -m mlx_lm.lora --train --model mlx-community/Llama-3.2-3B-Instruct-4bit \
    --data ./data --iters 1000
```

### Connect Local Models to Your Python Code
Both Ollama and LM Studio expose an OpenAI-compatible API — swap the base URL and you're done:

```python
from openai import OpenAI

# Use Ollama locally instead of OpenAI
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # required but ignored
)

response = client.chat.completions.create(
    model="qwen3:14b",
    messages=[{"role": "user", "content": "Explain embeddings in 2 sentences."}]
)
print(response.choices[0].message.content)
```

### Key Concepts to Learn
- **Quantization**: Q4_K_M = 4-bit weights with K-means grouping. Best quality/size tradeoff. Q2 = tiny but dumb. Q8 = near-full quality.
- **GGUF format**: The standard model file format for llama.cpp/Ollama. Download from Hugging Face `mlx-community` or `bartowski` namespaces.
- **Context window**: Most 7–14B models support 8k–128k tokens. Larger context = more RAM needed for the KV cache.
- **Memory pressure**: Watch Activity Monitor → Memory tab. If "Memory Pressure" is red, your model is too big.
- **Model vs Instruct variants**: Always use the `-Instruct` or `-Chat` variant for conversations. Base models need special prompting.
- **MoE (Mixture of Experts)**: Models like Qwen3-30B-A3B activate only a subset of parameters per token — smaller memory footprint at big-model quality.

### Resources
- Ollama model library: https://ollama.com/library
- MLX community models (Hugging Face): https://huggingface.co/mlx-community
- GGUF models (bartowski): https://huggingface.co/bartowski
- mlx-lm docs: https://github.com/ml-explore/mlx-examples/tree/main/llms
- Open WebUI (local ChatGPT UI for Ollama): https://openwebui.com/

## Projects
### Project 4: CLI Chatbot
Features:
- history
- persona
- transcript save

### Project 5: FastAPI GenAI Service
Endpoints:
- summarize
- rewrite
- classify
- extract

### Project 6: Structured Data Extractor
Extract JSON fields from raw text.

### Project 7: Resume vs JD Analyzer
Analyze fit, missing skills, and improvement suggestions.

## Completion goal
You can build Python LLM services without framework magic.

---

# PHASE 3 - EMBEDDINGS, VECTOR SEARCH, AND RAG

## Resources

> **Build-first rule:** Watch the 52min DLAI course, then start Project 8. Debugging bad retrieval teaches more than any video.

### 🟡 Pluralsight (paid)
- **Vector Databases and Embeddings for Developers** (43min) — Embeddings, cosine similarity, vector stores. **Watch before Project 8.**  
  https://www.pluralsight.com/courses/developers-vector-databases-embeddings

### 🟢 DeepLearning.AI (free)
- **Advanced Retrieval for AI with Chroma** (52min · Intermediate) — Query expansion, cross-encoder reranking, embedding adapters.  
  https://www.deeplearning.ai/short-courses/advanced-retrieval-for-ai/
- **Building and Evaluating Advanced RAG** (1h · Intermediate) — Sentence-window retrieval, auto-merging, RAG triad evals.  
  https://www.deeplearning.ai/short-courses/building-evaluating-advanced-rag/

### 📘 Docs — what to actually read
- **OpenAI Embeddings guide** (~15min — read all, compact)  
  https://platform.openai.com/docs/guides/embeddings  
  → Know: use `text-embedding-3-small` by default, cosine similarity, chunk before embedding.
- **Chroma quickstart** (~30min)  
  https://docs.trychroma.com/  
  → Read: "Getting started", "Creating collections", "Querying". Skip: cloud/deployment sections.
- **LangChain RAG tutorial** (~45min including running code)  
  https://python.langchain.com/docs/tutorials/rag/  
  → Run: "Indexing" and "Retrieval and generation". Skip "Advanced" until after Project 9.
- **sentence-transformers** (~15min — free local embeddings)  
  https://sbert.net/  
  → Read: "Getting started" and "Pretrained models". Use `all-MiniLM-L6-v2` for experiments.
- **MTEB Leaderboard** — use when choosing an embedding model  
  https://huggingface.co/spaces/mteb/leaderboard  
  → Don't read linearly. Filter by "Retrieval" task type when picking a model.

## Learn
- embeddings
- semantic similarity
- chunking
- overlap
- metadata filtering
- vector stores: **Chroma** (local/dev), **Qdrant** (production), **pgvector** (Postgres)
- hybrid search: BM25 keyword + vector (better than pure vector in production)
- retrieval
- reranking basics (Cohere Rerank, cross-encoders)
- **GraphRAG and LightRAG**: Moving beyond flat vector search by building entity relationship graphs for multi-hop reasoning. Critical for complex, knowledge-intensive retrieval where context clumping fails.
- grounded generation
- citations
- **Context Engineering**: smarter chunking, retrieval routing, memory management, and query rewriting to maximize relevance
- **Hugging Face sentence-transformers** — produce embeddings with open-source models (all-MiniLM-L6, BGE, nomic-embed)
- **Ollama** — run Llama 3 / Mistral locally for RAG experiments
- difference: OpenAI embeddings vs open-source embeddings (cost, privacy, quality)
- when to use OpenAI hosted `file_search` / managed retrieval vs building a custom RAG stack yourself
- when RAG beats fine-tuning

## Projects
### Project 8: Semantic Search Prototype
Search across a document collection.

### Project 9: PDF Q&A Assistant
Features:
- parse PDFs
- chunk text
- embed chunks
- retrieve
- answer with citations

### Project 10: Docs Knowledge Assistant
Use markdown/docs/READMEs. Prefer docs that look like real enterprise knowledge: service READMEs, API docs, deployment notes, support articles, policy notes, troubleshooting pages, and architecture decisions.

### Project 11: Enterprise Knowledge Bot
Answer from internal-style knowledge only, cite the exact source, and refuse unsupported answers.

Must handle:
- "what should I check first?"
- "which service/team owns this?"
- "what evidence supports this recommendation?"
- "what should I not do without approval?"

### Project 11a: GraphRAG Document Explorer
Build a knowledge graph to answer multi-hop reasoning questions over a complex enterprise corpus using LightRAG or Microsoft GraphRAG principles.

Portfolio-safe dataset idea:
- fake services
- fake alerts
- fake runbooks
- fake support articles
- fake change requests
- fake ownership metadata
- fake incident postmortems

## Completion goal
You have a strong production-style RAG project with citations.

---

# PHASE 4 - TOOL CALLING AND WORKFLOW AUTOMATION

## Resources

### 🟡 Pluralsight (paid)
- **OpenAI for Developers** — Covers function calling and tool use in depth.  
  https://www.pluralsight.com/paths/openai-for-developers
- Individual course: **Function Calling and Tool Use with OpenAI** (38min)  
  https://www.pluralsight.com/courses/function-calling-tool-use-openai
- Individual course: **OpenAI Responses API and Agents SDK** (45min) — Tool calling via the new Responses API.  
  https://www.pluralsight.com/courses/openai-responses-api-agents-sdk

> **Build-first rule:** Read the function calling guide, then build Project 12. Tool calling clicks the first time you debug a failed tool call yourself.

### 🟡 Pluralsight (paid)
- **Function Calling and Tool Use with OpenAI** (38min) — This is all you need to watch.  
  https://www.pluralsight.com/courses/function-calling-tool-use-openai  
  → Watch all — it's only 38min.
- **OpenAI Responses API and Agents SDK** (45min) — Tool calling via Responses API.  
  https://www.pluralsight.com/courses/openai-responses-api-agents-sdk

### 🟢 DeepLearning.AI (free)
- **Functions, Tools and Agents with LangChain** (1h44m · Intermediate) — Function calling, LCEL, tagging, extraction, tool routing.  
  https://www.deeplearning.ai/short-courses/functions-tools-agents-langchain/

### 📘 Docs — what to actually read
- **OpenAI Function Calling guide** (~30min — read all, moderate length)  
  https://platform.openai.com/docs/guides/function-calling  
  → Read: "Supported models", "Define functions", "Handle tool calls", "Parallel tool calling", "Edge cases". This is critical — read before starting Project 12.
- **OpenAI Tools guide** (~20min)  
  https://platform.openai.com/docs/guides/tools  
  → Read all. Understand: built-in tools (file_search, code_interpreter, web_search) vs your own functions vs remote MCP.
- **OpenAI Agents SDK docs** (~1h — skim structure, read key pages)  
  https://openai.github.io/openai-agents-python/  
  → Read: "Quick start", "Agents", "Tools", "Handoffs". Skip "Voice" for now.
- **LangChain tools concepts** (~15min)  
  https://python.langchain.com/docs/concepts/tools/  
  → Read all. Short and useful.

## Learn
- function/tool calling
- tool schemas
- deterministic wrapping around LLM decisions
- workflow design
- model chooses tool vs explicit routing
- built-in tools vs your own functions vs remote MCP servers
- safe execution boundaries

## Projects
### Project 12: Tool-Using Assistant
Tools:
- calculator
- docs search
- notes tool
- file lookup
- mock calendar
- mock alert lookup
- mock ticketing-system lookup
- mock change request lookup

### Project 13: Research Assistant
Retrieve docs/web content, synthesize, cite, and say when unsure.

### Project 14: SQL / Reporting Assistant
Generate read-only SQL safely.

### Project 15: Workflow Triage Assistant
Classify, prioritize, route, and draft a response for workflow items.

Must support:
- priority/severity recommendation with explanation
- likely owner/team routing
- knowledge/doc suggestions
- duplicate or related ticket detection
- suggested next action
- strict "no action taken automatically" mode

## Completion goal
You can build assistants that do useful actions, not just chat.

---

# PHASE 5 - EVALS, SAFETY, OBSERVABILITY, RELIABILITY

## Resources

### 🟡 Pluralsight (paid)
- **OpenAI for Developers** — Includes testing/monitoring/evals and security/moderation modules.  
  https://www.pluralsight.com/paths/openai-for-developers
- Individual course: **Testing, Monitoring, and Evaluating OpenAI Models** (59min)  
  https://www.pluralsight.com/courses/testing-monitoring-evaluating-openai-models
- Individual course: **OpenAI Security and Moderations** (28min)  
  https://www.pluralsight.com/courses/openai-security-moderations
- Individual course: **Generative AI Data Privacy and Safe Use for Developers** (54min)  
  https://www.pluralsight.com/courses/safe-use-developers-generative-ai-data-privacy

### 🟢 DeepLearning.AI (free)
- **Building and Evaluating Advanced RAG** — RAG triad: answer relevance, context relevance, groundedness evals.  
  https://www.deeplearning.ai/short-courses/building-evaluating-advanced-rag/
- **Red Teaming LLM Applications** — Identify and fix vulnerabilities, jailbreaks, and prompt injection attacks.  
  https://www.deeplearning.ai/short-courses/red-teaming-llm-applications/
- **Semantic Caching for AI Agents** (30min · Redis) — Speed up and reduce costs of AI agents using semantic caching that reuses responses based on meaning rather than exact text. Production-critical for high-traffic deployments.  
  https://www.deeplearning.ai/short-courses/semantic-caching-for-ai-agents/
- **NVIDIA NeMo Agent Toolkit: Making Agents Reliable** (45min · NVIDIA) — Turn proof-of-concept agent demos into production-ready systems using observability, evaluation, and deployment tools.  
  https://www.deeplearning.ai/short-courses/nvidia-nat-making-agents-reliable/

### 🎓 LangChain Academy (free)
- **Quickstart: LangSmith Essentials** (free · ~1h) — Practical tracing, feedback loops, and evaluation workflow for agent applications.  
  https://academy.langchain.com/courses/langsmith-essentials
- **Foundation: Introduction to Agent Observability & Evaluations** (free) — Strong addition for 2026-style agent eval workflows.  
  https://academy.langchain.com/

> **Build-first rule:** Start Project 16 (eval suite) right after Phase 4. Evals are easier to understand once you have a working app to evaluate against.

### 📘 Docs — what to actually read
- **DeepEval quickstart** (~20min)  
  https://docs.confident-ai.com/  
  → Read: "Getting started", "Metrics overview", "Writing test cases". Run the quickstart example before Project 16.
- **OpenAI evals guide** (~20min)  
  https://platform.openai.com/docs/guides/evals  
  → Read all. Understand: golden datasets, LLM-as-a-Judge, grading criteria.
- **OWASP LLM Top 10** (~30min — scan all 10 items)  
  https://owasp.org/www-project-top-10-for-large-language-model-applications/  
  → Read: the description and impact of all 10. Focus on LLM01 (prompt injection) and LLM08 (excessive agency). Reference during Project 17c.
- **LangSmith docs** (~30min — skim)  
  https://docs.smith.langchain.com/  
  → Read: "Quick start" and "Tracing overview". You'll use this actively in Project 17.
- **Langfuse docs** (~20min — for open-source alternative)  
  https://langfuse.com/docs  
  → Read: "Getting started". Use this if you want self-hosted observability.
- **GitHub Actions docs** (~20min)
  https://docs.github.com/en/actions
  → Read: "Quickstart", "Understanding GitHub Actions". Just enough to wire up Project 17b.
- **pytest-recording** (~15min) — record/replay third-party HTTP calls with VCR.py cassettes
  https://pypi.org/project/pytest-recording/
  → Read: "Usage", "Default recording mode", "Configuration", and "Blocking network access". Use this for ticketing/OpenAI/vendor API boundaries.
- **Syrupy snapshot testing** (~15min) — external snapshots for structured Python objects
  https://syrupy-project.github.io/syrupy/
  → Read: CLI options, `--snapshot-update`, and filters like `props`/`paths`. Use this for internal API responses, DB state summaries, and async flow outputs.
- **OpenAI moderation guide** (~10min)
  https://platform.openai.com/docs/guides/moderation
  → Read all. Short. Use the moderation API in Project 17c.

## Learn: Evals & Reliability
- evaluation datasets and golden test sets
- regression tests for prompts — treat prompts as code with version control
- deterministic API regression tests:
  - use `pytest-recording` for third-party HTTP record/replay cassettes
  - use `syrupy` for internal API response snapshots, DB state summaries, and async workflow results
  - scrub secrets/headers and normalize dynamic fields before committing recordings or snapshots
- groundedness checks
- hallucination controls
- **Eval-Driven Development (EDD):**
  - define success criteria upfront like TDD
  - LLM-as-a-Judge — use a powerful model to evaluate outputs of a smaller model on rubric-based metrics
  - Component-level tracing — isolate failures in retriever, reranker, or planner stages
  - DeepEval integrates with pytest — treat AI quality like unit tests
- **Programmatic Prompt Optimization (DSPy):**
  - Shift from manual prompt tweaking to defining modules and metrics
  - Let DSPy compile and optimize prompt weights autonomously
- moderation
- abuse prevention
- privacy / PII handling
- observability tools: **LangSmith**, **Langfuse** (open-source), **Arize Phoenix**, **Opik**, **Braintrust**
- tracing
- logging
- latency tracking
- caching
- fallback behavior
- prompt versioning and management: **PromptLayer**, **Maxim AI**
- cost tracking
- **Multi-LLM Routing**: preventing vendor lock-in and optimizing latency/cost using routing layers like **LiteLLM** or **Logic**

## Learn: AI Security ⭐ 2026 Critical
> Every production LLM app is an attack surface. OWASP LLM Top 10 is now the standard checklist.

- **OWASP LLM Top 10 (2025/2026 edition)** — the canonical checklist:
  - LLM01: Prompt Injection (direct and indirect)
  - LLM02: Insecure Output Handling (XSS, SSRF via LLM output)
  - LLM03: Training Data Poisoning
  - LLM04: Model Denial of Service (token flooding, context exhaustion)
  - LLM05: Supply Chain Vulnerabilities (compromised plugins, dependencies)
  - LLM06: Sensitive Information Disclosure (PII leakage via prompts)
  - LLM07: Insecure Plugin Design (overprivileged tool calls)
  - LLM08: Excessive Agency (agent acts without appropriate HITL approval)
  - LLM09: Overreliance (no fallback when model is wrong)
  - LLM10: Model Theft
- **Prompt injection defenses:** input validation, role separation, system prompt hardening, output parsers
- **Safe tool execution:** scope tool permissions to minimum required; never expose shell-exec as a tool without HITL
- **Red teaming:** adversarial prompt testing before production — jailbreak tests, indirect injection via RAG sources
- **Secrets management:** never pass API keys in prompts; use env vars and vaults
- **Rate limiting and abuse prevention** at API gateway level
- **Content filtering:** OpenAI Moderation API, custom regex guards, output scanners

## Learn: CI/CD for GenAI Apps ⭐ 2026 Critical
> AI apps need a different CI/CD strategy — non-deterministic outputs require eval-based gates instead of simple pass/fail assertions.

- **GitHub Actions for AI pipelines:**
  - Trigger eval suite on every PR
  - LLM-as-a-Judge quality gate — fail the build if quality score drops below threshold
  - Cost regression check — alert if new prompt version costs 2x more
- **Prompt version control:**
  - Store prompts in version-controlled files (not hardcoded strings)
  - Track prompt changes in git history
  - Tag prompt versions that go to production
- **Model version management:**
  - Pin model versions in production (`gpt-4o-2024-11-20` not `gpt-4o`)
  - Test against new model versions before upgrading
- **Container-based deployment pipeline:**
  - Docker → push to registry → deploy via GitHub Actions
  - Environment parity: dev/staging/prod
- **Integration tests vs eval tests:**
  - Integration tests: check API contracts, response schema, latency thresholds (deterministic)
  - Snapshot/regression tests: compare normalized internal API/DB flow outputs and replay third-party HTTP cassettes
  - Eval tests: check output quality on golden dataset (probabilistic, use threshold pass/fail)
- **Rollback strategy:** canary deployments; monitor latency and quality metrics before full rollout

## Projects
### Project 16: Eval Suite
Create 30-50 test cases for one app:
- golden dataset with expected outputs, preferably workflow/knowledge/triage examples
- pytest + DeepEval integration
- `pytest-recording` cassettes for external API calls
- `syrupy` snapshots for normalized API responses and DB state
- LLM-as-a-Judge metric for subjective quality
- groundedness check for any RAG outputs
- CI-ready: run eval suite automatically on push

### Project 17: Productionize a Workflow AI App
Add:
- logging
- retries
- timeouts
- caching
- metrics
- failure handling
- trace IDs across request, retrieval, tool calls, and LLM calls
- SLO notes: latency, cost, error rate, and quality thresholds
- operations guide: how to diagnose common failures
- safe degradation: return partial evidence instead of inventing answers
- prompt versioning (prompts as files, tracked in git)
- regression test workflow: `make test`, `make test-record`, `make test-refresh`
- README with cost/latency notes

### Project 17a: DSPy Prompt Optimizer
Replace manual prompts with compiled, programmatically optimized prompts.

### Project 17b: CI/CD Pipeline for AI
Automate tests and regression evals via GitHub Actions, building a container-based deployment pipeline.

### Project 17c: OWASP LLM Security Scanner
Implement security guardrails for prompt injection, test for indirect injection, and restrict tool scopes.

## Completion goal
You can evaluate, secure, and deploy an AI application like a production engineer.

---

# PHASE 6 - MCP + AGENTIC ORCHESTRATION + HITL + PERSISTENCE

## Resources

> **Build-first rule:** Do the LangGraph Academy course (55 lessons, ~6h) as your main input for this phase. Hands-on, not lecture-heavy.

### 🟡 Pluralsight (paid)
- **Agentic AI for Developers** (1h24m · Intermediate) — Agentic patterns, tool use, orchestration loops.  
  https://www.pluralsight.com/courses/agentic-ai-developers
- **OpenAI Responses API and Agents SDK** (45min) — Build agents with the official OpenAI SDK.  
  https://www.pluralsight.com/courses/openai-responses-api-agents-sdk

### 🟢 DeepLearning.AI (free)
- **AI Agents in LangGraph** (1h32m · Intermediate) — Build agents from scratch, LangGraph components, persistence, human-in-the-loop. By Harrison Chase (LangChain CEO).  
  https://www.deeplearning.ai/short-courses/ai-agents-in-langgraph/
- **Multi-AI Agent Systems with CrewAI** — Multi-agent collaboration, delegation, role-based agents.  
  https://www.deeplearning.ai/short-courses/multi-ai-agent-systems-with-crewai/
- **Build AI Apps with MCP Servers** — Model Context Protocol, connecting agents to external tools via MCP.  
  https://www.deeplearning.ai/short-courses/build-ai-apps-with-mcp-server-working-with-box-files/
- **A2A: The Agent2Agent Protocol** ⭐ NEW 2026 (1h27m · Intermediate) — Google Cloud + IBM Research. The open standard (donated to Linux Foundation) for **agent-to-agent communication**. Complements MCP: MCP connects agents to tools/data, A2A lets agents collaborate with each other across frameworks (LangGraph, ADK, CrewAI). **Must learn in 2026 — this is now part of every senior multi-agent system design.**  
  https://www.deeplearning.ai/short-courses/a2a-the-agent2agent-protocol/
- **Building Coding Agents with Tool Execution** ⭐ NEW 2026 (1h · E2B) — Build AI agents that write and execute code safely in **sandboxed cloud environments**. E2B sandboxes are now the standard pattern for any agent that runs code — prevents local system damage, enables parallel execution.  
  https://www.deeplearning.ai/short-courses/building-coding-agents-with-tool-execution/
- **Agent Skills with Anthropic** (45min · Anthropic) — Equip agents with expert on-demand knowledge for reliable coding, research, and data analysis workflows using Claude’s tool use patterns.  
  https://www.deeplearning.ai/short-courses/agent-skills-with-anthropic/
- **Agentic AI** by Andrew Ng — Agentic design patterns: reflection, tool use, planning, multi-agent.  
  https://www.deeplearning.ai/courses/agentic-ai/
- **Agent Memory: Building Memory-Aware Agents** — Memory types, in-context, external, episodic memory.  
  https://www.deeplearning.ai/short-courses/agent-memory-building-memory-aware-agents/

### 🎓 LangChain Academy (free)
- **Introduction to LangGraph** ⭐ HIGHLY RECOMMENDED (55 lessons · 6h · FREE) — Official LangGraph course covering state, memory, human-in-the-loop, long-term memory, and building your own assistant. Far more comprehensive than the DeepLearning.AI short course.  
  https://academy.langchain.com/courses/intro-to-langgraph
- **Quickstart: LangGraph Essentials** (free · ~1h) — Good fast-start companion before or during the full LangGraph course.  
  https://academy.langchain.com/courses/langgraph-essentials-python

### 📘 Docs — what to actually read
- **MCP official docs** (~1h — read core sections)  
  https://modelcontextprotocol.io/docs/  
  → Read: "Introduction", "Core architecture", "Writing your first server", "Tools", "Resources", "Prompts". Skip "Sampling" for now.
- **Python MCP SDK** (~20min)  
  https://github.com/modelcontextprotocol/python-sdk  
  → Read README + run the quickstart example before Project 18.
- **LangGraph docs — concepts** (~1h)  
  https://langchain-ai.github.io/langgraph/concepts/  
  → Read: "Why LangGraph?", "Low-level primer", "Persistence", "Human-in-the-loop", "Memory". Skip "Multi-agent" until Project 24.
- **LangGraph tutorials** (~2h — run the code)  
  https://langchain-ai.github.io/langgraph/tutorials/  
  → Do: "Introduction to LangGraph", "Customer support bot". These are hands-on.
- **OpenAI Agents SDK** (~45min — skim docs, run examples)  
  https://openai.github.io/openai-agents-python/  
  → Read: "Quick start", "Agents", "Tools", "Handoffs", "Guardrails". Run the examples.
- **OpenAI MCP guide** (~15min)  
  https://platform.openai.com/docs/mcp/  
  → Read all. Understand how ChatGPT and the API can act as MCP clients.
- **A2A spec overview** (~20min)  
  https://google.github.io/A2A/  
  → Read: "Introduction" and "Core concepts". This gives you the mental model for Project 24.

> **2026 Note:** MCP has clearly crossed into the mainstream tooling layer. OpenAI now documents MCP for ChatGPT/API integrations, Anthropic documents MCP as a first-class protocol, and Google positions A2A as the complementary agent-to-agent layer. Learn all three ideas: tool calling, MCP, and A2A.

## Why this phase exists
You already started MCP, and 2026 strongly rewards engineers who understand:
- standardized tool/context integration
- stateful workflows
- approvals
- resumability
- orchestration

## Learn MCP
### Concepts
- MCP host / client / server architecture
- tools
- resources
- prompts
- transports
- JSON-RPC basics
- local vs remote servers
- auth/security awareness
- registry/ecosystem awareness

### MCP projects
#### Project 18: Simple Workflow Context MCP Server
Expose:
- one tool
- one resource
- one prompt
Use a simple enterprise-workflow-flavored local use case.

Examples:
- `list_services`
- `read_knowledge_doc`
- `search_work_items`
- `summarize_recent_logs` over local sample files

#### Project 19: Workflow MCP Utility Server
Examples:
- local docs search
- task tracker
- local file summarizer
- personal notes lookup
- knowledge lookup
- fake alert/ticket/change lookup
- recent work-item timeline summary

#### Project 20: MCP-Powered Workflow Agent Integration
Connect an agent/client to your MCP server and use it in a workflow.

The workflow should look like:
1. user gives a workflow item such as an alert, ticket, change request, bug report, or support escalation
2. agent retrieves related knowledge/docs
3. agent checks mock ticket/service/change metadata
4. agent proposes next actions with citations
5. human approves before any side-effect tool runs

## Learn agentic orchestration
### Topics
- agent vs workflow
- stateful execution
- durable execution
- persistence/checkpointing
- human-in-the-loop
- interrupt/resume
- approval gates
- memory types
- side-effect safety
- long-running jobs

## Framework direction
Learn in this order:
1. direct tool-calling workflows
2. simple orchestration
3. PydanticAI (for type-safe, contract-driven LLM systems) and smolagents (for highly efficient, code-first execution)
4. LangChain only where useful
5. LangGraph for complex, stateful orchestration
6. CrewAI / Microsoft Agent Framework for multi-agent teams
7. Explore specialized SDKs: OpenAI Agents SDK (MCP native), Google ADK (GCP/Multimodal), Mastra (JS/TS)

## Projects
### Project 21: HITL SQL Assistant
Pause before execution, require approve/reject.

### Project 22: HITL File Action Agent
Pause before write/delete/send actions.

### Project 23: Stateful Workflow Automation
Resume after interruption, persist state.

Model a realistic long-running workflow:
- intake work item
- gather evidence
- search knowledge docs
- propose severity and owner
- wait for human approval
- draft update/comment or follow-up task
- resume after interruption without losing context

### Project 24: Orchestration & Multi-Agent
Implement using LangGraph, PydanticAI, or smolagents:
- triage/planner agent
- evidence retrieval agent
- knowledge/doc agent
- critic/safety reviewer
- approval gate
- resume execution
- final workflow summary synthesis

## Completion goal
You understand modern agentic systems, not just chatbot demos.

---

# PHASE 7 - AI-NATIVE DEVELOPER PRODUCTIVITY

## Resources

### 🟡 Pluralsight (paid)
- **Generative AI Integration for Developers** (6 courses · 4h) — Integrating AI into dev workflows, productivity patterns.  
  https://www.pluralsight.com/paths/generative-ai-integration-for-developers
- Individual course: **OpenAI Codex** (34min) — AI-assisted coding with OpenAI Codex.  
  https://www.pluralsight.com/courses/openai-codex
- Individual course: **Enhancing Developer Workflows with OpenAI** (33min)  
  https://www.pluralsight.com/courses/enhancing-developer-workflows-openai

### � DeepLearning.AI (free)
- **Gemini CLI: Code & Create with an Open-Source Agent** (1h · Beginner) — Build real-world applications from the command line using **Gemini CLI**, Google’s open-source agentic coding assistant that coordinates local tools and cloud services. Essential for 2026 vibe-coding workflows.  
  https://www.deeplearning.ai/short-courses/gemini-cli-code-and-create-with-an-open-source-agent/
- **Spec-Driven Development with Coding Agents** (45min · JetBrains) — Move beyond vibe coding: write clear specs that give your coding agent the context it needs to build intentional, maintainable software. The professional approach to AI-assisted development.  
  https://www.deeplearning.ai/short-courses/spec-driven-development-with-coding-agents/

### �📘 Official Docs (free)
- GitHub Copilot docs: https://docs.github.com/en/copilot
- Ollama (run local models): https://ollama.com/
- Ollama tool calling docs: https://docs.ollama.com/capabilities/tool-calling
- Ollama OpenAI compatibility docs: https://docs.ollama.com/openai
- LM Studio local server docs: https://lmstudio.ai/docs/developer/core/server
- LM Studio tool use docs: https://lmstudio.ai/docs/developer/openai-compat/tools
- Open WebUI MCP docs: https://docs.openwebui.com/features/extensibility/mcp/
- Continue.dev (open-source AI coding IDE extension): https://continue.dev/
- OpenAI Codex docs: https://platform.openai.com/docs/models

## Goal
Use AI to accelerate your own development workflow.

## Learn
- Copilot/Codex-style coding workflows
- code review with AI
- prompt-driven test generation
- AI-assisted debugging
- local model experimentation
- how to run a **local coding agent stack**:
  - serve a local model with Ollama or LM Studio
  - expose tools via Python functions or MCP
  - run the agent loop in your app, Codex, Claude Code, or Open WebUI
- **Agentic IDEs:** Use Cursor, Windsurf for deep codebase reasoning and refactoring.
- **Terminal Coding Agents:** Master Claude Code, Devin for autonomous end-to-end execution.
- AI-first IDE patterns
- dev workflow automation
- **Native Browser Agents vs MCP Browser**:
  - In 2026, many AI assistants (like Antigravity) have **native browser integration** (`browser_subagent`).
  - Use native tools for complex UI interaction, recording actions, and high-fidelity testing.
  - Use MCP-based browsers (like Playwright MCP) for headless, scriptable automation and structured data scraping.
  - **Rule of thumb**: If your agent has a native high-performance tool, prefer it over generic MCP equivalents for speed and deeper integration.

## Projects
### Project 25: Personal Dev Productivity Agent
Examples:
- summarize repo
- generate TODOs
- explain stack traces
- search docs
- update roadmap tracker

### Project 26: Local AI Coding Utility
Examples:
- local code explainer
- local grep + summarize
- local MCP helper for VS Code workflows
- local model served by Ollama or LM Studio
- one tool-calling loop with file/search/shell-safe tools
- compare one hosted model vs one local model on the same task and document tradeoffs

## Completion goal
You work like an AI-native developer, not just an AI consumer.

---

# PHASE 8 - MULTIMODAL, REAL-TIME AI, & SLMs (Small Language Models)

## Resources

### 📘 Official Docs (free)
- OpenAI Realtime API: https://platform.openai.com/docs/guides/realtime
- OpenAI Vision: https://platform.openai.com/docs/guides/vision
- Hugging Face SLM Guide: https://huggingface.co/blog/smollm
- Unsloth (Fast Fine-tuning): https://github.com/unslothai/unsloth
- Synthetic Data Generation with Argilla: https://docs.argilla.io/en/latest/

## Learn
- Multimodal architectures (Vision + Audio)
- Real-time streaming protocols (WebSockets / WebRTC for AI)
- SLMs (Small Language Models: Phi-3, Llama-3-8B, Qwen)
- Synthetic Data Generation techniques (using large models to train small models)
- Parameter-Efficient Fine-Tuning (PEFT, LoRA)

## Projects

### Project 27: Vision-Based Data Extractor
Extract structured JSON data (tables, charts, receipts) using vision models (GPT-4o or Claude 3.5 Sonnet).

### Project 28: Real-Time Voice Assistant
Use the OpenAI Realtime API (or WebSockets + local Whisper/TTS) to build a low-latency voice-in, voice-out assistant.

### Project 29: Local SLM Fine-Tuning
Generate a small synthetic dataset using a large model, then use Unsloth to fine-tune a Llama-3-8B model locally on your specific data.

## Completion goal
You can handle vision, audio, and custom-trained local SLMs, matching the 2026 enterprise trend.

---

# PHASE 9 - PORTFOLIO + JOB PREP

## Resources

### 📘 Free Tools and Guides
- README template generator: https://www.makeareadme.com/
- Architecture diagram tool (free): https://app.diagrams.net/
- Demo recording (free tier): https://www.loom.com/
- Portfolio repo inspiration: https://github.com/practical-tutorials/project-based-learning
- AI Engineer job descriptions: search "AI Engineer" or "LLM Engineer" on LinkedIn and job boards for bullet-point language

## Minimum portfolio target
Finish with:
- 1 strong RAG app over enterprise knowledge with citations
- 1 workflow triage app
- 1 MCP or orchestration project with HITL approvals
- 1 productionized app **live at a real URL**
- clean GitHub READMEs
- screenshots / demos
- architecture diagrams
- resume bullets

## GitHub profile — employers look here first
- **Pin your best 4 repos** on your GitHub profile (go to your profile → Customize your pins)
- **Write a profile README** — create a repo named `<your-username>/<your-username>` with a README.md showing your stack, current focus, and links to your best projects
- **Star count matters** — if your capstone projects are good, share them in communities (Reddit r/LocalLLaMA, X/Twitter, LinkedIn) to get stars
- **Green contribution graph** — commit daily during the roadmap; a green graph signals active builder
- **Profile photo + location + title** — set `AI / GenAI Engineer` as your headline on GitHub and LinkedIn simultaneously

## Best portfolio set
1. Enterprise Knowledge RAG assistant with citations
2. Workflow triage assistant with safe tool calling
3. MCP-based workflow utility or agent integration
4. Productionized FastAPI AI app with traces, evals, snapshots, and an operations guide

## Resume story to prove
When these projects are done, the public story should read:

> Built production-style GenAI systems for enterprise workflows: RAG over internal knowledge, workflow triage, MCP tool integration, human approvals for sensitive actions, eval-gated CI, traceability, and reliability patterns.

## For every repo include
- problem statement
- architecture
- stack
- setup
- screenshots
- sample input/output
- limitations
- next improvements

## Completion goal
You are interview-ready with real proof.

---

# PHASE 10 - CERTIFICATIONS

## Resources

### 🔵 Microsoft Learn (free) ⭐ Official prep
- **Azure AI Fundamentals learning path** (free · interactive labs · official)  
  https://learn.microsoft.com/en-us/credentials/certifications/azure-ai-fundamentals/  
  → This IS the official prep. The content map matches the exam. Do these modules in order.
- **AI-900 study guide** (free PDF) — official exam skill outline  
  https://aka.ms/ai900-StudyGuide  
  → Download and use this as your checklist. Every bullet is fair game in the exam.

### 📘 Other free resources
- AWS Certified AI Practitioner (AIF-C01) exam guide:  
  https://aws.amazon.com/certification/certified-ai-practitioner/
- AWS Skill Builder (free tier): https://skillbuilder.aws/

## Rule
Certifications only after 2-3 strong projects.

## Options

### Option A: AI-900 / AI-901 ⭐ Recommended
Microsoft Certified: Azure AI Fundamentals
- **AI-900** is still available NOW and valid to take — $99 USD — take it if you reach Phase 9 before **June 30, 2026**
- Microsoft has already announced that **AI-901** will replace AI-900 after **June 30, 2026**. Check the certification page for current availability and exact handoff details: https://learn.microsoft.com/en-us/credentials/certifications/azure-ai-fundamentals/
- **Recommendation:** If you reach Phase 9 before June 30, 2026, AI-900 is still the straightforward path. After that date, follow Microsoft’s AI-901 path.
- Note: Microsoft’s current branding is shifting from **Azure AI Foundry** to **Microsoft Foundry**, so newer prep material and skill outlines increasingly use the newer name.

### Option B: AI-102
Microsoft Certified: Azure AI Engineer Associate
- https://learn.microsoft.com/en-us/learn/certifications/exams/ai-102
- https://learn.microsoft.com/en-us/credentials/certifications/azure-ai-engineer/
Note:
- Also **retires June 30, 2026** — Microsoft currently shows no announced direct replacement on the certification page

### Option C: AWS AIF-C01
AWS Certified AI Practitioner
- https://docs.aws.amazon.com/aws-certification/latest/ai-practitioner-01/ai-practitioner-01.html
- https://docs.aws.amazon.com/aws-certification/latest/userguide/ai-practitioner-01.html

## Recommendation
Only one cert initially.
Projects are the real proof.

---

# PHASE 11 - CAPSTONE: RESUME-GRADE PROJECTS

> Do this LAST — after Phases 1-10. These are the crown jewels of your portfolio. Each one combines everything you have learned into one polished, deployable, demo-able product.

## Why this phase matters
Recruiters look for projects they can understand and imagine using. A certificate says you watched videos. These projects say you built things that work.

---

## Project 30: Workflow Intelligence Command Center
**"Enterprise workflow copilot" — an AI console for knowledge-backed workflow automation**

Build a full-stack AI workflow console that feels useful across enterprise domains while still letting observability be one strong demo scenario:

| Feature | Tech |
|---------|------|
| Workflow intake | Paste alert, ticket, bug report, change request, support escalation, or review request text |
| Enterprise Knowledge RAG | Retrieve runbooks, support docs, API docs, ownership metadata, policy notes, and previous case notes |
| Triage summary | Priority/severity, likely owner, impact hypothesis, missing evidence |
| Evidence timeline | Summarize events from logs, comments, docs, and status updates |
| Suggested next actions | Read-only recommendations with citations and confidence |
| HITL approval | Explicit approval before any side-effect action is proposed |
| Observability | Langfuse/LangSmith traces, eval scores, latency/cost metrics |
| FastAPI backend + React or Streamlit frontend | Clean, deployable, Docker |

**Tell Copilot:** `generate repo scaffold for phase 11 project 30`  
**You're done when:** You can record a 3-minute Loom demo: paste a work item → retrieve cited evidence → produce a safe triage plan → show traces/eval results.

---

## Project 31: Multi-Agent Review + Knowledge Platform
**"Review assistant" — automated workflow review with human approval**

Given a fake workflow timeline, comments, logs, docs, and status updates, this system produces a polished review and proposes knowledge-base improvements:

| Feature | Tech |
|---------|------|
| Intake agent | Parses timeline, ticket comments, log snippets, and status updates |
| Evidence agent | Finds supporting docs and flags gaps |
| Impact agent | Drafts user/service impact and blast radius |
| Action-item agent | Extracts remediations, owners, and follow-ups |
| Critic/safety agent | Checks unsupported claims, blame language, and missing evidence |
| Writer agent | Produces review report, executive summary, and knowledge-base patch suggestion |
| Human-in-the-loop checkpoint | Approve/reject before final report or knowledge patch is written |
| LangGraph orchestration | Full stateful multi-agent graph with persistence |
| MCP server | Expose "analyze workflow" as an MCP tool usable from an IDE/agent |

**Tell Copilot:** `generate repo scaffold for phase 11 project 31`  
**You're done when:** You can demo fake workflow data → cited review → approved knowledge update proposal in under 5 minutes.

---

## Project 32: Personal AI Dev/Workflow Copilot
**"My Copilot" — a coding, knowledge, and workflow assistant**

An MCP server + agent that integrates into your daily developer life:

| Feature | Tech |
|---------|------|
| Code review tool | Send a diff → get structured review with severity ratings |
| PR description generator | Git diff input → professional PR description |
| Ticket-to-code planner | Jira/GitHub issue → implementation plan + skeleton code |
| Work-item investigation planner | Alert/ticket/change text → evidence checklist + likely docs |
| Knowledge article generator | Notes or incident details → draft troubleshooting/support docs |
| Doc generator | Python function → docstring + README section |
| Daily standup generator | Git log + Jira comments → formats standup update |
| Slack/Teams message drafter | Context → professional message |
| Runs as MCP server | Usable from Claude Desktop, VS Code Copilot |
| Runs as FastAPI service | Also usable as REST API / webhook |
| Configurable persona | System prompt tuned to your stack and preferences |

**Tell Copilot:** `generate repo scaffold for phase 11 project 32`  
**You're done when:** You use it yourself every day for coding and roadmap work, and it is in your GitHub profile README as a production-minded MCP project.

---

## Resources (reference only — you already know enough by now)

### 🟢 DeepLearning.AI (free)
- **AI Agentic Design Patterns with AutoGen** — Multi-agent patterns, reflection, code execution agents.  
  https://www.deeplearning.ai/short-courses/ai-agentic-design-patterns-with-autogen/

### 📘 Official Docs
- LangGraph advanced: https://langchain-ai.github.io/langgraph/concepts/
- OpenAI GPT-4o vision: https://platform.openai.com/docs/guides/vision
- OpenAI Audio/TTS: https://platform.openai.com/docs/guides/text-to-speech
- OpenAI Whisper STT: https://platform.openai.com/docs/guides/speech-to-text
- python-pptx: https://python-pptx.readthedocs.io/
- Tavily search API: https://docs.tavily.com/

---

# 8H/DAY EXECUTION PLAN — ALL-IN MODE

> You have the time. Here's exactly how to use it. 8h/day, no bullshit.  
> **Rule:** 20% watching/reading, 80% building. If you're not writing code, you're wasting time.

## Week 1 — Foundation + first apps
| Day | What | Hours |
|-----|------|-------|
| Mon | Pluralsight: GenAI Foundations (2h) + DLAI Prompt Engineering (1h) + read OpenAI prompt guide + Projects 1-2 (Prompt Playground + Summarizer) | 8h |
| Tue | Finish Project 2, build Project 3 (Rewriter), read OpenAI docs overview + models page | 8h |
| Wed | Pluralsight: OpenAI for Developers — first 5 courses (Chat Completions, Responses API, streaming, structured outputs) | 8h |
| Thu | Pluralsight: OpenAI for Developers — next 5 courses (function calling, embeddings, moderation, evals) | 8h |
| Fri | LangChain DLAI course (1.5h) + LangChain Academy intro (1.5h) + start Project 4 (CLI chatbot) | 8h |
| Sat | Finish Project 4. Start Project 5 (FastAPI GenAI service) | 8h |
| Sun | Finish Project 5. Polish both. Push to GitHub with clean READMEs. | 8h |

## Week 2 — Structured extraction + RAG entry
| Day | What | Hours |
|-----|------|-------|
| Mon | Projects 6 + 7 (Structured Extractor + Resume Analyzer) — build both | 8h |
| Tue | Finish Projects 6 + 7. Read structured outputs docs fully. | 8h |
| Wed | Pluralsight: Vector DBs (43min) + DLAI: Advanced Retrieval for Chroma (52min) + run LangChain RAG tutorial | 8h |
| Thu | Project 8: Semantic Search Prototype — build + embed + query + score | 8h |
| Fri | DLAI: Building and Evaluating Advanced RAG (1h) + Project 9 (PDF Q&A) start | 8h |
| Sat | Finish Project 9. Citations, source attribution, chunking comparison | 8h |
| Sun | Projects 10 + 11 (Docs Assistant + Enterprise Knowledge Bot) — build both | 8h |

## Week 3 — Tool calling + workflow automation
| Day | What | Hours |
|-----|------|-------|
| Mon | Read OpenAI function calling docs fully + Pluralsight function calling (38min) + Project 12 start | 8h |
| Tue | Finish Project 12 (Tool-Using Assistant). 5 tools minimum. | 8h |
| Wed | DLAI: Functions, Tools, Agents with LangChain (1h44m) + Project 13 (Research Assistant) start | 8h |
| Thu | Finish Project 13. Web retrieval + synthesis + citations + "I don't know" handling | 8h |
| Fri | Projects 14 + 15 (SQL Assistant + Workflow Triage) — build both | 8h |
| Sat | Finish Projects 14 + 15. Push all Phase 4 projects. | 8h |
| Sun | Read: OWASP LLM Top 10, DeepEval quickstart, OpenAI evals guide | 8h |

## Week 4 — Evals + safety + observability
| Day | What | Hours |
|-----|------|-------|
| Mon | Project 16: Eval Suite — build 30 workflow/knowledge/triage test cases + pytest + DeepEval | 8h |
| Tue | Add LLM-as-a-Judge metric, groundedness checks, CI integration | 8h |
| Wed | Project 17: Productionize a workflow AI app — logging, retries, caching, metrics, operations guide | 8h |
| Thu | Project 17a: DSPy optimizer + Project 17b: GitHub Actions CI/CD | 8h |
| Fri | Project 17c: OWASP security scanner — prompt injection guards, tool scope limits | 8h |
| Sat | DLAI: NeMo Agent Toolkit (45min) + Semantic Caching (30min) + Red Teaming (1h) | 8h |
| Sun | LangSmith setup + add tracing to one existing app. Polish all Phase 5 work. | 8h |

## Week 5 — MCP + LangGraph
| Day | What | Hours |
|-----|------|-------|
| Mon | Read MCP docs (all core sections) + Python SDK quickstart + Projects 18-19 (workflow context MCP servers) | 8h |
| Tue | LangGraph Academy: Introduction to LangGraph (~6h self-paced) — do all 55 lessons | 8h |
| Wed | Continue LangGraph Academy + run all code examples | 8h |
| Thu | Project 20 (MCP-Powered Workflow Agent) + DLAI: AI Agents in LangGraph (1.5h) | 8h |
| Fri | Projects 21 + 22 (HITL SQL + HITL File Agent) | 8h |
| Sat | Project 23 (Stateful Workflow Automation — resume after interrupt) | 8h |
| Sun | Project 24 (Multi-Agent orchestration with LangGraph) | 8h |

## Week 6 — Agents, multimodal, AI dev productivity
| Day | What | Hours |
|-----|------|-------|
| Mon | DLAI: A2A Protocol (1h27m) + Gemini CLI (1h) + Spec-Driven Dev (45min) | 8h |
| Tue | Project 25: Personal Dev Productivity Agent | 8h |
| Wed | Project 26: Local AI Coding Utility (Ollama + MCP + tool call loop) | 8h |
| Thu | DLAI: E2B Coding Agents (1h) + Project 27: Vision-Based Data Extractor | 8h |
| Fri | Project 28: Real-Time Voice Assistant (Realtime API) | 8h |
| Sat | Project 29: Local SLM Fine-Tuning (Unsloth + Llama 3.2 3B) | 8h |
| Sun | Portfolio cleanup: pin 4 repos, write profile README, update all project READMEs | 8h |

## Week 7-8 — Capstone projects
| Period | What |
|--------|------|
| Days 1-4 | Project 30: Workflow Intelligence Command Center (enterprise knowledge RAG + triage + observability) |
| Days 5-8 | Project 31: Multi-Agent Review + Knowledge Platform (LangGraph + MCP + HITL) |
| Days 9-12 | Project 32: Personal AI Dev/Workflow Copilot (MCP server + FastAPI) |
| Days 13-14 | AI-900 prep (MS Learn free path, ~8h) + take exam |

---

**Total time to portfolio-ready: ~8 weeks if you do the 8h/day.**  
**The 3 capstone projects + 4 clean mid-phase repos = what you interview with.**

---

# 12-WEEK FAST EXECUTION VERSION

> Legacy plan, kept for reference. Use the 8h/day plan above instead if you're serious about moving fast.

## Weeks 1-2
- Foundations
- Prompt Playground
- Summarizer
- Rewriter

## Weeks 3-4
- Developer paths
- CLI chatbot
- FastAPI GenAI service
- extractor

## Weeks 5-6
- embeddings
- vector search
- semantic search prototype
- PDF Q&A app

## Weeks 7-8
- docs assistant
- enterprise knowledge bot
- tool calling
- tool-using assistant

## Weeks 9-10
- research assistant
- SQL/report assistant
- eval dataset
- production hardening start

## Weeks 11-12
- workflow context MCP server
- MCP-powered workflow agent integration
- one HITL workflow
- portfolio cleanup

---

# NON-NEGOTIABLE RULES

1. Projects > certs
2. Must build one strong RAG app
3. Must build one tool-calling/workflow app
4. Must build one eval suite
5. Must build one MCP-related project
6. Must build one productionized app
7. Learn LangGraph after simpler workflows
8. Prefer 4 polished projects over many incomplete ones

---

# STEP-BY-STEP ACTION PLAN

Work through these in exact order. Each step tells you what URL to open, what to watch, and what to build. Never skip ahead.

---

- [x] **Step 1 — ✅ DONE**
  **Created GenAI Python Starter Template**
  → Built at: `projects/p0-genai-starter-template/`
  → Run locally: `cd projects/p0-genai-starter-template && make run`

---

- [ ] **Step 2 — ⏳ DO THIS NOW**
  **Watch: Generative AI Foundations** (~3h total)
  🎯 Goal: Understand LLMs, tokens, context windows, and prompting before writing more code.

  | Resource | Duration | URL |
  |----------|----------|-----|
  | Generative AI Foundations — Pluralsight 🟡 | ~2h · 4 courses | https://www.pluralsight.com/paths/generative-ai-foundations |
  | Prompt Engineering — Pluralsight 🟡 | ~5h · 4 courses | https://www.pluralsight.com/paths/prompt-engineering-and-generative-ai |
  | ChatGPT Prompt Engineering for Developers — DeepLearning.AI 🟢 | ~1h FREE | https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/ |

  **You're done when you can answer:**
  - What are tokens and context windows?
  - What does temperature control and when do you change it?
  - What is hallucination and how do you reduce it?
  - Difference between zero-shot, few-shot, and chain-of-thought?

---

- [ ] **Step 3 — Build Project 1: Prompt Playground**
  **Tell Copilot:** `generate repo scaffold for phase 1 project 1`
  🎯 Goal: Get hands-on with the API. Compare prompt styles on the same input.

  **Exact build:**
  - Python script that sends the same task through 4 prompt strategies
  - Zero-shot / few-shot / role+system message / chain-of-thought
  - Print side-by-side output comparison with labels
  - Use `openai.chat.completions.create()` directly — no LangChain yet
  - **Reference:** https://platform.openai.com/docs/guides/prompt-engineering

---

- [ ] **Step 4 — Build Project 2: Summarizer**
  **Tell Copilot:** `generate repo scaffold for phase 1 project 2`
  🎯 Goal: Build a real, usable tool — something your colleagues could use today.

  **Exact build:**
  - FastAPI app — `POST /summarize`
  - Input: `{ "text": "...", "format": "paragraph|bullets|action_items" }`
  - Output: summarized text in requested format
  - Test with a long article or meeting transcript

---

- [ ] **Step 5 — Build Project 3: Rewriter**
  **Tell Copilot:** `generate repo scaffold for phase 1 project 3`
  🎯 Goal: Practice controlled tone/style prompting.

  **Exact build:**
  - FastAPI app — `POST /rewrite`
  - Input: `{ "text": "...", "tone": "professional|concise|technical|friendly" }`
  - Output: rewritten text
  - Stretch: add a diff showing original vs rewritten

---

- [x] **Step 6 — ✅ DONE (partially) — Python LLM App Development Courses**
  Completed: OpenAI for Developers (Pluralsight) + LangChain for LLM App Dev + LangChain Academy intro.  
  The Pluralsight path plus free Microsoft Learn/DLAI resources covers what you need for this phase.

---

- [x] **Step 7 — Build Project 4: CLI Chatbot** — ✅ DONE
  **Tell Copilot:** `generate repo scaffold for phase 2 project 4`
  🎯 Goal: Build conversation history, personas, and a clean CLI interface.

  **Exact build:**
  - CLI script: `python -m src.main`
  - Maintains conversation history (messages list pattern)
  - Switch persona via `--persona` flag (e.g. `--persona senior-engineer`)
  - Slash commands for save/export/stats/undo/clear
  - ✅ Built at: `projects/p4-cli-chatbot/`
  - ✅ Verified with local Ollama model: `qwen2.5:1.5b`

---

- [x] **Step 8 — Build Project 5: FastAPI GenAI Service** — ✅ DONE
  **Tell Copilot:** `generate repo scaffold for phase 2 project 5`
  🎯 Goal: Production-style multi-endpoint GenAI API — use p0 template as your base.

  **Exact build:**
  - `POST /summarize` / `POST /rewrite` / `POST /classify` / `POST /extract`
  - Pydantic schemas for all request/response types
  - Proper error handling, timeouts, retries
  - Docker ready + README with curl examples
  - ✅ Built at: `projects/p5-fastapi-genai-service/`
  - ✅ Verified with unit/API tests and local Ollama `/summarize` smoke test
  - ⚠️ Dockerfile added; Docker build waits for Docker daemon/Desktop to be running

---

- [x] **Step 9 — Build Project 6: Structured Data Extractor** — ✅ DONE
  **Tell Copilot:** `generate repo scaffold for phase 2 project 6`
  🎯 Goal: Extract structured JSON reliably from messy real-world text.

  **Exact build:**
  - Input: raw unstructured text (email, description, receipt, etc.)
  - Output: structured JSON matching a Pydantic model
  - Use OpenAI JSON mode / structured outputs
  - Test with 10+ examples of different messy inputs
  - **Reference:** https://platform.openai.com/docs/guides/structured-outputs
  - ✅ Built at: `projects/p6-structured-data-extractor/`
  - ✅ Verified with unit tests and local Ollama prompt-and-validate smoke test
  - ✅ Includes prompt mode, Chat Completions schema mode, Responses API schema mode, and validation reports

---

- [x] **Step 10 — Build Project 7: Resume vs JD Analyzer** — ✅ DONE
  **Tell Copilot:** `generate repo scaffold for phase 2 project 7`
  🎯 Goal: A real tool with structured multi-step prompting — great portfolio piece.

  **Exact build:**
  - Input: resume text + job description text
  - Output: `{ "fit_score": 82, "matching_skills": [...], "missing_skills": [...], "suggestions": [...] }`
  - Use structured output (JSON schema)
  - Add a CLI and/or FastAPI endpoint
  - ✅ Built at: `projects/p7-resume-vs-jd-analyzer/`
  - ✅ Verified with unit tests and local Ollama prompt-and-validate smoke test
  - ✅ Includes multi-document prompting, structured outputs, deterministic score blending, evidence items, and token usage metadata

---

- [ ] **Step 11 — Watch: Embeddings and RAG Courses** (~2h) ← **DO THIS NOW**
  🎯 Goal: Understand how embeddings work before touching a vector store.

  | Resource | Duration | URL |
  |----------|----------|-----|
  | Vector Databases and Embeddings for Developers 🟡 | 43min | https://www.pluralsight.com/courses/developers-vector-databases-embeddings |
  | Advanced Retrieval for AI with Chroma 🟢 | 52min FREE | https://www.deeplearning.ai/short-courses/advanced-retrieval-for-ai/ |
  | OpenAI Embeddings guide (read) 📘 | 15min | https://platform.openai.com/docs/guides/embeddings |

  **You're done when you can answer:**
  - What is cosine similarity and why does it matter?
  - What is chunking and how do you choose chunk size?
  - Why is hybrid search (BM25 + vector) better than pure vector in production?

---

- [ ] **Step 12 — Build Project 8: Semantic Search Prototype**
  **Tell Copilot:** `generate repo scaffold for phase 3 project 8`
  🎯 Goal: Your first working semantic search — embeddings → vector store → ranked results.

  **Exact build:**
  - Load 20-50 text documents (README files, articles, anything you have)
  - Chunk them → embed with OpenAI embeddings API → store in Chroma (local)
  - CLI: type a query → get top-5 most semantically similar chunks
  - Show similarity score + source document name
  - **Reference:** https://docs.trychroma.com/ and https://python.langchain.com/docs/tutorials/rag/

---

# WHEN I ASK COPILOT

If I ask:
- **"what next?"** → show highest-value unfinished task from the checklist
- **"mark X done"** → tick `[x]` on that project/task in the checklist, update Overall count, update Current Focus and Phase Summary
- **"show pending"** → list all unchecked `[ ]` items
- **"show phase N"** → show tasks and status for that phase
- **"summarize progress"** → show completed count, pending count, current focus, and next recommendation
- **"suggest next project"** → recommend the highest-leverage next unchecked project
- **"generate repo scaffold for phase X project"** → scaffold the project
- **"I'm starting X"** → update Current Focus to that project
- **"update last updated date"** → update the date at the top of the Progress Tracker
