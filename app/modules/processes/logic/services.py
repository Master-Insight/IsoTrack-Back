"""Business logic for processes and tasks."""

from __future__ import annotations

from typing import Any, Dict, Optional

from app.libraries.customs.base_service import BaseService
from app.libraries.exceptions.app_exceptions import AuthError, ValidationError
from app.modules.documents.data.dao import DocumentDAO
from app.modules.users.logic.services import UserService

from ..data.dao import ProcessArtifactLinkDAO, ProcessDAO, TaskDAO


class ProcessService(BaseService):
    def __init__(
        self,
        process_dao: Optional[ProcessDAO] = None,
        task_dao: Optional[TaskDAO] = None,
        link_dao: Optional[ProcessArtifactLinkDAO] = None,
        user_service: Optional[UserService] = None,
        document_dao: Optional[DocumentDAO] = None,
    ) -> None:
        super().__init__(process_dao or ProcessDAO())
        self.task_dao = task_dao or TaskDAO()
        self.link_dao = link_dao or ProcessArtifactLinkDAO()
        self.user_service = user_service or UserService()
        self.document_dao = document_dao or DocumentDAO()

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

    def _ensure_process_access(self, profile: Dict[str, Any], process: Dict[str, Any]):
        if profile.get("role") == "root":
            return
        company_id = self.user_service.ensure_has_company(profile)
        if process.get("company_id") != company_id:
            raise AuthError("No tienes permiso para este proceso")

    # ------------------------------------------------------------------
    # Processes
    # ------------------------------------------------------------------
    def list_processes(
        self,
        profile: Dict[str, Any],
        *,
        company_id: Optional[str] = None,
    ):
        resolved_company = self._resolve_company(profile, company_id)
        if resolved_company:
            return self.dao.filter(company_id=resolved_company)
        return self.dao.get_all()

    # TODO no devolver links hasta que este bien implmentado
    def get_process_detail(self, profile: Dict[str, Any], process_id: str):
        process = self.get_by_id(process_id)
        self._ensure_process_access(profile, process)
        tasks = self.task_dao.list_for_process(process_id)
        # links = self.link_dao.list_for_process(process_id)
        payload = {**process, "tasks": tasks}  # , "links": links
        return payload

    def create_process(
        self,
        profile: Dict[str, Any],
        data: Dict[str, Any],
    ):
        company_id = self._resolve_company(profile, data.get("company_id"))
        if not company_id:
            raise ValidationError("Debe indicarse una empresa para el proceso")
        data = {**data, "company_id": company_id}
        return self.create(
            data,
            performed_by=profile.get("id"),
            audit_metadata={"company_id": company_id},
        )

    def update_process(
        self,
        profile: Dict[str, Any],
        process_id: str,
        updates: Dict[str, Any],
    ):
        process = self.get_by_id(process_id)
        self._ensure_process_access(profile, process)
        if updates.get("company_id") and profile.get("role") != "root":
            raise AuthError("Solo un usuario root puede reasignar la empresa")
        return self.update(
            process_id,
            updates,
            performed_by=profile.get("id"),
            audit_metadata={"updated_fields": list(updates.keys())},
        )

    def delete_process(self, profile: Dict[str, Any], process_id: str):
        process = self.get_by_id(process_id)
        self._ensure_process_access(profile, process)
        return self.delete(
            process_id,
            performed_by=profile.get("id"),
            audit_metadata={"code": process.get("code")},
        )

    # ------------------------------------------------------------------
    # Tasks
    # ------------------------------------------------------------------
    def list_tasks(self, profile: Dict[str, Any], process_id: str):
        process = self.get_by_id(process_id)
        self._ensure_process_access(profile, process)
        return self.task_dao.list_for_process(process_id)

    def create_task(
        self,
        profile: Dict[str, Any],
        process_id: str,
        data: Dict[str, Any],
    ):
        process = self.get_by_id(process_id)
        self._ensure_process_access(profile, process)
        payload = {
            **data,
            "process_id": process_id,
            "company_id": process.get("company_id"),
        }
        return self.task_dao.insert(payload)

    def update_task(
        self,
        profile: Dict[str, Any],
        process_id: str,
        task_id: str,
        updates: Dict[str, Any],
    ):
        process = self.get_by_id(process_id)
        self._ensure_process_access(profile, process)
        task = self.task_dao.get_by_id(task_id)
        if not task or task.get("process_id") != process_id:
            raise ValidationError("La tarea no pertenece a este proceso")
        return self.task_dao.update(task_id, updates)

    def delete_task(
        self,
        profile: Dict[str, Any],
        process_id: str,
        task_id: str,
    ):
        process = self.get_by_id(process_id)
        self._ensure_process_access(profile, process)
        task = self.task_dao.get_by_id(task_id)
        if not task or task.get("process_id") != process_id:
            raise ValidationError("La tarea no pertenece a este proceso")
        return self.task_dao.delete(task_id)

    # ------------------------------------------------------------------
    # Links with documents
    # ------------------------------------------------------------------
    def list_links(self, profile: Dict[str, Any], process_id: str):
        process = self.get_by_id(process_id)
        self._ensure_process_access(profile, process)
        return self.link_dao.list_for_process(process_id)

    def create_link(
        self,
        profile: Dict[str, Any],
        process_id: str,
        data: Dict[str, Any],
    ):
        process = self.get_by_id(process_id)
        self._ensure_process_access(profile, process)
        document_id = data.get("document_id")
        if not document_id:
            raise ValidationError("Debe indicarse un documento a vincular")
        document = self.document_dao.get_by_id(document_id)
        if not document:
            raise ValidationError("Documento no encontrado")
        if document.get("company_id") != process.get("company_id"):
            raise AuthError("El documento pertenece a otra empresa")
        existing = self.link_dao.get_link(process_id, document_id)
        if existing:
            return existing
        payload = {
            **data,
            "process_id": process_id,
        }
        return self.link_dao.insert(payload)

    def delete_link(
        self,
        profile: Dict[str, Any],
        process_id: str,
        link_id: str,
    ):
        process = self.get_by_id(process_id)
        self._ensure_process_access(profile, process)
        link = self.link_dao.get_by_id(link_id)
        if not link or link.get("process_id") != process_id:
            raise ValidationError("El vínculo no pertenece a este proceso")
        return self.link_dao.delete(link_id)
