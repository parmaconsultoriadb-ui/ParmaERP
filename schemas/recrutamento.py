from pydantic import BaseModel, Field, EmailStr
from typing import Optional

# --------------------------
# Tabela: vagas
# --------------------------
class Vaga(BaseModel):
    id: Optional[int] = None
    data_de_abertura: Optional[str] = Field(None, description="DD/MM/YYYY")
    cliente: Optional[str] = None
    cargo: Optional[str] = None
    recrutador: Optional[str] = None
    status: Optional[str] = None
    atualizacao: Optional[str] = Field(None, description="DD/MM/YYYY")
    salario_1: Optional[str] = None
    salario_2: Optional[str] = None
    salario_final: Optional[str] = None
    reposicao: Optional[str] = Field(None, description="'Sim' ou vazio")
    created_at: Optional[str] = Field(None, description="DD/MM/YYYY HH:MM:SS")

# --------------------------
# Tabela: candidatos
# --------------------------
class Candidato(BaseModel):
    id: Optional[int] = None
    cliente: Optional[str] = None
    cargo: Optional[str] = None
    nome: Optional[str] = None
    telefone: Optional[str] = None
    recrutador: Optional[str] = None
    status: Optional[str] = None
    data_cadastro: Optional[str] = Field(None, description="DD/MM/YYYY")
    data_inicio: Optional[str] = Field(None, description="DD/MM/YYYY")
    atualizacao: Optional[str] = Field(None, description="DD/MM/YYYY")
