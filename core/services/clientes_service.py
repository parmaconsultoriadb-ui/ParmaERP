from typing import List, Dict, Any, Optional
from adapters.supabase_repo import list_rows, insert_row, get_row, update_row, delete_row
from schemas.clientes import Cliente

TABLE = "clientes"

class ClientesService:
    def listar(self, page: int = 1, busca: Optional[str] = None) -> List[Dict[str, Any]]:
        try:
            page = int(page)
        except (ValueError, TypeError):
            page = 1  # fallback seguro

        if busca:
            return list_rows(TABLE, page=page, ilike=("nome", busca), order_by="id", desc=True)
        return list_rows(TABLE, page=page, order_by="id", desc=True)

    def criar(self, data: Dict[str, Any]) -> Dict[str, Any]:
        obj = Cliente(**data).model_dump(exclude_none=True)
        return insert_row(TABLE, obj)

    def obter(self, row_id: int) -> Optional[Dict[str, Any]]:
        return get_row(TABLE, row_id, id_col="id")

    def atualizar(self, row_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        obj = Cliente(**{**data, "id": row_id}).model_dump(exclude={"id"}, exclude_none=True)
        return update_row(TABLE, row_id, obj, id_col="id")

    def excluir(self, row_id: int) -> None:
        delete_row(TABLE, row_id, id_col="id")
