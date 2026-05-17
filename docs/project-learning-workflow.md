# Project Learning Workflow

This repo is build-first, but every finished project should also be understood well enough to explain in an interview or reuse at work.

The goal is not to memorize every package. The goal is to understand the system joints:

```text
input -> validation -> prompt/context -> model/tool call -> parsing -> response -> tests
```

## The Loop

Use this workflow for every roadmap project after the first working implementation.

1. Run it
   - Start the app locally.
   - Call the main happy path.
   - Call one bad input path.
   - Save or note the real command and output.

2. Trace it
   - Identify the entrypoint.
   - Follow the request or command through the main files.
   - Write the path in one line.

3. Learn the package surface
   - List the external packages used.
   - For each package, name only the functions/classes we used.
   - Explain why that package exists in the project.

4. Learn the config
   - Read `.env.example`, `pyproject.toml`, `Makefile`, and Docker config if present.
   - Explain each important variable and command.
   - Separate local-dev config from production-like config.

5. Break one small thing on purpose
   - Send invalid input.
   - Use a tiny token budget.
   - Stop the model server.
   - Confirm the error is understandable.

6. Make one tiny improvement
   - Improve README clarity.
   - Add one focused test.
   - Improve an error message.
   - Add one missing example.

7. Teach it back
   - Explain what the project does in 60 seconds.
   - Explain the code flow in 5-8 bullets.
   - Explain the main tradeoff.

## Done Means Learned

A project is not fully done until these are true:

- You can run it without guessing.
- You can point to the entrypoint.
- You can explain the main code path.
- You know which packages matter and why.
- You know what config controls model/provider behavior.
- You have seen one success output and one failure output.
- Tests pass.
- README has enough examples for future you.

## Timebox

Keep the learning review small:

- Small project: 30-45 minutes
- Medium project: 60-90 minutes
- Large/capstone project: 2-3 hours

Do not turn every project into a multi-day study rabbit hole. Learn the spine, capture the takeaways, then move.

## P5 Learning Card: FastAPI GenAI Service

### What It Teaches

P5 turns a local or hosted LLM into a production-style HTTP API.

Core flow:

```text
HTTP JSON request
-> FastAPI route
-> Pydantic request validation
-> prompt builder
-> token budget check
-> LLM adapter
-> model output parsing/validation
-> response with usage and metadata
```

### Packages

`fastapi`

- `FastAPI(...)`: creates the web app.
- `@app.get`, `@app.post`: define routes.
- `@app.exception_handler`: maps Python exceptions to JSON HTTP responses.
- `RequestValidationError`: catches invalid request bodies.
- `JSONResponse`: returns custom error envelopes.

Why: exposes the GenAI functions as typed HTTP endpoints.

`pydantic`

- `BaseModel`: defines request and response models.
- `Field`: adds validation rules such as length, range, and pattern.
- `Literal`: restricts allowed values.
- `field_validator`: adds custom validation.
- `model_validate`: validates parsed model JSON.

Why: keeps API inputs and model outputs structured and safe.

`pydantic-settings`

- `BaseSettings`: loads config from environment variables and `.env`.
- `SettingsConfigDict`: configures `.env` loading and behavior.
- `AliasChoices`: allows multiple env var names for one field.
- `SecretStr`: hides secrets in logs/repr.
- `computed_field`: derives provider metadata.
- `model_validator`: validates cross-field config.

Why: keeps local, hosted, and future deployment config out of code.

`openai`

- `AsyncOpenAI`: async SDK client.
- `client.chat.completions.create`: OpenAI-compatible chat call for Ollama, LM Studio, OpenAI-compatible providers, HF Router, and GitHub Models.
- `client.responses.create`: OpenAI Responses API path.
- SDK exceptions: auth, rate limit, timeout, API errors.

Why: gives one SDK surface for local and hosted LLM providers.

`httpx`

- `AsyncClient`: custom async HTTP client passed into the OpenAI SDK.

Why: lets us configure request behavior cleanly.

`truststore`

- `SSLContext`: uses the operating system certificate store.

Why: useful on machines or corporate networks where certificate handling can be painful.

`uvicorn`

- Runs `src.main:app` as an ASGI server.

Why: serves the FastAPI app locally.

### Important Config

`LLM_ADAPTER=chat`

- Uses Chat Completions.
- Best default for Ollama and LM Studio.

`OPENAI_BASE_URL=http://127.0.0.1:11434/v1`

- Points the OpenAI SDK at Ollama's OpenAI-compatible API.

`OPENAI_API_KEY=local-model`

- Dummy value for local providers that do not need real auth.

`MODEL=qwen2.5:1.5b`

- Small local model for quick smoke tests.

`TEMPERATURE=0.2`

- Lower randomness. Better for backend APIs and structured outputs.

`MAX_TOKENS=700`

- Caps response size.

`MAX_INPUT_TOKENS=6000`

- Rejects oversized input before calling the model.

`REQUEST_TIMEOUT_SECONDS=60`

- Prevents stuck provider calls.

`INPUT_TOKEN_PRICE_PER_1M` and `OUTPUT_TOKEN_PRICE_PER_1M`

- Optional cost estimate inputs.

### Main Files

- `src/main.py`: FastAPI app, routes, exception handlers.
- `src/schemas.py`: Pydantic request/response models.
- `src/prompts.py`: prompt builders for each operation.
- `src/service.py`: business flow, budget checks, output validation.
- `src/llm.py`: provider adapter for chat and Responses API.
- `src/token_usage.py`: token and cost estimates.
- `src/errors.py`: app-specific exception types.
- `src/settings.py`: runtime config.

### Success Output To Recognize

`GET /health` should return:

```json
{
  "status": "ok",
  "app": "p5-fastapi-genai-service",
  "model": "qwen2.5:1.5b",
  "adapter": "chat",
  "provider": "ollama"
}
```

GenAI endpoints should return:

```json
{
  "result": "...",
  "usage": {
    "input_tokens_estimated": 93,
    "output_tokens_estimated": 112,
    "total_tokens_estimated": 205
  },
  "metadata": {
    "operation": "summarize",
    "model": "qwen2.5:1.5b",
    "adapter": "chat",
    "provider": "ollama",
    "budget_ok": true
  }
}
```

### Failure Output To Recognize

Over-budget input should return HTTP 422:

```json
{
  "error": "Input exceeds token budget.",
  "details": "Reduce the input text or increase max_input_tokens.",
  "estimated_input_tokens": 76,
  "max_input_tokens": 5,
  "suggestion": "Shorten text or pass a larger max_input_tokens value."
}
```

### Interview Explanation

P5 is a FastAPI backend that exposes common GenAI operations behind stable JSON endpoints. It validates input with Pydantic, builds operation-specific prompts, rejects over-budget requests before model calls, routes generation through a provider adapter, parses structured model output where needed, and returns token/cost metadata with consistent error handling.

### What Not To Overlearn Yet

- FastAPI internals
- ASGI internals
- OpenAI SDK internals
- Perfect tokenization
- Production auth
- Streaming HTTP responses

Those are later topics. For P5, the win is understanding the production backend shape.

### AI-Specific Takeaways

If FastAPI and Pydantic already feel familiar, focus your review here.

#### 1. OpenAI-Compatible APIs

The OpenAI Python SDK can talk to non-OpenAI providers when they expose an OpenAI-compatible API.

For Ollama:

```env
OPENAI_BASE_URL=http://127.0.0.1:11434/v1
OPENAI_API_KEY=local-model
MODEL=qwen2.5:1.5b
```

The key idea:

```text
same SDK call -> different provider by changing base_url/model/key
```

That is why our code can use `openai.AsyncOpenAI` for Ollama, LM Studio, OpenAI-compatible hosted APIs, HuggingFace Router, and GitHub Models.

#### 2. Chat Messages

Chat Completions use a list of messages:

```python
[
    {"role": "system", "content": "...behavior and rules..."},
    {"role": "user", "content": "...actual task..."},
]
```

The `system` message controls behavior. The `user` message carries the actual request.

In this project, prompt builders create those messages instead of building prompts inline in routes.

#### 3. Adapter Pattern

The service calls one internal function:

```python
generate(messages, settings, client)
```

That function decides whether to use:

- `client.chat.completions.create(...)`
- `client.responses.create(...)`

Why this matters:

```text
service code should not care which provider API is underneath
```

This is the beginning of provider portability.

#### 4. Chat Completions vs Responses API

Chat Completions:

- Best local compatibility today.
- Works with Ollama and LM Studio.
- Uses `messages=[...]`.
- Returns `choices[0].message.content`.

Responses API:

- OpenAI's newer primary API.
- Better long-term direction for OpenAI-hosted models.
- Uses `input=...`.
- Returns `output_text`.

P5 includes both so the project stays local-first but does not ignore the newer OpenAI direction.

#### 5. Prompt Builders

Prompts live in `src/prompts.py`.

That keeps business logic cleaner:

```text
route -> service -> prompt builder -> llm adapter
```

The important AI habit:

```text
do not scatter prompts across route handlers
```

Prompts are application behavior. Keep them visible and testable.

#### 6. Structured Model Output

For `/classify` and `/extract`, the model is asked to return JSON.

Then the app:

1. extracts the JSON object from the model text
2. runs `json.loads`
3. validates it with Pydantic
4. rejects invalid or incomplete model output

This is intentionally provider-compatible. It works with local models that do not support strict schema mode.

Future upgrade:

```text
OpenAI Structured Outputs / JSON schema mode for hosted models
```

But V1 keeps local compatibility first.

#### 7. Token Budgeting

Before the model call, the app estimates input tokens.

If the estimate exceeds the configured budget, it returns HTTP 422 and does not call the model.

Why this matters:

- avoids surprise cost
- avoids slow local-model requests
- avoids context-window failures
- makes failures explicit

P5 uses a simple chars-per-token estimate for now:

```text
estimated tokens ~= characters / 4
```

This is not perfect, but it is good enough for V1 and works without tokenizer dependencies.

#### 8. Provider-Reported Usage

When the provider returns token usage, P5 includes it:

```json
{
  "input_tokens_actual": 81,
  "output_tokens_actual": 76,
  "total_tokens_actual": 157
}
```

When the provider does not return usage, the app still has estimates.

This is the practical rule:

```text
estimate before the call, prefer actual usage after the call
```

#### 9. Cost Estimates

If pricing env vars are configured:

```env
INPUT_TOKEN_PRICE_PER_1M=0.15
OUTPUT_TOKEN_PRICE_PER_1M=0.60
```

The service can estimate request cost.

This is lightweight, but it introduces the right production thinking:

```text
every LLM endpoint should have some awareness of cost
```

#### 10. Local Model Reality

Small local models are useful for:

- smoke tests
- privacy-friendly local development
- checking app wiring
- avoiding paid API usage while building

But they may be weaker at:

- following JSON instructions perfectly
- reasoning
- high-quality writing
- complex extraction

That means local testing proves the integration works, not that final model quality is production-ready.

## Reusable Project Review Template

Use this for each project:

```markdown
# Project N Review

## What This Project Teaches

## How To Run

## Real Success Output

## Real Failure Output

## Main Code Path

## Packages Used

## Config Used

## Tests

## Key Tradeoffs

## What I Can Explain Now
```

## P7 Learning Card: Resume vs JD Analyzer

### What It Teaches

P7 compares two documents instead of extracting from one document.

Core flow:

```text
resume text + job description text
-> build comparison prompt
-> model returns structured fit analysis
-> app validates JSON
-> deterministic keyword scorer computes grounded overlap
-> final score blends model judgment with deterministic score
```

### AI-Specific Takeaways

1. Multi-document prompting
   - The prompt must clearly label each document.
   - The model should cite evidence from both sides.
   - Avoid letting the model invent missing experience.

2. Evidence-backed judgment
   - Each evidence item has `resume_evidence`, `jd_evidence`, and `judgment`.
   - This makes the output inspectable instead of just a mysterious score.

3. Hybrid scoring
   - The LLM gives a judgment score.
   - A deterministic keyword scorer computes overlap.
   - The final score blends both.

4. Local model reality
   - Small local models can produce valid JSON but rough analysis.
   - Use local models to prove wiring and schema handling.
   - Use stronger hosted/local models for final-quality judgment.

5. Product lesson
   - Resume/JD matching should not be treated as pure truth.
   - It is a decision-support tool, not a hiring decision engine.

### Main Files

- `src/prompts.py`: multi-document prompt.
- `src/schemas.py`: structured analysis schema.
- `src/scoring.py`: deterministic keyword score and blended score.
- `src/service.py`: analysis flow.
- `src/llm.py`: prompt/chat-schema/responses-schema adapters.
