from __future__ import annotations
import re
import csv
from pathlib import Path
from datetime import datetime

def normalize_text(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()

def normalize_name(s: str) -> str:
    s = normalize_text(s)
    return " ".join(p.capitalize() for p in s.split(" ")) if s else ""

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

def clean_row(row: dict) -> dict:
    return {
        "id": int(row["id"]),
        "customer": normalize_name(row["customer"]),
        "city": normalize_text(row["city"]).title(),
        "product": normalize_text(row["product"]).title(),
        "price": parse_price(row["price"]),
        "region": row.get("region", "").strip().lower(),
    }

def clean_one(src: Path, dst: Path) -> tuple[int, int]:
     rows_in = rows_out = 0
     dst.parent.mkdir(parents=True, exist_ok=True)
     with src.open("r", encoding="utf-8", newline="") as fin, \
     dst.open("w", encoding="utf-8", newline="") as fout:
          reader = csv.DictReader(fin)
          writer = csv.DictWriter(fout, fieldnames=["id", "customer", "city", "product", "price", "region"])
          writer.writeheader()
          for row in reader:
               rows_in += 1
               cleaned = clean_row(row)
               if cleaned["customer"] and cleaned["price"] is not None:
                    writer.writerow(cleaned)
                    rows_out += 1
     return rows_in, rows_out

def walk_and_clean(root: Path, out_root: Path) -> dict[str, tuple[int, int]]:
     results: dict[str, tuple[int, int]] = {}
     for src in root.rglob("*.csv"):
          rel = src.relative_to(root)
          dst = out_root / rel
          results[str(rel)] = clean_one(src, dst)
     return results

def main() -> None:
     src_root = Path("data")
     dst_root = Path("clean")
     if not src_root.exists():
          print("Run make_tree.py first.")
          return
     results = walk_and_clean(src_root, dst_root)
     total_in = total_out = 0
     print(f"{'file':<30} {'in':>6} {'out':>6} {'dropped':>8}")
     print("-" * 52)
     for name, (rin, rout) in sorted(results.items()):
          print(f"{name:<30} {rin:>6} {rout:>6} {rin - rout:>8}")
          total_in += rin
          total_out += rout
     print("-" * 52)
     print(f"{'TOTAL':<30} {total_in:>6} {total_out:>6} {total_in - total_out:>8}")

if __name__ == "__main__":
     main()