"""FastAPI routes for artifact link operations."""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, Query

from app.libraries.auth.roles import require_role
from app.libraries.utils.response_models import ApiResponse

from .controller import ArtifactLinkController
from .schemas import ArtifactEntityType, ArtifactLink, ArtifactLinkCreate

router = APIRouter()
controller = ArtifactLinkController()


@router.get("/", response_model=ApiResponse[List[ArtifactLink]])
async def list_links(
    entity_id: str = Query(..., description="ID del artefacto a consultar"),
    entity_type: ArtifactEntityType = Query(
        ..., description="Tipo del artefacto (document/process/task/diagram)"
    ),
    profile=Depends(require_role(["root", "admin", "user"])),
):
    return controller.list_links(profile, entity_id=entity_id, entity_type=entity_type)


@router.post("/", response_model=ApiResponse[ArtifactLink])
async def create_link(
    payload: ArtifactLinkCreate, profile=Depends(require_role(["root", "admin"]))
):
    return controller.create_link(profile, payload)


@router.delete("/{link_id}", response_model=ApiResponse[dict])
async def delete_link(
    link_id: str, profile=Depends(require_role(["root", "admin"]))
):
    return controller.delete_link(profile, link_id)
