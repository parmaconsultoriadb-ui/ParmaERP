import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

# ===========================================
# CARREGAMENTO DE VARIÁVEIS DE AMBIENTE (.env)
# ===========================================
load_dotenv()

class Settings:
    """Configurações globais do sistema (Supabase, timezone, etc)."""

    # Supabase
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")

    # Configurações gerais
    APP_NAME: str = "Parma ERP"
    TIMEZONE: timezone = timezone(timedelta(hours=-3))  # GMT-3
    DATE_FORMAT: str = "%d/%m/%Y"
    DATETIME_FORMAT: str = "%d/%m/%Y %H:%M:%S"

settings = Settings()

# ===========================================
# FUNÇÕES DE DATA / HORA
# ===========================================
def agora_datetime():
    """Retorna datetime com timezone GMT-3."""
    return datetime.now(settings.TIMEZONE)

def agora_formatado() -> str:
    """Retorna string de data/hora atual formatada (DD/MM/YYYY HH:MM:SS)."""
    return agora_datetime().strftime(settings.DATETIME_FORMAT)

def hoje_formatado() -> str:
    """Retorna string com a data atual formatada (DD/MM/YYYY)."""
    return agora_datetime().strftime(settings.DATE_FORMAT)
