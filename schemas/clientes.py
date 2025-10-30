from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class Cliente(BaseModel):
    id: int | None = None
    nome: str = Field(min_length=2, max_length=120)
    email: Optional[EmailStr] = None
    cidade: Optional[str] = None
    uf: Optional[str] = Field(default=None, min_length=2, max_length=2)
    telefone: Optional[str] = None
