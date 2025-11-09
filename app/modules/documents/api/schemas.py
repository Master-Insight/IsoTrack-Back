"""Pydantic schemas for document endpoints."""

from __future__ import annotations

from datetime import datetime, date
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class DocumentType(str, Enum):
    POE = "POE"
    INSTRUCTIVO = "Instructivo"
    POLITICA = "Política"
    PLANTILLA = "Plantilla"
    PRESENTACION = "Presentación"
    VIDEO = "Video"


class DocumentStatus(str, Enum):
    BORRADOR = "borrador"
    APROBADO = "aprobado"
    PUBLICADO = "publicado"


class DocumentBase(BaseModel):
    title: str = Field(..., description="Título del documento")
    code: Optional[str] = Field(default=None, description="Código interno")
    type: DocumentType = Field(default=DocumentType.POE)
    process_id: Optional[str] = Field(
        default=None, description="Proceso asociado al documento"
    )
    owner_id: Optional[str] = Field(
        default=None, description="Responsable del documento"
    )
    description: Optional[str] = Field(
        default=None, description="Descripción o resumen del contenido"
    )
    active: bool = Field(default=True, description="Indica si el documento está activo")


class DocumentCreate(DocumentBase):
    company_id: Optional[str] = Field(
        default=None, description="Empresa propietaria del documento"
    )


class DocumentCreatePayload(DocumentCreate):
    initial_version: Optional[DocumentVersionCreate] = Field(
        default=None,
        description="Versión inicial opcional que se crea junto con el documento",
    )


class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    code: Optional[str] = None
    type: Optional[DocumentType] = None
    process_id: Optional[str] = None
    owner_id: Optional[str] = None
    description: Optional[str] = None
    active: Optional[bool] = None
    company_id: Optional[str] = None


class Document(DocumentBase):
    id: str
    company_id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DocumentVersionBase(BaseModel):
    version: Optional[int] = Field(
        default=None, description="Número de versión (se autoincrementa si no se envía)"
    )
    status: DocumentStatus = DocumentStatus.BORRADOR
    file_url: Optional[str] = Field(
        default=None, description="URL del archivo almacenado en Supabase"
    )
    external_url: Optional[str] = Field(
        default=None, description="URL externa opcional"
    )
    notes: Optional[str] = Field(default=None, description="Notas o comentarios de la versión")
    approved_by: Optional[str] = Field(
        default=None, description="Usuario que aprobó la versión"
    )
    approved_at: Optional[datetime] = Field(
        default=None, description="Fecha de aprobación"
    )


class DocumentVersionCreate(DocumentVersionBase):
    pass


class DocumentVersion(DocumentVersionBase):
    id: str
    document_id: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DocumentReadCreate(BaseModel):
    version: Optional[int] = Field(default=None, description="Versión leída")
    read_at: Optional[datetime] = Field(
        default=None, description="Fecha de lectura (por defecto ahora)"
    )
    due_date: Optional[date] = Field(
        default=None, description="Fecha límite de lectura si aplica"
    )


class DocumentRead(BaseModel):
    id: Optional[str] = None
    document_id: str
    user_id: str
    version: int
    read_at: datetime
    due_date: Optional[date] = None

    class Config:
        from_attributes = True


class DocumentDetail(Document):
    versions: List[DocumentVersion] = Field(default_factory=list)
    latest_version: Optional[DocumentVersion] = None
    current_user_read: Optional[DocumentRead] = None


class DocumentListResponse(BaseModel):
    items: List[Document]
