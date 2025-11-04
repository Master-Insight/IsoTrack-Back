# app/services/whatsapp_client.py
"""Cliente HTTP simplificado para la integración de WhatsApp.

Este módulo cubre los requerimientos de la fase 3 descritos en la
documentación de arquitectura, permitiendo enviar notificaciones
automatizadas por WhatsApp sin acoplar la lógica del dominio a la
implementación específica del proveedor.
"""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from app.config.settings import settings

logger = logging.getLogger(__name__)


class WhatsAppService:
    """Encapsula el envío de mensajes de WhatsApp a través de una API HTTP."""

    def __init__(
        self,
        *,
        api_url: Optional[str] = None,
        api_token: Optional[str] = None,
        default_sender: Optional[str] = None,
        default_country_code: Optional[str] = None,
    ) -> None:
        self.api_url = api_url or settings.WHATSAPP_API_URL
        self.api_token = api_token or settings.WHATSAPP_API_TOKEN
        self.default_sender = default_sender or settings.WHATSAPP_DEFAULT_SENDER
        self.default_country_code = (
            default_country_code or settings.WHATSAPP_DEFAULT_COUNTRY_CODE
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _normalize_phone(self, phone: str) -> str:
        """Normaliza el teléfono a formato internacional."""

        if not phone:
            raise ValueError("El teléfono está vacío")

        phone = phone.strip()
        if phone.startswith("+"):
            digits = "".join(ch for ch in phone if ch.isdigit())
            return f"+{digits}" if digits else phone

        digits = "".join(ch for ch in phone if ch.isdigit())
        if not digits:
            raise ValueError("El teléfono no contiene dígitos")

        # Si se especificó un código de país por defecto, lo aplicamos.
        if self.default_country_code and not digits.startswith(
            self.default_country_code
        ):
            digits = f"{self.default_country_code}{digits.lstrip('0')}"

        return f"+{digits}"

    # ------------------------------------------------------------------
    # Operaciones públicas
    # ------------------------------------------------------------------
    def send_message(
        self,
        *,
        to: str,
        message: str,
        sender: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Envía un mensaje de WhatsApp y devuelve una respuesta normalizada."""

        if not self.api_url or not self.api_token:
            logger.warning(
                "Credenciales de WhatsApp incompletas. Se omite el envío a %s",
                to,
            )
            return {
                "sent": False,
                "reason": "missing_credentials",
                "to": to,
            }

        try:
            normalized_phone = self._normalize_phone(to)
        except ValueError as error:
            logger.error("No se pudo normalizar el teléfono %s: %s", to, error)
            return {
                "sent": False,
                "reason": "invalid_phone",
                "details": str(error),
            }

        payload: Dict[str, Any] = {
            "to": normalized_phone,
            "message": message,
        }

        if sender or self.default_sender:
            payload["sender"] = sender or self.default_sender

        if metadata:
            payload["metadata"] = metadata

        request = Request(
            self.api_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_token}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urlopen(request, timeout=10) as response:
                body = response.read().decode("utf-8")
                logger.info("Mensaje de WhatsApp enviado a %s", normalized_phone)
                return {
                    "sent": True,
                    "status": response.status,
                    "body": body,
                }
        except HTTPError as error:
            logger.exception(
                "Error HTTP al enviar mensaje de WhatsApp a %s", normalized_phone
            )
            return {
                "sent": False,
                "reason": "http_error",
                "status": error.code,
                "body": error.read().decode("utf-8") if error.fp else None,
            }
        except URLError as error:
            logger.exception(
                "No se pudo contactar al proveedor de WhatsApp para %s",
                normalized_phone,
            )
            return {
                "sent": False,
                "reason": "connection_error",
                "details": str(error.reason),
            }
        except Exception as error:  # pragma: no cover - salvaguarda general
            logger.exception(
                "Error inesperado al enviar mensaje de WhatsApp a %s",
                normalized_phone,
            )
            return {
                "sent": False,
                "reason": "unexpected_error",
                "details": str(error),
            }


whatsapp_service = WhatsAppService()
