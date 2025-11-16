"""Pydantic schemas for artifact link operations."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ArtifactEntityType(str, Enum):
    """Lista de artefactos soportados dentro del MVP."""

    DOCUMENT = "document"
    PROCESS = "process"
    TASK = "task"
    DIAGRAM = "diagram"


class ArtifactLinkBase(BaseModel):
    from_id: str = Field(..., description="Identificador del artefacto origen")
    from_type: ArtifactEntityType = Field(
        default=ArtifactEntityType.DOCUMENT,
        description="Tipo del artefacto origen",
    )
    to_id: str = Field(..., description="Identificador del artefacto destino")
    to_type: ArtifactEntityType = Field(
        default=ArtifactEntityType.DOCUMENT,
        description="Tipo del artefacto destino",
    )
    relation_type: Optional[str] = Field(
        default=None,
        description="Etiqueta opcional para describir la relación",
    )


class ArtifactLinkCreate(ArtifactLinkBase):
    pass


class ArtifactLink(ArtifactLinkBase):
    id: str
    company_id: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
