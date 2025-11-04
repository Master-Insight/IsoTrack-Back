# app\modules\Blancks\api\controller.py
from __future__ import annotations

from typing import Dict, Optional

from app.libraries.utils.response_builder import ResponseBuilder

from ..logic.services import BlanckService
from .schemas import BlanckCreate, BlanckUpdate


class BlanckController:
    def __init__(self) -> None:
        self.service = BlanckService()
