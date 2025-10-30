import uuid
from typing import List, Dict, Any, Optional
from adapters.supabase_repo import ComercialRepo
from schemas.comercial import Oportunidade
from common.errors import NotFoundError

class ComercialService:
    def __init__(self):
        self.repo = ComercialRepo()

    def listar_oportunidades(self, page: int = 1, busca: Optional[str] = None) -> List[Dict[str, Any]]:
        # busca por fase
        return self.repo.list(page=page, search_col="fase", search=busca or None)

    def criar_oportunidade(self, data: Dict[str, Any]) -> Dict[str, Any]:
        payload = {"id": data.get("id") or f"o_{uuid.uuid4().hex[:8]}", **data}
        opp = Oportunidade(**payload)
        return self.repo.insert(opp.model_dump())

    def obter_oportunidade(self, opp_id: str) -> Dict[str, Any]:
        obj = self.repo.get_by_id(opp_id)
        if not obj:
            raise NotFoundError("Oportunidade não encontrada")
        return obj
