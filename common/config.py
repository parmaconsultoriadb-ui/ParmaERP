import os
from datetime import datetime, timedelta, timezone

# =============================================
# CONFIGURAÇÃO DE FORMATAÇÃO DE DATA/HORA
# =============================================

GMT_MINUS_3 = timezone(timedelta(hours=-3))

DATE_FORMAT = "%d/%m/%Y"
DATETIME_FORMAT = "%d/%m/%Y %H:%M:%S"

def agora_formatado() -> str:
    """Retorna a data/hora atual formatada no padrão DD/MM/YYYY HH:MM:SS com fuso GMT-3"""
    agora = datetime.now(GMT_MINUS_3)
    return agora.strftime(DATETIME_FORMAT)

def agora_datetime():
    """Retorna o objeto datetime com timezone GMT-3"""
    return datetime.now(GMT_MINUS_3)

class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "ParmaERP")
    ENV: str = os.getenv("ENV", "dev")

    SUPABASE_URL: str | None = os.getenv("SUPABASE_URL")
    SUPABASE_KEY: str | None = os.getenv("SUPABASE_KEY")

    PAGE_SIZE: int = int(os.getenv("PAGE_SIZE", "50"))

    @property
    def DEMO_MODE(self) -> bool:
        # Forçamos Supabase; se faltar credencial, mostramos erro na UI
        return not (self.SUPABASE_URL and self.SUPABASE_KEY)

settings = Settings()
