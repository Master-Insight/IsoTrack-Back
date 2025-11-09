"""Mock Supabase client para entornos de desarrollo y pruebas."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


@dataclass
class MockResponse:
    """Objeto de respuesta similar al cliente de Supabase."""

    data: Any
    error: Any = None


class MockSupabaseClient:
    """Cliente simplificado que emula la interfaz básica del SDK de Supabase."""

    def __init__(
        self, initial_data: Optional[Dict[str, Iterable[Dict[str, Any]]]] = None
    ):
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

    def upsert(
        self, payload: Dict[str, Any], *, on_conflict: Optional[str] = None
    ) -> "MockQuery":
        return MockQuery(
            self._client,
            self._table_name,
            "upsert",
            payload=payload,
            on_conflict=on_conflict,
        )

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
        on_conflict: Optional[str] = None,
    ) -> None:
        self._client = client
        self._table_name = table_name
        self._action = action
        self._columns = columns
        self._payload = deepcopy(payload) if payload is not None else None
        self._filters: Dict[str, Any] = {}
        self._in_filters: Dict[str, Iterable[Any]] = {}
        self._orderings: List[Tuple[str, bool]] = []
        self._limit: Optional[int] = None
        self._on_conflict = on_conflict

    def eq(self, key: str, value: Any) -> "MockQuery":
        self._filters[key] = value
        return self

    def in_(self, key: str, values: Iterable[Any]) -> "MockQuery":
        self._in_filters[key] = list(values)
        return self

    def order(self, column: str, *, desc: bool = False) -> "MockQuery":
        self._orderings.append((column, desc))
        return self

    def limit(self, count: int) -> "MockQuery":
        self._limit = count
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
            ordered = self._apply_ordering(filtered)
            limited = self._apply_limit(ordered)
            result = [self._project_columns(row) for row in limited]
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

        if self._action == "upsert":
            upserted_rows = self._apply_upsert()
            return MockResponse(data=deepcopy(upserted_rows))

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

    def _apply_ordering(self, rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not self._orderings:
            return list(rows)

        ordered = list(rows)

        def normalize(value: Any) -> Any:
            if value is None:
                return value
            if isinstance(value, str):
                return value.lower()
            if isinstance(value, (int, float, bool)):
                return value
            return str(value)

        for column, desc in reversed(self._orderings):
            non_null = [row for row in ordered if row.get(column) is not None]
            nulls = [row for row in ordered if row.get(column) is None]
            non_null.sort(key=lambda item: normalize(item.get(column)), reverse=desc)
            ordered = non_null + nulls

        return ordered

    def _apply_limit(self, rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if self._limit is None:
            return list(rows)
        return list(rows)[: self._limit]

    def _project_columns(self, row: Dict[str, Any]) -> Dict[str, Any]:
        if self._columns in {"*", ""}:
            return deepcopy(row)

        columns = [col.strip() for col in self._columns.split(",") if col.strip()]
        return {column: deepcopy(row.get(column)) for column in columns}

    def _prepare_insert(self) -> List[Dict[str, Any]]:
        payloads = self._iter_payloads()
        if not payloads:
            return []

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

    def _apply_upsert(self) -> List[Dict[str, Any]]:
        payloads = self._iter_payloads()
        if not payloads:
            return []

        table_data = self._client._get_table_data(self._table_name)
        conflict_keys = self._parse_on_conflict()
        result: List[Dict[str, Any]] = []

        for payload in payloads:
            match = None
            if conflict_keys:
                for row in table_data:
                    if all(row.get(key) == payload.get(key) for key in conflict_keys):
                        match = row
                        break

            if match is not None:
                match.update(deepcopy(payload))
                result.append(match)
            else:
                new_row = deepcopy(payload)
                table_data.append(new_row)
                result.append(new_row)

        return result

    def _parse_on_conflict(self) -> List[str]:
        if not self._on_conflict:
            return []
        return [key.strip() for key in self._on_conflict.split(",") if key.strip()]

    def _iter_payloads(self) -> List[Dict[str, Any]]:
        if self._payload is None:
            return []

        if isinstance(self._payload, list):
            return [deepcopy(item) for item in self._payload]

        return [deepcopy(self._payload)]
