#!/usr/bin/env python3
"""
SPSMUN 3.0 — Database Update Script
=====================================
Run this whenever you update Kartik.xlsx (or your renamed Excel file).
It re-reads the Excel sheet, converts to JSON, and injects the data
into index.html, replacing the DELEGATES constant automatically.

Usage:
    python update_db.py
    python update_db.py path/to/MyUpdatedFile.xlsx

Requirements:
    pip install pandas openpyxl
"""

import sys
import json
import re
import os
import pandas as pd
from pathlib import Path

# ── Config ──────────────────────────────────────────────────────────────────
EXCEL_FILE = "Kartik.xlsx"          # Change to your Excel filename
HTML_LOGIN = "index.html"           # Login page
HTML_PROFILE = "profile.html"       # Profile page (no data injection needed)
PLACEHOLDER = "const DELEGATES = "  # Marker in index.html
# ────────────────────────────────────────────────────────────────────────────

def load_excel(path: str) -> list[dict]:
    df = pd.read_excel(path, dtype=str)
    df = df.fillna("-")
    records = []
    for _, row in df.iterrows():
        contact = str(row.get("Contact", "-")).strip().replace(" ", "")
        records.append({
            "name": str(row.get("Name", "")).strip(),
            "class": str(row.get("Class", "")).strip(),
            "section": str(row.get("Section", "")).strip(),
            "portfolio": str(row.get("Portfolio", "")).strip(),
            "committee": str(row.get("Committee", "")).strip(),
            "contact": contact,
        })
    return records


def inject_into_html(html_path: str, records: list[dict]) -> None:
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    json_str = json.dumps(records, ensure_ascii=False, separators=(",", ":"))
    new_line = f"  const DELEGATES = {json_str};"

    # Replace the entire const DELEGATES = [...]; line
    pattern = r"  const DELEGATES = \[.*?\];"
    flags = re.DOTALL
    if re.search(pattern, content, flags):
        new_content = re.sub(pattern, new_line, content, flags=flags)
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"  ✓ Injected {len(records)} records into {html_path}")
    else:
        print(f"  ✗ Could not find DELEGATES placeholder in {html_path}")


def main():
    # Determine script directory
    base = Path(__file__).parent

    excel_path = sys.argv[1] if len(sys.argv) > 1 else str(base / EXCEL_FILE)
    html_path  = str(base / HTML_LOGIN)

    if not os.path.exists(excel_path):
        print(f"ERROR: Excel file not found: {excel_path}")
        sys.exit(1)

    if not os.path.exists(html_path):
        print(f"ERROR: HTML file not found: {html_path}")
        sys.exit(1)

    print(f"\nSPSMUN 3.0 — Database Updater")
    print(f"Excel source : {excel_path}")
    print(f"Target HTML  : {html_path}\n")

    print("Reading Excel…")
    records = load_excel(excel_path)
    print(f"  Found {len(records)} delegates.\n")

    print("Injecting into HTML…")
    inject_into_html(html_path, records)

    print("\nDone! Deploy index.html and profile.html to your hosting.\n")


if __name__ == "__main__":
    main()
