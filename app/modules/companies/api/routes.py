# app\modules\companies\api\routes.py
"""Rutas para compañías."""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends

from app.libraries.auth.roles import require_role
from app.libraries.utils.response_models import ApiResponse

from .controller import CompanyController
from .schemas import Company, CompanyCreate, CompanyUpdate

router = APIRouter()
controller = CompanyController()


@router.get("/", response_model=ApiResponse[List[Company]])
def list_companies(current_user=Depends(require_role(["root", "admin"]))):
    return controller.list_all()


@router.post("/", response_model=ApiResponse[Company])
def create_company(
    payload: CompanyCreate, current_user=Depends(require_role(["root"]))
):
    return controller.create(payload)


@router.put("/{company_id}", response_model=ApiResponse[Company])
def update_company(
    company_id: str,
    payload: CompanyUpdate,
    current_user=Depends(require_role(["root"])),
):
    return controller.update_company(company_id, payload)


@router.delete("/{company_id}")
def delete_company(company_id: str, current_user=Depends(require_role(["root"]))):
    return controller.delete(company_id)
