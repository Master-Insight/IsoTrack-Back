# app/modules/blacnk/data/dao.py
from __future__ import annotations

from app.libraries.customs.supabase_dao import CustomSupabaseDAO


class BlanckDAO(CustomSupabaseDAO):
    def __init__(self) -> None:
        super().__init__("processes")
