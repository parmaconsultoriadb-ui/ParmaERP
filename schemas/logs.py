from pydantic import BaseModel
from typing import Optional

class Log(BaseModel):
    id: int | None = None
    datahora: str
    usuario: str
    aba: str
    acao: str
    item_id: Optional[str] = None
    campo: Optional[str] = None
    valor_anterior: Optional[str] = None
    valor_novo: Optional[str] = None
    detalhe: Optional[str] = None
