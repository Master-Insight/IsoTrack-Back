# IsoTrack Backend MVP

Backend construido con **FastAPI** siguiendo la metodología MVP. Esta versión incluye
módulos simulados para autenticación, compañías, documentos, procesos y diagramas,
organizados bajo las capas `dao`, `logic` y `api`.

## Requisitos

- Python 3.11+
- Dependencias del archivo `requeriments.txt`

## Configuración

1. Copiá el archivo `.env.example` a `.env` y completá los valores necesarios.
   - Utilizá `DATA_SOURCE=mock` para habilitar el cliente de datos en memoria definido en `app/services/mock_supabase_client.py`.
   - Cuando `DATA_SOURCE=mock`, podés indicar un archivo con datos iniciales mediante `MOCK_DATA_PATH` (ver `doc/mock_data.json`).
2. Instalá dependencias:

```bash
pip install -r requeriments.txt
```

## Ejecución local

```bash
python -m uvicorn app.main:app --reload
```

Esto levanta el servidor en `http://127.0.0.1:8000` con los endpoints base para la fase 1.1.
