"""Mock Supabase client para entornos de desarrollo y pruebas."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class MockResponse:
    """Objeto de respuesta similar al cliente de Supabase."""

    data: Any
    error: Any = None


class MockSupabaseClient:
    """Cliente simplificado que emula la interfaz básica del SDK de Supabase."""

    def __init__(self, initial_data: Optional[Dict[str, Iterable[Dict[str, Any]]]] = None):
        self._tables: Dict[str, List[Dict[str, Any]]] = {}
        if initial_data:
            for table, rows in initial_data.items():
                self._tables[table] = [deepcopy(row) for row in rows]

    # API compatible con supabase-py
    def table(self, table_name: str) -> "MockTable":
        return MockTable(self, table_name)

    # Utilidades internas
    def _get_table_data(self, table_name: str) -> List[Dict[str, Any]]:
        return self._tables.setdefault(table_name, [])

    def _set_table_data(self, table_name: str, data: List[Dict[str, Any]]) -> None:
        self._tables[table_name] = data


class MockTable:
    def __init__(self, client: MockSupabaseClient, table_name: str):
        self._client = client
        self._table_name = table_name

    def select(self, columns: str = "*") -> "MockQuery":
        return MockQuery(self._client, self._table_name, "select", columns=columns)

    def insert(self, payload: Dict[str, Any]) -> "MockQuery":
        return MockQuery(self._client, self._table_name, "insert", payload=payload)

    def update(self, payload: Dict[str, Any]) -> "MockQuery":
        return MockQuery(self._client, self._table_name, "update", payload=payload)

    def delete(self) -> "MockQuery":
        return MockQuery(self._client, self._table_name, "delete")


class MockQuery:
    def __init__(
        self,
        client: MockSupabaseClient,
        table_name: str,
        action: str,
        *,
        columns: str = "*",
        payload: Optional[Dict[str, Any]] = None,
    ) -> None:
        self._client = client
        self._table_name = table_name
        self._action = action
        self._columns = columns
        self._payload = deepcopy(payload) if payload is not None else None
        self._filters: Dict[str, Any] = {}
        self._in_filters: Dict[str, Iterable[Any]] = {}

    def eq(self, key: str, value: Any) -> "MockQuery":
        self._filters[key] = value
        return self

    def in_(self, key: str, values: Iterable[Any]) -> "MockQuery":
        self._in_filters[key] = list(values)
        return self

    def execute(self) -> MockResponse:
        data = self._client._get_table_data(self._table_name)

        # Filtrado
        filtered = []
        for row in data:
            if not self._matches_filters(row):
                continue
            filtered.append(row)

        if self._action == "select":
            result = [self._project_columns(row) for row in filtered]
            return MockResponse(data=deepcopy(result))

        if self._action == "insert":
            inserted_rows = self._prepare_insert()
            data.extend(inserted_rows)
            return MockResponse(data=deepcopy(inserted_rows))

        if self._action == "update":
            updated_rows = self._apply_update(filtered)
            return MockResponse(data=deepcopy(updated_rows))

        if self._action == "delete":
            deleted_rows = self._apply_delete(filtered)
            return MockResponse(data=deepcopy(deleted_rows))

        raise ValueError(f"Unsupported action: {self._action}")

    # Helpers
    def _matches_filters(self, row: Dict[str, Any]) -> bool:
        for key, value in self._filters.items():
            if row.get(key) != value:
                return False
        for key, values in self._in_filters.items():
            if row.get(key) not in values:
                return False
        return True

    def _project_columns(self, row: Dict[str, Any]) -> Dict[str, Any]:
        if self._columns in {"*", ""}:
            return deepcopy(row)

        columns = [col.strip() for col in self._columns.split(",") if col.strip()]
        return {column: deepcopy(row.get(column)) for column in columns}

    def _prepare_insert(self) -> List[Dict[str, Any]]:
        if self._payload is None:
            return []

        if isinstance(self._payload, list):
            payloads = self._payload
        else:
            payloads = [self._payload]

        return [deepcopy(item) for item in payloads]

    def _apply_update(self, rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not rows or self._payload is None:
            return []

        for row in rows:
            row.update(self._payload)
        return rows

    def _apply_delete(self, rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not rows:
            return []

        table_data = self._client._get_table_data(self._table_name)
        to_remove = {id(row) for row in rows}
        remaining = [row for row in table_data if id(row) not in to_remove]
        self._client._set_table_data(self._table_name, remaining)
        return rows
