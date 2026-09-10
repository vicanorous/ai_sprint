from __future__ import annotations
import re
import csv
from pathlib import Path

CITY_MAP = {
    "lagos": "Lagos",
    "la": "Los Angeles",
    "abuja": "Abuja",
    "london": "London",
    "nairobi": "Nairobi",
    "cape town": "Cape Town",
    "accra": "Accra",
}

def normalize_text(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()

def normalize_name(s: str) -> str:
    s = normalize_text(s)
    if not s:
        return " "
    part = s.split(" ")
    return " ".join(p.capitalize() for p in part)

def normalize_city(s: str) -> str:
    s = normalize_text(s).lower()
    return CITY_MAP.get(s, s.title() if s else "")

def normalize_product(s: str) -> str:
    return normalize_text(s).title() if s else ""

def parse_price(s: str) -> float | None:
    if s is None:
        return None
    s = s.replace(",", "").strip().lower()
    if s in ("", "n/a", "free", "-"):
        return None
    try:
        return float(s)
    except ValueError:
        return None

def pars_date(s: str) -> str:
    if not s:
        return ""
    s = s.strip()
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y"):
        try:
            from datetime import datetime
            return datetime.strptime(s, fmt).date().isoformat()
        except ValueError:
            continue
        return ""

def clean_row(row: dict) -> dict:
    return {
        "id": int(row["id"]),
        "name": normalize_name(row["name"]),
        "city": normalize_city(row["city"]),
        "product": normalize_product(row["product"]),
        "price": parse_price(row["price"]),
        "signup_date": pars_date(row["signup_date"])
    }

def clean_csv(src: Path, dst: Path) -> tuple[int, int]:
    rows_in = 0
    rows_out = 0
    with src.open("r", encoding="utf-8", newline="") as fin, \
        dst.open("w", encoding="utf-8", newline="") as fout:
        reader = csv.DictReader(fin)
        writer = csv.DictWriter(fout, fieldnames=["id", "name", "city", "product", "price", "signup_date"])
        writer.writeheader()
        for row in reader:
            rows_in += 1
            cleaned = clean_row(row)
            if cleaned["name"] and cleaned["price"] is not None:
                writer.writerow(cleaned)
                rows_out += 1
    return rows_in, rows_out

def main() -> None:
    src = Path("messy.csv")
    dst = Path("clean.csv")
    if not src.exists():
        print("Run messy_data.py first.")
        return
    rows_in, rows_out = clean_csv(src, dst)
    print(f"In: {rows_in} rows → Out: {rows_out} rows → {dst}")

if __name__ == "__main__":
    main()
