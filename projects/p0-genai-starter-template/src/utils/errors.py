"""GenAI Starter Template — custom exception hierarchy.

:class AppError: Base exception for all app-level errors.
:class LLMError: Raised when the LLM API call fails.
:class ValidationError: Raised when request input fails validation.
"""


class AppError(Exception):
    """Base class for all application errors.

    :param message: Short human-readable error summary.
    :param details: Optional extended details.
    """

    def __init__(self, message: str, details: str = "") -> None:
        super().__init__(message)
        self.message = message
        self.details = details

    def __str__(self) -> str:
        if self.details:
            return f"{self.message}: {self.details}"
        return self.message


class LLMError(AppError):
    """Raised when the LLM (OpenAI) API call fails.

    :param message: Short human-readable error summary.
    :param details: Optional extended details.
    """


class ValidationError(AppError):
    """Raised when request input fails schema validation.

    :param message: Short human-readable error summary.
    :param details: Optional extended details.
    """
