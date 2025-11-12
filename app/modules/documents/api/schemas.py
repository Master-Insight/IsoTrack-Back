"""Pydantic schemas for document endpoints."""

from __future__ import annotations

from datetime import datetime, date
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict, field_validator


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
    REVISION = "en_revision"
    VIGENTE = "vigente"


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
    category: Optional[str] = None
    tags: Optional[List[str]] = None


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
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    nextReviewAt: Optional[datetime] = None


class Document(DocumentBase):
    id: str
    company_id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DocumentVersionBase(BaseModel):
    version: Optional[float] = Field(
        default=None, description="Número de versión (se autoincrementa si no se envía)"
    )
    status: DocumentStatus = DocumentStatus.BORRADOR
    file_url: Optional[str] = Field(
        default=None, description="URL del archivo almacenado en Supabase"
    )
    external_url: Optional[str] = Field(
        default=None, description="URL externa opcional"
    )
    status
    notes: Optional[str] = Field(
        default=None, description="Notas o comentarios de la versión"
    )
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


class DocumentVersionListItem(BaseModel):
    id: str
    document_id: str
    version: Optional[str] = None
    status: Optional[str] = None
    file_url: Optional[str] = None
    external_url: Optional[str] = None
    notes: Optional[str] = None
    approved_by: Optional[str] = None
    approved_by_name: Optional[str] = None
    approved_at: Optional[datetime] = None
    format: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    @field_validator("version", mode="before")
    @classmethod
    def _coerce_version(cls, value):  # noqa: D401 - simple coercion helper
        """Ensure version values are serialized as strings when present."""
        if value is None:
            return value
        return str(value)


class DocumentReadSummary(BaseModel):
    id: Optional[str] = None
    document_id: Optional[str] = None
    user_id: str
    user: Optional[str] = None
    position: Optional[str] = None
    read_at: datetime = Field(alias="readAt")
    due_date: Optional[date] = Field(default=None, alias="dueDate")

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class DocumentListItem(Document):
    owner: Optional[str] = None
    status: Optional[str] = None
    category: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    created_at: Optional[datetime] = Field(default=None, alias="createdAt")
    updated_at: Optional[datetime] = Field(default=None, alias="updatedAt")
    current_version: Optional[DocumentVersionListItem] = Field(
        default=None, alias="currentVersion"
    )
    versions: List[DocumentVersionListItem] = Field(default_factory=list)
    reads: List[DocumentReadSummary] = Field(default_factory=list)
    next_review_at: Optional[datetime] = Field(default=None, alias="nextReviewAt")

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class DocumentListResponse(BaseModel):
    items: List[DocumentListItem]
