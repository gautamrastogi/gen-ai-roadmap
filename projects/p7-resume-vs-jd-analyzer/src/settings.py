"""Runtime settings for P7."""

from typing import Literal

import pydantic
import pydantic_settings

from src import schemas

ProviderName = Literal[
    "ollama",
    "lm-studio",
    "openai-chat",
    "openai-responses",
    "huggingface-router",
    "github-models",
    "openai-compatible",
]


class Settings(pydantic_settings.BaseSettings):
    """Application config loaded from environment variables or ``.env``."""

    model_config = pydantic_settings.SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
        populate_by_name=True,
    )

    analysis_mode: schemas.AnalysisMode = pydantic.Field(
        default="prompt",
        validation_alias=pydantic.AliasChoices("ANALYSIS_MODE", "MODE"),
    )
    openai_base_url: str = pydantic.Field(
        default="http://127.0.0.1:11434/v1",
        validation_alias=pydantic.AliasChoices("OPENAI_BASE_URL", "BASE_URL"),
    )
    openai_api_key: pydantic.SecretStr = pydantic.SecretStr("")
    hf_token: pydantic.SecretStr = pydantic.SecretStr("")
    github_token: pydantic.SecretStr = pydantic.SecretStr("")
    openai_model: str = pydantic.Field(
        default="qwen2.5:1.5b",
        validation_alias=pydantic.AliasChoices("MODEL", "OPENAI_MODEL"),
    )
    temperature: float = pydantic.Field(default=0.1, ge=0.0, le=2.0)
    max_tokens: int = pydantic.Field(default=1400, ge=1, le=20_000)
    max_input_tokens: int = pydantic.Field(default=9000, ge=1, le=200_000)
    request_timeout_seconds: float = pydantic.Field(default=60.0, ge=1.0, le=300.0)

    @pydantic.computed_field  # type: ignore[prop-decorator]
    @property
    def use_local_or_custom_base_url(self) -> bool:
        """Return whether a custom OpenAI-compatible base URL is configured."""

        return bool(self.openai_base_url.strip())

    @pydantic.computed_field  # type: ignore[prop-decorator]
    @property
    def use_hf(self) -> bool:
        """Return whether HuggingFace Router should be used."""

        return bool(self.hf_token.get_secret_value().strip())

    @pydantic.computed_field  # type: ignore[prop-decorator]
    @property
    def use_github_models(self) -> bool:
        """Return whether GitHub Models should be used."""

        return bool(self.github_token.get_secret_value().strip())

    @pydantic.computed_field  # type: ignore[prop-decorator]
    @property
    def provider(self) -> ProviderName:
        """Return a human-readable provider name."""

        base_url = self.openai_base_url.lower()
        if self.analysis_mode == "responses_schema":
            return "openai-responses"
        if "11434" in base_url:
            return "ollama"
        if "1234" in base_url:
            return "lm-studio"
        if self.use_hf:
            return "huggingface-router"
        if self.use_github_models:
            return "github-models"
        if self.openai_api_key.get_secret_value().strip() and not self.openai_base_url.strip():
            return "openai-chat"
        return "openai-compatible"

    @pydantic.model_validator(mode="after")
    def validate_provider(self) -> "Settings":
        """Ensure configured mode has usable credentials."""

        has_openai_key = bool(self.openai_api_key.get_secret_value().strip())
        if self.analysis_mode == "responses_schema" and not has_openai_key:
            raise ValueError("OPENAI_API_KEY is required when ANALYSIS_MODE=responses_schema.")
        if (
            self.analysis_mode in {"prompt", "chat_schema"}
            and not self.use_local_or_custom_base_url
            and not self.use_hf
            and not self.use_github_models
            and not has_openai_key
        ):
            raise ValueError(
                "Set OPENAI_BASE_URL for local/custom providers, or set "
                "HF_TOKEN, GITHUB_TOKEN, or OPENAI_API_KEY."
            )
        return self
