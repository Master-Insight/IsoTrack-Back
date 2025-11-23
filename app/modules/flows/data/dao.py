"""Data access layer for flow entities."""

from __future__ import annotations

from app.libraries.customs.supabase_dao import CustomSupabaseDAO


class FlowDAO(CustomSupabaseDAO):
    def __init__(self) -> None:
        super().__init__("flows")


class FlowNodeDAO(CustomSupabaseDAO):
    def __init__(self) -> None:
        super().__init__("flow_nodes")

    def list_for_flow(self, flow_id: str):
        return self.filter(flow_id=flow_id)


class FlowEdgeDAO(CustomSupabaseDAO):
    def __init__(self) -> None:
        super().__init__("flow_edges")

    def list_for_flow(self, flow_id: str):
        return self.filter(flow_id=flow_id)
