"""
Schemas for flow management endpoints (IsoTrack).
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional, Literal, Union

from pydantic import BaseModel, Field


# ----------------------------------------------------------------------
# Position
# ----------------------------------------------------------------------
class Position(BaseModel):
    x: float = Field(..., description="Posición X en el lienzo")
    y: float = Field(..., description="Posición Y en el lienzo")


# ----------------------------------------------------------------------
# Node Metadata
# ----------------------------------------------------------------------
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


# ----------------------------------------------------------------------
# Flow Node Base
# ----------------------------------------------------------------------
class FlowNodeBase(BaseModel):
    label: str = Field(..., description="Etiqueta visible del nodo")

    type: Literal["step", "decision", "event", "process", "integration"] = Field(
        ..., description="Tipo del nodo"
    )

    system: Optional[str] = Field(
        default=None, description="Sistema relacionado (VTEX, Gateway, etc.)"
    )

    code: Optional[str] = Field(
        default=None, description="Identificador opcional del nodo"
    )

    metadata: Optional[Union[FlowNodeMetadata, Dict[str, Any]]] = Field(
        default=None, description="Metadatos enriquecidos para el nodo"
    )

    position: Optional[Position] = Field(
        default=None, description="Posición inicial del nodo"
    )

    lane: Optional[str] = Field(
        default=None, description="Swimlane o agrupación vertical"
    )

    icon: Optional[str] = Field(
        default=None,
        description="Nombre del icono (lucide-react), ej: 'Zap', 'GitBranch', 'ShoppingCart'",
    )

    color: Optional[str] = Field(
        default=None,
        description="Color del nodo en HEX o nombre (blue/emerald/etc.)",
    )

    width: Optional[int] = Field(
        default=None, description="Ancho del nodo (para nodos custom)"
    )

    height: Optional[int] = Field(
        default=None, description="Alto del nodo (para nodos custom)"
    )

    order_index: Optional[int] = Field(
        default=None,
        description="Orden lógico del nodo dentro del flujo (no afecta al layout auto)",
    )


# ----------------------------------------------------------------------
# Flow Node Create
# ----------------------------------------------------------------------
class FlowNodeCreate(FlowNodeBase):
    position: Position = Field(..., description="Posición inicial del nodo")

    id: Optional[str] = Field(
        default=None,
        description="Permite indicar un ID custom (útil al importar desde CSV/ReactFlow)",
    )


# ----------------------------------------------------------------------
# Flow Node full (DB)
# ----------------------------------------------------------------------
class FlowNode(FlowNodeBase):
    id: str
    flow_id: str
    company_id: Optional[str] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------------------------
# Flow Edge Base
# ----------------------------------------------------------------------
class FlowEdgeBase(BaseModel):
    source_node: Optional[str] = Field(default=None, description="Nodo origen")
    target_node: Optional[str] = Field(default=None, description="Nodo destino")
    label: Optional[str] = Field(default=None, description="Etiqueta opcional del edge")

    metadata: Optional[Dict[str, Any]] = Field(
        default=None, description="Metadatos adicionales del edge"
    )

    type: Literal["straight", "bezier", "smoothstep"] = Field(
        "smoothstep", description="Tipo visual del edge"
    )

    style: Optional[Dict[str, Any]] = Field(
        default=None, description="Estilos del edge (stroke, dash, arrow markers)"
    )


# ----------------------------------------------------------------------
# Flow Edge Create
# ----------------------------------------------------------------------
class FlowEdgeCreate(FlowEdgeBase):
    source_node: str = Field(..., description="Nodo origen")
    target_node: str = Field(..., description="Nodo destino")

    id: Optional[str] = Field(default=None, description="ID custom del edge (opcional)")


# ----------------------------------------------------------------------
# Flow Edge full
# ----------------------------------------------------------------------
class FlowEdge(FlowEdgeBase):
    id: str
    flow_id: str
    company_id: Optional[str] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------------------------
# Flow Base
# ----------------------------------------------------------------------
class FlowBase(BaseModel):
    title: str = Field(..., description="Nombre del flujo visual")

    description: Optional[str] = Field(
        default=None, description="Descripción del flujo"
    )

    type: Literal["principal", "auxiliar", "área"] = Field(
        "principal", description="Tipo de flujo"
    )

    tags: Optional[List[str]] = Field(
        default_factory=list, description="Tags del flujo"
    )

    area: Optional[str] = Field(
        default=None, description="Área o dominio asociado al flujo"
    )

    visibility: Literal["public", "role-based", "private"] = Field(
        "public", description="Nivel de visibilidad del flujo"
    )

    visibility_roles: Optional[List[str]] = Field(
        default=None, description="Roles que pueden ver el flujo"
    )

    layout_mode: Literal["auto", "manual"] = Field(
        "auto", description="Modo de layout: auto (dagre) o manual (usuario)"
    )

    default_lane_mode: Literal["system", "area", "none"] = Field(
        "system", description="Cómo agrupar automáticamente los nodos"
    )

    metadata: Optional[Dict[str, Any]] = Field(
        default=None, description="Metadatos adicionales del flujo (jsonb)"
    )


# ----------------------------------------------------------------------
# Flow Create
# ----------------------------------------------------------------------
class FlowCreate(FlowBase):
    company_id: Optional[str] = Field(
        default=None, description="Empresa a la que pertenece el flujo"
    )


# ----------------------------------------------------------------------
# Flow (DB model)
# ----------------------------------------------------------------------
class Flow(FlowBase):
    id: str
    company_id: str

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------------------------
# Flow Detail (Flow + nodes + edges)
# ----------------------------------------------------------------------
class FlowDetail(Flow):
    nodes: List[FlowNode] = Field(default_factory=list)
    edges: List[FlowEdge] = Field(default_factory=list)


# ----------------------------------------------------------------------
# Import payload (flow + nodes + edges)
# ----------------------------------------------------------------------
class FlowImportPayload(BaseModel):
    flow: FlowCreate = Field(..., description="Datos base del flujo")

    nodes: List[FlowNodeCreate] = Field(
        default_factory=list, description="Listado de nodos a crear"
    )

    edges: List[FlowEdgeCreate] = Field(
        default_factory=list, description="Listado de edges a crear"
    )
