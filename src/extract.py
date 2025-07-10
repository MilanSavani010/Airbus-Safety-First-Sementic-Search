"""
extract.py  –  Step-2 of the SRM demo pipeline
Tailored for the five sample SRM pages (png) you placed in data/raw/.

Workflow
1.  Read raw OCR text from 'staging' in srm_demo.db
2.  Parse:
      • section  – e.g. 'Wing Rib 12 — Crack near Leading Edge Panel'
      • limit_mm – list of numeric millimetre limits found in the table
3.  Write results to a fresh table 'srm' (over-writes each run)
"""

from __future__ import annotations
import re, sqlite3, pandas as pd
from pathlib import Path
from src.config import DB_PATH

# ---------------------------------------------------------------------------
# Regex helpers – tuned after looking at the OCR output of page1-5
# ---------------------------------------------------------------------------

RE_SECTION = re.compile(r"^(frame|wing|tail|cargo|nose)\b.*$", re.I | re.M)

# e.g. '2 (0,8)'  OR  '2 (0.8)'  OR  '0.04'
RE_MM = re.compile(r"\b(\d+(?:[.,]\d+)?)\s*(?=\(|mm|\s)", re.I)

def clean(txt: str) -> str:
    txt = txt.replace("O", "0")  # common OCR swap in tables
    txt = txt.replace(" ", " ")  # nbsp to normal space
    return re.sub(r"\s+", " ", txt.strip())


def parse(row: pd.Series) -> dict:
    raw = clean(row["text"].lower())

    # 1️⃣  section / subtitle
    section = ""
    m = RE_SECTION.search(raw)
    if m:
        # take the whole line the match sits on
        section = raw.splitlines()[raw.count("\n", 0, m.start())].strip().title()

    # 2️⃣  numeric limits (collect unique mm values)
    limits = {val.replace(",", ".") for val in RE_MM.findall(raw)}
    limits_sorted = ", ".join(sorted(limits, key=lambda x: float(x)))

    return {
        "fname":     row["fname"],
        "section":   section,
        "limit_mm":  limits_sorted,
        "preview":   raw[:220] + "…"
    }


# ---------------------------------------------------------------------------
def main() -> None:
    if not Path(DB_PATH).exists():
        raise SystemExit(f"DB not found → {DB_PATH}. Run ingest first.")

    with sqlite3.connect(DB_PATH) as con:
        df = pd.read_sql("SELECT fname, text FROM staging", con)
        if df.empty:
            print("[EXTRACT] staging table empty – nothing to parse.")
            return

        parsed = pd.DataFrame(df.apply(parse, axis=1).tolist())

        # (re)create the structured table
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS srm")
        cur.execute("""
            CREATE TABLE srm (
              fname    TEXT PRIMARY KEY,
              section  TEXT,
              limit_mm TEXT,
              preview  TEXT
            )""")
        parsed.to_sql("srm", con, if_exists="append", index=False)

        print(f"[EXTRACT] Parsed {len(parsed)} docs ➜ table 'srm'")
        # quick eyeball
        print(parsed[["fname", "section", "limit_mm"]].to_markdown(index=False))


if __name__ == "__main__":
    main()
