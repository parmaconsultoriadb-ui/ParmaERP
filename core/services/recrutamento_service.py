from typing import Optional, Dict, Any, List
from adapters.supabase_repo import list_rows, insert_row, update_row, delete_row
from schemas.recrutamento import Vaga, Candidato
from common.config import agora_formatado, agora_datetime, settings

TABLE_VAGAS = "vagas"
TABLE_CANDIDATOS = "candidatos"

def _hoje_ddmmyyyy() -> str:
    return agora_datetime().strftime(settings.DATE_FORMAT)

class RecrutamentoService:
    # -------------------------
    # VAGAS
    # -------------------------
    def listar_vagas(self, page: int = 1, busca: Optional[str] = None) -> List[Dict[str, Any]]:
        try:
            page = int(page)
        except (ValueError, TypeError):
            page = 1
        if busca:
            return list_rows(TABLE_VAGAS, page=page, ilike=("cargo", busca), order_by="id", desc=True)
        return list_rows(TABLE_VAGAS, page=page, order_by="id", desc=True)

    def criar_vaga(self, data: Dict[str, Any]) -> Dict[str, Any]:
        base = {
            "data_de_abertura": _hoje_ddmmyyyy(),
            "atualizacao": _hoje_ddmmyyyy(),
            "created_at": agora_datetime().strftime(settings.DATETIME_FORMAT),
        }
        obj = Vaga(**{**base, **data}).model_dump(exclude_none=True)
        return insert_row(TABLE_VAGAS, obj)

    def atualizar_vaga(self, row_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        obj = Vaga(**{**data, "id": row_id}).model_dump(exclude={"id"}, exclude_none=True)
        return update_row(TABLE_VAGAS, row_id, obj, id_col="id")

    def excluir_vaga(self, row_id: int) -> None:
        delete_row(TABLE_VAGAS, row_id, id_col="id")

    # -------------------------
    # CANDIDATOS
    # -------------------------
    def listar_candidatos(self, page: int = 1, busca: Optional[str] = None) -> List[Dict[str, Any]]:
        try:
            page = int(page)
        except (ValueError, TypeError):
            page = 1
        if busca:
            return list_rows(TABLE_CANDIDATOS, page=page, ilike=("nome", busca), order_by="id", desc=True)
        return list_rows(TABLE_CANDIDATOS, page=page, order_by="id", desc=True)

    def criar_candidato(self, data: Dict[str, Any]) -> Dict[str, Any]:
        base = {
            "data_cadastro": _hoje_ddmmyyyy(),
            "atualizacao": agora_datetime().strftime(settings.DATETIME_FORMAT),
        }
        obj = Candidato(**{**base, **data}).model_dump(exclude_none=True)
        return insert_row(TABLE_CANDIDATOS, obj)

    def atualizar_candidato(self, row_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        obj = Candidato(**{**data, "id": row_id}).model_dump(exclude={"id"}, exclude_none=True)
        return update_row(TABLE_CANDIDATOS, row_id, obj, id_col="id")

    def excluir_candidato(self, row_id: int) -> None:
        delete_row(TABLE_CANDIDATOS, row_id, id_col="id")
