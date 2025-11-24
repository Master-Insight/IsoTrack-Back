"""Schemas for flow management endpoints."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class Position(BaseModel):
    x: float = Field(..., description="Posición X en el lienzo")
    y: float = Field(..., description="Posición Y en el lienzo")


class FlowNodeMetadata(BaseModel):
    notes: Optional[str] = Field(
        default=None, description="Notas contextuales del nodo"
    )
    artifacts: Optional[List[Dict[str, Any]]] = Field(
        default=None, description="Artefactos asociados (documentos, procesos, etc.)"
    )
    roles: Optional[List[str]] = Field(default=None, description="Roles responsables")
    user_assigned: Optional[str] = Field(
        default=None, description="Usuario asignado directamente al nodo"
    )
    visible_for: Optional[List[str]] = Field(
        default=None, description="Roles o usuarios con visibilidad específica"
    )


class FlowNodeBase(BaseModel):
    label: str = Field(..., description="Etiqueta visible del nodo")
    type: str = Field(
        ..., description="Tipo del nodo (step/decision/event/process/integration)"
    )
    system: Optional[str] = Field(
        default=None, description="Sistema relacionado, ej: Vtex"
    )
    code: Optional[str] = Field(
        default=None, description="Identificador opcional del nodo"
    )
    metadata: Optional[FlowNodeMetadata | Dict[str, Any]] = Field(
        default=None, description="Metadatos enriquecidos para el nodo"
    )
    position: Position = Field(..., description="Posición inicial del nodo")


class FlowNodeCreate(FlowNodeBase):
    id: Optional[str] = Field(
        default=None,
        description="Permite indicar un ID custom (útil al importar desde CSV/ReactFlow)",
    )


class FlowNode(FlowNodeBase):
    id: str
    flow_id: str
    company_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class FlowEdgeBase(BaseModel):
    source: str = Field(..., description="Nodo origen")
    target: str = Field(..., description="Nodo destino")
    label: Optional[str] = Field(default=None, description="Etiqueta opcional del edge")
    metadata: Optional[Dict[str, Any]] = Field(
        default=None, description="Metadatos adicionales del edge"
    )


class FlowEdgeCreate(FlowEdgeBase):
    id: Optional[str] = Field(default=None, description="ID custom del edge (opcional)")


class FlowEdge(FlowEdgeBase):
    id: str
    flow_id: str
    company_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class FlowBase(BaseModel):
    title: str = Field(..., description="Nombre del flujo visual")
    description: Optional[str] = Field(
        default=None, description="Descripción del flujo"
    )
    type: Optional[str] = Field(
        default=None, description="Clasificación: principal/auxiliar/área"
    )
    tags: Optional[List[str]] = Field(default=[], description="Tags del flujo")
    area: Optional[str] = Field(default=None, description="Área o dominio asociado")
    visibility: Optional[str] = Field(
        default="public", description="Visibilidad: public/role-based/private"
    )
    visibility_roles: Optional[List[str]] = Field(
        default=None, description="Roles que pueden ver el flujo"
    )


class FlowCreate(FlowBase):
    company_id: Optional[str] = Field(
        default=None, description="Empresa a la que pertenece el flujo"
    )


class Flow(FlowBase):
    id: str
    company_id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class FlowDetail(Flow):
    nodes: List[FlowNode] = Field(default_factory=list)
    edges: List[FlowEdge] = Field(default_factory=list)


class FlowImportPayload(BaseModel):
    flow: FlowCreate = Field(..., description="Datos base del flujo")
    nodes: List[FlowNodeCreate] = Field(
        default_factory=list, description="Listado de nodos a crear"
    )
    edges: List[FlowEdgeCreate] = Field(
        default_factory=list, description="Listado de edges a crear"
    )
