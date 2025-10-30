from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class Cliente(BaseModel):
    id: str
    nome: str = Field(min_length=2, max_length=120)
    email: Optional[EmailStr] = None
    cnpj: Optional[str] = Field(default=None, min_length=14, max_length=14)
