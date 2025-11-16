"""Routes for diagram management."""

from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, Query

from app.libraries.auth.roles import require_role
from app.libraries.utils.response_models import ApiResponse
from app.modules.artifact_links.api.schemas import ArtifactLink

from .controller import DiagramController
from .schemas import (
    Diagram,
    DiagramCreate,
    DiagramDetail,
    DiagramLinkPayload,
    DiagramUpdate,
)

router = APIRouter()
controller = DiagramController()


@router.get("/", response_model=ApiResponse[List[Diagram]])
async def list_diagrams(
    company_id: Optional[str] = Query(default=None),
    profile=Depends(require_role(["root", "admin", "user"])),
):
    return controller.list_diagrams(profile, company_id)


@router.post("/", response_model=ApiResponse[Diagram])
async def create_diagram(
    payload: DiagramCreate, profile=Depends(require_role(["root", "admin"]))
):
    return controller.create_diagram(profile, payload)


@router.get("/{diagram_id}", response_model=ApiResponse[DiagramDetail])
async def get_diagram(
    diagram_id: str, profile=Depends(require_role(["root", "admin", "user"]))
):
    return controller.get_diagram(profile, diagram_id)


@router.put("/{diagram_id}", response_model=ApiResponse[Diagram])
async def update_diagram(
    diagram_id: str,
    payload: DiagramUpdate,
    profile=Depends(require_role(["root", "admin"])),
):
    return controller.update_diagram(profile, diagram_id, payload)


@router.delete("/{diagram_id}", response_model=ApiResponse[dict])
async def delete_diagram(
    diagram_id: str, profile=Depends(require_role(["root", "admin"]))
):
    return controller.delete_diagram(profile, diagram_id)


@router.get(
    "/{diagram_id}/links",
    response_model=ApiResponse[List[ArtifactLink]],
)
async def list_links(
    diagram_id: str,
    profile=Depends(require_role(["root", "admin", "user"])),
):
    return controller.list_links(profile, diagram_id)


@router.post(
    "/{diagram_id}/links",
    response_model=ApiResponse[ArtifactLink],
)
async def create_link(
    diagram_id: str,
    payload: DiagramLinkPayload,
    profile=Depends(require_role(["root", "admin"])),
):
    return controller.create_link(profile, diagram_id, payload)


@router.delete(
    "/{diagram_id}/links/{link_id}",
    response_model=ApiResponse[dict],
)
async def delete_link(
    diagram_id: str,
    link_id: str,
    profile=Depends(require_role(["root", "admin"])),
):
    return controller.delete_link(profile, diagram_id, link_id)
