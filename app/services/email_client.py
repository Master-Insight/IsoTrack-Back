# app\services\email_client.py
"""
Cliente simple para enviar correos usando la API de Resend.

El objetivo es cubrir los requerimientos de la Fase 2, permitiendo
enviar notificaciones sin acoplar la lógica del dominio a la librería
HTTP concreta. Si la API Key no está configurada, el envío se omite
grácilmente dejando constancia en los logs.
"""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, Optional

import httpx

from app.config.settings import settings

logger = logging.getLogger(__name__)


class EmailService:
    """Encapsula el envío de emails a través de Resend."""

    RESEND_ENDPOINT = "https://api.resend.com/emails"

    def __init__(self, api_key: Optional[str] = None) -> None:
        self.api_key = api_key or settings.RESEND_API_KEY

    async def send_email(
        self,
        *,
        to: str,
        subject: str,
        html_body: str,
        from_email: str = "InsightDev <noreply@email.insightdevs.com.ar>",  # TODO ver email: "noreply@dealerapp.ar",
    ) -> Dict[str, Any]:
        """Envía un email y devuelve la respuesta o un mensaje informativo."""

        if not self.api_key:
            logger.warning(
                "No se configuró RESEND_API_KEY. Se omite el envío de correo a %s",
                to,
            )
            return {
                "sent": False,
                "reason": "missing_api_key",
                "to": to,
            }

        payload = {
            "from": from_email,
            "to": [to],
            "subject": subject,
            "html": html_body,
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    self.RESEND_ENDPOINT,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    content=json.dumps(payload).encode("utf-8"),
                )
                response.raise_for_status()
        except httpx.HTTPStatusError as error:
            logger.exception("Error HTTP al enviar email a %s", to)
            return {
                "sent": False,
                "reason": "http_error",
                "status": error.response.status_code,
                "body": error.response.text,
            }
        except httpx.TransportError as error:
            logger.exception("No se pudo contactar a Resend para %s", to)
            return {
                "sent": False,
                "reason": "connection_error",
                "details": str(error),
            }
        except Exception as error:  # pragma: no cover - salvaguarda general
            logger.exception("Error inesperado al enviar email a %s", to)
            return {
                "sent": False,
                "reason": "unexpected_error",
                "details": str(error),
            }

        logger.info("Email enviado a %s", to)
        return {
            "sent": True,
            "status": response.status_code,
            "body": response.text,
        }


email_service = EmailService()
