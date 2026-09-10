from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path
from statistics import mean

DATA_FILE = Path("moods.json")

#-----Storage Layer-----
def load_entries() -> list[dict]:
    if not DATA_FILE.exists():
        return[]
    try:    
        return json.loads(DATA_FILE.read_text())
    except json.JSONDecodeError:
        return[]

def save_entries(entries: list[dict]) -> None:
    DATA_FILE.write_text(json.dumps(entries, indent=2))        

#-----Domain Logic-----
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

#-----CLI-----
def prompt_int(prompt: str, lo: int, hi: int) -> int:
    while True:
        try:
            value = int(input(prompt))
            if lo <= value <= hi:
                return value
            print(f"Please enter a number between {lo} and {hi}.")
        except ValueError:
            print("That was not a number - try again")

def main() -> None:
    entries = load_entries()
    print("=== MoodLog ===")
    print(summarize(entries))

    while True:
        choice = input("\n[a]dd [v]iew recent [s]ummary [streak] [q]uit: ").strip().lower()
        match choice:
            case "a":
                mood = prompt_int("Mood(1-10): ", 1, 10)
                note = input("One-line note: ").strip()
                add_entry(entries, mood, note)
                print("Saved ✔")
            case "v":
                for e in entries[-5:]:
                    print(f"{e['timestamp']} {e['mood']}/10 {e['note']}")
            case "s":
                print(summarize(entries))
            case "streak":
                streak = len(entries)
                if streak == 1:
                    print(f"You've showed up for {streak} day")
                else:
                    print(f"You've showed up for {streak} days")
            case "q":
                print("Bye 👋")
                break
            case _:
                print("Unknown Option.")

if __name__ == "__main__":
    main()