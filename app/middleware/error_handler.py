# app/middleware/error_handler.py
import logging

from fastapi import Request
from fastapi.responses import JSONResponse
from app.libraries.utils.response_builder import ResponseBuilder
from app.libraries.exceptions.app_exceptions import AppError

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
