"""FastAPI routes for processes and tasks."""

from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, Query

from app.libraries.auth.roles import require_role
from app.libraries.utils.response_models import ApiResponse

from .controller import ProcessController
from .schemas import (
    Process,
    ProcessCreate,
    ProcessDetail,
    ProcessDocumentLink,
    ProcessUpdate,
    Task,
    TaskCreate,
    TaskUpdate,
)

router = APIRouter()
controller = ProcessController()


@router.get("/", response_model=ApiResponse[List[Process]])
async def list_processes(
    company_id: Optional[str] = Query(default=None),
    profile=Depends(require_role(["root", "admin", "user"])),
):
    return controller.list_processes(profile, company_id)


@router.post("/", response_model=ApiResponse[Process])
async def create_process(
    payload: ProcessCreate,
    profile=Depends(require_role(["root", "admin"])),
):
    return controller.create_process(profile, payload)


@router.get("/{process_id}", response_model=ApiResponse[ProcessDetail])
async def get_process(
    process_id: str,
    profile=Depends(require_role(["root", "admin", "user"])),
):
    return controller.get_process(profile, process_id)


@router.put("/{process_id}", response_model=ApiResponse[Process])
async def update_process(
    process_id: str,
    payload: ProcessUpdate,
    profile=Depends(require_role(["root", "admin"])),
):
    return controller.update_process(profile, process_id, payload)


@router.delete("/{process_id}", response_model=ApiResponse[dict])
async def delete_process(
    process_id: str,
    profile=Depends(require_role(["root", "admin"])),
):
    return controller.delete_process(profile, process_id)


# ---- Tasks ----
@router.get("/{process_id}/tasks", response_model=ApiResponse[List[Task]])
async def list_tasks(
    process_id: str,
    profile=Depends(require_role(["root", "admin", "user"])),
):
    return controller.list_tasks(profile, process_id)


@router.post("/{process_id}/tasks", response_model=ApiResponse[Task])
async def create_task(
    process_id: str,
    payload: TaskCreate,
    profile=Depends(require_role(["root", "admin"])),
):
    return controller.create_task(profile, process_id, payload)


@router.put(
    "/{process_id}/tasks/{task_id}",
    response_model=ApiResponse[Task],
)
async def update_task(
    process_id: str,
    task_id: str,
    payload: TaskUpdate,
    profile=Depends(require_role(["root", "admin"])),
):
    return controller.update_task(profile, process_id, task_id, payload)


@router.delete(
    "/{process_id}/tasks/{task_id}",
    response_model=ApiResponse[dict],
)
async def delete_task(
    process_id: str,
    task_id: str,
    profile=Depends(require_role(["root", "admin"])),
):
    return controller.delete_task(profile, process_id, task_id)


# ---- Links ----
@router.get(
    "/{process_id}/links",
    response_model=ApiResponse[List[ProcessDocumentLink]],
)
async def list_links(
    process_id: str,
    profile=Depends(require_role(["root", "admin", "user"])),
):
    return controller.list_links(profile, process_id)


@router.post(
    "/{process_id}/links",
    response_model=ApiResponse[ProcessDocumentLink],
)
async def create_link(
    process_id: str,
    payload: ProcessDocumentLink,
    profile=Depends(require_role(["root", "admin"])),
):
    return controller.create_link(profile, process_id, payload)


@router.delete(
    "/{process_id}/links/{link_id}",
    response_model=ApiResponse[dict],
)
async def delete_link(
    process_id: str,
    link_id: str,
    profile=Depends(require_role(["root", "admin"])),
):
    return controller.delete_link(profile, process_id, link_id)
