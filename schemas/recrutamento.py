from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal

class Candidato(BaseModel):
    id: int | None = None
    cliente: str
    cargo: str
    nome: str = Field(min_length=2, max_length=120)
    telefone: Optional[str] = None
    recrutador: Optional[str] = None
    status: Literal["Enviado", "Validado", "Não validado", "Desistência"] = "Enviado"
    data_cadastro: Optional[str] = None
    data_inicio: Optional[str] = None

class Vaga(BaseModel):
    id: int | None = None
    cliente: str
    cargo: str
    recrutador: Optional[str] = None
    status: Literal["Aberta", "Ag. Inicio", "Cancelada", "Fechada", "Reaberta", "Pausada"] = "Aberta"
    data_abertura: Optional[str] = None
    atualizacao: Optional[str] = None
    salario1: Optional[str] = None
    salario2: Optional[str] = None
    salario_final: Optional[str] = None
    reposicao: Optional[str] = None
