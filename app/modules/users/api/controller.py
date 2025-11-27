"""Controller orchestrating user-related use cases."""

from __future__ import annotations

from typing import Dict, Optional

from app.libraries.utils.response_builder import ResponseBuilder
from app.libraries.utils.response_models import ApiResponse

from ..logic.services import UserService
from .schemas import (
    DeleteUserResponse,
    LoginResponse,
    LogoutResponse,
    RefreshTokenRequest,
    RefreshTokenResponse,
    User,
    UserCreate,
    UserLogin,
    UserUpdate,
    UserSummary,
)


class UserController:
    def __init__(self, service: UserService | None = None) -> None:
        self.service = service or UserService()

    def list_users(self, profile: Dict, company_id: Optional[str]):
        """Listar usuarios visibles para el perfil autenticado."""

        users = self.service.list_users(profile=profile, company_id=company_id)
        items = [User.model_validate(user) for user in users]
        return ResponseBuilder.success(
            data=items, message="Usuarios obtenidos correctamente"
        )

    def login(self, login_data: UserLogin) -> ApiResponse[LoginResponse]:
        data = self.service.login(login_data.email, login_data.password)
        response = LoginResponse(**data)
        return ResponseBuilder.success(response, "Login exitoso ✅")

    def logout(self) -> ApiResponse[LogoutResponse]:
        result = self.service.logout()
        response = LogoutResponse(**result)
        return ResponseBuilder.success(response, "Sesión cerrada ✅")

    def refresh_token(
        self, payload: RefreshTokenRequest
    ) -> ApiResponse[RefreshTokenResponse]:
        """Refresh access token using refresh token."""
        data = self.service.refresh_token(payload.refresh_token)
        response = RefreshTokenResponse(**data)
        return ResponseBuilder.success(response, "Token actualizado correctamente ✅")

    def get_me(self, current_user) -> ApiResponse[User]:
        record = self.service.get_user(current_user.id)
        schema = User.model_validate(record)
        return ResponseBuilder.success(schema, "Perfil del usuario obtenido")

    def register_user(self, profile: Dict, user: UserCreate):
        target_company = user.company_id or profile.get("company_id")
        profile_data = {
            "company_id": target_company,
            "full_name": user.full_name,
            "position": user.position,
        }

        created_profile = self.service.register_user(
            email=user.email,
            password=user.password,
            role=user.role.value,
            profile_data=profile_data,
            current_profile=profile,
        )
        schema = User.model_validate(created_profile)
        return ResponseBuilder.success(schema, "Usuario registrado correctamente")

    def update_user(self, profile: Dict, user_id: str, payload: UserUpdate):
        updates = payload.model_dump(exclude_unset=True)
        updated = self.service.update_user(
            profile=profile,
            user_id=user_id,
            updates=updates,
        )
        schema = User.model_validate(updated)
        return ResponseBuilder.success(schema, "Usuario actualizado correctamente")

    def delete_user(self, profile: Dict, user_id: str):
        result = self.service.delete_user(profile, user_id)
        summary = UserSummary(**result["user"]) if result.get("user") else None
        response = DeleteUserResponse(user=summary)
        message = result.get("message", f"Usuario {user_id} eliminado correctamente")
        return ResponseBuilder.success(response, message)
