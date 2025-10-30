import os

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
