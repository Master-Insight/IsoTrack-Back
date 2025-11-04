# app/config/settings.py
from pydantic import Extra
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # --- DB ---
    SUPABASE_URL: str
    SUPABASE_KEY: str

    # --- Logging ---
    LOG_LEVEL: str = "INFO"
    LOG_JSON_FORMAT: bool = False
    LOG_FILE_PATH: str | None = None
    LOG_FILE_RETENTION: int = 7
    ENVIRONMENT: str = "development"

    # --- Integraciones ---
    RESEND_API_KEY: str | None = None

    # --- Defaults multiempresa ---
    DEFAULT_COMPANY_ID: str | None = None

    # --- Integraciones externas ---
    WHATSAPP_API_URL: str | None = None
    WHATSAPP_API_TOKEN: str | None = None
    WHATSAPP_DEFAULT_SENDER: str | None = None
    WHATSAPP_DEFAULT_COUNTRY_CODE: str | None = None

    class Config:
        env_file = ".env"
        extra = Extra.ignore  # 👈 ignora variables adicionales


# Instancia global
settings = Settings()
