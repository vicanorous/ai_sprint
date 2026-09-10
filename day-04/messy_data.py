import csv
import random
from pathlib import Path

random.seed(42)

names = ["Ada Lovelace", "alan turing","Grace Hopper", "Linus Torvalds", "Tim Berners-Lee", "Margaret Hamilton", "Dennis Ritchie", "Donald Knuth", "guido van rossum", "Brian Kernighan"]
cities = ["Lagos", "lagos", "LA", "Abuja", "London", "london", "Nairobi", "Cape Town", "Accra, "]
products = ["Laptop", "laptop", "Phone", "PHONE", "Tablet", "tablet", "Monitor", "monitor", "Keyboard", "MOUSE"]

rows = []
for i in range(1, 51):
    rows.append({
        "id": i,
        "name": random.choice(names),
        "city": random.choice(cities),
        "product": random.choice(products),
        "price": random.choice([1200, "1,200.00", 1299.99, "N/A", 850, None, "free", 0]),
        "signup_date": random.choice(["2026-01-15", "2026/01/15", "15-01-2026", "", None, "yesterday"]),
    })

out = Path("messy.csv")
with out.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote {len(rows)} rows to {out}")