"""Application factory for IsoTrack backend."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config.logging import setup_logging
from app.middleware.error_handler import (
    custom_error_handler,
    http_exception_handler,
    validation_exception_handler,
)
from app.middleware.request_context import RequestContextLogMiddleware
from app.modules.routes import register_routes

# 🔹 Lista de orígenes permitidos
origins = ["http://localhost:3000", "http://localhost:4321"]


def create_app() -> FastAPI:
    """Create and configure a FastAPI instance."""
    setup_logging()

    app = FastAPI(
        title="IsoTrack API",
        version="0.1.0",
        description="Backend MVP for documentation and processes management.",
    )

    app.add_middleware(RequestContextLogMiddleware)

    app.middleware("http")(custom_error_handler)

    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        # allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_routes(app)
    return app


app = create_app()
