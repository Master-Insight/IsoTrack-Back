# app/middleware/request_context.py
"""Middleware para enriquecer los logs con contexto de cada petición."""

from __future__ import annotations

import logging
import time
import uuid
from typing import Awaitable, Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.config.logging import clear_logging_context, set_request_id


class RequestContextLogMiddleware(BaseHTTPMiddleware):
    """Agrega un request_id y tiempos de respuesta a los logs."""

    def __init__(self, app):  # type: ignore[override]
        super().__init__(app)
        self.logger = logging.getLogger("app.request")

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        set_request_id(request_id)

        start_time = time.perf_counter()
        self.logger.info(
            "Nueva petición",
            extra={
                "http_method": request.method,
                "path": request.url.path,
                "query": request.url.query,
                "client": request.client.host if request.client else None,
            },
        )

        response = None
        try:
            response = await call_next(request)
            return response
        except Exception:
            self.logger.exception(
                "Error no controlado durante la petición",
                extra={
                    "http_method": request.method,
                    "path": request.url.path,
                },
            )
            raise
        finally:
            duration_ms = (time.perf_counter() - start_time) * 1000
            status_code = response.status_code if response is not None else 500
            self.logger.info(
                "Petición completada",
                extra={
                    "http_method": request.method,
                    "path": request.url.path,
                    "status_code": status_code,
                    "process_time_ms": round(duration_ms, 2),
                },
            )

            if response is not None:
                response.headers["X-Request-ID"] = request_id

            clear_logging_context()
