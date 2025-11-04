# IsoTrack Backend MVP

Backend construido con **FastAPI** siguiendo la metodología MVP. Esta versión incluye
módulos simulados para autenticación, compañías, documentos, procesos y diagramas,
organizados bajo las capas `dao`, `logic` y `api`.

## Requisitos

- Python 3.11+
- Dependencias del archivo `requeriments.txt`

## Configuración

1. Copiá el archivo `.env.example` a `.env` y completá los valores necesarios.
2. Instalá dependencias:

```bash
pip install -r requeriments.txt
```

## Ejecución local

```bash
python -m uvicorn app.main:app --reload
```

Esto levanta el servidor en `http://127.0.0.1:8000` con los endpoints base para la fase 1.1.
