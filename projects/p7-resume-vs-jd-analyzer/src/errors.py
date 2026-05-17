"""Application exception types."""


class AppError(Exception):
    """Base app exception."""

    def __init__(self, message: str, details: str = "") -> None:
        super().__init__(message)
        self.message = message
        self.details = details


class BudgetExceededError(AppError):
    """Raised when input exceeds configured budget."""

    def __init__(self, estimated_input_tokens: int, max_input_tokens: int) -> None:
        super().__init__(
            "Input exceeds token budget.",
            "Shorten the resume/JD or increase MAX_INPUT_TOKENS.",
        )
        self.estimated_input_tokens = estimated_input_tokens
        self.max_input_tokens = max_input_tokens


class LLMProviderError(AppError):
    """Raised when provider call fails."""


class LLMTimeoutError(LLMProviderError):
    """Raised when provider call times out."""


class LLMOutputError(AppError):
    """Raised when model output cannot be parsed or validated."""
