"""Data access layer for the artifact_links table."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from app.libraries.customs.supabase_dao import CustomSupabaseDAO


class ArtifactLinkDAO(CustomSupabaseDAO):
    """Encapsula operaciones de lectura/escritura sobre ``artifact_links``."""

    def __init__(self) -> None:
        super().__init__("artifact_links")

    def list_for_entity(self, entity_id: str, entity_type: str) -> List[Dict[str, Any]]:
        """Devuelve los vínculos donde la entidad participa como origen o destino."""

        outgoing = self.filter(from_id=entity_id, from_type=entity_type)
        incoming = self.filter(to_id=entity_id, to_type=entity_type)

        records: Dict[str, Dict[str, Any]] = {}
        for item in outgoing + incoming:
            identifier = item.get("id")
            if identifier is None:
                continue
            records.setdefault(identifier, item)
        return list(records.values())

    def get_by_pair(
        self,
        *,
        from_id: str,
        from_type: str,
        to_id: str,
        to_type: str,
    ) -> Optional[Dict[str, Any]]:
        return self.get_first(
            from_id=from_id, from_type=from_type, to_id=to_id, to_type=to_type
        )
