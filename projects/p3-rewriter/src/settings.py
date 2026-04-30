"""Rewriter — settings.

Reads configuration from environment variables or a ``.env`` file.
Either ``HF_TOKEN`` (recommended on corporate/Danske networks) or
``OPENAI_API_KEY`` must be set.
"""

import pydantic
import pydantic_settings


class Settings(pydantic_settings.BaseSettings):
    """Runtime configuration.

    :param hf_token: HuggingFace access token — routes via router.huggingface.co.
    :param openai_api_key: OpenAI API key — used on personal/home networks only.
    :param openai_model: Model name. Defaults to ``"Qwen/Qwen2.5-7B-Instruct"``.
    :param max_tokens: Maximum tokens per completion. Defaults to ``512``.
    :param temperature: Sampling temperature. Defaults to ``0.4`` (rewriting task).
    """

    model_config = pydantic_settings.SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    hf_token: pydantic.SecretStr = pydantic.Field(
        default=pydantic.SecretStr(""),
        description="HuggingFace access token — routes via router.huggingface.co.",
    )
    openai_api_key: pydantic.SecretStr = pydantic.Field(
        default=pydantic.SecretStr(""),
        description="OpenAI API key — used on personal/home networks only.",
    )
    openai_model: str = pydantic.Field(
        default="Qwen/Qwen2.5-7B-Instruct",
        description="Model identifier. HF models use org/name format.",
    )
    max_tokens: int = pydantic.Field(
        default=512,
        description="Maximum tokens per completion response.",
    )
    temperature: float = pydantic.Field(
        default=0.4,
        description="Sampling temperature — 0.4 balances creativity and coherence for rewriting.",
    )

    @pydantic.computed_field  # type: ignore[misc]
    @property
    def use_hf(self) -> bool:
        """True when HF_TOKEN is set and should be used.

        :return: Whether to route via HuggingFace.
        """
        return bool(self.hf_token.get_secret_value().strip())

    @pydantic.model_validator(mode="after")
    def require_at_least_one_key(self) -> "Settings":
        """Abort if no credential is set.

        :raises ValueError: If all credential fields are blank.
        :return: The validated settings instance.
        """
        has_hf = bool(self.hf_token.get_secret_value().strip())
        has_oai = bool(self.openai_api_key.get_secret_value().strip())
        if not has_hf and not has_oai:
            raise ValueError(
                "Set HF_TOKEN (recommended) or OPENAI_API_KEY in your .env file.\n"
                "Copy .env.example → .env and fill in your token."
            )
        return self
