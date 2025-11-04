# app/modules/routes.py

from __future__ import annotations

from fastapi import FastAPI

from app.libraries.utils.response_builder import ResponseBuilder

from app.modules.companies.api.routes import router as companies_router
from app.modules.users.api.routes import router as users_router

# from app.modules.diagrams.api.routes import router as diagrams_router
# from app.modules.documents.api.routes import router as documents_router
# from app.modules.processes.api.routes import router as processes_router
# from app.modules.analytics.api.routes import router as analytics_router


def register_routes(app: FastAPI) -> None:
    """Attach all module routers to the FastAPI application."""

    # --- Rutas de módulos Primarios ---
    app.include_router(companies_router, prefix="/companies", tags=["Companies"])
    app.include_router(users_router, prefix="/users", tags=["Users"])
    # app.include_router(documents_router, prefix="/documents", tags=["Documents"])
    # app.include_router(processes_router, prefix="/processes", tags=["Processes"])
    # app.include_router(diagrams_router, prefix="/diagrams", tags=["Diagrams"])

    # --- Rutas de módulos Adicionales ---
    # app.include_router(analytics_router, prefix="/analytics", tags=["Analytics"])
