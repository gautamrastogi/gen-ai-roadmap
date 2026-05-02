# Tiny Local Agent Demo

This is the smallest useful version of a local agent:

- local model server: `Ollama` or `LM Studio`
- agent loop: `demos/local_agent_demo.py`
- tools: time, list files, read file

## What this proves

The model can run locally and still behave like an agent because your Python app gives it tools and loops over tool calls.

## Option 1: Ollama

Start Ollama, then pull a tool-capable model:

```bash
ollama pull qwen3
```

Run the demo:

```bash
python3 demos/local_agent_demo.py --base-url http://127.0.0.1:11434/v1 --model qwen3
```

## Option 2: LM Studio

1. Start LM Studio
2. Open the `Developer` tab
3. Start the local server
4. Load a tool-capable model

Then run:

```bash
python3 demos/local_agent_demo.py --base-url http://127.0.0.1:1234/v1 --model <your-model-name>
```

## Good test prompts

- `list files here`
- `read genai-roadmap.md and summarize phase 2`
- `what time is it?`
- `read dashboard.html and tell me what this app does`

## Important limitation

The local model is only the brain.

The Python script is what gives it:

- tools
- tool execution
- memory across turns
- the agent loop

That is the key idea.
