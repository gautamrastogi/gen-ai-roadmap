import re

with open("genai-roadmap.md", "r") as f:
    content = f.read()

# 1. Update Phase Summary
old_summary = """## Phase Summary
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
| 8 | Portfolio + Job Prep | ⬜ Not Started |
| 9 | Certifications | ⬜ Not Started |
| 10 | Capstone: Resume-Grade Projects | ⬜ Not Started |"""

new_summary = """## Phase Summary
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
| 8 | DevOps, LLMOps & Cloud Architecture | ⬜ Not Started |
| 9 | Security Architecture & Compliance | ⬜ Not Started |
| 10 | Portfolio + Job Prep | ⬜ Not Started |
| 11 | Certifications | ⬜ Not Started |
| 12 | Capstone: Resume-Grade Projects | ⬜ Not Started |"""

content = content.replace(old_summary, new_summary)

# 2. Update Checklist (Change Phase 10 to Phase 12)
content = content.replace("### Phase 10 — Capstone: Resume-Grade Projects", "### Phase 12 — Capstone: Resume-Grade Projects")

# Add Phase 8 and 9 to Checklist
new_checklists = """### Phase 8 — DevOps, LLMOps & Cloud Architecture
- [ ] Project 27: CI/CD Pipeline for AI Agent
- [ ] Project 28: Containerized LangGraph Deployment

### Phase 9 — Security Architecture & Compliance
- [ ] Project 29: OWASP API Security Audit
- [ ] Project 30: Prompt Injection Defense System

### Phase 12 — Capstone: Resume-Grade Projects"""
content = content.replace("### Phase 12 — Capstone: Resume-Grade Projects", new_checklists)

# Adjust Capstone project numbers
content = content.replace("Project 27: Unified AI Assistant", "Project 31: Unified AI Assistant")
content = content.replace("Project 28: Multi-Agent Research", "Project 32: Multi-Agent Research")
content = content.replace("Project 29: Personal AI Dev Copilot", "Project 33: Personal AI Dev Copilot")

# Update Total projects count
content = content.replace("**Overall: 4 / 30 projects done**", "**Overall: 4 / 33 projects done**")

# 3. Update FINAL ROADMAP ORDER
old_order = """# FINAL ROADMAP ORDER

1. Foundations
2. Python LLM apps
3. Embeddings + vector search + RAG
4. Tool calling + workflow automation
5. Evals + safety + observability + production reliability
6. MCP + agentic orchestration + HITL + persistence
7. AI-native developer productivity
8. Portfolio + job prep
9. One certification
10. Capstone: 3 big resume-grade projects that combine everything"""

new_order = """# FINAL ROADMAP ORDER

1. Foundations
2. Python LLM apps
3. Embeddings + vector search + RAG
4. Tool calling + workflow automation
5. Evals + safety + observability + production reliability
6. MCP + agentic orchestration + HITL + persistence
7. AI-native developer productivity
8. DevOps, LLMOps & Cloud Architecture (AWS/Azure)
9. Security Architecture & Compliance (OWASP)
10. Portfolio + job prep
11. One certification
12. Capstone: 3 big resume-grade projects that combine everything"""

content = content.replace(old_order, new_order)

# 4. Update PHASE 0 Skills
old_skills = """## Skills
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
- CLI basics"""

new_skills = """## Skills
- Python (Advanced OOP, typing, async)
- TypeScript/JavaScript (Frontend UI basics)
- Backend: FastAPI (Microservices), Django (Monoliths)
- REST APIs & GraphQL basics
- JSON / YAML
- Databases: PostgreSQL, SQLite, ChromaDB
- Git/GitHub
- logging & monitoring
- testing (pytest)
- Docker & CI/CD basics
- environment variables & secrets management
- CLI & bash basics"""

content = content.replace(old_skills, new_skills)

# 5. Insert Phase 8 and Phase 9
old_phase_8_header = "# PHASE 8 - PORTFOLIO + JOB PREP"
new_phases = """# PHASE 8 - DEVOPS, LLMOPS & CLOUD ARCHITECTURE

## Goal
Deploy AI applications reliably to production with proper observability and scale.

## Learn
- AWS / Azure core services for AI (Bedrock, SageMaker, Azure OpenAI)
- Infrastructure as Code (AWS CDK, Bicep, Terraform)
- Containerization (Docker multi-stage builds)
- CI/CD for AI (GitHub Actions)
- LLMOps: model versioning, prompt registries
- Open-source observability (Langfuse, Arize Phoenix)

## Projects
### Project 27: CI/CD Pipeline for AI Agent
- Create GitHub Action to lint, test, and deploy FastAPI LLM backend
- Include a step to run LLM evals before deployment

### Project 28: Containerized LangGraph Deployment
- Deploy a LangGraph workflow using Docker to AWS App Runner or Azure Container Apps

---

# PHASE 9 - SECURITY ARCHITECTURE & COMPLIANCE

## Goal
Ensure AI systems are secure against agentic vulnerabilities and compliant with data laws.

## Learn
- OWASP Top 10 for LLMs and Agentic Security (ASI)
- Prompt Injection & Jailbreak defenses
- Data Poisoning mitigation
- PII sanitization and GDPR compliance for AI
- Safe tool execution (sandboxing)
- Secret Scanning and Access Controls

## Projects
### Project 29: OWASP API Security Audit
- Evaluate a vulnerable AI endpoint and secure it against IDOR and injection attacks

### Project 30: Prompt Injection Defense System
- Build a middleware layer that detects and blocks adversarial prompts using a local classifier

---

# PHASE 10 - PORTFOLIO + JOB PREP"""

content = content.replace(old_phase_8_header, new_phases)

# 6. Rename old Phase 9 to 11 and Phase 10 to 12
content = content.replace("# PHASE 9 - CERTIFICATIONS", "# PHASE 11 - CERTIFICATIONS")
content = content.replace("# PHASE 10 - CAPSTONE: RESUME-GRADE PROJECTS", "# PHASE 12 - CAPSTONE: RESUME-GRADE PROJECTS")

# Update Capstone project numbers inside Phase 12
content = content.replace("### Project 27:", "### Project 31:")
content = content.replace("### Project 28:", "### Project 32:")
content = content.replace("### Project 29:", "### Project 33:")

with open("genai-roadmap.md", "w") as f:
    f.write(content)
