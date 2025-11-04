# app\modules\companies\api\schemas.py
"""Esquemas para compañías."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl


class CompanyBase(BaseModel):
    name: str = Field(..., description="Nombre de la concesionaria")
    description: Optional[str] = Field(
        default=None, description="Descripción comercial de la empresa"
    )
    tax_id: Optional[str] = Field(default=None, description="CUIL / CUIT")
    phone: Optional[str] = Field(default=None, description="Teléfono principal")
    address: Optional[str] = Field(default=None, description="Dirección legal")
    logo_url: Optional[HttpUrl] = Field(default=None, description="Logo para branding")


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    tax_id: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    logo_url: Optional[HttpUrl] = None


class Company(CompanyBase):
    id: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
