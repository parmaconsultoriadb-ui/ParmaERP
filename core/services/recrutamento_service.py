from typing import Optional, Dict, Any, List
from adapters.supabase_repo import list_rows, insert_row, update_row, delete_row
from schemas.recrutamento import Vaga, Candidato
from common.config import agora_formatado, agora_datetime, settings

TABLE_VAGAS = "vagas"
TABLE_CANDIDATOS = "candidatos"

def _hoje_ddmmyyyy() -> str:
    return agora_datetime().strftime(settings.DATE_FORMAT)

class RecrutamentoService:
    def listar_vagas(self, page: int = 1, busca: Optional[str] = None):
        if busca:
            return list_rows(TABLE_VAGAS, page=page, ilike=("cliente", busca), order_by="id", desc=True)
        return list_rows(TABLE_VAGAS, page=page, order_by="id", desc=True)

    def criar_vaga(self, data: dict):
        obj = Vaga(**data).model_dump(exclude_none=True)
        obj["data_de_abertura"] = _hoje_ddmmyyyy()
        obj["atualizacao"] = agora_datetime().strftime(settings.DATETIME_FORMAT)
        return insert_row(TABLE_VAGAS, obj)

    def listar_candidatos(self, page: int = 1, busca_nome: Optional[str] = None):
        if busca_nome:
            return list_rows(TABLE_CANDIDATOS, page=page, ilike=("nome", busca_nome), order_by="id", desc=True)
        return list_rows(TABLE_CANDIDATOS, page=page, order_by="id", desc=True)

    def criar_candidato(self, data: dict):
        obj = Candidato(**data).model_dump(exclude_none=True)
        obj["data_cadastro"] = _hoje_ddmmyyyy()
        obj["atualizacao"] = agora_datetime().strftime(settings.DATETIME_FORMAT)
        return insert_row(TABLE_CANDIDATOS, obj)
