from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class Cliente(BaseModel):
    id: Optional[int] = None
    data: Optional[str] = Field(None, description="Data de cadastro (DD/MM/YYYY)")
    cliente: Optional[str] = Field(None, description="Nome ou razão social do cliente")
    nome: Optional[str] = Field(None, description="Nome do contato principal")
    cidade: Optional[str] = None
    uf: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[EmailStr] = None
    created_at: Optional[str] = Field(None, description="Data/hora de criação (DD/MM/YYYY HH:MM:SS)")
