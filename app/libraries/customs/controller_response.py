# app/libraries/customs/controller_base.py
from typing import TypeVar, Generic, Any

from app.libraries.utils.response_builder import ResponseBuilder
from app.libraries.utils.response_models import ApiResponse

T = TypeVar("T")  # Modelo de salida (por ejemplo, Product)
C = TypeVar("C")  # Modelo de creación (por ejemplo, ProductCreate)


class ResponseController(Generic[T, C]):
    """
    Controlador genérico con manejo estándar de errores y operaciones CRUD básicas.
    Los controladores específicos (como ProductController) heredan de esta clase.
    """

    def __init__(self, service: Any):
        self.service = service

    def list_all(self) -> ApiResponse[Any]:
        """Obtiene todos los registros."""
        return ResponseBuilder.success(self.service.list_all())

    def get_by_id(self, item_id: int) -> ApiResponse[Any]:
        """Obtiene un registro por ID."""
        item = self.service.get_by_id(item_id)
        return ResponseBuilder.success(item)

    def create(self, data: C) -> ApiResponse[Any]:
        """Crea un nuevo registro."""
        payload = (
            data.model_dump(exclude_unset=True)
            if hasattr(data, "model_dump")
            else data.dict()
        )
        created = self.service.create(payload)
        return ResponseBuilder.success(created, "Registro creado correctamente")

    def update(self, item_id: int, data: Any) -> ApiResponse[Any]:
        """Actualiza un registro existente."""
        payload = (
            data.model_dump(exclude_unset=True) if hasattr(data, "model_dump") else data
        )
        updated = self.service.update(item_id, payload)
        return ResponseBuilder.success(updated, "Registro actualizado correctamente")

    def delete(self, item_id: int) -> ApiResponse[Any]:
        """Elimina un registro."""
        result = self.service.delete(item_id)
        message = (
            result.get("message")
            if isinstance(result, dict)
            else f"Registro {item_id} eliminado correctamente"
        )
        return ResponseBuilder.success(result, message)
