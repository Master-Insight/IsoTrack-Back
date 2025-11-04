# app/services/supabase_client.py
"""Singleton del cliente de Supabase usado en toda la aplicación."""

from supabase import Client, create_client

from app.config.settings import settings

url: str = settings.SUPABASE_URL
key: str = settings.SUPABASE_KEY

supabase: Client = create_client(url, key)
