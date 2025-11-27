# app/modules/users/api/routes.py
from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, Query

"""Public API routes for user management."""

from app.libraries.auth.dependencies import get_current_user
from app.libraries.auth.roles import require_role
from app.libraries.utils.response_models import ApiResponse

from .controller import UserController
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
)

router = APIRouter()
controller = UserController()


@router.post("/register", response_model=ApiResponse[User])
def register_user(
    user: UserCreate,
    current_user=Depends(require_role(["root", "admin"])),
):
    return controller.register_user(current_user, user)


@router.post("/login", response_model=ApiResponse[LoginResponse])
def login(user: UserLogin):
    return controller.login(user)


@router.post("/logout", response_model=ApiResponse[LogoutResponse])
def logout():
    return controller.logout()


@router.post("/refresh", response_model=ApiResponse[RefreshTokenResponse])
def refresh_token(payload: RefreshTokenRequest):
    """Refresh access token using refresh token."""
    return controller.refresh_token(payload)


@router.get("/me", response_model=ApiResponse[User])
def get_me(current_user=Depends(get_current_user)):
    return controller.get_me(current_user)


@router.get("/", response_model=ApiResponse[List[User]])
def list_users(
    company_id: Optional[str] = Query(default=None),
    current_user=Depends(require_role(["root", "admin"])),
):
    return controller.list_users(current_user, company_id)


@router.put("/{user_id}", response_model=ApiResponse[User])
def update_user(
    user_id: str,
    payload: UserUpdate,
    current_user=Depends(require_role(["root", "admin"])),
):
    return controller.update_user(current_user, user_id, payload)


@router.delete("/{user_id}", response_model=ApiResponse[DeleteUserResponse])
def delete_user(
    user_id: str,
    current_user=Depends(require_role(["root", "admin"])),
):
    return controller.delete_user(current_user, user_id)
