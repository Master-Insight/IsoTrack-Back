# app/modules/auth/api/controller.py
"""Controller for authentication related endpoints."""
from __future__ import annotations

from typing import Dict

from app.libraries.utils.response_builder import ResponseBuilder
from app.libraries.utils.response_models import ApiResponse

from ..logic.services import AuthService
from app.modules.users.api.schemas import UserProfile


class AuthController:
    def __init__(self, service: AuthService | None = None) -> None:
        self.service = service or AuthService()

    def get_me(self, profile: Dict) -> ApiResponse[UserProfile]:
        normalized = self.service.get_current_profile(profile)
        schema = UserProfile.model_validate(normalized)
        return ResponseBuilder.success(schema, "Perfil obtenido")
