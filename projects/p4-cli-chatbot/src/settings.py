"""CLI Chatbot settings.

Reads configuration from environment variables or a local ``.env`` file.
The app supports local OpenAI-compatible servers plus hosted providers.
"""

from pathlib import Path

import pydantic
import pydantic_settings


class Settings(pydantic_settings.BaseSettings):
    """Runtime configuration for the chatbot."""

    model_config = pydantic_settings.SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
        populate_by_name=True,
    )

    hf_token: pydantic.SecretStr = pydantic.Field(
        default=pydantic.SecretStr(""),
        description="HuggingFace token for router.huggingface.co.",
    )
    github_token: pydantic.SecretStr = pydantic.Field(
        default=pydantic.SecretStr(""),
        description="GitHub token for GitHub Models.",
    )
    openai_api_key: pydantic.SecretStr = pydantic.Field(
        default=pydantic.SecretStr(""),
        description="OpenAI API key, or a dummy key for local OpenAI-compatible servers.",
    )
    openai_base_url: str = pydantic.Field(
        default="",
        description="Optional OpenAI-compatible base URL for LM Studio, Ollama, or another provider.",
    )
    openai_model: str = pydantic.Field(
        default="Qwen/Qwen2.5-7B-Instruct",
        validation_alias=pydantic.AliasChoices("MODEL", "OPENAI_MODEL"),
        description="Model identifier.",
    )
    temperature: float = pydantic.Field(
        default=0.7,
        validation_alias=pydantic.AliasChoices("TEMPERATURE", "OPENAI_TEMPERATURE"),
        description="Sampling temperature.",
    )
    max_tokens: int = pydantic.Field(
        default=700,
        validation_alias=pydantic.AliasChoices("MAX_TOKENS", "OPENAI_MAX_TOKENS"),
        description="Maximum completion tokens per assistant response.",
    )
    session_path: Path = pydantic.Field(
        default=Path("sessions/default.json"),
        validation_alias=pydantic.AliasChoices("SESSION_PATH", "CHATBOT_SESSION_PATH"),
        description="Default session JSON path.",
    )

    @pydantic.computed_field  # type: ignore[prop-decorator]
    @property
    def use_local_or_custom_base_url(self) -> bool:
        """Return whether a custom OpenAI-compatible base URL is configured."""

        return bool(self.openai_base_url.strip())

    @pydantic.computed_field  # type: ignore[prop-decorator]
    @property
    def use_hf(self) -> bool:
        """Return whether HuggingFace should be used."""

        return bool(self.hf_token.get_secret_value().strip())

    @pydantic.computed_field  # type: ignore[prop-decorator]
    @property
    def use_github_models(self) -> bool:
        """Return whether GitHub Models should be used."""

        return bool(self.github_token.get_secret_value().strip())

    @pydantic.model_validator(mode="after")
    def require_provider(self) -> "Settings":
        """Require a local/custom endpoint or at least one hosted-provider credential."""

        has_openai = bool(self.openai_api_key.get_secret_value().strip())
        if not (
            self.use_local_or_custom_base_url or self.use_hf or self.use_github_models or has_openai
        ):
            raise ValueError(
                "Set OPENAI_BASE_URL for a local model, or set HF_TOKEN, "
                "GITHUB_TOKEN, or OPENAI_API_KEY. Copy .env.example to .env first."
            )
        return self
