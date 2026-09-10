from . import storage, domain

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
    entries = storage.load_entries()
    print("=== MoodLog ===")
    print(domain.summarize(entries))

    while True:
        choice = input("\n[a]dd [v]iew recent [s]ummary [streak] [q]uit: ").strip().lower()
        match choice:
            case "a":
                mood = prompt_int("Mood(1-10): ", 1, 10)
                note = input("One-line note: ").strip()
                domain.add_entry(entries, mood, note)
                storage.save_entries(entries)
                print("Saved")
            case "v":
                for e in entries[-5:]:
                    print(f"{e['timestamp']} {e['mood']}/10 {e['note']}")
            case "s":
                print(domain.summarize(entries))
            case "streak":
                streak = len(entries)
                if streak == 1:
                    print(f"You've showed up for {streak} day")
                else:
                    print(f"You've showed up for {streak} days")
            case "q":
                print("Bye")
                break
            case _:
                print("Unknown Option.")

if __name__ == "__main__":
    main()