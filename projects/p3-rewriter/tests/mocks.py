"""Shared test fixtures and sample data for P3 Rewriter."""

SAMPLE_TEXT = (
    "Transformers have changed how we build AI systems. "
    "They use attention to figure out which parts of the input matter most. "
    "Unlike older RNNs that go word by word, transformers look at everything at once. "
    "This makes them much faster to train. "
    "Big models like BERT and GPT are based on this idea. "
    "Teams that want to use them need to update their pipelines and infrastructure. "
    "It is also worth archiving old RNN-based documentation."
)

PROFESSIONAL_SYSTEM = "You are a professional business writer."
CONCISE_SYSTEM = "You are an editor who specialises in concise writing."
TECHNICAL_SYSTEM = "You are a technical writer."
FRIENDLY_SYSTEM = "You are a friendly communicator."
