from datetime import datetime
from statistics import mean

def add_entry(entries: list[dict], mood: int, note: str) -> None:
    entries.append({
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "mood": mood,
        "note": note,
    })

def summarize(entries: list[dict]) -> str:
    if not entries:
        return "No entries yet - add one!"
    moods = [e["mood"] for e in entries]
    return (
        f"Entries: {len(entries)} | "
        f"Avg mood: {mean(moods):.1f}/10 | "
        f"Best: {max(moods)} | Worst: {min(moods)}"
    )