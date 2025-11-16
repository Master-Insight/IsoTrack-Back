"""Data access layer for processes and related entities."""

from __future__ import annotations

from typing import Dict

from app.libraries.customs.supabase_dao import CustomSupabaseDAO


class ProcessDAO(CustomSupabaseDAO):
    def __init__(self) -> None:
        super().__init__("processes")


class TaskDAO(CustomSupabaseDAO):
    def __init__(self) -> None:
        super().__init__("tasks")

    def list_for_process(self, process_id: str):
        data = self.filter(process_id=process_id)
        return data


