import os

class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "ParmaERP")
    ENV: str = os.getenv("ENV", "dev")

    # Supabase
    SUPABASE_URL: str | None = os.getenv("SUPABASE_URL")
    SUPABASE_KEY: str | None = os.getenv("SUPABASE_KEY")

    # Paginação padrão
    PAGE_SIZE: int = int(os.getenv("PAGE_SIZE", "50"))

    # Modo demo se não houver credenciais
    @property
    def DEMO_MODE(self) -> bool:
        return not (self.SUPABASE_URL and self.SUPABASE_KEY)

settings = Settings()
