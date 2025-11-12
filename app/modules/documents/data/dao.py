from __future__ import annotations

from typing import Any, Dict, Optional, Sequence

from app.libraries.customs.supabase_dao import CustomSupabaseDAO


class DocumentDAO(CustomSupabaseDAO):
    def __init__(self) -> None:
        super().__init__("documents")


class DocumentVersionDAO(CustomSupabaseDAO):
    def __init__(self) -> None:
        super().__init__("document_versions")

    def get_last_version(self, document_id: str) -> Optional[Dict[str, Any]]:
        data = self.table.select("*").eq("document_id", document_id).execute().data
        if not data:
            return None
        # Ordena por versión semántica como string
        sorted_data = sorted(
            data, key=lambda x: str(x.get("version", "")), reverse=True
        )
        return sorted_data[0]

    def list_for_document(self, document_id: str):
        data = self.table.select("*").eq("document_id", document_id).execute().data
        return sorted(data, key=lambda x: str(x.get("version", "")))

    def list_for_documents(self, document_ids: Sequence[str]):
        if not document_ids:
            return []

        query = (
            self.table.select("*")
            .in_("document_id", list(document_ids))
            .order("document_id", desc=False)
            .order("version", desc=False)
        )
        return self._execute(query, "list_for_documents")


class DocumentReadDAO(CustomSupabaseDAO):
    def __init__(self) -> None:
        super().__init__("document_reads")

    def upsert_read(self, payload: Dict[str, Any]):
        query = self.table.upsert(payload, on_conflict="document_id,user_id,version")
        data = self._execute(query, "upsert_read")
        return data[0] if data else None

    def list_for_document(self, document_id: str, user_id: Optional[str] = None):
        query = self.table.select("*").eq("document_id", document_id)
        if user_id:
            query = query.eq("user_id", user_id)
        return self._execute(query, "list_reads")

    def list_for_documents(self, document_ids: Sequence[str]):
        if not document_ids:
            return []

        query = self.table.select("*").in_("document_id", list(document_ids))
        return self._execute(query, "list_reads_for_documents")

    def get_user_read(
        self, document_id: str, user_id: str, version: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        query = (
            self.table.select("*").eq("document_id", document_id).eq("user_id", user_id)
        )
        if version is not None:
            query = query.eq("version", version)
        query = query.order("read_at", desc=True).limit(1)
        data = self._execute(query, "get_user_read")
        return data[0] if data else None
