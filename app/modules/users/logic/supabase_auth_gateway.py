# app/services/supabase_auth_gateway.py
"""Gateway abstraction for Supabase authentication interactions."""

from __future__ import annotations

from typing import Any, Dict, Optional

from supabase.client import Client

from app.services.supabase_client import create_supabase_auth_client


class SupabaseAuthGateway:
    """Thin wrapper around Supabase Auth operations.

    Centralizes direct calls to the Supabase client so services can be easily
    unit tested (by injecting a fake gateway) and the auth provider can be
    swapped or extended with minimal changes.
    """

    def __init__(self, client: Optional[Client] = None) -> None:
        # Cada gateway tiene su propio cliente para no alterar el singleton
        # usado por los DAO al momento de ejecutar operaciones de Auth.
        self._client: Client = client or create_supabase_auth_client()

    def sign_up(self, email: str, password: str) -> Any:
        return self._client.auth.sign_up({"email": email, "password": password})

    def sign_in_with_password(self, email: str, password: str) -> Any:
        return self._client.auth.sign_in_with_password(
            {"email": email, "password": password}
        )

    def sign_out(self) -> None:
        self._client.auth.sign_out()

    def refresh_session(self, refresh_token: str) -> Any:
        """Refresh the access token using a refresh token."""
        return self._client.auth.refresh_session(refresh_token)

    def delete_user(self, user_id: str) -> Dict[str, Any]:
        return self._client.auth.admin.delete_user(user_id)

    def client(self) -> Client:
        """Expose the underlying client when lower-level access is required."""

        return self._client
