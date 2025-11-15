# app/libraries/auth/dependencies.py
from fastapi import Header

from app.config.logging import set_user_id
from app.libraries.exceptions.app_exceptions import AuthError
from app.services.supabase_client import create_supabase_auth_client


auth_client = create_supabase_auth_client()


async def get_current_user(authorization: str = Header(...)):

    # Validar header presente
    if not authorization:
        raise AuthError("Falta token de autorización")

    # Validar formato
    if not authorization.startswith("Bearer "):
        raise AuthError("Token inválido")

    # Validar token no vacío
    token = authorization.replace("Bearer ", "").strip()
    if not token:
        raise AuthError("Token inválido o vacío")

    # Validar token via Supabase
    try:
        user = auth_client.auth.get_user(token)
        if not user or not user.user:
            raise AuthError("Token inválido o expirado")
        set_user_id(getattr(user.user, "id", None))
        return user.user

    except Exception as e:
        raise AuthError("Token inválido", details={"supabase_error": str(e)})
