from typing import List, Dict, Any, Optional
from adapters.supabase_repo import list_rows, insert_row, get_row, update_row, delete_row
from schemas.recrutamento import Candidato, Vaga

T_VAGAS = "vagas"
T_CANDIDATOS = "candidatos"

class RecrutamentoService:
    # Vagas
    def vagas_listar(self, page: int = 1, busca_cliente: Optional[str] = None) -> List[Dict[str, Any]]:
        if busca_cliente:
            return list_rows(T_VAGAS, page=page, ilike=("cliente", busca_cliente), order_by="id", desc=True)
        return list_rows(T_VAGAS, page=page, order_by="id", desc=True)

    def vaga_criar(self, data: Dict[str, Any]) -> Dict[str, Any]:
        obj = Vaga(**data).model_dump(exclude_none=True)
        return insert_row(T_VAGAS, obj)

    def vaga_atualizar(self, row_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        return update_row(T_VAGAS, row_id, data, id_col="id")

    def vaga_excluir(self, row_id: int) -> None:
        delete_row(T_VAGAS, row_id, id_col="id")

    # Candidatos
    def candidatos_listar(self, page: int = 1, busca_nome: Optional[str] = None) -> List[Dict[str, Any]]:
        if busca_nome:
            return list_rows(T_CANDIDATOS, page=page, ilike=("nome", busca_nome), order_by="id", desc=True)
        return list_rows(T_CANDIDATOS, page=page, order_by="id", desc=True)

    def candidato_criar(self, data: Dict[str, Any]) -> Dict[str, Any]:
        obj = Candidato(**data).model_dump(exclude_none=True)
        return insert_row(T_CANDIDATOS, obj)

    def candidato_atualizar(self, row_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        return update_row(T_CANDIDATOS, row_id, data, id_col="id")

    def candidato_excluir(self, row_id: int) -> None:
        delete_row(T_CANDIDATOS, row_id, id_col="id")
