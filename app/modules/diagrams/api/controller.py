"""Controllers for diagram endpoints."""

from __future__ import annotations

from typing import Dict, List

from app.libraries.utils.response_builder import ResponseBuilder
from app.libraries.utils.response_models import ApiResponse
from app.modules.artifact_links.api.schemas import ArtifactLink

from ..logic.services import DiagramService
from .schemas import (
    Diagram,
    DiagramCreate,
    DiagramDetail,
    DiagramLinkPayload,
    DiagramUpdate,
)


class DiagramController:
    def __init__(self, service: DiagramService | None = None) -> None:
        self.service = service or DiagramService()

    def list_diagrams(self, profile: Dict, company_id: str | None) -> ApiResponse[List[Diagram]]:
        records = self.service.list_diagrams(profile, company_id=company_id)
        items = [Diagram.model_validate(record) for record in records]
        return ResponseBuilder.success(items, "Diagramas obtenidos")

    def get_diagram(self, profile: Dict, diagram_id: str) -> ApiResponse[DiagramDetail]:
        record = self.service.get_diagram(profile, diagram_id)
        schema = DiagramDetail.model_validate(record)
        return ResponseBuilder.success(schema, "Diagrama obtenido")

    def create_diagram(self, profile: Dict, payload: DiagramCreate) -> ApiResponse[Diagram]:
        data = payload.model_dump(exclude_unset=True)
        created = self.service.create_diagram(profile, data)
        schema = Diagram.model_validate(created)
        return ResponseBuilder.success(schema, "Diagrama creado")

    def update_diagram(
        self, profile: Dict, diagram_id: str, payload: DiagramUpdate
    ) -> ApiResponse[Diagram]:
        updates = payload.model_dump(exclude_unset=True)
        record = self.service.update_diagram(profile, diagram_id, updates)
        schema = Diagram.model_validate(record)
        return ResponseBuilder.success(schema, "Diagrama actualizado")

    def delete_diagram(self, profile: Dict, diagram_id: str) -> ApiResponse[Dict]:
        result = self.service.delete_diagram(profile, diagram_id)
        return ResponseBuilder.success(result, "Diagrama eliminado")

    def list_links(self, profile: Dict, diagram_id: str):
        records = self.service.list_links(profile, diagram_id)
        items = [ArtifactLink.model_validate(record) for record in records]
        return ResponseBuilder.success(items, "Vínculos obtenidos")

    def create_link(
        self, profile: Dict, diagram_id: str, payload: DiagramLinkPayload
    ) -> ApiResponse[ArtifactLink]:
        data = payload.model_dump(exclude_unset=True)
        created = self.service.create_link(profile, diagram_id, data)
        schema = ArtifactLink.model_validate(created)
        return ResponseBuilder.success(schema, "Vínculo creado")

    def delete_link(self, profile: Dict, diagram_id: str, link_id: str):
        result = self.service.delete_link(profile, diagram_id, link_id)
        return ResponseBuilder.success(result, "Vínculo eliminado")
