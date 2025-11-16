"""Controller layer for artifact link operations."""

from __future__ import annotations

from typing import Dict, List

from app.libraries.utils.response_builder import ResponseBuilder
from app.libraries.utils.response_models import ApiResponse

from ..logic.services import ArtifactLinkService
from .schemas import ArtifactEntityType, ArtifactLink, ArtifactLinkCreate


class ArtifactLinkController:
    """Orquesta la interacción entre FastAPI y la capa de servicios."""

    def __init__(self, service: ArtifactLinkService | None = None) -> None:
        self.service = service or ArtifactLinkService()

    def list_links(
        self, profile: Dict, *, entity_id: str, entity_type: ArtifactEntityType
    ) -> ApiResponse[List[ArtifactLink]]:
        records = self.service.list_for_entity(profile, entity_id, entity_type)
        items = [ArtifactLink.model_validate(record) for record in records]
        return ResponseBuilder.success(items, "Vínculos obtenidos")

    def create_link(
        self, profile: Dict, payload: ArtifactLinkCreate
    ) -> ApiResponse[ArtifactLink]:
        data = payload.model_dump(exclude_unset=True)
        created = self.service.create_link(profile, data)
        schema = ArtifactLink.model_validate(created)
        return ResponseBuilder.success(schema, "Vínculo creado")

    def delete_link(self, profile: Dict, link_id: str) -> ApiResponse[Dict]:
        result = self.service.delete_link(profile, link_id)
        return ResponseBuilder.success(result, "Vínculo eliminado")
