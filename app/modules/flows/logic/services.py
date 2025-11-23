"""Business logic for visual flows (ReactFlow backend)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from app.libraries.customs.base_service import BaseService
from app.libraries.exceptions.app_exceptions import AuthError, ValidationError
from app.modules.users.logic.services import UserService

from ..data.dao import FlowDAO, FlowEdgeDAO, FlowNodeDAO


class FlowService(BaseService):
    def __init__(
        self,
        flow_dao: Optional[FlowDAO] = None,
        node_dao: Optional[FlowNodeDAO] = None,
        edge_dao: Optional[FlowEdgeDAO] = None,
        user_service: Optional[UserService] = None,
    ) -> None:
        super().__init__(flow_dao or FlowDAO())
        self.node_dao = node_dao or FlowNodeDAO()
        self.edge_dao = edge_dao or FlowEdgeDAO()
        self.user_service = user_service or UserService()

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

    def _ensure_flow_access(self, profile: Dict[str, Any], flow: Dict[str, Any]):
        if profile.get("role") == "root":
            return
        company_id = self.user_service.ensure_has_company(profile)
        if flow.get("company_id") != company_id:
            raise AuthError("No tienes permiso para acceder a este flujo")

    def _ensure_node_in_flow(self, flow_id: str, node_id: str):
        node = self.node_dao.get_by_id(node_id)
        if not node or node.get("flow_id") != flow_id:
            raise ValidationError("El nodo indicado no pertenece a este flujo")
        return node

    # ------------------------------------------------------------------
    # Flows
    # ------------------------------------------------------------------
    def list_flows(self, profile: Dict[str, Any], *, company_id: Optional[str] = None):
        resolved_company = self._resolve_company(profile, company_id)
        if resolved_company:
            return self.dao.filter(company_id=resolved_company)
        return self.dao.get_all()

    def get_flow(self, profile: Dict[str, Any], flow_id: str):
        flow = self.get_by_id(flow_id)
        self._ensure_flow_access(profile, flow)
        nodes = self.node_dao.list_for_flow(flow_id)
        edges = self.edge_dao.list_for_flow(flow_id)
        return {**flow, "nodes": nodes, "edges": edges}

    def create_flow(self, profile: Dict[str, Any], data: Dict[str, Any]):
        company_id = self._resolve_company(profile, data.get("company_id"))
        if not company_id:
            raise ValidationError("Debe indicarse una empresa para el flujo")
        payload = {**data, "company_id": company_id}
        return self.create(
            payload,
            performed_by=profile.get("id"),
            audit_metadata={"company_id": company_id, "title": data.get("title")},
        )

    # ------------------------------------------------------------------
    # Nodes
    # ------------------------------------------------------------------
    def create_node(
        self, profile: Dict[str, Any], flow_id: str, data: Dict[str, Any]
    ):
        flow = self.get_by_id(flow_id)
        self._ensure_flow_access(profile, flow)
        payload = {**data, "flow_id": flow_id, "company_id": flow.get("company_id")}
        return self.node_dao.insert(payload)

    # ------------------------------------------------------------------
    # Edges
    # ------------------------------------------------------------------
    def create_edge(
        self, profile: Dict[str, Any], flow_id: str, data: Dict[str, Any]
    ):
        flow = self.get_by_id(flow_id)
        self._ensure_flow_access(profile, flow)
        source = data.get("source")
        target = data.get("target")
        if not source or not target:
            raise ValidationError("Debe indicarse nodo origen y destino")
        self._ensure_node_in_flow(flow_id, source)
        self._ensure_node_in_flow(flow_id, target)
        payload = {
            **data,
            "flow_id": flow_id,
            "company_id": flow.get("company_id"),
        }
        return self.edge_dao.insert(payload)

    # ------------------------------------------------------------------
    # Import/Batch helpers
    # ------------------------------------------------------------------
    def import_flow(self, profile: Dict[str, Any], data: Dict[str, Any]):
        flow_data = data.get("flow") or {}
        nodes_data: List[Dict[str, Any]] = data.get("nodes") or []
        edges_data: List[Dict[str, Any]] = data.get("edges") or []

        created_flow = self.create_flow(profile, flow_data)
        flow_id = created_flow.get("id")
        if not flow_id:
            raise ValidationError("No se pudo obtener el ID del flujo creado")

        created_nodes = [
            self.create_node(profile, flow_id, node_payload) for node_payload in nodes_data
        ]
        created_edges = [
            self.create_edge(profile, flow_id, edge_payload) for edge_payload in edges_data
        ]

        return {**created_flow, "nodes": created_nodes, "edges": created_edges}
