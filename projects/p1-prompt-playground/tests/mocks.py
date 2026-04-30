"""Central fixture store — all test data lives here.

Import from this module instead of building data inline in tests.
"""

# ── Input fixtures ────────────────────────────────────────────────
SAMPLE_TASK = "Explain what a transformer model is."

# ── Expected message shapes ───────────────────────────────────────
# Zero-shot: single user message
ZERO_SHOT_MESSAGES = [
    {"role": "user", "content": SAMPLE_TASK},
]

# Few-shot: 2 example pairs + final user message = 5 messages total
FEW_SHOT_MESSAGE_COUNT = 5

# System-role: system message + user message = 2
SYSTEM_ROLE_MESSAGE_COUNT = 2

# Chain-of-thought: system message + user message (with appended instruction) = 2
CHAIN_OF_THOUGHT_MESSAGE_COUNT = 2
