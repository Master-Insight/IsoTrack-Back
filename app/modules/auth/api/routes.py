# app/modules/auth/api/routes.py
"""Auth endpoints."""
from __future__ import annotations

from fastapi import APIRouter, Depends

from app.libraries.auth.roles import get_current_profile
from app.libraries.utils.response_models import ApiResponse
from app.modules.users.api.schemas import UserProfile

from .controller import AuthController

router = APIRouter()
controller = AuthController()


@router.get("/me", response_model=ApiResponse[UserProfile])
async def get_me(profile=Depends(get_current_profile)):
    """Return the authenticated user profile."""
    return controller.get_me(profile)
