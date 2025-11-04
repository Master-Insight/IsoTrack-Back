"""Router definitions for company endpoints."""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends

from app.libraries.auth.roles import get_current_profile, require_role
from app.libraries.utils.response_models import ApiResponse

from .controller import CompanyController
from .schemas import Company, CompanyCreate, CompanyUpdate

router = APIRouter()
controller = CompanyController()


@router.get("/", response_model=ApiResponse[List[Company]])
async def list_companies(profile=Depends(get_current_profile)):
    return controller.list_companies(profile)


@router.get("/{company_id}", response_model=ApiResponse[Company])
async def retrieve_company(company_id: str, profile=Depends(get_current_profile)):
    return controller.get_company(company_id, profile)


@router.post("/", response_model=ApiResponse[Company])
async def create_company(
    payload: CompanyCreate, _profile=Depends(require_role(["root"]))
):
    return controller.create_company(payload)


@router.put("/{company_id}", response_model=ApiResponse[Company])
async def update_company(
    company_id: str,
    payload: CompanyUpdate,
    profile=Depends(require_role(["root", "admin"])),
):
    return controller.update_company(company_id, payload, profile)
