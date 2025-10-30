from pydantic import BaseModel, Field
from typing import Literal

class Oportunidade(BaseModel):
    id: str
    cliente_id: str
    valor: float = Field(ge=0)
    fase: Literal["Lead", "Qualificação", "Proposta", "Fechamento", "Ganho", "Perdido"] = "Lead"
