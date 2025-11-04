# app\modules\companies\data\dao.py
"""DAO para compañías."""

from __future__ import annotations

from app.libraries.customs.supabase_dao import CustomSupabaseDAO


class CompanyDAO(CustomSupabaseDAO):
    def __init__(self) -> None:
        super().__init__("companies")
