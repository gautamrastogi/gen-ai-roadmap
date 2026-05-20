# P7 - Resume vs JD Analyzer

Structured fit analysis for a resume against a job description.

This project teaches multi-document GenAI analysis:

- pass two documents into one structured analysis prompt
- ask for evidence-based JSON output
- validate model output with Pydantic
- add deterministic scoring to keep the fit score grounded
- support local Ollama/LM Studio and hosted structured-output modes

## Quickstart

```bash
make install

# Local Ollama path
ollama pull gemma4:latest
make run-ollama
```

## Usage

```bash
python -m src.main --resume examples/resume.txt --jd examples/job-description.txt
python -m src.main --resume-text "Python FastAPI engineer..." --jd-text "We need Python and Kafka..."
```

Choose a mode:

```bash
# Local-friendly mode
ANALYSIS_MODE=prompt python -m src.main --resume examples/resume.txt --jd examples/job-description.txt

# Chat Completions structured output
ANALYSIS_MODE=chat_schema python -m src.main --resume examples/resume.txt --jd examples/job-description.txt

# OpenAI Responses API structured output
ANALYSIS_MODE=responses_schema OPENAI_BASE_URL= OPENAI_API_KEY=<openai-api-key> MODEL=gpt-4.1-mini \
  python -m src.main --resume examples/resume.txt --jd examples/job-description.txt
```

## Output Shape

```json
{
  "fit_score": 82,
  "recommendation": "strong_match",
  "matching_skills": ["Python", "FastAPI", "Kafka"],
  "partial_matches": ["AWS", "Terraform"],
  "missing_skills": ["LangGraph", "RAG evals"],
  "strengths": ["backend APIs", "event-driven systems"],
  "risks": ["limited production GenAI evidence"],
  "suggestions": ["Add a RAG project with evals"],
  "evidence": [
    {
      "area": "Backend",
      "resume_evidence": "Built Django/FastAPI services",
      "jd_evidence": "Requires Python backend services",
      "judgment": "strong_match"
    }
  ],
  "score_breakdown": {
    "llm_fit_score": 84,
    "deterministic_fit_score": 76,
    "final_fit_score": 82
  }
}
```

## Important Learning

P6 extracted one document into one schema. P7 compares two documents and produces a judgment.

The core flow:

```text
resume text + job description text
-> build comparison prompt
-> model returns structured analysis
-> app validates JSON
-> deterministic keyword scorer computes grounded overlap
-> final score blends model judgment with deterministic score
```

This is a useful pattern for business AI systems: let the model reason, but keep a deterministic check beside it.

## Developer Commands

```bash
make install
make fmt
make ci
make run
make run-ollama
```
