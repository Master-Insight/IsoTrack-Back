# app/libraries/customs/controller_base.py
from fastapi import HTTPException
from typing import TypeVar, Generic, List, Optional, Any, Dict, Type

T = TypeVar("T")  # Modelo de salida (por ejemplo, Product)
C = TypeVar("C")  # Modelo de creación (por ejemplo, ProductCreate)

class CustomController(Generic[T, C]):
    """
    Controlador genérico con manejo estándar de errores y operaciones CRUD básicas.
    Los controladores específicos (como ProductController) heredan de esta clase.
    """

    def __init__(self, service: Any):
        self.service = service

    def list_all(self) -> List[T]:
        """Obtiene todos los registros."""
        try:
            return self.service.list_all()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al listar: {str(e)}")

    def get_by_id(self, item_id: int) -> Optional[T]:
        """Obtiene un registro por ID."""
        try:
            item = self.service.get_by_id(item_id)
            if not item:
                raise HTTPException(status_code=404, detail=f"Registro con ID {item_id} no encontrado")
            return item
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener registro: {str(e)}")

    def create(self, data: C) -> T:
        """Crea un nuevo registro."""
        try:
            return self.service.create(data.dict())
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al crear registro: {str(e)}")

    def update(self, item_id: int, data: Dict[str, Any]) -> T:
        """Actualiza un registro existente."""
        try:
            updated = self.service.update(item_id, data)
            if not updated:
                raise HTTPException(status_code=404, detail=f"Registro con ID {item_id} no encontrado")
            return updated
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al actualizar registro: {str(e)}")

    def delete(self, item_id: int) -> Dict[str, Any]:
        """Elimina un registro."""
        try:
            success = self.service.delete(item_id)
            if not success:
                raise HTTPException(status_code=404, detail=f"Registro con ID {item_id} no encontrado")
            return {"message": f"Registro {item_id} eliminado correctamente"}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al eliminar registro: {str(e)}")
