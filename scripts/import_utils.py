"""Shared helpers for bulk-import scripts."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, List, Sequence

from app.services.supabase_client import supabase

TABLE_SEQUENCE: Sequence[str] = (
    "companies",
    "user_profiles",
    "documents",
    "document_versions",
    "document_reads",
    "processes",
    "tasks",
    "diagrams",
    "artifact_links",
)

CSV_FILE_MAP: Dict[str, str] = {
    table: f"{table}.csv" for table in TABLE_SEQUENCE
}


def load_csv_file(path: Path) -> List[Dict[str, str]]:
    import csv

    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return [dict(row) for row in reader]


def deduplicate_links(rows: Iterable[Dict[str, str]]) -> List[Dict[str, str]]:
    seen = set()
    result: List[Dict[str, str]] = []
    for row in rows:
        key = (
            row.get("from_id"),
            row.get("from_type"),
            row.get("to_id"),
            row.get("to_type"),
        )
        if key in seen:
            continue
        seen.add(key)
        result.append(row)
    return result


def upsert_rows(table: str, rows: List[Dict[str, object]], *, dry_run: bool = False) -> int:
    if not rows:
        return 0
    if dry_run:
        return len(rows)
    supabase.table(table).upsert(rows).execute()
    return len(rows)
