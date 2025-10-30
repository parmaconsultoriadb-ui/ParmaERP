from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal

class Candidato(BaseModel):
    id: str
    nome: str = Field(min_length=2, max_length=120)
    email: Optional[EmailStr] = None
    status: Literal["Novo", "Em análise", "Entrevista", "Aprovado", "Reprovado"] = "Novo"

class Vaga(BaseModel):
    id: str
    titulo: str = Field(min_length=3, max_length=140)
    status: Literal["Aberta", "Fechada", "Pausada"] = "Aberta"
