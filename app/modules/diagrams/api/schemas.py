# app/modules/blanck/api/schemas.py
from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, condecimal


class BlanckBase(BaseModel):
    pass


class BlanckCreate(BlanckBase):
    pass


class BlanckUpdate(BaseModel):
    pass


class Blanck(BlanckBase):
    pass

    class Config:
        from_attributes = True
