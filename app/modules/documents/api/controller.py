"""Controllers for document endpoints."""

from __future__ import annotations

from typing import Dict, List

from app.libraries.utils.response_builder import ResponseBuilder
from app.libraries.utils.response_models import ApiResponse

from ..logic.services import DocumentService
from .schemas import (
    Document,
    DocumentCreatePayload,
    DocumentDetail,
    DocumentListItem,
    DocumentRead,
    DocumentReadCreate,
    DocumentUpdate,
    DocumentVersion,
    DocumentVersionCreate,
)


class DocumentController:
    def __init__(self, service: DocumentService | None = None) -> None:
        self.service = service or DocumentService()

    def list_documents(
        self,
        profile: Dict,
        *,
        company_id: str | None,
        process_id: str | None,
        include_inactive: bool,
    ) -> ApiResponse[List[DocumentListItem]]:
        records = self.service.list_documents(
            profile,
            company_id=company_id,
            process_id=process_id,
            include_inactive=include_inactive,
        )
        items = [
            DocumentListItem.model_validate(record).model_dump(by_alias=True)
            for record in records
        ]
        return ResponseBuilder.success(items, "Documentos obtenidos")

    def get_document(self, document_id: str, profile: Dict) -> ApiResponse[DocumentDetail]:
        record = self.service.get_document_detail(document_id, profile)
        schema = DocumentDetail.model_validate(record)
        return ResponseBuilder.success(schema, "Documento obtenido")

    def create_document(
        self, profile: Dict, payload: DocumentCreatePayload
    ) -> ApiResponse[DocumentDetail]:
        data = payload.model_dump(exclude_unset=True)
        initial_version = None
        if payload.initial_version is not None:
            initial_version = payload.initial_version.model_dump(exclude_unset=True)
            data.pop("initial_version", None)
        created = self.service.create_document(
            profile,
            data,
            initial_version=initial_version,
        )
        schema = DocumentDetail.model_validate(created)
        return ResponseBuilder.success(schema, "Documento creado")

    def update_document(
        self, profile: Dict, document_id: str, payload: DocumentUpdate
    ) -> ApiResponse[Document]:
        updates = payload.model_dump(exclude_unset=True)
        record = self.service.update_document(profile, document_id, updates)
        schema = Document.model_validate(record)
        return ResponseBuilder.success(schema, "Documento actualizado")

    def delete_document(self, profile: Dict, document_id: str) -> ApiResponse[Dict]:
        result = self.service.delete_document(profile, document_id)
        return ResponseBuilder.success(result, "Documento eliminado")

    def create_version(
        self,
        profile: Dict,
        document_id: str,
        payload: DocumentVersionCreate,
    ) -> ApiResponse[DocumentVersion]:
        version_data = payload.model_dump(exclude_unset=True)
        created = self.service.create_version(profile, document_id, version_data)
        schema = DocumentVersion.model_validate(created)
        return ResponseBuilder.success(schema, "Versión creada")

    def record_read(
        self, profile: Dict, document_id: str, payload: DocumentReadCreate
    ) -> ApiResponse[DocumentRead]:
        read_payload = payload.model_dump(exclude_unset=True)
        recorded = self.service.record_read(profile, document_id, read_payload)
        schema = DocumentRead.model_validate(recorded)
        return ResponseBuilder.success(schema, "Lectura registrada")
