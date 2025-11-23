"""Routes for flow management (ReactFlow backend)."""

from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, Query

from app.libraries.auth.roles import require_role
from app.libraries.utils.response_models import ApiResponse

from .controller import FlowController
from .schemas import (
    Flow,
    FlowCreate,
    FlowDetail,
    FlowEdge,
    FlowEdgeCreate,
    FlowImportPayload,
    FlowNode,
    FlowNodeCreate,
)

router = APIRouter()
controller = FlowController()


@router.get("/", response_model=ApiResponse[List[Flow]])
async def list_flows(
    company_id: Optional[str] = Query(default=None),
    profile=Depends(require_role(["root", "admin", "user"])),
):
    return controller.list_flows(profile, company_id)


@router.get("/{flow_id}", response_model=ApiResponse[FlowDetail])
async def get_flow(flow_id: str, profile=Depends(require_role(["root", "admin", "user"]))):
    return controller.get_flow(profile, flow_id)


@router.post("/", response_model=ApiResponse[Flow])
async def create_flow(
    payload: FlowCreate, profile=Depends(require_role(["root", "admin"]))
):
    return controller.create_flow(profile, payload)


@router.post("/import", response_model=ApiResponse[FlowDetail])
async def import_flow(
    payload: FlowImportPayload, profile=Depends(require_role(["root", "admin"]))
):
    return controller.import_flow(profile, payload)


@router.post("/{flow_id}/nodes", response_model=ApiResponse[FlowNode])
async def create_node(
    flow_id: str,
    payload: FlowNodeCreate,
    profile=Depends(require_role(["root", "admin"])),
):
    return controller.create_node(profile, flow_id, payload)


@router.post("/{flow_id}/edges", response_model=ApiResponse[FlowEdge])
async def create_edge(
    flow_id: str,
    payload: FlowEdgeCreate,
    profile=Depends(require_role(["root", "admin"])),
):
    return controller.create_edge(profile, flow_id, payload)
