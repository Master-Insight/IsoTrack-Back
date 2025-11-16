"""Business logic for diagrams (organigrams and flows)."""

from __future__ import annotations

from typing import Any, Dict, Optional

from app.libraries.customs.base_service import BaseService
from app.libraries.exceptions.app_exceptions import AuthError, ValidationError
from app.modules.artifact_links.api.schemas import ArtifactEntityType
from app.modules.artifact_links.logic.services import ArtifactLinkService
from app.modules.users.logic.services import UserService

from ..data.dao import DiagramDAO


class DiagramService(BaseService):
    def __init__(
        self,
        diagram_dao: Optional[DiagramDAO] = None,
        user_service: Optional[UserService] = None,
        artifact_link_service: Optional[ArtifactLinkService] = None,
    ) -> None:
        super().__init__(diagram_dao or DiagramDAO())
        self.user_service = user_service or UserService()
        self.artifact_links = artifact_link_service or ArtifactLinkService()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _resolve_company(self, profile: Dict[str, Any], company_id: Optional[str]):
        role = profile.get("role")
        if role == "root":
            return company_id or profile.get("company_id")

        profile_company = self.user_service.ensure_has_company(profile)
        if company_id and company_id != profile_company:
            raise AuthError("No puedes operar sobre otra empresa")
        return profile_company

    def _ensure_access(self, profile: Dict[str, Any], diagram: Dict[str, Any]):
        if profile.get("role") == "root":
            return
        company_id = self.user_service.ensure_has_company(profile)
        if diagram.get("company_id") != company_id:
            raise AuthError("No tienes permiso para acceder a este diagrama")

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------
    def list_diagrams(
        self, profile: Dict[str, Any], *, company_id: Optional[str] = None
    ):
        resolved_company = self._resolve_company(profile, company_id)
        if resolved_company:
            return self.dao.filter(company_id=resolved_company)
        return self.dao.get_all()

    def get_diagram(self, profile: Dict[str, Any], diagram_id: str):
        diagram = self.get_by_id(diagram_id)
        self._ensure_access(profile, diagram)
        links = self.artifact_links.list_for_entity(
            profile, diagram_id, ArtifactEntityType.DIAGRAM
        )
        return {**diagram, "links": links}

    def create_diagram(self, profile: Dict[str, Any], data: Dict[str, Any]):
        company_id = self._resolve_company(profile, data.get("company_id"))
        if not company_id:
            raise ValidationError("Debe indicarse una empresa para el diagrama")
        data = {**data, "company_id": company_id}
        return self.create(
            data,
            performed_by=profile.get("id"),
            audit_metadata={"company_id": company_id, "title": data.get("title")},
        )

    def update_diagram(
        self,
        profile: Dict[str, Any],
        diagram_id: str,
        updates: Dict[str, Any],
    ):
        diagram = self.get_by_id(diagram_id)
        self._ensure_access(profile, diagram)
        if updates.get("company_id") and profile.get("role") != "root":
            raise AuthError("Solo un usuario root puede reasignar la empresa")
        return self.update(
            diagram_id,
            updates,
            performed_by=profile.get("id"),
            audit_metadata={"updated_fields": list(updates.keys())},
        )

    def delete_diagram(self, profile: Dict[str, Any], diagram_id: str):
        diagram = self.get_by_id(diagram_id)
        self._ensure_access(profile, diagram)
        return self.delete(
            diagram_id,
            performed_by=profile.get("id"),
            audit_metadata={"title": diagram.get("title")},
        )

    # ------------------------------------------------------------------
    # Links helpers
    # ------------------------------------------------------------------
    def list_links(self, profile: Dict[str, Any], diagram_id: str):
        diagram = self.get_by_id(diagram_id)
        self._ensure_access(profile, diagram)
        return self.artifact_links.list_for_entity(
            profile, diagram_id, ArtifactEntityType.DIAGRAM
        )

    def create_link(self, profile: Dict[str, Any], diagram_id: str, data: Dict[str, Any]):
        diagram = self.get_by_id(diagram_id)
        self._ensure_access(profile, diagram)
        target_id = data.get("target_id")
        if not target_id:
            raise ValidationError("Debe indicarse un artefacto a vincular")
        target_type = data.get("target_type", ArtifactEntityType.PROCESS)
        if isinstance(target_type, ArtifactEntityType):
            target_type_value = target_type.value
        else:
            target_type_value = str(target_type)
        payload = {
            "from_id": diagram_id,
            "from_type": ArtifactEntityType.DIAGRAM.value,
            "to_id": target_id,
            "to_type": target_type_value,
            "relation_type": data.get("relation_type"),
        }
        return self.artifact_links.create_link(profile, payload)

    def delete_link(self, profile: Dict[str, Any], diagram_id: str, link_id: str):
        diagram = self.get_by_id(diagram_id)
        self._ensure_access(profile, diagram)
        link = self.artifact_links.get_by_id(link_id)
        if not link:
            raise ValidationError("El vínculo solicitado no existe")
        if diagram_id not in {link.get("from_id"), link.get("to_id")}:
            raise ValidationError("El vínculo no pertenece a este diagrama")
        return self.artifact_links.delete_link(profile, link_id)
