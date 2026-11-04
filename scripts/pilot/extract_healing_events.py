"""
SelfHeal Pilot — Healing Event Extractor.
Moon Sanctum Labs -- Decode. Build. Evolve.

Extracts healing events from the local selfheal.db SQLite database
and exports them as anonymised JSON records.

Usage:
    python scripts/pilot/extract_healing_events.py
    python scripts/pilot/extract_healing_events.py --db artifacts/selfheal.db --output pilot_events.json

Read-only: does not modify the database.
"""

import argparse
import json
import sqlite3
import sys
from pathlib import Path


def extract_events(db_path: str, anonymise: bool = True) -> list[dict]:
    """Extract healing events from the SQLite database."""
    if not Path(db_path).exists():
        print(f"[EXTRACT] Database not found: {db_path}")
        return []

    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row

    try:
        # Check if healing_events table exists
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='healing_events'"
        )
        if not cursor.fetchone():
            print("[EXTRACT] No healing_events table found in database.")
            return []

        rows = conn.execute("""
            SELECT * FROM healing_events
            ORDER BY rowid DESC
        """).fetchall()

        events = []
        for row in rows:
            event = dict(row)

            if anonymise:
                # Remove potentially sensitive fields
                for key in list(event.keys()):
                    # Redact any field that might contain application URLs or content
                    if key in ("page_url", "url"):
                        event[key] = "[REDACTED]"

            events.append(event)

        print(f"[EXTRACT] Found {len(events)} healing event(s)")
        return events

    finally:
        conn.close()


def extract_baselines(db_path: str) -> dict:
    """Extract baseline summary statistics (not raw fingerprints)."""
    if not Path(db_path).exists():
        return {"total": 0, "error": "Database not found"}

    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    try:
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='element_fingerprints'"
        )
        if not cursor.fetchone():
            return {"total": 0, "error": "No fingerprints table"}

        count = conn.execute("SELECT COUNT(*) FROM element_fingerprints").fetchone()[0]
        return {"total": count}
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(
        description="SelfHeal Pilot — Extract healing events from database"
    )
    parser.add_argument(
        "--db",
        default="artifacts/selfheal.db",
        help="Path to selfheal.db (default: artifacts/selfheal.db)",
    )
    parser.add_argument("--output", help="Save events to JSON file")
    parser.add_argument(
        "--no-anonymise",
        action="store_true",
        help="Disable URL anonymisation (not recommended for sharing)",
    )
    parser.add_argument(
        "--include-baselines",
        action="store_true",
        help="Include baseline fingerprint count in output",
    )

    args = parser.parse_args()

    events = extract_events(args.db, anonymise=not args.no_anonymise)

    output_data = {
        "selfheal_version": "1.0.0",
        "total_events": len(events),
        "events": events,
    }

    if args.include_baselines:
        output_data["baselines"] = extract_baselines(args.db)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2, default=str)
        print(f"[EXTRACT] Events saved to {output_path}")
    else:
        print(json.dumps(output_data, indent=2, default=str))


if __name__ == "__main__":
    main()

