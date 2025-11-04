# app/libraries/customs/base_service.py
"""Capa base para encapsular operaciones comunes de los servicios."""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from app.libraries.audit import AuditTrailService
from app.libraries.exceptions.app_exceptions import (
    AppError,
    NotFoundError,
    ServiceError,
)


class BaseService:
    """Clase base reutilizable para las operaciones de negocio."""

    def __init__(self, dao):
        self.dao = dao
        self.logger = logging.getLogger(
            f"{self.__class__.__module__}.{self.__class__.__name__}"
        )
        self.audit_trail = AuditTrailService()
        self._audit_entity = getattr(self.dao, "table_name", self.__class__.__name__)

    # ------------------------------------------------------------------
    # Métodos auxiliares de auditoría
    # ------------------------------------------------------------------
    def _record_audit(
        self,
        *,
        action: str,
        entity_id: Any | None,
        metadata: Optional[Dict[str, Any]] = None,
        performed_by: Optional[str] = None,
    ) -> None:
        try:
            self.audit_trail.record_action(
                entity=self._audit_entity,
                action=action,
                entity_id=str(entity_id) if entity_id is not None else None,
                metadata=metadata,
                performed_by=str(performed_by) if performed_by is not None else None,
            )
        except Exception:
            # No interrumpe el flujo principal, solo registra en logs internos
            self.logger.debug(
                "Fallo silencioso al registrar auditoría",
                extra={"action": action, "entity_id": entity_id},
            )

    def list_all(self):
        """Devuelve todos los registros."""
        try:
            return self.dao.get_all()
        except AppError:
            raise
        except Exception as exc:
            self.logger.exception("Error inesperado al listar registros")
            raise ServiceError(details={"error": str(exc)}) from exc

    def get_by_id(self, record_id: Any):
        """Devuelve un registro por su ID."""
        try:
            record = self.dao.get_by_id(record_id)
            if not record:
                raise NotFoundError(
                    message=f"Registro con ID {record_id} no encontrado",
                    details={"id": record_id},
                )
            return record
        except AppError:
            raise
        except Exception as exc:
            self.logger.exception(
                "Error inesperado al obtener el registro con ID %s", record_id
            )
            raise ServiceError(
                message="Error al obtener registro",
                details={"id": record_id, "error": str(exc)},
            ) from exc

    def create(
        self,
        data: Dict[str, Any],
        *,
        audit_metadata: Optional[Dict[str, Any]] = None,
        performed_by: Optional[str] = None,
    ):
        """Crea un nuevo registro."""
        try:
            created = self.dao.insert(data)
            entity_id = created.get("id") if isinstance(created, dict) else None
            metadata = {"fields": sorted(data.keys())}
            if audit_metadata:
                metadata.update(audit_metadata)
            self._record_audit(
                action="create",
                entity_id=entity_id,
                metadata=metadata,
                performed_by=performed_by,
            )
            return created
        except AppError:
            raise
        except Exception as exc:
            self.logger.exception("Error inesperado al crear registro")
            raise ServiceError(
                message="Error al crear registro", details={"error": str(exc)}
            ) from exc

    def update(
        self,
        record_id: Any,
        data: Dict[str, Any],
        *,
        audit_metadata: Optional[Dict[str, Any]] = None,
        performed_by: Optional[str] = None,
    ):
        """Actualiza un registro existente."""
        try:
            updated = self.dao.update(record_id, data)
            if not updated:
                raise NotFoundError(
                    message=f"Registro con ID {record_id} no encontrado",
                    details={"id": record_id},
                )
            metadata = {"fields_updated": sorted(data.keys())}
            if audit_metadata:
                metadata.update(audit_metadata)
            self._record_audit(
                action="update",
                entity_id=record_id,
                metadata=metadata,
                performed_by=performed_by,
            )
            return updated
        except AppError:
            raise
        except Exception as exc:
            self.logger.exception(
                "Error inesperado al actualizar el registro con ID %s", record_id
            )
            raise ServiceError(
                message="Error al actualizar registro",
                details={"id": record_id, "error": str(exc)},
            ) from exc

    def delete(
        self,
        record_id: Any,
        *,
        audit_metadata: Optional[Dict[str, Any]] = None,
        performed_by: Optional[str] = None,
    ):
        """Elimina un registro existente."""
        try:
            deleted = self.dao.delete(record_id)
            if not deleted:
                raise NotFoundError(
                    message=f"Registro con ID {record_id} no encontrado",
                    details={"id": record_id},
                )
            result = {
                "deleted": True,
                "id": record_id,
                "message": f"Registro {record_id} eliminado correctamente",
            }
            metadata = audit_metadata.copy() if audit_metadata else {}
            self._record_audit(
                action="delete",
                entity_id=record_id,
                metadata=metadata if metadata else None,
                performed_by=performed_by,
            )
            return result
        except AppError:
            raise
        except Exception as exc:
            self.logger.exception(
                "Error inesperado al eliminar el registro con ID %s", record_id
            )
            raise ServiceError(
                message="Error al eliminar registro",
                details={"id": record_id, "error": str(exc)},
            ) from exc
