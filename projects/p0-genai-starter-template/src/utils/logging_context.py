"""GenAI Starter Template — structured JSON logging to stderr.

All loggers are named ``genai_starter.<module>`` and emit JSON to *stderr*.
stdout is reserved exclusively for the web server / ASGI layer.

Usage::

    from src.utils import logging_context

    logger = logging_context.get_logger("genai_starter.tools.health")
    logger.info("Request received", extra={"endpoint": "/health"})
"""

import logging
import os
import sys

from pythonjsonlogger.json import JsonFormatter

_configured = False


def get_logger(name: str) -> logging.Logger:
    """Return a JSON-over-stderr logger for the given module name.

    Configures the root ``genai_starter`` logger exactly once (idempotent).

    :param name: Logger name — conventionally ``"genai_starter.<module_path>"``.
    :return: A :class:`logging.Logger` instance that writes JSON to ``stderr``.
    """
    global _configured

    if not _configured:
        level_name = os.environ.get("LOG_LEVEL", "INFO").upper()
        level = getattr(logging, level_name, logging.INFO)

        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(
            JsonFormatter(
                fmt="%(asctime)s %(name)s %(levelname)s %(message)s",
                datefmt="%Y-%m-%dT%H:%M:%S",
            )
        )

        root_logger = logging.getLogger("genai_starter")
        root_logger.setLevel(level)
        root_logger.addHandler(handler)
        root_logger.propagate = False

        _configured = True

    return logging.getLogger(name)
