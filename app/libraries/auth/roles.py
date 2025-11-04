# app/libraries/auth/roles.py
from functools import lru_cache
from typing import Any

from fastapi import Depends
from app.libraries.exceptions.app_exceptions import AuthError
from app.modules.users.logic.services import UserService

from .dependencies import get_current_user


@lru_cache
def get_user_service() -> UserService:
    """Obtiene una única instancia reutilizable del servicio de usuarios."""
    return UserService()


async def get_current_profile(
    current_user=Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> Any:
    """Recupera el perfil asociado al usuario autenticado."""

    profile = user_service.get_user_by_email(current_user.email)
    if not profile:
        raise AuthError("Perfil no encontrado para este usuario")

    return profile


def require_role(allowed_roles: list[str]):
    async def role_checker(profile=Depends(get_current_profile)):
        role = (
            profile.get("role")
            if isinstance(profile, dict)
            else getattr(profile, "role", None)
        )

        if role not in allowed_roles:
            raise AuthError("No tienes permiso para acceder a este recurso")

        return profile

    return role_checker
