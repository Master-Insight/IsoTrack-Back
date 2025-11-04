# app/modules/test/routes.py
from fastapi import APIRouter, Query

from app.libraries.utils.response_builder import ResponseBuilder
from app.services.email_client import email_service

router = APIRouter()


# 00 - Verifica conexión básica
@router.get("/")
def test_connection():
    """
    Verifica que el módulo Test esté activo.
    """
    return ResponseBuilder.success(message="DealerApp Backend activo 🚀")


# 01 - Prueba de envío de email con Resend
@router.get("/email")
async def test_email(
    to: str = Query(..., description="Correo destinatario para la prueba"),
    subject: str = Query("Prueba de envío", description="Asunto del correo"),
):
    """
    Envía un correo de prueba usando Resend y devuelve el resultado.
    Ejemplo:
    /test/email?to=tucorreo@ejemplo.com
    """
    html_body = """
    <h2>Prueba de Envío desde DealerApp</h2>
    <p>Este es un correo de prueba enviado mediante Resend API desde el backend FastAPI.</p>
    """

    result = await email_service.send_email(
        to=to,
        subject=subject,
        html_body=html_body,
    )

    if result.get("sent"):
        return ResponseBuilder.success(
            message=f"Correo enviado correctamente a {to}",
            data=result,
        )
    else:
        return ResponseBuilder.error(
            f"No se pudo enviar el correo a {to}",
            details=result,
            status_code=502,
        )
