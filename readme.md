# IsoTrack Backend MVP — Importación de Datos (Excel y CSV)

Backend construido con **FastAPI** siguiendo el enfoque MVP.  
Incluye módulos para compañías, usuarios, documentos, versiones, lecturas,
procesos, tareas, diagramas y vínculos (`artifact_links`), organizados en capas
`dao`, `logic` y `api`.

---

# 📦 Requisitos

- Python 3.11+
- Dependencias en `requirements.txt`

---

# ⚙️ Configuración Inicial

1. Copiá `.env.example` → `.env` y completá los valores necesarios.

### Para usar datos mock

```
DATA_SOURCE=mock
MOCK_DATA_PATH=doc/mock_data.json
```

### Para usar Supabase real

```
DATA_SOURCE=supabase
SUPABASE_URL=...
SUPABASE_KEY=...
```

2. Instalá dependencias:

```bash
pip install -r requirements.txt
```

---

# 🚀 Ejecución del servidor

```bash
python -m uvicorn app.main:app --reload
```

---

# 📥 Importación de Datos (Excel y CSV)

IsoTrack permite cargar datos desde:

- Archivos **Excel (.xlsx)**
- Archivos **CSV**
- JSON (cuando `DATA_SOURCE=mock`)

Los scripts están ubicados en:

```
scripts/import_excel.py
scripts/import_supabase.py
scripts/import_utils.py
scripts/excel_to_csv.py
```

---

# 📘 1. Importar desde Excel (.xlsx)

El archivo Excel debe tener **una hoja por tabla**, siguiendo este orden:

```python
TABLE_SEQUENCE = (
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
```

### ▶ Ejecutar importación completa

```bash
python scripts/import_excel.py --file doc/imports/base.xlsx
```

### Opciones

```
--file     archivo a procesar
--dry-run  muestra lo que se importaría sin escribir en Supabase
```

---

# 📗 2. Importar desde CSV (todos los CSV a la vez)

Los CSV deben estar en la carpeta:

```
doc/imports/
```

Ejemplo de estructura:

```
doc/imports/
   companies.csv
   user_profiles.csv
   documents.csv
   document_versions.csv
   document_reads.csv
   processes.csv
   tasks.csv
   diagrams.csv
   artifact_links.csv
```

### ▶ Ejecutar importación

```bash
python scripts/import_supabase.py --folder doc/imports
```

Este script:

- Lee cada CSV
- Normaliza arrays, fechas, jsonb
- Deduplica `artifact_links`
- Ejecuta `upsert` por tabla

---

# 📘 3. Importar un CSV por separado (tabla única)

Cuando quieras importar solo **una tabla**, podés usar:

### Ejemplo: importar solo `documents.csv`

```bash
python - << 'EOF'
from app.services.supabase_client import supabase
import csv

table = "documents"
with open("doc/imports/documents.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

supabase.table(table).upsert(rows).execute()
print(f"{len(rows)} filas importadas en '{table}'")
EOF
```

### Ejemplo: importar solo procesos

```bash
python - << 'EOF'
from app.services.supabase_client import supabase
import csv

table = "processes"
with open("doc/imports/processes.csv", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

supabase.table(table).upsert(rows).execute()
print("Procesos importados:", len(rows))
EOF
```

📌 **Este método sirve cuando querés depurar / corregir una sola tabla.**

---

# 🔄 4. Conversión de Excel (.xlsx) → CSV

Ya tenés el script:

`scripts/excel_to_csv.py`

### ▶ Ejecutar conversión

```bash
python scripts/excel_to_csv.py
```

Esto generará:

```
companies.csv
user_profiles.csv
documents.csv
...
```

en la carpeta actual del script.

---

# 🧪 5. Prueba completa (Smoke Test)

Ejecutar:

```bash
python scripts/smoke_test.py
```

Verifica:

- Creación de documentos
- Creación de versiones
- Registro de lecturas
- Creación de procesos y vínculos
- Creación de diagramas

---

# 📌 Reglas Importantes para Importar

✔ Todos los IDs deben ser **UUID válidos**  
✔ Arrays deben usar formato PostgreSQL:  

```
{"valor1","valor2"}
```  

✔ JSONB debe ser un string JSON válido  
✔ No debe haber filas con columnas fuera del esquema  
✔ `artifact_links` debe respetar:  

```
(from_id, from_type, to_id, to_type)
```

---

# ✔ Archivo mantenido por Insight Devs
