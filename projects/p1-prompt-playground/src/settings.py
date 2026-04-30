"""Prompt Playground — settings.

Reads configuration from environment variables or a ``.env`` file.
One of ``HF_TOKEN`` (recommended on corporate networks),
``GITHUB_TOKEN``, or ``OPENAI_API_KEY`` must be set.
"""

import pydantic
import pydantic_settings


class Settings(pydantic_settings.BaseSettings):
    """Runtime configuration.

    Priority order: HF_TOKEN > GITHUB_TOKEN > OPENAI_API_KEY.

    :param hf_token: HuggingFace access token.  Routes calls through
        ``router.huggingface.co`` — reachable on corporate networks.
        Free at huggingface.co/settings/tokens.
    :param github_token: GitHub PAT (legacy option, enterprise-blocked).
    :param openai_api_key: Direct OpenAI API key (home/personal networks).
    :param openai_model: Model name. Defaults to ``"Qwen/Qwen2.5-7B-Instruct"``.
    :param max_tokens: Maximum tokens per completion. Defaults to ``512``.
    :param temperature: Sampling temperature. Defaults to ``0.7``.
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
    github_token: pydantic.SecretStr = pydantic.Field(
        default=pydantic.SecretStr(""),
        description="GitHub PAT (legacy, enterprise-blocked on corporate networks).",
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
        default=256,
        description="Maximum tokens per completion response. Lower = fewer rate-limit hits.",
    )
    temperature: float = pydantic.Field(
        default=0.7,
        description="Sampling temperature — 0 is deterministic, 1 is creative.",
    )

    @pydantic.model_validator(mode="after")
    def require_at_least_one_key(self) -> "Settings":
        """Abort if no API credential is set.

        :raises ValueError: If all credential fields are blank.
        :return: The validated settings instance.
        """
        has_hf = bool(self.hf_token.get_secret_value().strip())
        has_gh = bool(self.github_token.get_secret_value().strip())
        has_oai = bool(self.openai_api_key.get_secret_value().strip())
        if not has_hf and not has_gh and not has_oai:
            raise ValueError(
                "Set HF_TOKEN (recommended on corporate networks) or OPENAI_API_KEY in your .env file.\n"
                "See .env.example for instructions."
            )
        return self

    @property
    def use_hf(self) -> bool:
        """Return True when HuggingFace routing should be used.

        :return: True if HF_TOKEN is present.
        """
        return bool(self.hf_token.get_secret_value().strip())

    @property
    def use_copilot(self) -> bool:
        """Return True when GitHub token is present (legacy).

        :return: True if GITHUB_TOKEN is present and HF_TOKEN is not.
        """
        return not self.use_hf and bool(self.github_token.get_secret_value().strip())
