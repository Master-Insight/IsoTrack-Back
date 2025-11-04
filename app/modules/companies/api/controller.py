"""Controller for company endpoints."""

from __future__ import annotations

from typing import Dict, List

from app.libraries.utils.response_builder import ResponseBuilder
from app.libraries.utils.response_models import ApiResponse

from ..logic.services import CompanyService
from .schemas import Company, CompanyCreate, CompanyUpdate


class CompanyController:
    def __init__(self, service: CompanyService | None = None) -> None:
        self.service = service or CompanyService()

    def list_companies(self, profile: Dict) -> ApiResponse[List[Company]]:
        records = self.service.list_for_profile(profile)
        items = [Company.model_validate(record) for record in records]
        return ResponseBuilder.success(items, "Empresas obtenidas")

    def get_company(self, company_id: str, profile: Dict) -> ApiResponse[Company]:
        record = self.service.get_for_profile(company_id, profile)
        schema = Company.model_validate(record)
        return ResponseBuilder.success(schema, "Empresa obtenida")

    def create_company(self, payload: CompanyCreate) -> ApiResponse[Company]:
        created = self.service.create_company(payload.model_dump(exclude_unset=True))
        schema = Company.model_validate(created)
        return ResponseBuilder.success(schema, "Empresa creada")

    def update_company(
        self, company_id: str, payload: CompanyUpdate, profile: Dict
    ) -> ApiResponse[Company]:
        updated = self.service.update_company(
            company_id, payload.model_dump(exclude_unset=True), profile
        )
        schema = Company.model_validate(updated)
        return ResponseBuilder.success(schema, "Empresa actualizada")
