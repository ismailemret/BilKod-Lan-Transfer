"""Application logging utilities."""

import logging
from typing import Optional


DEFAULT_LOG_LEVEL = logging.INFO


def configure_logging(level: int = DEFAULT_LOG_LEVEL) -> None:
    """Configure application-wide logging with a consistent console format."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Return a named application logger, auto-configuring if needed."""
    if not logging.getLogger().handlers:
        configure_logging()
    return logging.getLogger(name or "bilkod")