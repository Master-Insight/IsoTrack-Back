"""Data access helpers for diagrams."""

from __future__ import annotations

from app.libraries.customs.supabase_dao import CustomSupabaseDAO


class DiagramDAO(CustomSupabaseDAO):
    def __init__(self) -> None:
        super().__init__("diagrams")
