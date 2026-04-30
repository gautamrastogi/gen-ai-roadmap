import os, ssl, httpx, truststore, json

ctx = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
c = httpx.Client(verify=ctx, timeout=30)
TOKEN = os.environ["HF_TOKEN"]
h = {"Authorization": f"Bearer {TOKEN}"}

# Find models specifically available on hf-inference provider with conversational/text-gen task
r = c.get(
    "https://huggingface.co/api/models"
    "?inference_provider=hf-inference"
    "&pipeline_tag=text-generation"
    "&sort=downloads"
    "&limit=20",
    headers=h,
)
print(f"hf-inference text-gen models: {r.status_code}")
if r.status_code == 200:
    models = json.loads(r.text)
    for m in models:
        print(f"  {m['id']}")

# Also try auto-routing - no provider specified
print("\n--- Auto-route attempt ---")
for model in ["Qwen/Qwen2.5-7B-Instruct", "meta-llama/Llama-3.1-8B-Instruct"]:
    r2 = c.post(
        "https://router.huggingface.co/v1/chat/completions",
        headers=h,
        json={
            "model": model,
            "messages": [{"role": "user", "content": "Say hi"}],
            "max_tokens": 20,
        },
        timeout=20,
    )
    print(f"[auto] {model}: {r2.status_code} -> {r2.text[:150]}")
