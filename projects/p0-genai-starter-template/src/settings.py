"""GenAI Starter Template — application settings.

All configuration is read from environment variables (or a ``.env`` file).
The app refuses to start if ``OPENAI_API_KEY`` is missing.

Usage::

    from src.settings import Settings

    settings = Settings()
"""

import pydantic
import pydantic_settings


class Settings(pydantic_settings.BaseSettings):
    """Application-level configuration read from environment variables.

    :param openai_api_key: OpenAI API key (required).
    :param openai_model: Model name to use for completions. Defaults to ``"gpt-4o-mini"``.
    :param log_level: Python logging level string. Defaults to ``"INFO"``.
    :param app_name: Human-readable service name used in logs and health responses.
    """

    model_config = pydantic_settings.SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    openai_api_key: pydantic.SecretStr = pydantic.SecretStr("")
    openai_model: str = "gpt-4o-mini"
    log_level: str = "INFO"
    app_name: str = "genai-starter"

    @pydantic.model_validator(mode="after")
    def validate_api_key_present(self) -> "Settings":
        """Ensure OPENAI_API_KEY is provided.

        :return: The validated :class:`Settings` instance.
        :raises ValueError: If ``OPENAI_API_KEY`` is empty.
        """
        if not self.openai_api_key.get_secret_value():
            raise ValueError(
                "OPENAI_API_KEY is required. Add it to your .env file or environment."
            )
        return self
