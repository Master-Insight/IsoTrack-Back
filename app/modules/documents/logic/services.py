"""Business logic for document management."""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List, Optional

from app.libraries.customs.base_service import BaseService
from app.libraries.exceptions.app_exceptions import AuthError, ValidationError
from app.modules.users.logic.services import UserService

from ..data.dao import DocumentDAO, DocumentReadDAO, DocumentVersionDAO


class DocumentService(BaseService):
    def __init__(
        self,
        document_dao: Optional[DocumentDAO] = None,
        version_dao: Optional[DocumentVersionDAO] = None,
        read_dao: Optional[DocumentReadDAO] = None,
        user_service: Optional[UserService] = None,
    ) -> None:
        super().__init__(document_dao or DocumentDAO())
        self.version_dao = version_dao or DocumentVersionDAO()
        self.read_dao = read_dao or DocumentReadDAO()
        self.user_service = user_service or UserService()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _resolve_company(self, profile: Dict[str, Any], company_id: Optional[str]):
        role = profile.get("role")
        if role == "root":
            return company_id or profile.get("company_id")

        profile_company = self.user_service.ensure_has_company(profile)
        if company_id and company_id != profile_company:
            raise AuthError("No puedes operar sobre otra empresa")
        return profile_company

    def _ensure_document_access(self, profile: Dict[str, Any], document: Dict[str, Any]):
        if profile.get("role") == "root":
            return
        company_id = self.user_service.ensure_has_company(profile)
        if document.get("company_id") != company_id:
            raise AuthError("No tienes permiso para acceder a este documento")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def list_documents(
        self,
        profile: Dict[str, Any],
        *,
        company_id: Optional[str] = None,
        process_id: Optional[str] = None,
        include_inactive: bool = False,
    ):
        resolved_company = self._resolve_company(profile, company_id)
        filters: Dict[str, Any] = {}
        if resolved_company:
            filters["company_id"] = resolved_company
        if process_id:
            filters["process_id"] = process_id
        if not include_inactive:
            filters["active"] = True

        if not filters and profile.get("role") == "root":
            documents = self.dao.get_all()
        else:
            documents = self.dao.filter(**filters)

        return self._hydrate_documents(documents)

    def get_document_detail(self, document_id: str, profile: Dict[str, Any]):
        document = self.get_by_id(document_id)
        self._ensure_document_access(profile, document)
        versions = self.version_dao.list_for_document(document_id)
        latest_version = self.version_dao.get_last_version(document_id)
        current_user_read = None
        if profile.get("id"):
            current_user_read = self.read_dao.get_user_read(
                document_id, profile["id"],
                latest_version.get("version") if latest_version else None,
            )
        payload = {
            **document,
            "versions": versions,
            "latest_version": latest_version,
            "current_user_read": current_user_read,
        }
        return payload

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------
    def _hydrate_documents(self, documents: List[Dict[str, Any]]):
        if not documents:
            return []

        document_ids = [doc.get("id") for doc in documents if doc.get("id")]
        versions = self.version_dao.list_for_documents(document_ids)
        reads = self.read_dao.list_for_documents(document_ids)

        versions_by_document: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        for version in versions:
            document_id = version.get("document_id")
            if not document_id:
                continue
            version_payload = dict(version)
            version_value = version_payload.get("version")
            if version_value is not None:
                version_payload["version"] = str(version_value)
            versions_by_document[document_id].append(version_payload)

        def version_sort_key(item: Dict[str, Any]):
            raw = item.get("version")
            if raw is None:
                return (1, "")
            try:
                return (0, float(str(raw)))
            except (TypeError, ValueError):
                return (0, str(raw))

        for document_id in versions_by_document:
            versions_by_document[document_id].sort(key=version_sort_key)

        reads_by_document: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        for read in reads:
            document_id = read.get("document_id")
            if not document_id:
                continue
            reads_by_document[document_id].append(dict(read))

        for document_id in reads_by_document:
            reads_by_document[document_id].sort(
                key=lambda item: item.get("read_at") or "",
                reverse=True,
            )

        user_ids = {
            value
            for doc in documents
            for value in [doc.get("owner_id")]
            if value
        }
        for version in versions:
            approved_by = version.get("approved_by")
            if approved_by:
                user_ids.add(approved_by)
        for read in reads:
            user_id = read.get("user_id")
            if user_id:
                user_ids.add(user_id)

        user_lookup: Dict[str, Dict[str, Any]] = {}
        if user_ids:
            users = self.user_service.dao.get_by_ids(list(user_ids))
            user_lookup = {user.get("id"): user for user in users if user}

        def get_user_display_name(user: Optional[Dict[str, Any]]):
            if not user:
                return None
            return user.get("full_name") or user.get("email") or user.get("id")

        hydrated: List[Dict[str, Any]] = []
        for document in documents:
            document_id = document.get("id")
            owner_id = document.get("owner_id")
            owner = user_lookup.get(owner_id) if owner_id else None
            owner_name = get_user_display_name(owner)

            document_versions = []
            for version in versions_by_document.get(document_id, []):
                version_payload = dict(version)
                approved_by = version_payload.get("approved_by")
                if approved_by:
                    approved_user = user_lookup.get(approved_by)
                    version_payload["approved_by_name"] = get_user_display_name(
                        approved_user
                    )
                document_versions.append(version_payload)

            current_version = document_versions[-1] if document_versions else None

            document_reads = []
            for read in reads_by_document.get(document_id, []):
                read_payload = dict(read)
                user_id = read_payload.get("user_id")
                if user_id:
                    read_user = user_lookup.get(user_id)
                    read_payload["user"] = get_user_display_name(read_user)
                    if read_user:
                        read_payload["position"] = read_user.get("position")
                document_reads.append(read_payload)

            tags_value = document.get("tags")
            if tags_value is None:
                tags = []
            elif isinstance(tags_value, list):
                tags = tags_value
            else:
                tags = [tags_value]

            hydrated.append(
                {
                    **document,
                    "tags": tags,
                    "owner": owner_name,
                    "current_version": current_version,
                    "versions": document_versions,
                    "reads": document_reads,
                }
            )

        return hydrated

    def create_document(
        self,
        profile: Dict[str, Any],
        data: Dict[str, Any],
        *,
        initial_version: Optional[Dict[str, Any]] = None,
    ):
        company_id = self._resolve_company(profile, data.get("company_id"))
        if not company_id:
            raise ValidationError("Debe indicarse una empresa para el documento")

        data = {**data, "company_id": company_id}
        if "active" not in data:
            data["active"] = True

        created = self.create(
            data,
            performed_by=profile.get("id"),
            audit_metadata={"company_id": company_id},
        )

        if initial_version:
            version_payload = {**initial_version, "document_id": created["id"]}
            created_version = self._create_version_internal(
                profile, created, version_payload
            )
            created["latest_version"] = created_version
            created["versions"] = [created_version]
        return created

    def update_document(
        self,
        profile: Dict[str, Any],
        document_id: str,
        updates: Dict[str, Any],
    ):
        document = self.get_by_id(document_id)
        self._ensure_document_access(profile, document)

        if updates.get("company_id") and profile.get("role") != "root":
            raise AuthError("Solo un usuario root puede cambiar la empresa")

        return self.update(
            document_id,
            updates,
            performed_by=profile.get("id"),
            audit_metadata={"updated_fields": list(updates.keys())},
        )

    def delete_document(self, profile: Dict[str, Any], document_id: str):
        document = self.get_by_id(document_id)
        self._ensure_document_access(profile, document)
        return self.delete(
            document_id,
            performed_by=profile.get("id"),
            audit_metadata={"code": document.get("code")},
        )

    def create_version(
        self,
        profile: Dict[str, Any],
        document_id: str,
        payload: Dict[str, Any],
    ):
        document = self.get_by_id(document_id)
        self._ensure_document_access(profile, document)
        version_payload = {**payload, "document_id": document_id}
        return self._create_version_internal(profile, document, version_payload)

    def _create_version_internal(
        self,
        profile: Dict[str, Any],
        document: Dict[str, Any],
        payload: Dict[str, Any],
    ):
        if "version" not in payload or payload["version"] is None:
            last_version = self.version_dao.get_last_version(document["id"])
            next_version = (last_version.get("version") if last_version else 0) + 1
            payload["version"] = next_version

        payload.setdefault("status", "borrador")
        payload.setdefault("created_at", datetime.utcnow())

        created = self.version_dao.insert(payload)
        self._record_audit(
            action="create_version",
            entity_id=document.get("id"),
            metadata={
                "version": created.get("version"),
                "status": created.get("status"),
            },
            performed_by=profile.get("id"),
        )
        return created

    def record_read(
        self,
        profile: Dict[str, Any],
        document_id: str,
        payload: Dict[str, Any],
    ):
        document = self.get_by_id(document_id)
        self._ensure_document_access(profile, document)

        version_number = payload.get("version")
        if version_number is None:
            latest = self.version_dao.get_last_version(document_id)
            if not latest:
                raise ValidationError("El documento no posee versiones publicadas")
            version_number = latest.get("version")

        read_data = {
            "document_id": document_id,
            "user_id": profile.get("id"),
            "version": version_number,
            "read_at": payload.get("read_at") or datetime.utcnow(),
            "due_date": payload.get("due_date"),
        }
        recorded = self.read_dao.upsert_read(read_data)
        self._record_audit(
            action="document_read",
            entity_id=document_id,
            metadata={"version": version_number},
            performed_by=profile.get("id"),
        )
        return recorded
