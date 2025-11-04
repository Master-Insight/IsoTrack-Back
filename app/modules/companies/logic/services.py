"""Business logic for companies."""

from __future__ import annotations

from typing import Any, Dict, Optional

from app.libraries.customs.base_service import BaseService
from app.libraries.exceptions.app_exceptions import AuthError
from app.modules.users.logic.services import UserService

from ..data.dao import CompanyDAO


class CompanyService(BaseService):
    def __init__(
        self,
        dao: Optional[CompanyDAO] = None,
        user_service: Optional[UserService] = None,
    ) -> None:
        super().__init__(dao or CompanyDAO())
        self.user_service = user_service or UserService()

    def list_for_profile(self, profile: Dict[str, Any]):
        role = profile.get("role")
        if role == "root":
            return self.list_all()

        company_id = self.user_service.ensure_has_company(profile)
        company = self.dao.get_by_id(company_id)
        return [company] if company else []

    def get_for_profile(self, company_id: str, profile: Dict[str, Any]):
        self.user_service.ensure_can_access_company(profile, company_id)
        record = self.dao.get_by_id(company_id)
        if not record:
            raise AuthError("Empresa no encontrada o sin acceso")
        return record

    def create_company(self, payload: Dict[str, Any]):
        return self.create(payload)

    def update_company(
        self, company_id: str, payload: Dict[str, Any], profile: Dict[str, Any]
    ):
        role = profile.get("role")
        if role != "root" and profile.get("company_id") != company_id:
            raise AuthError("No tienes permisos para modificar esta empresa")
        return self.update(company_id, payload)
