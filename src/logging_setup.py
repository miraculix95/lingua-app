"""Central logging configuration.

Replaces the scattered ``print(...)`` calls from the legacy monolith. Streamlit
sessions write to stderr by default; keeping one format makes the run log
actually readable.
"""
from __future__ import annotations

import logging
import os

_CONFIGURED = False


def configure_logging(level: str | int | None = None) -> None:
    global _CONFIGURED
    if _CONFIGURED:
        return
    lvl = level or os.environ.get("LOG_LEVEL", "INFO")
    logging.basicConfig(
        level=lvl,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )
    _CONFIGURED = True


def get_logger(name: str) -> logging.Logger:
    configure_logging()
    return logging.getLogger(name)
