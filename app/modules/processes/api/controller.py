"""Controllers for process endpoints."""

from __future__ import annotations

from typing import Dict, List

from app.libraries.utils.response_builder import ResponseBuilder
from app.libraries.utils.response_models import ApiResponse

from ..logic.services import ProcessService
from .schemas import (
    Process,
    ProcessCreate,
    ProcessDetail,
    ProcessDocumentLink,
    ProcessUpdate,
    Task,
    TaskCreate,
    TaskUpdate,
)


class ProcessController:
    def __init__(self, service: ProcessService | None = None) -> None:
        self.service = service or ProcessService()

    def list_processes(self, profile: Dict, company_id: str | None) -> ApiResponse[List[Process]]:
        records = self.service.list_processes(profile, company_id=company_id)
        items = [Process.model_validate(record) for record in records]
        return ResponseBuilder.success(items, "Procesos obtenidos")

    def get_process(self, profile: Dict, process_id: str) -> ApiResponse[ProcessDetail]:
        record = self.service.get_process_detail(profile, process_id)
        schema = ProcessDetail.model_validate(record)
        return ResponseBuilder.success(schema, "Proceso obtenido")

    def create_process(self, profile: Dict, payload: ProcessCreate) -> ApiResponse[Process]:
        data = payload.model_dump(exclude_unset=True)
        created = self.service.create_process(profile, data)
        schema = Process.model_validate(created)
        return ResponseBuilder.success(schema, "Proceso creado")

    def update_process(
        self, profile: Dict, process_id: str, payload: ProcessUpdate
    ) -> ApiResponse[Process]:
        updates = payload.model_dump(exclude_unset=True)
        record = self.service.update_process(profile, process_id, updates)
        schema = Process.model_validate(record)
        return ResponseBuilder.success(schema, "Proceso actualizado")

    def delete_process(self, profile: Dict, process_id: str) -> ApiResponse[Dict]:
        result = self.service.delete_process(profile, process_id)
        return ResponseBuilder.success(result, "Proceso eliminado")

    # Tasks
    def list_tasks(self, profile: Dict, process_id: str) -> ApiResponse[List[Task]]:
        records = self.service.list_tasks(profile, process_id)
        items = [Task.model_validate(record) for record in records]
        return ResponseBuilder.success(items, "Tareas obtenidas")

    def create_task(
        self, profile: Dict, process_id: str, payload: TaskCreate
    ) -> ApiResponse[Task]:
        data = payload.model_dump(exclude_unset=True)
        created = self.service.create_task(profile, process_id, data)
        schema = Task.model_validate(created)
        return ResponseBuilder.success(schema, "Tarea creada")

    def update_task(
        self, profile: Dict, process_id: str, task_id: str, payload: TaskUpdate
    ) -> ApiResponse[Task]:
        updates = payload.model_dump(exclude_unset=True)
        record = self.service.update_task(profile, process_id, task_id, updates)
        schema = Task.model_validate(record)
        return ResponseBuilder.success(schema, "Tarea actualizada")

    def delete_task(
        self, profile: Dict, process_id: str, task_id: str
    ) -> ApiResponse[Dict]:
        result = self.service.delete_task(profile, process_id, task_id)
        return ResponseBuilder.success(result, "Tarea eliminada")

    # Links
    def list_links(
        self, profile: Dict, process_id: str
    ) -> ApiResponse[List[ProcessDocumentLink]]:
        records = self.service.list_links(profile, process_id)
        items = [ProcessDocumentLink.model_validate(record) for record in records]
        return ResponseBuilder.success(items, "Vínculos obtenidos")

    def create_link(
        self,
        profile: Dict,
        process_id: str,
        payload: ProcessDocumentLink,
    ) -> ApiResponse[ProcessDocumentLink]:
        data = payload.model_dump(exclude_unset=True)
        created = self.service.create_link(profile, process_id, data)
        schema = ProcessDocumentLink.model_validate(created)
        return ResponseBuilder.success(schema, "Vínculo creado")

    def delete_link(
        self, profile: Dict, process_id: str, link_id: str
    ) -> ApiResponse[Dict]:
        result = self.service.delete_link(profile, process_id, link_id)
        return ResponseBuilder.success(result, "Vínculo eliminado")
