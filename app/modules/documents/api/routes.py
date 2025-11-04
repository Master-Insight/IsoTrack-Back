# app/modules/Blancks/api/routes.py
from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, Query

from app.libraries.auth.roles import require_role
from app.libraries.utils.response_models import ApiResponse

from .controller import BlanckController
from .schemas import Blanck, BlanckCreate, BlanckUpdate

router = APIRouter()
controller = BlanckController()


@router.get("/", response_model=ApiResponse[List[Blanck]])
def list_Blancks(
    company_id: Optional[str] = Query(default=None),
    deal_id: Optional[str] = Query(default=None),
    current_user=Depends(require_role(["root", "admin", "user"])),
):
    return controller.list_Blancks(current_user, company_id, deal_id)


@router.post("/", response_model=ApiResponse[Blanck])
def create_Blanck(
    payload: BlanckCreate,
    current_user=Depends(require_role(["root", "admin", "user"])),
):
    return controller.create_Blanck(current_user, payload)


@router.put("/{Blanck_id}", response_model=ApiResponse[Blanck])
def update_Blanck(
    Blanck_id: str,
    payload: BlanckUpdate,
    current_user=Depends(require_role(["root", "admin", "user"])),
):
    return controller.update_Blanck(current_user, Blanck_id, payload)


@router.delete("/{Blanck_id}")
def delete_Blanck(
    Blanck_id: str,
    current_user=Depends(require_role(["root", "admin"])),
):
    return controller.delete_Blanck(current_user, Blanck_id)
