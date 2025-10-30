from typing import List, Dict, Any, Optional
from adapters.supabase_repo import list_rows, insert_row, get_row, update_row, delete_row
from schemas.comercial import Oportunidade

TABLE = "comercial"

class ComercialService:
    def listar(self, page: int = 1, busca_status: Optional[str] = None) -> List[Dict[str, Any]]:
        if busca_status:
            return list_rows(TABLE, page=page, where={"status": busca_status}, order_by="id", desc=True)
        return list_rows(TABLE, page=page, order_by="id", desc=True)

    def criar(self, data: Dict[str, Any]) -> Dict[str, Any]:
        obj = Oportunidade(**data).model_dump(exclude_none=True)
        return insert_row(TABLE, obj)

    def mover_status(self, row_id: int, novo_status: str) -> Dict[str, Any]:
        return update_row(TABLE, row_id, {"status": novo_status}, id_col="id")

    def atualizar(self, row_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        return update_row(TABLE, row_id, data, id_col="id")

    def excluir(self, row_id: int) -> None:
        delete_row(TABLE, row_id, id_col="id")
