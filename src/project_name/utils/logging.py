"""Centralised logging configuration."""

import logging
import sys

from project_name.config import get_settings


def get_logger(name: str) -> logging.Logger:
    """Return a configured logger for the given module name.

    Usage:
        from project_name.utils.logging import get_logger
        logger = get_logger(__name__)
        logger.info("Hello!")
    """
    settings = get_settings()

    logger = logging.getLogger(name)
    logger.setLevel(settings.log_level)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(settings.log_level)
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d — %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger