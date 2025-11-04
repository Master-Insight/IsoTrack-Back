# app\modules\companies\api\controller.py
"""Controlador para compañías."""

from __future__ import annotations

from app.libraries.customs.controller_response import ResponseController

from ..logic.services import CompanyService
from .schemas import Company, CompanyCreate, CompanyUpdate


class CompanyController(ResponseController[Company, CompanyCreate]):
    def __init__(self) -> None:
        super().__init__(CompanyService())

    def update_company(self, company_id: str, payload: CompanyUpdate):
        return self.update(company_id, payload)
