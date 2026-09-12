import csv
import random
from pathlib import Path

random.seed(42)

regions = {"europe": 30, "asia": 40, "africa": 35}
products = ["Laptop", "Phone", "Tablet", "Monitor", "Keyboard", "Mouse"]
cities = ["Lagos", "lagos", "London", "london", "Tokyo", "delhi", "Berlin"]

root = Path("data")
root.mkdir(exist_ok=True)

def make_csv(path: Path, n: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "customer", "city", "product", "price", "region"])
        for i in range(1, n + 1):
            w.writerow([
                i,
                random.choice([" ada lovelace", "ALAN TURING", "Grace Hopper"]),
                random.choice(cities),
                random.choice(products),
                random.choice([1200, "1,200.00", "N/A", 850, None, "free"]),
                path.parts[1] if len(path.parts) > 1 else "unknown",
            ])

for region, n in regions.items():
    make_csv(root / region / f"{region}_north.csv", n)
    make_csv(root / region / f"{region}_south.csv", n)

print(f"Created tree under {root.resolve()}")