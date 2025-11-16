import sys
import csv
from pathlib import Path

# -----------------------------------------
# Agregar root del proyecto al PYTHONPATH
# -----------------------------------------
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from app.services.supabase_client import supabase

# -----------------------------------------
# Seleccionar tabla por número
# python scripts/import_csv_one_table.py
# -----------------------------------------
TABLE_NUMBER = 9  # 👈 CAMBIÁ ESTE NÚMERO Y LISTO

TABLES = {
    1: "companies",
    2: "user_profiles",
    3: "documents",
    4: "document_versions",
    5: "document_reads",
    6: "processes",
    7: "tasks",
    8: "diagrams",
    9: "artifact_links",
}

# -----------------------------------------
# Validar número
# -----------------------------------------
if TABLE_NUMBER not in TABLES:
    raise SystemExit(
        f"Error: El número {TABLE_NUMBER} no corresponde a ninguna tabla.\n"
        f"Tablas disponibles:\n" + "\n".join([f"{k} → {v}" for k, v in TABLES.items()])
    )

table_name = TABLES[TABLE_NUMBER]
csv_path = Path(f"doc/imports/{table_name}.csv")

if not csv_path.exists():
    raise SystemExit(f"Error: no existe el archivo CSV: {csv_path}")

# -----------------------------------------
# Leer CSV
# -----------------------------------------
with csv_path.open("r", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

if not rows:
    print(f"Advertencia: '{table_name}.csv' está vacío.")

# -----------------------------------------
# Importar usando upsert
# -----------------------------------------
print(f"Importando {len(rows)} filas en la tabla '{table_name}'...")

response = supabase.table(table_name).upsert(rows).execute()

print("✔ Importación completada.")
print(f"✔ Tabla: {table_name}")
print(f"✔ Filas procesadas: {len(rows)}")
