from pydantic import BaseModel, EmailStr
from typing import Optional

class Cliente(BaseModel):
    id: Optional[int] = None
    nome: str
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None
    criado_em: Optional[str] = None
