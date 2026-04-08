"""
logger.py
Centralized logging configuration for OverAI Windows overlay.
Outputs to both console and a rotating log file under %APPDATA%/overai/.
"""

import logging
import sys
from logging.handlers import RotatingFileHandler

from .health_checks import LOG_DIR

LOG_FILE = LOG_DIR / "overai.log"
MAX_LOG_SIZE = 2 * 1024 * 1024  # 2 MB
BACKUP_COUNT = 3


def get_logger(name: str) -> logging.Logger:
    """Return a named logger with console and file handlers."""
    logger = logging.getLogger(f"overai.{name}")
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)-8s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    logger.addHandler(console)

    try:
        file_handler = RotatingFileHandler(
            LOG_FILE,
            maxBytes=MAX_LOG_SIZE,
            backupCount=BACKUP_COUNT,
            encoding="utf-8",
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except OSError:
        logger.warning("Could not create log file at %s", LOG_FILE)

    return logger
