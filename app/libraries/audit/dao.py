# app\libraries\audit\dao.py
"""DAO para registros de auditoría."""

from __future__ import annotations

from typing import Any, Dict

from app.libraries.customs.supabase_dao import CustomSupabaseDAO


class AuditLogDAO(CustomSupabaseDAO):
    """Capa de acceso a datos para la tabla ``audit_logs``."""

    def __init__(self) -> None:
        super().__init__("audit_logs")

    def record(self, payload: Dict[str, Any]):
        """Inserta un registro de auditoría y retorna el resultado bruto."""

        return self.insert(payload)
