"""Schemas for company endpoints."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class CompanyBase(BaseModel):
    name: str = Field(..., description="Nombre legal de la empresa")
    brand_logo: Optional[str] = Field(
        default=None,
        description="URL opcional al logo de la empresa",
    )
    theme: Optional[dict[str, Any]] = Field(
        default=None,
        description="Configuración de colores y branding",
    )


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    name: Optional[str] = Field(default=None, description="Nombre de la empresa")
    brand_logo: Optional[str] = Field(
        default=None, description="URL opcional al logo de la empresa"
    )
    theme: Optional[dict[str, Any]] = Field(
        default=None, description="Configuración de colores y branding"
    )


class Company(CompanyBase):
    id: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
