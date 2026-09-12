from __future__ import annotations
import logging
import sys
from datetime import datetime, timedelta
from logging.handlers import RotatingFileHandler

from app_config import config


def setup_logging(name: str = "workplays") -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(getattr(logging, config.log_level, logging.INFO))

    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    stream = logging.StreamHandler(sys.stdout)
    stream.setFormatter(fmt)
    logger.addHandler(stream)

    config.log_dir.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    file_handler = RotatingFileHandler(
        config.log_dir / f"{today}.log",
        maxBytes=1_000_000,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(fmt)
    logger.addHandler(file_handler)

    return logger

def clean_old_logs() -> int:
    if not config.log_dir.exists():
        return 0
    cutoff = datetime.now() - timedelta(days=config.log_retention_days)
    removed = 0
    for f in config.log_dir.glob("*.log"):
        if datetime.fromtimestamp(f.stat().st_mtime) < cutoff:
            f.unlink()
            removed += 1
    return removed


log = setup_logging()