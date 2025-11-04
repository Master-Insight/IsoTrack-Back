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
    phone: Optional[str] = Field(default=None, description="Teléfono de contacto")
    active: bool = Field(default=True, description="Estado de la cuenta")


class UserCreate(UserBase):
    password: str
    role: RoleEnum = RoleEnum.user


class User(UserBase):
    id: str
    role: Optional[RoleEnum] = RoleEnum.user
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    token: str
    profile: Optional[User] = None


class LogoutResponse(BaseModel):
    status: str


class UserSummary(BaseModel):
    id: str
    email: EmailStr


class DeleteUserResponse(BaseModel):
    user: Optional[UserSummary] = None
