# app/modules/users/data/dao.py
"""DAO específico para usuarios usando Supabase."""

from __future__ import annotations

from app.libraries.customs.supabase_dao import CustomSupabaseDAO


class UserDAO(CustomSupabaseDAO):
    """Capa de acceso a datos de usuarios."""

    def __init__(self):
        super().__init__("user_profiles")

    def get_by_email(self, email: str):
        return self.get_first(email=email)

    def create_profile(self, user_data: dict):
        return self.insert(user_data)

    def update_profile(self, user_id: str, data: dict):
        return self.update(user_id, data)

    def update_role_by_email(self, email: str, role: str):
        return self.update_where({"email": email}, {"role": role})

    def delete_profile(self, user_id: str):
        return super().delete(user_id)
