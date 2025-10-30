class AppError(Exception):
    """Erro genérico do aplicativo."""

class NotFoundError(AppError):
    """Recurso não encontrado."""
