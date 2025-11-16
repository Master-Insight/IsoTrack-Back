"""Simple smoke test to validate the Phase 1.6 flow using mock data."""

from __future__ import annotations

import os
import sys
from datetime import datetime
from pathlib import Path
from uuid import uuid4

# Force mock datasource before importing the app settings
ROOT_DIR = Path(__file__).resolve().parents[1]
os.environ.setdefault("DATA_SOURCE", "mock")
os.environ.setdefault("MOCK_DATA_PATH", str(ROOT_DIR / "doc" / "mock_data.json"))
sys.path.append(str(ROOT_DIR))

from app.modules.diagrams.logic.services import DiagramService
from app.modules.documents.logic.services import DocumentService
from app.modules.processes.logic.services import ProcessService


def main() -> None:
    profile = {
        "id": "05dc56fe-10eb-41d1-9305-340de88c5296",
        "role": "root",
        "company_id": "7d9cf77c-bc42-405c-b211-b905d576624b",
    }

    document_service = DocumentService()
    process_service = ProcessService()
    diagram_service = DiagramService()

    new_document = {
        "id": str(uuid4()),
        "title": "Procedimiento de Smoke Test",
        "code": "PR-SM-001",
        "type": "POE",
        "description": "Documento temporal generado por el smoke test",
        "owner_id": profile["id"],
        "company_id": profile["company_id"],
        "category": "QA",
        "tags": ["smoke", "automático"],
    }
    document = document_service.create_document(
        profile,
        new_document,
        initial_version={
            "version": "1.0",
            "status": "vigente",
            "notes": "Versión inicial",
            "created_at": datetime.utcnow(),
        },
    )

    process_id = "process-gestion-calidad"
    process_service.create_link(
        profile,
        process_id,
        {"target_id": document["id"], "target_type": "document"},
    )
    document_service.record_read(
        profile,
        document["id"],
        {"version": "1.0", "read_at": datetime.utcnow()},
    )

    diagram = diagram_service.create_diagram(
        profile,
        {
            "id": str(uuid4()),
            "title": "Mapa rápido de procesos",
            "type": "flujo",
            "company_id": profile["company_id"],
            "data": {
                "nodes": [
                    {"id": "p1", "label": "Proceso"},
                    {"id": "doc", "label": "Documento"},
                ],
                "edges": [{"source": "p1", "target": "doc"}],
            },
        },
    )
    diagram_service.create_link(
        profile,
        diagram["id"],
        {"target_id": process_id, "target_type": "process", "relation_type": "vista"},
    )

    print("Smoke test completado:")
    print(f"- Documento creado: {document['id']}")
    print(f"- Diagrama creado: {diagram['id']}")
    print("- Vínculos registrados en artifact_links")


if __name__ == "__main__":
    main()
