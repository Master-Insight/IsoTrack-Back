"""Pydantic schemas for process and task endpoints."""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ProcessBase(BaseModel):
    code: Optional[str] = Field(default=None, description="Código del proceso")
    name: str = Field(..., description="Nombre del proceso")
    area: Optional[str] = Field(default=None, description="Área responsable")
    owner_id: Optional[str] = Field(default=None, description="Responsable del proceso")
    description: Optional[str] = Field(
        default=None, description="Descripción general del proceso"
    )


class ProcessCreate(ProcessBase):
    company_id: Optional[str] = Field(
        default=None, description="Empresa a la que pertenece el proceso"
    )


class ProcessUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    area: Optional[str] = None
    owner_id: Optional[str] = None
    description: Optional[str] = None
    company_id: Optional[str] = None


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


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    purpose: Optional[str] = None
    scope: Optional[str] = None
    frequency: Optional[str] = None
    responsible_roles: Optional[List[str]] = None


class Task(TaskBase):
    id: str
    company_id: str
    process_id: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ProcessDocumentLink(BaseModel):
    id: Optional[str] = None
    process_id: str
    document_id: str
    artifact_type: Optional[str] = Field(
        default="document",
        description="Tipo de artefacto vinculado (document, diagram, etc)",
    )
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ProcessDetail(Process):
    tasks: List[Task] = Field(default_factory=list)
    links: List[ProcessDocumentLink] = Field(default_factory=list)
