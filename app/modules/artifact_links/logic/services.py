"""Business logic to manage the artifact links matrix."""

from __future__ import annotations

from typing import Any, Dict, Optional

from app.libraries.customs.base_service import BaseService
from app.libraries.exceptions.app_exceptions import NotFoundError, ValidationError
from app.modules.diagrams.data.dao import DiagramDAO
from app.modules.documents.data.dao import DocumentDAO
from app.modules.processes.data.dao import ProcessDAO, TaskDAO
from app.modules.users.logic.services import UserService

from ..api.schemas import ArtifactEntityType
from ..data.dao import ArtifactLinkDAO


class ArtifactLinkService(BaseService):
    """Orquesta la creación, consulta y eliminación de vínculos cruzados."""

    def __init__(
        self,
        dao: Optional[ArtifactLinkDAO] = None,
        *,
        user_service: Optional[UserService] = None,
        document_dao: Optional[DocumentDAO] = None,
        process_dao: Optional[ProcessDAO] = None,
        task_dao: Optional[TaskDAO] = None,
        diagram_dao: Optional[DiagramDAO] = None,
    ) -> None:
        super().__init__(dao or ArtifactLinkDAO())
        self.user_service = user_service or UserService()
        self.entity_daos = {
            ArtifactEntityType.DOCUMENT: document_dao or DocumentDAO(),
            ArtifactEntityType.PROCESS: process_dao or ProcessDAO(),
            ArtifactEntityType.TASK: task_dao or TaskDAO(),
            ArtifactEntityType.DIAGRAM: diagram_dao or DiagramDAO(),
        }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _resolve_entity(
        self, entity_type: ArtifactEntityType, entity_id: str
    ) -> Dict[str, Any]:
        dao = self.entity_daos.get(entity_type)
        if dao is None:
            raise ValidationError("Tipo de artefacto no soportado")
        record = dao.get_by_id(entity_id)
        if not record:
            raise NotFoundError("El artefacto solicitado no existe")
        return record

    @staticmethod
    def _coerce_type(value: Any) -> ArtifactEntityType:
        if isinstance(value, ArtifactEntityType):
            return value
        try:
            return ArtifactEntityType(str(value))
        except Exception as exc:  # noqa: BLE001 - translate to ValidationError
            raise ValidationError("Tipo de artefacto inválido") from exc

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def list_for_entity(
        self, profile: Dict[str, Any], entity_id: str, entity_type: ArtifactEntityType
    ):
        entity = self._resolve_entity(entity_type, entity_id)
        company_id = entity.get("company_id")
        if company_id:
            self.user_service.ensure_can_access_company(profile, company_id)
        return self.dao.list_for_entity(entity_id, entity_type.value)

    def create_link(self, profile: Dict[str, Any], payload: Dict[str, Any]):
        from_id = payload.get("from_id")
        to_id = payload.get("to_id")
        if not from_id or not to_id:
            raise ValidationError("Debes indicar los artefactos a vincular")

        from_type = self._coerce_type(payload.get("from_type"))
        to_type = self._coerce_type(payload.get("to_type"))

        from_entity = self._resolve_entity(from_type, from_id)
        to_entity = self._resolve_entity(to_type, to_id)

        from_company = from_entity.get("company_id")
        to_company = to_entity.get("company_id")

        if from_company and to_company and from_company != to_company:
            raise ValidationError(
                "No se pueden vincular artefactos de empresas distintas",
                details={"from_company": from_company, "to_company": to_company},
            )

        company_id = from_company or to_company
        if not company_id:
            raise ValidationError("Los artefactos deben pertenecer a una empresa")

        self.user_service.ensure_can_access_company(profile, company_id)

        existing = self.dao.get_by_pair(
            from_id=from_id,
            from_type=from_type.value,
            to_id=to_id,
            to_type=to_type.value,
        )
        if existing:
            return existing

        payload = {
            "from_id": from_id,
            "from_type": from_type.value,
            "to_id": to_id,
            "to_type": to_type.value,
            "relation_type": payload.get("relation_type"),
            "company_id": company_id,
        }

        return self.create(
            payload,
            performed_by=profile.get("id"),
            audit_metadata={
                "from": {"id": from_id, "type": from_type.value},
                "to": {"id": to_id, "type": to_type.value},
            },
        )

    def delete_link(self, profile: Dict[str, Any], link_id: str):
        link = self.get_by_id(link_id)
        company_id = link.get("company_id")
        if company_id:
            self.user_service.ensure_can_access_company(profile, company_id)
        return self.delete(link_id, performed_by=profile.get("id"))
