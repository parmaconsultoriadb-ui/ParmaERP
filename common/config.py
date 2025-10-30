import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()

class Settings:
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    APP_NAME: str = "Parma ERP"
    TIMEZONE: timezone = timezone(timedelta(hours=-3))  # GMT-3
    DATE_FORMAT: str = "%d/%m/%Y"
    DATETIME_FORMAT: str = "%d/%m/%Y %H:%M:%S"
    PAGE_SIZE: int = 20

settings = Settings()

def agora_datetime():
    return datetime.now(settings.TIMEZONE)

def agora_formatado() -> str:
    return agora_datetime().strftime(settings.DATETIME_FORMAT)

def hoje_formatado() -> str:
    return agora_datetime().strftime(settings.DATE_FORMAT)
