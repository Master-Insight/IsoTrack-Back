"""FastAPI application bootstrap for IsoTrack."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import settings
from app.modules.routes import register_routes


app = FastAPI(
    title="IsoTrack API",
    version="0.1.0",
    description=(
        "API MVP para la plataforma IsoTrack. "
        "Incluye módulos simulados de autenticación, compañías, documentos, "
        "procesos y diagramas."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def log_environment() -> None:
    # Para la fase MVP dejamos un log simple que confirme el entorno cargado.
    environment = settings.ENVIRONMENT
    print(f"Starting IsoTrack API in {environment} mode")


register_routes(app)
