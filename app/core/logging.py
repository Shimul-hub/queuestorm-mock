import logging
import sys
from typing import Any

from app.core.config import Settings


def setup_logging(settings: Settings) -> None:
    level = getattr(logging, settings.log_level.upper(), logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        stream=sys.stdout,
    )


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


def log_event(logger: logging.Logger, event: str, **fields: Any) -> None:
    safe_fields = {k: v for k, v in fields.items() if _is_safe_log_value(v)}
    parts = " ".join(f"{key}={value}" for key, value in safe_fields.items())
    logger.info("%s %s", event, parts)


def _is_safe_log_value(value: Any) -> bool:
    if value is None:
        return True
    text = str(value)
    blocked = ("api_key", "secret", "password", "token", "authorization")
    return not any(marker in text.lower() for marker in blocked)
