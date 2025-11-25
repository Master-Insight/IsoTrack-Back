# app/middleware/error_handler.py
"""Manejadores de errores globales para la aplicación FastAPI."""

from __future__ import annotations

import logging
from typing import Any, Awaitable, Callable

from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.libraries.exceptions.app_exceptions import AppError
from app.libraries.utils.response_models import ErrorResponse

logger = logging.getLogger("app.errors")


async def custom_error_handler(
    request: Request, call_next: Callable[[Request], Awaitable[JSONResponse]]
):
    """Intercepta todas las peticiones para capturar errores controlados y genéricos."""

    try:
        return await call_next(request)

    except AppError as error:
        # Manejo de errores de dominio con payload estructurado
        logger.warning(
            "Error de aplicación controlado",
            extra={
                "error": error.message,
                "status_code": error.status_code,
                "details": error.details,
            },
        )
        return JSONResponse(status_code=error.status_code, content=error.to_dict())

    except Exception as error:  # pragma: no cover - fallback defensivo
        # Errores inesperados → 500 genérico
        logger.exception(
            "Error inesperado no controlado", extra={"path": request.url.path}
        )
        content = {
            "success": False,
            "error": str(error),
            "origin": "Desconocido",
            "status_code": 500,
        }
        return JSONResponse(status_code=500, content=content)


def _build_error_response(
    message: str, *, details: Any = None, status_code: int = 400
) -> JSONResponse:
    """Genera respuestas de error con el contrato estándar de la API."""

    payload = ErrorResponse(error=message, details=details)
    return JSONResponse(status_code=status_code, content=payload.model_dump())


async def http_exception_handler(
    request: Request, exc: HTTPException | StarletteHTTPException
):
    """Normaliza respuestas de :class:`HTTPException` a nuestro formato."""

    detail = exc.detail

    if (
        isinstance(detail, dict)
        and detail.get("success") is False
        and "error" in detail
    ):
        return JSONResponse(status_code=exc.status_code, content=detail)

    if isinstance(detail, dict):
        message = (
            detail.get("message") or detail.get("error") or "Error en la solicitud"
        )
        extra_details = detail.get("details")
    else:
        message = str(detail) if detail else "Error en la solicitud"
        extra_details = None

    return _build_error_response(
        message, details=extra_details, status_code=exc.status_code
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Normaliza errores de validación generados por FastAPI."""

    return _build_error_response(
        "Datos inválidos", details=exc.errors(), status_code=422
    )
