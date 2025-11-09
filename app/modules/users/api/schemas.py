# app/modules/users/api/schemas.py
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class RoleEnum(str, Enum):
    root = "root"
    admin = "admin"
    user = "user"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserBase(BaseModel):
    email: EmailStr
    company_id: Optional[str] = Field(
        default=None, description="Empresa a la que pertenece el usuario"
    )
    full_name: Optional[str] = Field(default=None, description="Nombre completo")
    position: Optional[str] = Field(default=None, description="Cargo o puesto")


class UserCreate(UserBase):
    password: str
    role: RoleEnum = RoleEnum.user


class UserUpdate(BaseModel):
    company_id: Optional[str] = Field(
        default=None, description="Empresa a la que pertenece el usuario"
    )
    full_name: Optional[str] = Field(default=None, description="Nombre completo")
    position: Optional[str] = Field(default=None, description="Cargo o puesto")
    role: Optional[RoleEnum] = Field(default=None, description="Rol del usuario")


class User(UserBase):
    id: str
    role: RoleEnum = RoleEnum.user
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    accessToken: str
    refresh_token: str
    profile: Optional[User] = None


class LogoutResponse(BaseModel):
    status: str


class UserSummary(BaseModel):
    id: str
    email: EmailStr


class DeleteUserResponse(BaseModel):
    user: Optional[UserSummary] = None
