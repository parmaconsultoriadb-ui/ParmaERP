from functools import lru_cache
from typing import Optional
from common.config import settings

try:
    from supabase import create_client, Client  # type: ignore
except Exception:
    Client = object  # fallback de tipo

@lru_cache(maxsize=1)
def get_supabase() -> "Client":
    if settings.DEMO_MODE:
        raise RuntimeError("Credenciais do Supabase ausentes. Defina SUPABASE_URL e SUPABASE_KEY.")
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)  # type: ignore
