# app\libraries\utils\response_models.py
"""Typed response payloads shared across the API."""

from __future__ import annotations

from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel


T = TypeVar("T")


class ApiResponse(GenericModel, Generic[T]):
    """Envelope for successful responses."""

    success: bool = True
    message: str = "Operación exitosa"
    data: Optional[T] = None


class ErrorResponse(BaseModel):
    """Envelope for error responses."""

    success: bool = False
    error: str
    details: Optional[Any] = None
