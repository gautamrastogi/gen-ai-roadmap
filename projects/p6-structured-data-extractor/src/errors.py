"""Application exception types."""


class AppError(Exception):
    """Base app exception."""

    def __init__(self, message: str, details: str = "") -> None:
        super().__init__(message)
        self.message = message
        self.details = details


class BudgetExceededError(AppError):
    """Raised before model calls when input exceeds budget."""

    def __init__(self, estimated_input_tokens: int, max_input_tokens: int) -> None:
        super().__init__(
            "Input exceeds token budget.",
            "Shorten the document or increase MAX_INPUT_TOKENS.",
        )
        self.estimated_input_tokens = estimated_input_tokens
        self.max_input_tokens = max_input_tokens


class LLMProviderError(AppError):
    """Raised when the model provider fails."""


class LLMTimeoutError(LLMProviderError):
    """Raised when the model provider times out."""


class LLMOutputError(AppError):
    """Raised when the model output cannot be parsed or validated."""
