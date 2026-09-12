from __future__ import annotations
import re
import csv
from pathlib import Path
#from datetime import datetime

from app_config import config
from app_logging import log, clean_old_logs

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
     log.debug(f"cleaning {src} -> {dst}")
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
     log.info(f"{src.name}: {rows_in} in, {rows_out} out, {rows_in - rows_out} dropped")
     return rows_in, rows_out

def walk_and_clean(root: Path, out_root: Path) -> dict[str, tuple[int, int]]:
     results: dict[str, tuple[int, int]] = {}
     csvs = list(root.rglob("*.csv"))
     log.info(f"found {len(csvs)} CSV files under {root}")
     for src in root.rglob("*.csv"):
          rel = src.relative_to(root)
          dst = out_root / rel
          #results[str(rel)] = clean_one(src, dst)
          try:
               results[str(rel)] = clean_one(src, dst)
          except Exception as e:
               log.exception(f"failed to clean {src}: {e}")
     return results

def main() -> None:
     log.info(f"app cleaner starting (env={config.app_env})")
     removed = clean_old_logs()
     if removed:
          log.info(f"cleaned {removed} old log file(s)")

     src_root = config.data_dir
     dst_root = config.clean_dir
     if not src_root.exists():
          log.warning(f"source dir {src_root} does not exist; run make_tree.py first")
          return
     results = walk_and_clean(src_root, dst_root)
     total_in = total_out = 0
     for rin, rout in results.values():
          total_in += rin
          total_out += rout
     log.info(f"DONE: {total_in} rows in, {total_out} rows out, {total_in - total_out} dropped")

if __name__ == "__main__":
     main()