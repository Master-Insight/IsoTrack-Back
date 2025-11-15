# app/middleware/error_handler.py
import logging
from typing import Any

from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.libraries.exceptions.app_exceptions import AppError
from app.libraries.utils.response_models import ErrorResponse

logger = logging.getLogger("app.errors")

""" Error Handler middleware con Custom Exceptions """


async def custom_error_handler(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except AppError as e:
        # Manejo de errores personalizados
        logger.warning(
            "Error de aplicación controlado",
            extra={
                "error": e.message,
                "status_code": e.status_code,
                "details": e.details,
            },
        )
        return JSONResponse(status_code=e.status_code, content=e.to_dict())

    except Exception as e:
        # Errores inesperados → 500 genérico
        logger.exception(
            "Error inesperado no controlado", extra={"path": request.url.path}
        )
        content = {
            "success": False,
            "error": str(e),
            "origin": "Desconocido",
            "status_code": 500,
        }
        return JSONResponse(status_code=500, content=content)


def _build_error_response(
    message: str, *, details: Any = None, status_code: int = 400
) -> JSONResponse:
    """Helper to build a JSONResponse using the standard error envelope."""

    payload = ErrorResponse(error=message, details=details)
    return JSONResponse(status_code=status_code, content=payload.dict())


async def http_exception_handler(
    request: Request, exc: HTTPException | StarletteHTTPException
):
    """Normalize HTTPException payloads to the standard error format."""

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
    """Normalize validation errors raised by FastAPI."""

    return _build_error_response(
        "Datos inválidos", details=exc.errors(), status_code=422
    )


""" Error Handler middleware sin Custom Exceptions """
# async def custom_error_handler(request: Request, call_next):
#     try:
#         return await call_next(request)
#     except Exception as e:
#         # Si ya es HTTPException, la dejamos pasar
#         if hasattr(e, "status_code"):
#             content = getattr(e, "detail", str(e))
#             return JSONResponse(status_code=e.status_code, content=content)

#         # Si es otra excepción, la normalizamos
#         error = ResponseBuilder.error("Error interno del servidor", str(e), 500)

#         # No levantamos, devolvemos la respuesta directamente
#         return JSONResponse(status_code=500, content=error)
