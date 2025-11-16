"""Bulk import data from CSV files into Supabase tables."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from scripts import import_utils


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Importa archivos CSV con datos base hacia Supabase"
    )
    parser.add_argument(
        "--folder",
        default="doc/imports",
        help="Carpeta que contiene los CSV (por defecto doc/imports)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Solo muestra qué se importaría sin escribir en Supabase",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    base_path = Path(args.folder)
    if not base_path.exists():
        raise SystemExit(f"La carpeta {base_path} no existe")

    summary = {}
    for table in import_utils.TABLE_SEQUENCE:
        file_name = import_utils.CSV_FILE_MAP[table]
        csv_path = base_path / file_name
        rows = import_utils.load_csv_file(csv_path)
        if table == "artifact_links":
            rows = import_utils.deduplicate_links(rows)
        inserted = import_utils.upsert_rows(table, rows, dry_run=args.dry_run)
        summary[table] = {"rows": len(rows), "imported": inserted}

    for table, stats in summary.items():
        status = "SKIPPED" if stats["rows"] == 0 else "OK"
        print(f"[{status}] {table}: {stats['imported']} filas importadas")


if __name__ == "__main__":
    main()
