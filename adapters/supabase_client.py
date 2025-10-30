from functools import lru_cache
from typing import Optional
from common.config import settings

try:
    from supabase import create_client, Client  # type: ignore
except Exception:  # lib não instalada ou ambiente limitado
    Client = object  # fallback de tipo


@lru_cache(maxsize=1)
def get_supabase() -> Optional["Client"]:
    """Retorna o cliente do Supabase ou None em modo demo."""
    if settings.DEMO_MODE:
        return None
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)  # type: ignore
