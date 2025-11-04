# app/libraries/utils/response_builder.py
from __future__ import annotations

from typing import Optional, TypeVar

from fastapi import HTTPException

from app.libraries.utils.response_models import ApiResponse, ErrorResponse

T = TypeVar("T")


class ResponseBuilder:
    """Utilidad para estandarizar respuestas de la API."""

    @staticmethod
    def success(
        data: Optional[T] = None, message: str = "Operación exitosa"
    ) -> ApiResponse[Optional[T]]:
        return ApiResponse[Optional[T]](message=message, data=data)

    @staticmethod
    def error(error: str, details: Optional[T] = None, status_code: int = 400):
        """Lanza una HTTPException con formato normalizado."""
        content = ErrorResponse(error=error, details=details)
        raise HTTPException(status_code=status_code, detail=content.dict())
