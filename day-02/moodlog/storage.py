import json
from pathlib import Path

DATA_FILE = Path("moods.json")

def load_entries() -> list[dict]:
    if not DATA_FILE.exists():
        return[]
    try:
        return json.loads(DATA_FILE.read_text())
    except json.JSONDecodeError:
        return []

def save_entries(entries: list[dict]) -> None:
    DATA_FILE.write_text(json.dumps(entries, indent=2))