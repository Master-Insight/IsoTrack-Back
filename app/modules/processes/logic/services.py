"""Business logic for processes and tasks."""

from __future__ import annotations

from typing import Any, Dict, Optional

from app.libraries.customs.base_service import BaseService
from app.libraries.exceptions.app_exceptions import AuthError, ValidationError
from app.modules.artifact_links.api.schemas import ArtifactEntityType
from app.modules.artifact_links.logic.services import ArtifactLinkService
from app.modules.users.logic.services import UserService

from ..data.dao import ProcessDAO, TaskDAO


class ProcessService(BaseService):
    def __init__(
        self,
        process_dao: Optional[ProcessDAO] = None,
        task_dao: Optional[TaskDAO] = None,
        user_service: Optional[UserService] = None,
        artifact_link_service: Optional[ArtifactLinkService] = None,
    ) -> None:
        super().__init__(process_dao or ProcessDAO())
        self.task_dao = task_dao or TaskDAO()
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

    def _ensure_process_access(self, profile: Dict[str, Any], process: Dict[str, Any]):
        if profile.get("role") == "root":
            return
        company_id = self.user_service.ensure_has_company(profile)
        if process.get("company_id") != company_id:
            raise AuthError("No tienes permiso para este proceso")

    def _ensure_task(self, process_id: str, task_id: str):
        task = self.task_dao.get_by_id(task_id)
        if not task or task.get("process_id") != process_id:
            raise ValidationError("La tarea no pertenece a este proceso")
        return task

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

    def get_process_detail(self, profile: Dict[str, Any], process_id: str):
        process = self.get_by_id(process_id)
        self._ensure_process_access(profile, process)
        tasks = self.task_dao.list_for_process(process_id)
        links = self.artifact_links.list_for_entity(
            profile, process_id, ArtifactEntityType.PROCESS
        )
        payload = {**process, "tasks": tasks, "links": links}
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
        self._ensure_task(process_id, task_id)
        return self.task_dao.update(task_id, updates)

    def delete_task(
        self,
        profile: Dict[str, Any],
        process_id: str,
        task_id: str,
    ):
        process = self.get_by_id(process_id)
        self._ensure_process_access(profile, process)
        self._ensure_task(process_id, task_id)
        return self.task_dao.delete(task_id)

    # ------------------------------------------------------------------
    # Links with documents
    # ------------------------------------------------------------------
    def list_links(self, profile: Dict[str, Any], process_id: str):
        process = self.get_by_id(process_id)
        self._ensure_process_access(profile, process)
        return self.artifact_links.list_for_entity(
            profile, process_id, ArtifactEntityType.PROCESS
        )

    def create_link(
        self,
        profile: Dict[str, Any],
        process_id: str,
        data: Dict[str, Any],
    ):
        process = self.get_by_id(process_id)
        self._ensure_process_access(profile, process)
        target_id = data.get("target_id") or data.get("document_id")
        if not target_id:
            raise ValidationError("Debe indicarse un artefacto a vincular")
        target_type_value = data.get("target_type", ArtifactEntityType.DOCUMENT)
        if isinstance(target_type_value, ArtifactEntityType):
            target_type_value = target_type_value.value
        else:
            target_type_value = str(target_type_value)
        payload = {
            "from_id": process_id,
            "from_type": ArtifactEntityType.PROCESS.value,
            "to_id": target_id,
            "to_type": target_type_value,
            "relation_type": data.get("relation_type"),
        }
        return self.artifact_links.create_link(profile, payload)

    def delete_link(
        self,
        profile: Dict[str, Any],
        process_id: str,
        link_id: str,
    ):
        process = self.get_by_id(process_id)
        self._ensure_process_access(profile, process)
        link = self.artifact_links.get_by_id(link_id)
        if not link:
            raise ValidationError("El vínculo solicitado no existe")
        if process_id not in {link.get("from_id"), link.get("to_id")}:
            raise ValidationError("El vínculo no pertenece a este proceso")
        return self.artifact_links.delete_link(profile, link_id)

    # ------------------------------------------------------------------
    # Task links
    # ------------------------------------------------------------------
    def list_task_links(self, profile: Dict[str, Any], process_id: str, task_id: str):
        process = self.get_by_id(process_id)
        self._ensure_process_access(profile, process)
        task = self._ensure_task(process_id, task_id)
        return self.artifact_links.list_for_entity(
            profile, task["id"], ArtifactEntityType.TASK
        )

    def create_task_link(
        self,
        profile: Dict[str, Any],
        process_id: str,
        task_id: str,
        data: Dict[str, Any],
    ):
        process = self.get_by_id(process_id)
        self._ensure_process_access(profile, process)
        task = self._ensure_task(process_id, task_id)
        target_id = data.get("target_id")
        if not target_id:
            raise ValidationError("Debe indicarse un artefacto a vincular")
        target_type_value = data.get("target_type", ArtifactEntityType.DOCUMENT)
        if isinstance(target_type_value, ArtifactEntityType):
            target_type_value = target_type_value.value
        else:
            target_type_value = str(target_type_value)
        payload = {
            "from_id": task["id"],
            "from_type": ArtifactEntityType.TASK.value,
            "to_id": target_id,
            "to_type": target_type_value,
            "relation_type": data.get("relation_type"),
        }
        return self.artifact_links.create_link(profile, payload)

    def delete_task_link(
        self,
        profile: Dict[str, Any],
        process_id: str,
        task_id: str,
        link_id: str,
    ):
        process = self.get_by_id(process_id)
        self._ensure_process_access(profile, process)
        task = self._ensure_task(process_id, task_id)
        link = self.artifact_links.get_by_id(link_id)
        if not link:
            raise ValidationError("El vínculo solicitado no existe")
        if task["id"] not in {link.get("from_id"), link.get("to_id")}:
            raise ValidationError("El vínculo no pertenece a esta tarea")
        return self.artifact_links.delete_link(profile, link_id)
