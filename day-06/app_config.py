from __future__ import annotations
import os
from pathlib import Path
from dotenv import load_dotenv

def _find_env(start: Path) -> Path | None:
    for parent in [start, *start.parents]:
        candidate = parent/ ".env"
        if candidate.is_file():
            return candidate
    return None

_env_path = _find_env(Path(__file__).resolve().parent)
if _env_path:
    load_dotenv(_env_path)
else:
    print("WARNING: no .env file found. Using environment defaults")


def _get(name: str, default: str | None = None, *, required: bool = False) -> str:
    val = os.getenv(name, default)
    if required and (val is None or val == ""):
        raise RuntimeError(f"Missing required env var: {name}")
    return val or ""


class Config:
    @property
    def data_dir(self) -> Path:
        return Path(_get("DATA_DIR", "data"))

    @property
    def clean_dir(self) -> Path:
        return Path(_get("CLEAN_DIR", "clean"))

    @property
    def log_dir(self) -> Path:
        return Path(_get("LOG_DIR", "logs"))

    @property
    def log_level(self) -> str:
        return _get("LOG_LEVEL", "INFO").upper()

    @property
    def log_retention_days(self) -> int:
        return int(_get("LOG_RETENTION_DAYS", "7"))

    @property
    def app_env(self) -> str:
        return _get("APP_ENV", "development")

    @property
    def app_port(self) -> int:
        return int(_get("APP_PORT", "5000"))

config = Config()