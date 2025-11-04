"""Data access layer for user profiles."""

from __future__ import annotations

from typing import Any, Dict, Optional

from app.libraries.customs.supabase_dao import CustomSupabaseDAO


class UserDAO(CustomSupabaseDAO):
    """Capa de acceso a datos para la tabla ``user_profiles``."""

    def __init__(self) -> None:
        super().__init__("user_profiles")

    def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        return self.get_first(email=email)

    def list_by_company(self, company_id: str):
        return self.filter(company_id=company_id)
