# app/services/supabase_client.py
"""Singleton del cliente de datos usado en toda la aplicación."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict

from supabase import Client, create_client

from app.config.settings import settings
from app.services.mock_supabase_client import MockSupabaseClient

logger = logging.getLogger(__name__)


def _load_mock_data(path: str | Path | None) -> Dict[str, Any] | None:
    if not path:
        return None

    try:
        content = Path(path).read_text(encoding="utf-8")
        data = json.loads(content)
    except FileNotFoundError:
        logger.warning("Mock data file not found at %s", path)
        return None
    except json.JSONDecodeError as error:
        logger.warning("Invalid JSON mock data at %s: %s", path, error)
        return None

    if not isinstance(data, dict):
        logger.warning(
            "Mock data must be a JSON object mapping table names to records."
        )
        return None

    return data


def _create_supabase_client() -> Client | MockSupabaseClient:
    data_source = settings.DATA_SOURCE.lower()

    if data_source == "mock":
        initial_data = _load_mock_data(settings.MOCK_DATA_PATH)
        return MockSupabaseClient(initial_data=initial_data)

    if data_source != "supabase":
        raise RuntimeError("DATA_SOURCE must be either 'supabase' or 'mock'")

    if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
        raise RuntimeError(
            "SUPABASE_URL and SUPABASE_KEY must be configured when DATA_SOURCE is 'supabase'."
        )

    return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)


supabase: Client | MockSupabaseClient = _create_supabase_client()


def create_supabase_auth_client() -> Client | MockSupabaseClient:
    """Return a fresh Supabase client for Auth operations.

    Auth workflows mutate the internal session of the Supabase client
    (por ejemplo, ``sign_in_with_password`` reemplaza el access token).
    Al entregar un cliente nuevo para Auth evitamos que esas mutaciones
    afecten al singleton reutilizado por los DAO para acceder a las tablas.
    """

    return _create_supabase_client()
