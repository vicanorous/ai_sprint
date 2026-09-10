from rich.console import Console
from datetime import datetime
import requests
from rich.panel import Panel
import json
from pathlib import Path

DATA_FILE = Path("quotes.json")

console = Console()

def fetch_quote() -> dict:
    url = "https://zenquotes.io/api/random"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    return {"content": data[0]["q"], "author": data[0]["a"]}

#def load_quotes() -> list[dict]:
#    if not DATA_FILE.exists():
#        return[]
#    try:
#        return json.loads(DATA_FILE.read_text())
#    except json.JSONDecodeError:
#        return []
    
def save_quotes(quotes: list[dict]) -> None:
    DATA_FILE.write_text(json.dumps(quotes, indent=2))

def main() -> None:
    try:
        quote = fetch_quote()
    except requests.RequestException as e:
        console.print(f"[red]Could not fetch quote: {e}[/red]")
        return
    body = f'"{quote["content"]}"\n\n-{quote["author"]}'
    console.print(Panel(body, title="Quote of the moment", border_style="cyan"))
    save_quotes(quote)

if __name__ == "__main__":
    main()