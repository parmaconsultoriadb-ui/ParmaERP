from adapters.supabase_repo import list_rows, insert_row, get_row, update_row, delete_row
from schemas.recrutamento import Vaga, Candidato
from common.config import agora_formatado

TABLE_VAGAS = "vagas"
TABLE_CANDIDATOS = "candidatos"

class RecrutamentoService:
    # ---------------------------------------
    # VAGAS
    # ---------------------------------------
    def listar_vagas(self, page: int = 1, busca: str = None):
        try:
            page = int(page)
        except (ValueError, TypeError):
            page = 1
        if busca:
            return list_rows(TABLE_VAGAS, page=page, ilike=("titulo", busca), order_by="id", desc=True)
        return list_rows(TABLE_VAGAS, page=page, order_by="id", desc=True)

    def criar_vaga(self, data: dict):
        obj = Vaga(**data).model_dump(exclude_none=True)
        obj["criado_em"] = agora_formatado()
        return insert_row(TABLE_VAGAS, obj)

    def atualizar_vaga(self, row_id: int, data: dict):
        obj = Vaga(**{**data, "id": row_id}).model_dump(exclude={"id"}, exclude_none=True)
        return update_row(TABLE_VAGAS, row_id, obj, id_col="id")

    def excluir_vaga(self, row_id: int):
        return delete_row(TABLE_VAGAS, row_id, id_col="id")

    # ---------------------------------------
    # CANDIDATOS
    # ---------------------------------------
    def listar_candidatos(self, page: int = 1, busca: str = None):
        try:
            page = int(page)
        except (ValueError, TypeError):
            page = 1
        if busca:
            return list_rows(TABLE_CANDIDATOS, page=page, ilike=("nome", busca), order_by="id", desc=True)
        return list_rows(TABLE_CANDIDATOS, page=page, order_by="id", desc=True)

    def criar_candidato(self, data: dict):
        obj = Candidato(**data).model_dump(exclude_none=True)
        obj["criado_em"] = agora_formatado()
        return insert_row(TABLE_CANDIDATOS, obj)

    def atualizar_candidato(self, row_id: int, data: dict):
        obj = Candidato(**{**data, "id": row_id}).model_dump(exclude={"id"}, exclude_none=True)
        return update_row(TABLE_CANDIDATOS, row_id, obj, id_col="id")

    def excluir_candidato(self, row_id: int):
        return delete_row(TABLE_CANDIDATOS, row_id, id_col="id")
