# app/modules/processes/logic/service.py
"""Process logic layer."""

from __future__ import annotations

from typing import List, Optional

from ..dao.memory import InMemoryProcessDAO

ProcessPayload = dict


class ProcessService:
    def __init__(self, dao: Optional[InMemoryProcessDAO] = None) -> None:
        self._dao = dao or InMemoryProcessDAO()

    def list_processes(self) -> List[ProcessPayload]:
        return self._dao.list_processes()
