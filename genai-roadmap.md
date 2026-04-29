# Final Best GenAI Roadmap for a Python Developer (2026)
Last updated: 2026-04-28

> Verification note (2026-04-29): Re-checked against official OpenAI, Microsoft, Anthropic, Google A2A, and LangChain Academy sources. The biggest updates are: use the OpenAI `Responses API` for new builds, treat the `Assistants API` as legacy/deprecating, account for `AI-900` retirement on **June 30, 2026**, and give more weight to MCP, remote MCP, agent evals, A2A, and the latest specialized agent frameworks (PydanticAI for type-safety, smolagents for code-first execution).

## Goal
Transition from Python Software Engineer to:
- GenAI Engineer
- LLM Application Developer
- Applied AI Engineer
- AI Backend Engineer
- Agentic Systems Engineer

## 2026 GenAI Industry Trends
> These are the high-signal topics the industry is actively hiring and building around in 2026. Prioritize them.

| Trend | Why It Matters | Covered In |
|-------|---------------|------------|
| **Agentic Systems** (LangGraph, CrewAI, PydanticAI) | The dominant engineering paradigm — agents planning and executing multi-step tasks autonomously | Phase 6 |
| **Model Context Protocol (MCP)** | Industry-standard "USB-C for AI" — standardizes how agents connect to tools, files, and databases | Phase 6 |
| **A2A (Agent-to-Agent Protocol)** | Google/Linux Foundation standard for agents collaborating cross-framework (LangGraph ↔ CrewAI ↔ ADK) | Phase 6 |
| **Reasoning-First Models** (o1/o3, DeepSeek-R1) | Chain-of-thought deliberation loops — know when to use expensive reasoning vs fast generalist models | Phase 2 |
| **GraphRAG & Knowledge Fabrics** | Moving beyond flat vector search to handle multi-hop reasoning and entity relationships | Phase 3 |
| **Programmatic Prompting** (DSPy) | Replacing manual prompt engineering with compiled, metric-optimized prompt weights | Phase 5 |
| **Evals-as-Code (EDD)** | AI is non-deterministic — treat prompts like code with CI-integrated test suites (DeepEval, LangSmith) | Phase 5 |
| **AI Security & Prompt Injection** | OWASP LLM Top 10 — every production AI app needs guardrails | Phase 5 |
| **CI/CD for AI Apps** | Automated eval pipelines on every PR, LLM-as-a-Judge regression checks | Phase 5 |
| **Multimodal** (Vision, Audio, Video) | GPT-4o vision, Whisper STT, TTS — first-class in capstone projects | Phase 10 |
| **Local Models** (Ollama, LM Studio, llama.cpp) | Cost/privacy/air-gap — know when open-weights beats hosted | Phases 2, 7 |

## What gets you hired after this roadmap:
1. 2-3 polished GitHub repos that work end-to-end (not half-finished)
2. One live deployed app (not just localhost) with a real URL
3. Can explain your RAG architecture, chunking strategy, evaluation approach
4. Can build and expose a tool/function-calling flow from scratch
5. Understands agents, state, HITL — can talk about tradeoffs

**What this roadmap does NOT teach (and that's fine):**
- Pre-training / fine-tuning large models from scratch (that's ML research, not applied AI engineering)
- Deep ML maths (not needed for most GenAI roles)
- Kubernetes / SRE (infrastructure — you'd learn that on the job)

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
> Last updated: 2026-04-22

## Current Focus
**Phase:** Phase 2 — Python LLM App Development  
**Working on:** Course 4/5 — Generative AI Fundamentals of AWS — **IN PROGRESS**
**Status:** 🟡 In Progress — studying Phase 2 courses

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
10. 🟡 **NOW → Phase 2: Python LLM App Development** ← *you are here*
    - ✅ ~~OpenAI for Developers~~ — DONE
    - ✅ ~~Generative AI for Developers~~ — DONE
    - ✅ ~~Generative AI Integration for Developers~~ — DONE
    - ✅ ~~Generative AI Fundamentals of AWS~~ — DONE
    - 📖 **Studying: Using Generative AI in Azure and Microsoft Power Platform** (QA Platform, ~1h 22m)

## Phase Summary
| Phase | Name | Status |
|-------|------|--------|
| 0 | Software Baseline | ✅ Done |
| 1 | Foundations | ✅ Done |
| 2 | Python LLM App Development | 🟡 In Progress |
| 3 | Embeddings + Vector Search + RAG | ⬜ Not Started |
| 4 | Tool Calling + Workflow Automation | ⬜ Not Started |
| 5 | Evals + Safety + Observability | ⬜ Not Started |
| 6 | MCP + Agentic Orchestration | ⬜ Not Started |
| 7 | AI-Native Developer Productivity | ⬜ Not Started |
| 8 | Multimodal, Real-Time AI, & SLMs | ⬜ Not Started |
| 9 | Portfolio + Job Prep | ⬜ Not Started |
| 10 | Certifications | ⬜ Not Started |
| 11 | Capstone: Resume-Grade Projects | ⬜ Not Started |

**Overall: 4 / 33 projects done**

## Project Checklist

### Phase 0 — Software Baseline
- [x] Project 0: GenAI Python starter template

### Phase 1 — Foundations
- [x] Project 1: Prompt Playground
- [x] Project 2: Summarizer
- [x] Project 3: Rewriter

### Phase 2 — Python LLM App Development
- [ ] Project 4: CLI Chatbot
- [ ] Project 5: FastAPI GenAI Service
- [ ] Project 6: Structured Data Extractor
- [ ] Project 7: Resume vs JD Analyzer

### Phase 3 — Embeddings + Vector Search + RAG
- [ ] Project 8: Semantic Search Prototype
- [ ] Project 9: PDF Q&A Assistant
- [ ] Project 10: Docs Knowledge Assistant
- [ ] Project 11: Support Knowledge Bot
- [ ] Project 11a: GraphRAG Document Explorer

### Phase 4 — Tool Calling + Workflow Automation
- [ ] Project 12: Tool-Using Assistant
- [ ] Project 13: Research Assistant
- [ ] Project 14: SQL / Reporting Assistant
- [ ] Project 15: Ticket Triage Assistant

### Phase 5 — Evals + Safety + Observability
- [ ] Project 16: Eval Suite
- [ ] Project 17: Productionize One App
- [ ] Project 17a: DSPy Prompt Optimizer
- [ ] Project 17b: CI/CD Pipeline for AI
- [ ] Project 17c: OWASP LLM Security Scanner

### Phase 6 — MCP + Agentic Orchestration
- [ ] Project 18: Simple MCP Server
- [ ] Project 19: Python MCP Utility Server
- [ ] Project 20: MCP-Powered Agent Integration
- [ ] Project 21: HITL SQL Assistant
- [ ] Project 22: HITL File Action Agent
- [ ] Project 23: Stateful Research Workflow
- [ ] Project 24: Orchestration & Multi-Agent

### Phase 7 — AI-Native Developer Productivity
- [ ] Project 25: Personal Dev Productivity Agent
- [ ] Project 26: Local AI Coding Utility

### Phase 8 — Multimodal, Real-Time AI, & SLMs
- [ ] Project 27: Vision-Based Data Extractor
- [ ] Project 28: Real-Time Voice Assistant
- [ ] Project 29: Local SLM Fine-Tuning

### Phase 11 — Capstone: Resume-Grade Projects
- [ ] Project 30: Unified AI Assistant (ChatGPT clone — voice, vision, files, memory)
- [ ] Project 31: Multi-Agent Research & Report Platform
- [ ] Project 32: Personal AI Dev Copilot

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

### 🟡 Pluralsight (paid)
- **Generative AI Foundations** (4 courses · 2h) — What GenAI is, prompt engineering basics, ethics, GenAI in action.  
  https://www.pluralsight.com/paths/generative-ai-foundations
- **Prompt Engineering** (4 courses · 2 labs · 5h) — Getting started, best practices, advanced techniques.  
  https://www.pluralsight.com/paths/prompt-engineering-and-generative-ai
- **Large Language Models (LLM)** (4 courses · 4h) — Transformers, RLHF, foundation models, practical LLM application.  
  https://www.pluralsight.com/paths/large-language-models-llm

### 🔵 QA Platform (paid)
- **Intro to Generative AI** (49min · Beginner) — Gentle overview, business context, future of GenAI.  
  https://platform.qa.com/learning-paths/intro-to-generative-ai-13286/
- **AI-900 Exam Prep: Azure AI Fundamentals** (9h46m · Beginner) — Azure AI concepts, responsible AI principles.  
  https://platform.qa.com/learning-paths/ai-900-exam-preparation-microsoft-azure-ai-fundamentals-1968/

### 🟢 DeepLearning.AI (free)
- **ChatGPT Prompt Engineering for Developers** (1h · Beginner) — Andrew Ng + OpenAI. Zero-shot, few-shot, chain-of-thought prompting.  
  https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/
- **Generative AI for Everyone** (3h · Beginner) — Andrew Ng. Broad, accessible overview of GenAI concepts.  
  https://www.deeplearning.ai/courses/generative-ai-for-everyone/

### 📘 Official Docs (free)
- OpenAI Platform Docs: https://platform.openai.com/docs/
- OpenAI Prompt Engineering Guide: https://platform.openai.com/docs/guides/prompt-engineering
- Microsoft Learn — AI Fundamentals path: https://learn.microsoft.com/en-us/training/paths/get-started-with-artificial-intelligence-on-azure/

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

### 🟡 Pluralsight (paid)
- **Generative AI for Developers** (7 courses · 6h) — Models, parameters, vector DBs, embeddings, agentic AI concepts, data privacy, prompt engineering.  
  https://www.pluralsight.com/paths/generative-ai-for-developers
- **OpenAI for Developers** (13 courses · 2 labs · 12h) — Full OpenAI API: prompts, function calling, Responses API, Agents SDK, embeddings, moderation, evals, multimodal, Codex.  
  https://www.pluralsight.com/paths/openai-for-developers
- **Generative AI Integration for Developers** (6 courses · 4h) — Integrating GenAI, aligning with business cases, security, cost management, scaling.  
  https://www.pluralsight.com/paths/generative-ai-integration-for-developers

### 🔵 QA Platform (paid)
- **Generative AI Fundamentals of AWS** (5 lessons · 2h23m · Beginner) — GenAI services and patterns on AWS.  
  https://platform.qa.com/learning-paths/generative-ai-fundamentals-of-aws-13866/
- **Using Generative AI in Azure and Microsoft Power Platform** (4 lessons · 1h22m · Beginner)  
  https://platform.qa.com/learning-paths/using-generative-ai-in-azure-and-microsoft-power-platform-11921/

### 🟢 DeepLearning.AI (free)
- **LangChain for LLM Application Development** (1h38m · Beginner) — Models, prompts, memory, chains, Q&A, and agents with LangChain. By Harrison Chase.  
  https://www.deeplearning.ai/short-courses/langchain-for-llm-application-development/

### 🎓 LangChain Academy (free)
- **Introduction to LangChain: Build AI Agents with Python** (free · ~1.5h) — Newer official LangChain Academy foundation course covering tools, short-term memory, MCP, multi-agent systems, and HITL patterns. Use this as a modern complement to the older DeepLearning.AI LangChain short course.  
  https://academy.langchain.com/courses/foundation-introduction-to-langchain-python

### 📘 Official Docs (free)
- OpenAI API Reference: https://platform.openai.com/docs/api-reference/
- OpenAI Cookbook (code examples): https://cookbook.openai.com/
- OpenAI Responses vs Chat Completions: https://platform.openai.com/docs/guides/migrate-to-responses
- OpenAI Structured Outputs guide: https://platform.openai.com/docs/guides/structured-outputs
- openai-python library: https://github.com/openai/openai-python
- Real Python async guide: https://realpython.com/async-io-python/

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

```bash
# Install Ollama first: https://ollama.com
brew install ollama

# Best everyday model — fast + smart
ollama run qwen3:14b

# Best coding model
ollama run qwen3:14b  # or qwen2.5-coder:14b

# Reasoning model (like a local o1)
ollama pull deepseek-r1:14b

# Tiny but surprisingly capable
ollama run phi4:latest

# Vision model (multimodal)
ollama run llava:13b
```

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

### 🟡 Pluralsight (paid)
- **Generative AI for Developers** — Includes "Vector Databases and Embeddings for Developers" module (43min).  
  https://www.pluralsight.com/paths/generative-ai-for-developers
- Individual course: **Vector Databases and Embeddings for Developers** (43min)  
  https://www.pluralsight.com/courses/developers-vector-databases-embeddings
- Individual course: **OpenAI Embeddings API** (31min)  
  https://www.pluralsight.com/courses/openai-embeddings-api

### 🔵 QA Platform (paid)
- **Enhancing Generative AI Models with RAG** (hands-on lab · 30min · Beginner) — Build a RAG pipeline end-to-end.  
  https://platform.qa.com/lab/enhancing-generative-ai-models-with-retrieval-augmented-generation-rag/
- **Building Generative AI Applications with Amazon Bedrock** (10h28m · Intermediate) — Covers RAG patterns on AWS.  
  https://platform.qa.com/learning-paths/building-generative-ai-applications-with-amazon-bedrock-14069/

### 🟢 DeepLearning.AI (free)
- **Advanced Retrieval for AI with Chroma** (52min · Intermediate) — Query expansion, cross-encoder reranking, embedding adapters. Production RAG techniques.  
  https://www.deeplearning.ai/short-courses/advanced-retrieval-for-ai/
- **Building and Evaluating Advanced RAG** — Sentence-window retrieval, auto-merging retrieval, RAG triad evaluation.  
  https://www.deeplearning.ai/short-courses/building-evaluating-advanced-rag/

### 🤗 Hugging Face (free) ⭐ Don’t skip this
- **sentence-transformers** — The industry-standard Python library for open-source embeddings. Used in production RAG everywhere. Faster and cheaper than OpenAI embeddings for high-volume use.  
  https://sbert.net/ | install: `pip install sentence-transformers`
- **Hugging Face Hub** — Browse 800K+ models. Know how to load an embedding model or a small LLM with `transformers` pipeline. Employers expect basic HF literacy.  
  https://huggingface.co/docs/transformers/quicktour
- **MTEB Leaderboard** — How to pick the best embedding model for your task.  
  https://huggingface.co/spaces/mteb/leaderboard
- **Ollama** — Run Llama 3, Mistral, Gemma, Phi-3 locally. Must-have for local RAG + cost experiments.  
  https://ollama.com/

### 📘 Official Docs (free)
- LangChain RAG tutorial: https://python.langchain.com/docs/tutorials/rag/
- Chroma docs: https://docs.trychroma.com/
- Qdrant docs: https://qdrant.tech/documentation/
- pgvector (Postgres vector): https://github.com/pgvector/pgvector
- OpenAI embeddings guide: https://platform.openai.com/docs/guides/embeddings
- OpenAI file search guide: https://platform.openai.com/docs/guides/tools-file-search

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
Use markdown/docs/READMEs.

### Project 11: Support Knowledge Bot
Answer from support docs only and refuse unsupported answers.

### Project 11a: GraphRAG Document Explorer
Build a knowledge graph to answer multi-hop reasoning questions over a complex text corpus using LightRAG or Microsoft GraphRAG principles.

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

### 🔵 QA Platform (paid)
- **Employing Generative AI for Development with Amazon Bedrock** (lab · 1h30m · Beginner) — LLM development with tool-like patterns.  
  https://platform.qa.com/lab/employing-generative-ai-for-development-with-amazon-bedrock/

### 🟢 DeepLearning.AI (free)
- **Functions, Tools and Agents with LangChain** (1h44m · Intermediate) — Function calling, LCEL, tagging, extraction, tool routing, conversational agents. By Harrison Chase.  
  https://www.deeplearning.ai/short-courses/functions-tools-agents-langchain/
- **LangChain for LLM Application Development** — Agents and tools section covers tool selection.  
  https://www.deeplearning.ai/short-courses/langchain-for-llm-application-development/

### 📘 Official Docs (free)
- OpenAI Function Calling guide: https://platform.openai.com/docs/guides/function-calling
- OpenAI Tools guide: https://platform.openai.com/docs/guides/tools
- OpenAI remote MCP / connectors guide: https://platform.openai.com/docs/guides/tools-remote-mcp
- LangChain tools docs: https://python.langchain.com/docs/concepts/tools/
- OpenAI Agents SDK docs: https://openai.github.io/openai-agents-python/

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

### Project 13: Research Assistant
Retrieve docs/web content, synthesize, cite, and say when unsure.

### Project 14: SQL / Reporting Assistant
Generate read-only SQL safely.

### Project 15: Ticket Triage Assistant
Classify, prioritize, route, draft response.

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

### 🔵 QA Platform (paid)
- Individual lesson: **Generative AI — Concerns and Ethics** (12min · Beginner)  
  https://platform.qa.com/course/concerns-ethics-generative-ai-5034/
- Individual lesson: **Designing Responsible Generative AI** (14min · Beginner)  
  https://platform.qa.com/course/designing-responsible-generative-ai-1/

### 🟢 DeepLearning.AI (free)
- **Building and Evaluating Advanced RAG** — RAG triad: answer relevance, context relevance, groundedness evals.  
  https://www.deeplearning.ai/short-courses/building-evaluating-advanced-rag/
- **Red Teaming LLM Applications** — Identify and fix vulnerabilities, jailbreaks, and prompt injection attacks.  
  https://www.deeplearning.ai/short-courses/red-teaming-llm-applications/

### 🎓 LangChain Academy (free)
- **Quickstart: LangSmith Essentials** (free · ~1h) — Practical tracing, feedback loops, and evaluation workflow for agent applications.  
  https://academy.langchain.com/courses/langsmith-essentials
- **Foundation: Introduction to Agent Observability & Evaluations** (free) — Strong addition for 2026-style agent eval workflows.  
  https://academy.langchain.com/

### 📘 Official Docs (free)
- LangSmith docs (tracing + evals): https://docs.smith.langchain.com/
- Langfuse docs (open-source observability): https://langfuse.com/docs
- Arize Phoenix (open-source evals + tracing): https://docs.arize.com/phoenix
- DeepEval framework (pytest-integrated evals): https://docs.confident-ai.com/
- OpenAI moderation guide: https://platform.openai.com/docs/guides/moderation
- OpenAI agent evals guide: https://platform.openai.com/docs/guides/agent-evals
- OpenAI evals guide: https://platform.openai.com/docs/guides/evals
- OpenAI evaluation best practices: https://platform.openai.com/docs/guides/evaluation-best-practices
- OWASP LLM Top 10 (2025): https://owasp.org/www-project-top-10-for-large-language-model-applications/
- GitHub Actions CI/CD docs: https://docs.github.com/en/actions

## Learn: Evals & Reliability
- evaluation datasets and golden test sets
- regression tests for prompts — treat prompts as code with version control
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
  - Eval tests: check output quality on golden dataset (probabilistic, use threshold pass/fail)
- **Rollback strategy:** canary deployments; monitor latency and quality metrics before full rollout

## Projects
### Project 16: Eval Suite
Create 30-50 test cases for one app:
- golden dataset with expected outputs
- pytest + DeepEval integration
- LLM-as-a-Judge metric for subjective quality
- groundedness check for any RAG outputs
- CI-ready: run eval suite automatically on push

### Project 17: Productionize One App
Add:
- logging
- retries
- timeouts
- caching
- metrics
- failure handling
- prompt versioning (prompts as files, tracked in git)
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

### 🟡 Pluralsight (paid)
- Individual course: **Agentic AI for Developers** (1h24m · Intermediate) — Agentic patterns, tool use, orchestration loops.  
  https://www.pluralsight.com/courses/agentic-ai-developers
- Individual course: **OpenAI Responses API and Agents SDK** (45min) — Build agents with the official OpenAI SDK.  
  https://www.pluralsight.com/courses/openai-responses-api-agents-sdk
- Individual course: **Developing AI Agents with OpenAI AgentKit** (1h24m)  
  https://www.pluralsight.com/courses/developing-ai-agents-openai-agentkit

### 🔵 QA Platform (paid)
- Individual lesson: **Extending Agents with AWS Lambda and Step Functions** (37min · Intermediate) — Serverless agent patterns.  
  https://platform.qa.com/course/extending-agents-with-aws-lambda-and-step-functions/
- Hands-on lab: **Orchestrating Generative AI Applications with AWS Step Functions and Amazon Bedrock** (1h15m) — Prompt chaining, stateful AI orchestration.  
  https://platform.qa.com/lab/orchestrating-generative-ai-applications-with-aws-step-functions-and-amazon-bedrock/

### 🟢 DeepLearning.AI (free)
- **AI Agents in LangGraph** (1h32m · Intermediate) — Build agents from scratch, LangGraph components, persistence, human-in-the-loop. By Harrison Chase (LangChain CEO).  
  https://www.deeplearning.ai/short-courses/ai-agents-in-langgraph/
- **Multi-AI Agent Systems with CrewAI** — Multi-agent collaboration, delegation, role-based agents.  
  https://www.deeplearning.ai/short-courses/multi-ai-agent-systems-with-crewai/
- **Build AI Apps with MCP Servers** — Model Context Protocol, connecting agents to external tools via MCP.  
  https://www.deeplearning.ai/short-courses/build-ai-apps-with-mcp-server-working-with-box-files/
- **A2A: The Agent2Agent Protocol** ⭐ NEW 2026 (1h27m · Intermediate) — Google Cloud + IBM Research. The open standard (donated to Linux Foundation) for **agent-to-agent communication**. Complements MCP: MCP connects agents to tools/data, A2A lets agents collaborate with each other across frameworks (LangGraph, ADK, CrewAI). **Must learn in 2026 — this is now part of every senior multi-agent system design.**  
  https://www.deeplearning.ai/short-courses/a2a-the-agent2agent-protocol/
- **Agentic AI** by Andrew Ng — Agentic design patterns: reflection, tool use, planning, multi-agent.  
  https://www.deeplearning.ai/courses/agentic-ai/
- **Agent Memory: Building Memory-Aware Agents** — Memory types, in-context, external, episodic memory.  
  https://www.deeplearning.ai/short-courses/agent-memory-building-memory-aware-agents/

### 🎓 LangChain Academy (free)
- **Introduction to LangGraph** ⭐ HIGHLY RECOMMENDED (55 lessons · 6h · FREE) — Official LangGraph course covering state, memory, human-in-the-loop, long-term memory, and building your own assistant. Far more comprehensive than the DeepLearning.AI short course.  
  https://academy.langchain.com/courses/intro-to-langgraph
- **Quickstart: LangGraph Essentials** (free · ~1h) — Good fast-start companion before or during the full LangGraph course.  
  https://academy.langchain.com/courses/langgraph-essentials-python

### 📘 Official Docs (free)
- MCP official docs: https://modelcontextprotocol.io/docs/
- Anthropic MCP docs: https://docs.anthropic.com/en/docs/mcp
- Python MCP SDK: https://github.com/modelcontextprotocol/python-sdk
- A2A Python SDK: https://github.com/google-a2a/a2a-python
- A2A spec: https://google.github.io/A2A/
- Google A2A announcement: https://developers.googleblog.com/es/a2a-a-new-era-of-agent-interoperability/
- LangGraph docs: https://langchain-ai.github.io/langgraph/
- LangGraph tutorials: https://langchain-ai.github.io/langgraph/tutorials/
- OpenAI Agents SDK: https://openai.github.io/openai-agents-python/
- OpenAI MCP guide: https://platform.openai.com/docs/mcp/
- OpenAI remote MCP guide: https://platform.openai.com/docs/guides/tools-remote-mcp
- Open WebUI MCP docs: https://docs.openwebui.com/features/extensibility/mcp/

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
#### Project 18: Simple MCP Server
Expose:
- one tool
- one resource
- one prompt
Use a simple local use case.

#### Project 19: Python MCP Utility Server
Examples:
- local docs search
- task tracker
- local file summarizer
- personal notes lookup

#### Project 20: MCP-Powered Agent Integration
Connect an agent/client to your MCP server and use it in a workflow.

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

### Project 23: Stateful Research Workflow
Resume after interruption, persist state.

### Project 24: Orchestration & Multi-Agent
Implement using LangGraph, PydanticAI, or smolagents:
- planner
- tool call or code-execution
- approval gate
- resume execution
- final result synthesis

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

### 🔵 QA Platform (paid)
- Individual lesson: **Creating a Generative AI Coding Assistant for VSCode Using Ollama** (6min)  
  https://platform.qa.com/course/creating-a-generative-ai-coding-assistant-for-vscode-using-ollama-1/

### 📘 Official Docs (free)
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
- 1 strong RAG app
- 1 tool-calling/workflow app
- 1 MCP or orchestration project
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
1. RAG assistant with citations
2. Tool-calling workflow assistant
3. MCP-based utility or agent integration
4. Productionized FastAPI AI app

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

### 🔵 QA Platform (paid)
- **AI-900 Exam Prep: Microsoft Azure AI Fundamentals** (15 lessons · 9h46m · Beginner) — Official cert prep with hands-on labs.  
  https://platform.qa.com/learning-paths/ai-900-exam-preparation-microsoft-azure-ai-fundamentals-1968/

### 📘 Official Docs (free)
- Microsoft Learn — Azure AI Fundamentals learning path (free official prep):  
  https://learn.microsoft.com/en-us/credentials/certifications/azure-ai-fundamentals/
- AWS Certified AI Practitioner (AIF-C01) exam guide:  
  https://aws.amazon.com/certification/certified-ai-practitioner/
- AWS Skill Builder (free tier available): https://skillbuilder.aws/

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

## Project 30: Unified AI Assistant
**"My ChatGPT" — the all-in-one AI platform**

Build a full-stack web AI assistant that rivals ChatGPT in features:

| Feature | Tech |
|---------|------|
| Text chat with memory | OpenAI GPT-4o + Redis or Postgres for session memory |
| Voice input + output | OpenAI Whisper (STT) + TTS API — speak to it, it speaks back |
| Image understanding | GPT-4o vision — paste or upload an image, ask questions |
| File analysis | PDF, DOCX, Excel upload → RAG pipeline answers questions |
| PowerPoint generation | python-pptx + LLM → auto-generate slides from a topic |
| Video summary | yt-dlp + Whisper → transcribe + summarise YouTube videos |
| Web search | Tool call → SerpAPI or Tavily for live web answers |
| Persistent memory | Remembers who you are, your preferences, past conversations |
| FastAPI backend + React or Streamlit frontend | Clean, deployable, Docker |

**Tell Copilot:** `generate repo scaffold for phase 11 project 30`  
**You're done when:** You can record a 3-minute Loom demo showing voice in, image Q&A, file upload, and a web search.

---

## Project 31: Multi-Agent Research & Report Platform
**"Deep Research" — automated intelligence briefing generator**

Given a topic, this system autonomously researches it and produces a polished report:

| Feature | Tech |
|---------|------|
| Planner agent | Breaks topic into sub-questions |
| Web search agents (parallel) | Each sub-question gets its own search agent via Tavily/SerpAPI |
| Summariser agent | Condenses each source |
| Critic / reflection agent | Checks gaps, requests more research if needed |
| Writer agent | Assembles final report with citations |
| Output formats | Markdown, PDF (via weasyprint), and optional PowerPoint |
| Human-in-the-loop checkpoint | Approve/reject before final report is written |
| LangGraph orchestration | Full stateful multi-agent graph with persistence |
| MCP server | Expose "run research" as an MCP tool usable from Claude Desktop |

**Tell Copilot:** `generate repo scaffold for phase 11 project 31`  
**You're done when:** You can demo "research the impact of GenAI on software engineering" → full PDF report in 2 minutes.

---

## Project 32: Personal AI Dev Copilot
**"My Copilot" — a coding + productivity assistant built for your own workflow**

An MCP server + agent that integrates into your daily developer life:

| Feature | Tech |
|---------|------|
| Code review tool | Send a diff → get structured review with severity ratings |
| PR description generator | Git diff input → professional PR description |
| Ticket-to-code planner | Jira/GitHub issue → implementation plan + skeleton code |
| Doc generator | Python function → docstring + README section |
| Daily standup generator | Git log + Jira comments → formats standup update |
| Slack/Teams message drafter | Context → professional message |
| Runs as MCP server | Usable from Claude Desktop, VS Code Copilot |
| Runs as FastAPI service | Also usable as REST API / webhook |
| Configurable persona | System prompt tuned to your stack and preferences |

**Tell Copilot:** `generate repo scaffold for phase 11 project 32`  
**You're done when:** You use it yourself every day and it's in your GitHub profile README.

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

# 12-WEEK FAST EXECUTION VERSION

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
- support bot
- tool calling
- tool-using assistant

## Weeks 9-10
- research assistant
- SQL/report assistant
- eval dataset
- production hardening start

## Weeks 11-12
- MCP server
- MCP agent integration
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

- [ ] **Step 6 — Watch: Python LLM App Development Courses** (~10h — spread over days)
  🎯 Goal: Master the full OpenAI API before building more complex apps.

  | Resource | Duration | Priority | URL |
  |----------|----------|----------|-----|
  | OpenAI for Developers 🟡 | ~12h · 13 courses | ⭐ MUST DO | https://www.pluralsight.com/paths/openai-for-developers |
  | Generative AI for Developers 🟡 | ~6h · 7 courses | High | https://www.pluralsight.com/paths/generative-ai-for-developers |
  | LangChain for LLM App Dev 🟢 | ~1h38m FREE | High | https://www.deeplearning.ai/short-courses/langchain-for-llm-application-development/ |

  **Focus on inside the OpenAI path:**
  - Function calling and tool use
  - Responses API and Agents SDK
  - Embeddings API
  - Streaming responses
  - Security and Moderation

---

- [ ] **Step 7 — Build Project 4: CLI Chatbot**
  **Tell Copilot:** `generate repo scaffold for phase 2 project 4`
  🎯 Goal: Build conversation history, personas, and a clean CLI interface.

  **Exact build:**
  - CLI script: `python chatbot.py`
  - Maintains conversation history (messages list pattern)
  - Switch persona via `--persona` flag (e.g. `--persona senior-engineer`)
  - `--save` flag to write transcript to `transcript.json`

---

- [ ] **Step 8 — Build Project 5: FastAPI GenAI Service**
  **Tell Copilot:** `generate repo scaffold for phase 2 project 5`
  🎯 Goal: Production-style multi-endpoint GenAI API — use p0 template as your base.

  **Exact build:**
  - `POST /summarize` / `POST /rewrite` / `POST /classify` / `POST /extract`
  - Pydantic schemas for all request/response types
  - Proper error handling, timeouts, retries
  - Docker ready + README with curl examples

---

- [ ] **Step 9 — Build Project 6: Structured Data Extractor**
  **Tell Copilot:** `generate repo scaffold for phase 2 project 6`
  🎯 Goal: Extract structured JSON reliably from messy real-world text.

  **Exact build:**
  - Input: raw unstructured text (email, description, receipt, etc.)
  - Output: structured JSON matching a Pydantic model
  - Use OpenAI JSON mode / structured outputs
  - Test with 10+ examples of different messy inputs
  - **Reference:** https://platform.openai.com/docs/guides/structured-outputs

---

- [ ] **Step 10 — Build Project 7: Resume vs JD Analyzer**
  **Tell Copilot:** `generate repo scaffold for phase 2 project 7`
  🎯 Goal: A real tool with structured multi-step prompting — great portfolio piece.

  **Exact build:**
  - Input: resume text + job description text
  - Output: `{ "fit_score": 82, "matching_skills": [...], "missing_skills": [...], "suggestions": [...] }`
  - Use structured output (JSON schema)
  - Add a CLI and/or FastAPI endpoint

---

- [ ] **Step 11 — Watch: Embeddings and RAG Courses** (~2h)
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
