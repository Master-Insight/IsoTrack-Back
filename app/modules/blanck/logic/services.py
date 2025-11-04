# app/modules/blanck/logic/services.py
from __future__ import annotations

from typing import Dict, Optional

from app.config.settings import settings
from app.libraries.customs.base_service import BaseService
from app.libraries.exceptions.app_exceptions import (
    AuthError,
    NotFoundError,
    ValidationError,
)

from ..data.dao import QuotationDAO


class BlanckService(BaseService):
    def __init__(self) -> None:
        super().__init__(BlanckDAO())
