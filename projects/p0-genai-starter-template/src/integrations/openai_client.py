"""GenAI Starter Template — OpenAI client factory.

Provides :func:`init`, which builds an :class:`openai.AsyncOpenAI` client
configured from the application settings.

Usage::

    from src.integrations import openai_client
    from src.settings import Settings

    settings = Settings()
    client = openai_client.init(settings)
"""

import openai

from src.settings import Settings
from src.utils import constants


def init(settings: Settings) -> openai.AsyncOpenAI:
    """Build an authenticated :class:`openai.AsyncOpenAI` client.

    :param settings: Validated :class:`~src.settings.Settings` instance.
    :return: Ready-to-use async OpenAI client.
    """
    return openai.AsyncOpenAI(
        api_key=settings.openai_api_key.get_secret_value(),
        timeout=constants.REQUEST_TIMEOUT_S,
    )
