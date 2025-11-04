# app/libraries/exceptions/app_exceptions.py
import inspect


class AppError(Exception):
    """Excepción base para la app, con detección automática del origen."""

    def __init__(
        self, message: str, status_code: int = 500, details: dict | None = None
    ):
        # Guarda el mensaje y código HTTP
        self.message = message
        self.status_code = status_code
        self.details = details or {}

        # Detecta automáticamente de dónde se lanzó
        frame = inspect.stack()[2]
        self.origin = f"{frame.function}() in {frame.filename.split('/')[-1]}"

        super().__init__(self.message)

    def to_dict(self):
        return {
            "success": False,
            "error": self.message,
            "details": self.details,
            "origin": self.origin,
            "status_code": self.status_code,
        }


class ValidationError(AppError):
    """Error de validación (inputs incorrectos)."""

    def __init__(self, message="Datos inválidos", details=None):
        super().__init__(message, status_code=400, details=details)


class AuthError(AppError):
    """Error de autenticación o permisos."""

    def __init__(self, message="No autorizado", details=None):
        super().__init__(message, status_code=401, details=details)


class NotFoundError(AppError):
    """Recurso no encontrado."""

    def __init__(self, message="Recurso no encontrado", details=None):
        super().__init__(message, status_code=404, details=details)


class DataAccessError(AppError):
    """Error relacionado con la comunicación con la base de datos."""

    def __init__(self, message="Error de acceso a datos", details=None):
        super().__init__(message, status_code=500, details=details)


class ServiceError(AppError):
    """Error genérico para la capa de servicios."""

    def __init__(self, message="Error interno del servicio", details=None):
        super().__init__(message, status_code=500, details=details)
