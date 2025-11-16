"""Pydantic schemas for process and task endpoints."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field

from app.modules.artifact_links.api.schemas import ArtifactEntityType, ArtifactLink


class TaskStatus(str, Enum):
    BORRADOR = "borrador"
    APROBADO = "aprobado"
    PUBLICADO = "publicado"
    REVISION = "en_revision"
    VIGENTE = "vigente"


class MaturityLabels(str, Enum):
    ESTABLECIDO = "establecido"
    EN_MEJORA = "en_mejora"
    CRITICO = "critico"


class ProcessBase(BaseModel):
    code: Optional[str] = Field(default=None, description="Código del proceso")
    name: str = Field(..., description="Nombre del proceso")
    area: Optional[str] = Field(default=None, description="Área responsable")
    owner_id: Optional[str] = Field(default=None, description="Responsable del proceso")
    owner: Optional[str] = Field(
        default=None, description="Nombre de la persona responsable del proceso"
    )
    description: Optional[str] = Field(
        default=None, description="Descripción general del proceso"
    )
    parent_id: Optional[str] = Field(
        default=None, description="Proceso padre dentro del mapa de procesos"
    )
    objective: Optional[str] = Field(
        default=None, description="Objetivo principal del proceso"
    )
    inputs: Optional[List[str]] = Field(
        default=None, description="Entradas clave requeridas por el proceso"
    )
    outputs: Optional[List[str]] = Field(
        default=None, description="Entregables generados por el proceso"
    )
    related_documents: Optional[List[str]] = Field(
        default=None,
        description="Documentos asociados directamente al proceso",
    )
    maturity: Optional[MaturityLabels] = Field(
        default=None, description="Nivel de madurez según el sistema de gestión"
    )


class ProcessCreate(ProcessBase):
    company_id: Optional[str] = Field(
        default=None, description="Empresa a la que pertenece el proceso"
    )


class ProcessUpdate(ProcessBase):
    name: Optional[str] = None
    updated_at: Optional[datetime] = Field(
        default=None, description="Fecha de última actualización del proceso"
    )


class Process(ProcessBase):
    id: str
    company_id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TaskBase(BaseModel):
    code: Optional[str] = Field(default=None, description="Código de la tarea")
    name: str = Field(..., description="Nombre de la tarea")
    purpose: Optional[str] = Field(default=None, description="Propósito de la tarea")
    scope: Optional[str] = Field(default=None, description="Alcance de la tarea")
    frequency: Optional[str] = Field(
        default=None, description="Frecuencia de ejecución de la tarea"
    )
    responsible_roles: Optional[List[str]] = Field(
        default=None, description="Roles responsables"
    )
    owner_id: Optional[str] = Field(
        default=None, description="Identificador del responsable directo"
    )
    owner: Optional[str] = Field(
        default=None, description="Nombre del responsable directo"
    )
    related_documents: Optional[List[str]] = Field(
        default=None, description="Documentos vinculados con la tarea"
    )
    status: Optional[TaskStatus] = TaskStatus.BORRADOR


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    purpose: Optional[str] = None
    scope: Optional[str] = None
    frequency: Optional[str] = None
    responsible_roles: Optional[List[str]] = None
    owner_id: Optional[str] = None
    owner: Optional[str] = None
    related_documents: Optional[List[str]] = None
    status: Optional[str] = None
    updated_at: Optional[datetime] = None


class Task(TaskBase):
    id: str
    company_id: str
    process_id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ProcessLinkPayload(BaseModel):
    target_id: str = Field(..., description="ID del artefacto a vincular")
    target_type: ArtifactEntityType = Field(
        default=ArtifactEntityType.DOCUMENT,
        description="Tipo del artefacto destino",
    )
    relation_type: Optional[str] = Field(
        default=None, description="Etiqueta opcional de la relación"
    )


class TaskLinkPayload(ProcessLinkPayload):
    pass


class ProcessDetail(Process):
    tasks: List[Task] = Field(default_factory=list)
    links: List[ArtifactLink] = Field(default_factory=list)
