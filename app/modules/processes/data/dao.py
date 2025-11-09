"""Data access layer for processes and related entities."""

from __future__ import annotations

from typing import Dict, Optional

from app.libraries.customs.supabase_dao import CustomSupabaseDAO


class ProcessDAO(CustomSupabaseDAO):
    def __init__(self) -> None:
        super().__init__("processes")


class TaskDAO(CustomSupabaseDAO):
    def __init__(self) -> None:
        super().__init__("tasks")

    def list_for_process(self, process_id: str):
        return self.filter(process_id=process_id)


class ProcessArtifactLinkDAO(CustomSupabaseDAO):
    def __init__(self) -> None:
        super().__init__("links_process_artifacts")

    def get_link(
        self, process_id: str, document_id: str
    ) -> Optional[Dict[str, Any]]:
        return self.get_first(process_id=process_id, document_id=document_id)

    def list_for_process(self, process_id: str):
        return self.filter(process_id=process_id)
