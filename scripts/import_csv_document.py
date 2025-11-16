from app.services.supabase_client import supabase
import csv

table = "documents"
with open("doc/imports/documents.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

supabase.table(table).upsert(rows).execute()
print(f"{len(rows)} filas importadas en '{table}'")
