"""Controllers for flow endpoints."""

from __future__ import annotations

from typing import Dict

from app.libraries.utils.response_builder import ResponseBuilder
from app.libraries.utils.response_models import ApiResponse

from ..logic.services import FlowService
from .schemas import (
    Flow,
    FlowCreate,
    FlowDetail,
    FlowEdge,
    FlowEdgeCreate,
    FlowImportPayload,
    FlowNode,
    FlowNodeCreate,
)


class FlowController:
    def __init__(self, service: FlowService | None = None) -> None:
        self.service = service or FlowService()

    def list_flows(self, profile: Dict, company_id: str | None):
        records = self.service.list_flows(profile, company_id=company_id)
        items = [Flow.model_validate(record) for record in records]
        return ResponseBuilder.success(items, "Flujos obtenidos")

    def get_flow(self, profile: Dict, flow_id: str) -> ApiResponse[FlowDetail]:
        record = self.service.get_flow(profile, flow_id)
        schema = FlowDetail.model_validate(record)
        return ResponseBuilder.success(schema, "Flujo obtenido")

    def create_flow(self, profile: Dict, payload: FlowCreate) -> ApiResponse[Flow]:
        data = payload.model_dump(exclude_unset=True)
        created = self.service.create_flow(profile, data)
        schema = Flow.model_validate(created)
        return ResponseBuilder.success(schema, "Flujo creado")

    def import_flow(
        self, profile: Dict, payload: FlowImportPayload
    ) -> ApiResponse[FlowDetail]:
        data = payload.model_dump(exclude_unset=True)
        created = self.service.import_flow(profile, data)
        schema = FlowDetail.model_validate(created)
        return ResponseBuilder.success(schema, "Flujo importado")

    def create_node(
        self, profile: Dict, flow_id: str, payload: FlowNodeCreate
    ) -> ApiResponse[FlowNode]:
        data = payload.model_dump(exclude_unset=True)
        created = self.service.create_node(profile, flow_id, data)
        schema = FlowNode.model_validate(created)
        return ResponseBuilder.success(schema, "Nodo creado")

    def create_edge(
        self, profile: Dict, flow_id: str, payload: FlowEdgeCreate
    ) -> ApiResponse[FlowEdge]:
        data = payload.model_dump(exclude_unset=True)
        created = self.service.create_edge(profile, flow_id, data)
        schema = FlowEdge.model_validate(created)
        return ResponseBuilder.success(schema, "Conexión creada")
