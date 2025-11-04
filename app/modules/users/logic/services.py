# app/modules/users/logic/services.py
from __future__ import annotations

from typing import Dict, Optional

from app.libraries.customs.base_service import BaseService
from app.libraries.exceptions.app_exceptions import (
    AuthError,
    NotFoundError,
    ValidationError,
)
from .supabase_auth_gateway import SupabaseAuthGateway

from ..data.dao import UserDAO


class UserService(BaseService):
    def __init__(self, auth_gateway: Optional[SupabaseAuthGateway] = None):
        super().__init__(UserDAO())
        self.auth_gateway = auth_gateway or SupabaseAuthGateway()

    def register_user(
        self,
        *,
        email: str,
        password: str,
        role: str = "user",
        profile_data: Optional[Dict] = None,
        current_profile: Optional[Dict] = None,
    ):
        profile_data = profile_data or {}

        # 0) Controles de seguridad
        if (
            current_profile
            and current_profile.get("role") == "admin"
            and role == "root"
        ):
            raise AuthError("Los administradores no pueden crear usuarios root")

        if current_profile and current_profile.get("role") == "admin":
            target_company = profile_data.get("company_id") or current_profile.get(
                "company_id"
            )
            if target_company != current_profile.get("company_id"):
                raise AuthError("No puedes asignar usuarios a otra empresa")
            profile_data["company_id"] = target_company

        # 1) Intentar crear usuario en Auth (o confirmar existencia)
        try:
            """Crea usuario en Supabase Auth."""
            auth_user = self.auth_gateway.sign_up(email, password)
            user_id = auth_user.user.id

        except Exception as e:
            error_str = str(e)

            # Caso: Contraseña inválida
            if "Password should be at least 6 characters" in error_str:
                raise ValidationError("La contraseña debe tener al menos 6 caracteres")

            # Caso: Email ya registrado -> Sign-in para obtener ID real
            if "User already registered" in error_str:
                auth_user = self.auth_gateway.sign_in_with_password(email, password)

                if not auth_user or not auth_user.user:
                    raise AuthError(
                        "Email duplicado. No se puede loguear. Credenciales inválidas o usuario bloqueado",
                        details={"supabase_error": error_str},
                    )
                user_id = auth_user.user.id

            else:
                raise AuthError(
                    "Error al registrar usuario", details={"supabase_error": error_str}
                )

        # 2) Revisar/asegurar el perfil (el trigger debería haberlo creado)
        profile = self.dao.get_by_email(email)
        if profile:
            # 2a) Si el perfil existe, asegurar el role (idempotente)
            current_role = profile.get("role")

            updates = {
                key: value
                for key, value in (profile_data or {}).items()
                if value is not None
            }

            metadata = {"email": email}
            if current_role != role:
                updates["role"] = role
                metadata["previous_role"] = current_role
                metadata["role"] = role

            if updates:
                profile = self.update(
                    profile.get("id"),
                    updates,
                    audit_metadata=metadata,
                )
            return profile

        # 3) Si NO existe perfil (trigger falló), lo creamos manualmente
        new_profile = {
            "id": user_id,
            "email": email,
            "role": role,
        }
        for key, value in profile_data.items():
            if value is not None:
                new_profile[key] = value

        metadata = {"email": email, "role": role}
        created = self.create(new_profile, audit_metadata=metadata)
        return created

    def login(self, email: str, password: str):
        try:
            auth_user = self.auth_gateway.sign_in_with_password(email, password)

            if not auth_user.user:
                raise AuthError("Credenciales inválidas")

            profile = self.dao.get_by_email(email)
            return {
                "token": auth_user.session.access_token,
                "profile": profile,
            }

        except Exception:
            raise AuthError("Credenciales inválidas")

    def logout(self):
        try:
            self.auth_gateway.sign_out()
            return {"status": "signed_out"}
        except Exception as e:
            error_msg = str(getattr(e, "message", e))
            raise AuthError(
                "No se pudo cerrar sesión", details={"supabase_error": error_msg}
            )

    def list_users(self, *, profile: Dict, company_id: Optional[str] = None):
        if profile.get("role") == "root" and not company_id:
            return self.dao.get_all()

        target_company = company_id or profile.get("company_id")

        if not target_company:
            raise ValidationError("Debes indicar una empresa para listar usuarios")

        if profile.get("role") == "admin" and target_company != profile.get(
            "company_id"
        ):
            raise AuthError("No puedes ver usuarios de otra empresa")

        return self.dao.filter(company_id=target_company)

    def get_user(self, user_id: str):
        return self.get_by_id(user_id)

    def get_user_by_email(self, email: str):
        user = self.dao.get_by_email(email)
        return user

    def delete_user(self, profile: Dict, user_id: str):
        try:
            # 1️⃣ Verificar si el usuario existe en tu tabla
            user = self.get_by_id(user_id)

            if profile.get("role") == "admin":
                if user.get("company_id") != profile.get("company_id"):
                    raise AuthError("No puedes eliminar usuarios de otra empresa")
                if user.get("role") == "root":
                    raise AuthError("No puedes eliminar usuarios root")

            # 2️⃣ Eliminar perfil en tu base de datos
            self.delete(user_id, audit_metadata={"email": user.get("email")})

            # 3️⃣ Eliminar usuario en Supabase Auth (requiere Service Role Key)
            self.auth_gateway.delete_user(user_id)

            return {"user": {"id": user_id, "email": user.get("email")}}

        except NotFoundError:
            raise
        except Exception as e:
            raise AuthError("Error al eliminar usuario", details={"error": str(e)})
