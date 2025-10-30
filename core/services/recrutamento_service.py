import uuid
from typing import List, Dict, Any, Optional
from adapters.supabase_repo import CandidatosRepo, VagasRepo
from schemas.recrutamento import Candidato, Vaga
from common.errors import NotFoundError

class RecrutamentoService:
    def __init__(self):
        self.candidatos_repo = CandidatosRepo()
        self.vagas_repo = VagasRepo()

    # Candidatos
    def listar_candidatos(self, page: int = 1, busca: Optional[str] = None) -> List[Dict[str, Any]]:
        return self.candidatos_repo.list(page=page, search_col="nome", search=busca)

    def criar_candidato(self, data: Dict[str, Any]) -> Dict[str, Any]:
        payload = {"id": data.get("id") or f"k_{uuid.uuid4().hex[:8]}", **data}
        cand = Candidato(**payload)
        return self.candidatos_repo.insert(cand.model_dump())

    def obter_candidato(self, candidato_id: str) -> Dict[str, Any]:
        obj = self.candidatos_repo.get_by_id(candidato_id)
        if not obj:
            raise NotFoundError("Candidato não encontrado")
        return obj

    # Vagas
    def listar_vagas(self, page: int = 1, busca: Optional[str] = None) -> List[Dict[str, Any]]:
        return self.vagas_repo.list(page=page, search_col="titulo", search=busca)

    def criar_vaga(self, data: Dict[str, Any]) -> Dict[str, Any]:
        payload = {"id": data.get("id") or f"v_{uuid.uuid4().hex[:8]}", **data}
        vaga = Vaga(**payload)
        return self.vagas_repo.insert(vaga.model_dump())

    def obter_vaga(self, vaga_id: str) -> Dict[str, Any]:
        obj = self.vagas_repo.get_by_id(vaga_id)
        if not obj:
            raise NotFoundError("Vaga não encontrada")
        return obj
