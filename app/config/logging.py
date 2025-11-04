# app\config\logging.py
"""Configuración centralizada y avanzada de logging para la aplicación."""

from __future__ import annotations

import json
import logging
from contextvars import ContextVar
from logging.config import dictConfig
from typing import Any, Dict, Iterable, MutableMapping

from app.config.settings import settings

_request_id_ctx: ContextVar[str] = ContextVar("request_id", default="-")
_user_id_ctx: ContextVar[str] = ContextVar("user_id", default="-")


class ContextFilter(logging.Filter):
    """Agrega metadatos de contexto (request y usuario) a cada registro."""

    def filter(self, record: logging.LogRecord) -> bool:  # noqa: D401 - heredado
        record.request_id = _request_id_ctx.get()
        record.user_id = _user_id_ctx.get()
        record.environment = settings.ENVIRONMENT
        return True


class JsonFormatter(logging.Formatter):
    """Formatter que serializa el registro a JSON estructurado."""

    def format(self, record: logging.LogRecord) -> str:
        base: Dict[str, Any] = {
            "timestamp": self.formatTime(record, datefmt="%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "request_id": getattr(record, "request_id", "-"),
            "user_id": getattr(record, "user_id", "-"),
            "environment": getattr(record, "environment", settings.ENVIRONMENT),
        }

        extra_keys = set(record.__dict__.keys()) - {
            "name",
            "msg",
            "args",
            "levelname",
            "levelno",
            "pathname",
            "filename",
            "module",
            "exc_info",
            "exc_text",
            "stack_info",
            "lineno",
            "funcName",
            "created",
            "msecs",
            "relativeCreated",
            "thread",
            "threadName",
            "processName",
            "process",
            "request_id",
            "user_id",
            "environment",
        }

        for key in extra_keys:
            value = record.__dict__[key]
            if isinstance(value, (str, int, float, bool)) or value is None:
                base[key] = value
            else:
                base[key] = self._safe_serialize(value)

        if record.exc_info:
            base["exception"] = self.formatException(record.exc_info)

        return json.dumps(base, ensure_ascii=False)

    @staticmethod
    def _safe_serialize(value: Any) -> Any:
        try:
            json.dumps(value)
        except TypeError:
            return repr(value)
        return value


def set_request_id(request_id: str | None) -> None:
    """Guarda el identificador de petición en el contexto actual."""

    _request_id_ctx.set(request_id or "-")


def set_user_id(user_id: str | None) -> None:
    """Guarda el identificador de usuario en el contexto actual."""

    _user_id_ctx.set(user_id or "-")


def clear_logging_context() -> None:
    """Limpia los valores de contexto para la siguiente petición."""

    _request_id_ctx.set("-")
    _user_id_ctx.set("-")


def get_request_id() -> str:
    """Obtiene el identificador de petición activo."""

    return _request_id_ctx.get()


def get_user_id() -> str:
    """Obtiene el identificador de usuario asociado al contexto actual."""

    return _user_id_ctx.get()


def _build_handlers(formatter: str, filters: Iterable[str]) -> Dict[str, Any]:
    handlers: Dict[str, Any] = {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": formatter,
            "filters": list(filters),
            "stream": "ext://sys.stdout",
        }
    }

    if settings.LOG_FILE_PATH:
        handlers["file"] = {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": formatter,
            "filters": list(filters),
            "filename": settings.LOG_FILE_PATH,
            "when": "midnight",
            "backupCount": settings.LOG_FILE_RETENTION,
            "encoding": "utf-8",
        }

    return handlers


def _handler_names(handlers: MutableMapping[str, Any]) -> list[str]:
    return list(handlers.keys())


def build_logging_config() -> Dict[str, Any]:
    """Genera el diccionario de configuración dinámicamente."""

    formatter = "json" if settings.LOG_JSON_FORMAT else "console"
    handlers = _build_handlers(formatter=formatter, filters=["context"])

    return {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {
            "context": {"()": ContextFilter},
        },
        "formatters": {
            "console": {
                "format": (
                    "%(asctime)s | %(levelname)s | %(environment)s | %(name)s | "
                    "req=%(request_id)s | user=%(user_id)s | %(message)s"
                ),
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "json": {
                "()": JsonFormatter,
            },
        },
        "handlers": handlers,
        "root": {
            "handlers": _handler_names(handlers),
            "level": settings.LOG_LEVEL,
        },
        "loggers": {
            "uvicorn": {
                "handlers": _handler_names(handlers),
                "level": settings.LOG_LEVEL,
                "propagate": False,
            },
            "uvicorn.error": {
                "handlers": _handler_names(handlers),
                "level": settings.LOG_LEVEL,
                "propagate": False,
            },
            "uvicorn.access": {
                "handlers": _handler_names(handlers),
                "level": "INFO",
                "propagate": False,
            },
        },
    }


def setup_logging() -> None:
    """Inicializa la configuración de logging."""
    dictConfig(build_logging_config())
    logging.getLogger(__name__).debug("Logging configurado correctamente")
