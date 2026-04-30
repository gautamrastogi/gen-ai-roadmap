"""Shared test fixtures and sample data."""

SAMPLE_TEXT = (
    "Transformer models use a self-attention mechanism to process sequences. "
    "They were introduced in the paper 'Attention Is All You Need' in 2017. "
    "Unlike RNNs, transformers process all tokens in parallel, making them faster to train. "
    "BERT and GPT are two well-known transformer architectures. "
    "BERT is used for understanding tasks; GPT is used for text generation. "
    "The key components are: multi-head attention, feed-forward layers, and positional encodings. "
    "Teams adopting transformers should audit their data pipelines, retrain existing models, "
    "and update their serving infrastructure. "
    "Documentation for legacy RNN systems should be archived."
)

SUMMARY_PROMPT_SYSTEM = "You are a precise summarizer."
BULLETS_PROMPT_SYSTEM = "You are a precise summarizer."
ACTION_ITEMS_PROMPT_SYSTEM = "You are an assistant that extracts actionable tasks."
