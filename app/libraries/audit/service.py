# app/libraries/audit/service.py
"""Servicio centralizado para registrar acciones en la bitácora de auditoría."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from app.config.logging import get_request_id, get_user_id
from app.libraries.audit.dao import AuditLogDAO
from app.libraries.exceptions.app_exceptions import AppError


class AuditTrailService:
    """Registra eventos relevantes para trazabilidad operativa."""

    def __init__(self) -> None:
        self.dao = AuditLogDAO()
        self.logger = logging.getLogger("app.audit")

    def record_action(
        self,
        *,
        entity: str,
        action: str,
        entity_id: Optional[str] = None,
        performed_by: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Persiste un evento de auditoría sin interrumpir el flujo principal."""

        payload: Dict[str, Any] = {
            "entity": entity,
            "action": action,
            "entity_id": entity_id,
            "performed_by": performed_by or self._resolve_actor(),
            "request_id": self._resolve_request_id(),
            "performed_at": datetime.now(timezone.utc).isoformat(),
        }

        sanitized_metadata = self._sanitize_metadata(metadata)
        if sanitized_metadata:
            payload["metadata"] = sanitized_metadata

        payload = {key: value for key, value in payload.items() if value is not None}

        try:
            self.dao.record(payload)
        except AppError as exc:
            self.logger.warning(
                "No se pudo registrar auditoría controlada",  # noqa: G004 - mensaje en español
                extra={"entity": entity, "action": action, "error": exc.message},
            )
        except Exception:
            self.logger.exception(
                "Error inesperado al registrar auditoría",  # noqa: G004 - mensaje en español
                extra={"entity": entity, "action": action},
            )

    @staticmethod
    def _sanitize_metadata(
        metadata: Optional[Dict[str, Any]],
    ) -> Optional[Dict[str, Any]]:
        if not metadata:
            return None

        sanitized: Dict[str, Any] = {}
        for key, value in metadata.items():
            if isinstance(value, (str, int, float, bool)) or value is None:
                sanitized[key] = value
            else:
                try:
                    sanitized[key] = str(value)
                except Exception:
                    sanitized[key] = repr(value)
        return sanitized if sanitized else None

    @staticmethod
    def _resolve_actor() -> Optional[str]:
        user_id = get_user_id()
        if not user_id or user_id == "-":
            return None
        return user_id

    @staticmethod
    def _resolve_request_id() -> Optional[str]:
        request_id = get_request_id()
        if not request_id or request_id == "-":
            return None
        return request_id
