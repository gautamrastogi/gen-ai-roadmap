"""Application exception types."""


class AppError(Exception):
    """Base application exception."""

    def __init__(self, message: str, details: str = "") -> None:
        super().__init__(message)
        self.message = message
        self.details = details


class BudgetExceededError(AppError):
    """Raised when input exceeds the configured prompt budget."""

    def __init__(self, estimated_input_tokens: int, max_input_tokens: int) -> None:
        super().__init__(
            "Input exceeds token budget.",
            "Reduce the input text or increase max_input_tokens.",
        )
        self.estimated_input_tokens = estimated_input_tokens
        self.max_input_tokens = max_input_tokens


class LLMProviderError(AppError):
    """Raised when the LLM provider call fails."""


class LLMTimeoutError(LLMProviderError):
    """Raised when the LLM provider times out."""


class LLMOutputError(AppError):
    """Raised when the LLM returns malformed or invalid output."""
