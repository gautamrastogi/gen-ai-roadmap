# P6 - Structured Data Extractor

Schema-first extraction from messy text into typed JSON.

This project is about the AI engineering layer behind structured extraction:

- define strict target schemas with Pydantic
- ask local or hosted models to extract JSON
- use OpenAI-style structured outputs when available
- fall back to prompt-and-validate mode for Ollama/LM Studio
- validate model output and return a business validation report

## Quickstart

```bash
make install

# Local Ollama path
ollama pull qwen2.5:1.5b
make run-ollama
```

## Usage

```bash
python -m src.main --schema invoice --file examples/invoice.txt
python -m src.main --schema support_ticket --file examples/support-ticket.txt
python -m src.main --schema log_incident --file examples/log-incident.txt
python -m src.main --schema invoice --text "Invoice INV-1 from Acme..."
```

Use a different extraction mode:

```bash
# Local-friendly mode: prompt asks for JSON, app validates after
EXTRACTION_MODE=prompt python -m src.main --schema invoice --file examples/invoice.txt

# Chat Completions structured output
EXTRACTION_MODE=chat_schema python -m src.main --schema invoice --file examples/invoice.txt

# OpenAI Responses API structured output
EXTRACTION_MODE=responses_schema OPENAI_BASE_URL= OPENAI_API_KEY=sk-... MODEL=gpt-4.1-mini \
  python -m src.main --schema invoice --file examples/invoice.txt
```

## Schemas

| Schema | Use Case |
|---|---|
| `invoice` | Vendor invoices with line items, totals, tax, and payment info |
| `support_ticket` | Support/request tickets with priority, service, requester, and action |
| `log_incident` | Operational log snippets with severity, service, hosts, and likely cause |

List schemas:

```bash
python -m src.main --list-schemas
```

## Modes

| Mode | What It Does | Best For |
|---|---|---|
| `prompt` | Sends schema and instructions in the prompt, then parses and validates JSON locally | Ollama, LM Studio, broad compatibility |
| `chat_schema` | Sends JSON Schema through Chat Completions `response_format` | OpenAI-compatible providers that support structured outputs |
| `responses_schema` | Sends JSON Schema through Responses API `text.format` | OpenAI-hosted models and newer structured output workflows |

## Response Shape

```json
{
  "schema_name": "invoice",
  "mode": "prompt",
  "data": {
    "invoice_number": "INV-2026-0142",
    "vendor_name": "Northwind Cloud Services",
    "currency": "EUR",
    "total": 1560.9
  },
  "validation_report": {
    "valid": true,
    "issue_count": 0,
    "issues": []
  },
  "usage": {
    "input_tokens_estimated": 450,
    "output_tokens_estimated": 180,
    "total_tokens_estimated": 630,
    "input_tokens_actual": null,
    "output_tokens_actual": null,
    "total_tokens_actual": null
  },
  "metadata": {
    "model": "qwen2.5:1.5b",
    "provider": "ollama",
    "schema_name": "invoice",
    "mode": "prompt",
    "warnings": []
  }
}
```

## Important Learning

P5 extracted flexible fields. P6 extracts into predefined contracts.

The key workflow is:

```text
messy text
-> choose schema
-> build extraction messages
-> optionally pass JSON Schema to the provider
-> parse model JSON
-> validate with Pydantic
-> run business validation
-> return typed JSON + validation report
```

Structured outputs reduce malformed JSON and missing fields, but prompt-and-validate mode is still useful for local models and providers without schema support.

## Developer Commands

```bash
make install
make fmt
make ci
make run
make run-ollama
```
