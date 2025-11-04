# app\modules\companies\logic\services.py
"""Servicios para compañías."""

from __future__ import annotations

from app.libraries.customs.base_service import BaseService

from ..data.dao import CompanyDAO


class CompanyService(BaseService):
    def __init__(self) -> None:
        super().__init__(CompanyDAO())
