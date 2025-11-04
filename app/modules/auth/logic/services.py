# app/modules/auth/logic/services.py
"""Authentication related business logic."""
from __future__ import annotations

from typing import Any, Dict

from app.libraries.exceptions.app_exceptions import AuthError
from app.modules.users.logic.services import UserService


class AuthService:
    """Service responsible for session related operations."""

    def __init__(self, user_service: UserService | None = None) -> None:
        self.user_service = user_service or UserService()

    def get_current_profile(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Return a normalized view of the authenticated profile."""
        if not profile_data:
            raise AuthError("Perfil de usuario no disponible")

        # Ensure we always return the latest data from the database.
        user_id = profile_data.get("id")
        if user_id:
            profile = self.user_service.get_profile(user_id)
            if profile:
                return profile

        email = profile_data.get("email")
        if email:
            profile = self.user_service.get_user_by_email(email)
            if profile:
                return profile

        raise AuthError("No se encontró el perfil del usuario")
