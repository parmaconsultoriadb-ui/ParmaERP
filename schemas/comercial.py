from pydantic import BaseModel, Field
from typing import Literal, Optional

StatusFunil = Literal["Prospect", "Lead Qualificado", "Negociação",
                      "Proposta Enviada", "Contrato Enviado", "Negócio Fechado", "Declinado"]

class Oportunidade(BaseModel):
    id: int | None = None
    data: Optional[str] = None
    cliente: str
    cidade: Optional[str] = None
    uf: Optional[str] = None
    nome: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    produto: Optional[str] = None
    canal: Optional[str] = None
    status: StatusFunil = "Prospect"
    observacoes: Optional[str] = ""
    pagamento: Optional[str] = ""
    contrato_enviado: Optional[str] = ""
    contrato_assinado: Optional[str] = ""
    pag1_efetivado: Optional[str] = ""
    pag2_efetivado: Optional[str] = ""
