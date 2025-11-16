"""Schemas for diagram endpoints."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from app.modules.artifact_links.api.schemas import ArtifactLink, ArtifactEntityType


class DiagramBase(BaseModel):
    title: str = Field(..., description="Nombre del diagrama")
    type: str = Field(..., description="Tipo del diagrama (organigrama/flujo)")
    data: Optional[Dict[str, Any]] = Field(
        default=None, description="Payload JSON del editor visual"
    )
    svg_export: Optional[str] = Field(
        default=None, description="Representación SVG opcional"
    )


class DiagramCreate(DiagramBase):
    company_id: Optional[str] = Field(
        default=None, description="Empresa a la que pertenece el diagrama"
    )


class DiagramUpdate(BaseModel):
    title: Optional[str] = None
    type: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    svg_export: Optional[str] = None
    company_id: Optional[str] = None


class Diagram(DiagramBase):
    id: str
    company_id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DiagramDetail(Diagram):
    links: List[ArtifactLink] = Field(default_factory=list)


class DiagramLinkPayload(BaseModel):
    target_id: str = Field(..., description="ID del artefacto a vincular")
    target_type: ArtifactEntityType = Field(
        default=ArtifactEntityType.PROCESS,
        description="Tipo de artefacto destino",
    )
    relation_type: Optional[str] = Field(default=None)
