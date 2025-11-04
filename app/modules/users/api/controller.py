# app/modules/users/api/controller.py
from typing import Dict, Optional

from app.libraries.utils.response_builder import ResponseBuilder

from ..logic.services import UserService
from .schemas import UserCreate


class UserController:
    def __init__(self):
        self.service = UserService()

    def list_users(self, profile: Dict, company_id: Optional[str]):
        """Obtiene todos los registros."""
        users = self.service.list_users(profile=profile, company_id=company_id)
        return ResponseBuilder.success(
            data=users, message="Usuarios obtenidos correctamente"
        )

    def login(self, login_data):
        data = self.service.login(login_data.email, login_data.password)
        return ResponseBuilder.success(data, "Login exitoso ✅")

    def logout(self):
        result = self.service.logout()
        return ResponseBuilder.success(result, "Sesión cerrada ✅")

    def get_me(self, current_user):
        data = self.service.get_user(current_user.id)
        return ResponseBuilder.success(data, "Perfil del usuario obtenido")

    # TODO en caso de usar un role distinto  a "user" deberia confirmar medidas de seguridad para limitar acción
    def register_user(self, profile: Dict, user: UserCreate):
        target_company = user.company_id or profile.get("company_id")
        profile_data = {
            "company_id": target_company,
            "full_name": user.full_name,
            "phone": user.phone,
            "active": user.active,
        }

        created_profile = self.service.register_user(
            email=user.email,
            password=user.password,
            role=user.role.value,
            profile_data=profile_data,
            current_profile=profile,
        )
        return ResponseBuilder.success(
            created_profile, "Usuario registrado correctamente"
        )

    def delete_user(self, profile: Dict, user_id: str):
        result = self.service.delete_user(profile, user_id)
        message = result.get("message", f"Usuario {user_id} eliminado correctamente")
        return ResponseBuilder.success(result, message)
