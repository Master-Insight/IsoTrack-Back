"""FastAPI routes for documents."""

from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, Query

from app.libraries.auth.roles import require_role
from app.libraries.utils.response_models import ApiResponse

from .controller import DocumentController
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

router = APIRouter()
controller = DocumentController()


@router.get("/", response_model=ApiResponse[List[DocumentListItem]])
async def list_documents(
    company_id: Optional[str] = Query(default=None),
    process_id: Optional[str] = Query(default=None),
    include_inactive: bool = Query(default=False),
    profile=Depends(require_role(["root", "admin", "user"])),
):
    return controller.list_documents(
        profile,
        company_id=company_id,
        process_id=process_id,
        include_inactive=include_inactive,
    )


@router.get("/{document_id}", response_model=ApiResponse[DocumentDetail])
async def get_document(document_id: str, profile=Depends(require_role(["root", "admin", "user"]))):
    return controller.get_document(document_id, profile)


@router.post("/", response_model=ApiResponse[DocumentDetail])
async def create_document(
    payload: DocumentCreatePayload,
    profile=Depends(require_role(["root", "admin"])),
):
    return controller.create_document(profile, payload)


@router.put("/{document_id}", response_model=ApiResponse[Document])
async def update_document(
    document_id: str,
    payload: DocumentUpdate,
    profile=Depends(require_role(["root", "admin"])),
):
    return controller.update_document(profile, document_id, payload)


@router.delete("/{document_id}", response_model=ApiResponse[dict])
async def delete_document(
    document_id: str,
    profile=Depends(require_role(["root", "admin"])),
):
    return controller.delete_document(profile, document_id)


@router.post(
    "/{document_id}/versions",
    response_model=ApiResponse[DocumentVersion],
)
async def create_version(
    document_id: str,
    payload: DocumentVersionCreate,
    profile=Depends(require_role(["root", "admin"])),
):
    return controller.create_version(profile, document_id, payload)


@router.post(
    "/{document_id}/reads",
    response_model=ApiResponse[DocumentRead],
)
async def record_read(
    document_id: str,
    payload: DocumentReadCreate,
    profile=Depends(require_role(["root", "admin", "user"])),
):
    return controller.record_read(profile, document_id, payload)
