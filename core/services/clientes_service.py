from adapters.supabase_repo import list_rows, insert_row, update_row, delete_row
from schemas.clientes import Cliente
from common.config import agora_formatado

TABLE = "clientes"

class ClientesService:
    def listar(self, page: int = 1, busca: str = None):
        try:
            page = int(page)
        except (ValueError, TypeError):
            page = 1
        if busca:
            return list_rows(TABLE, page=page, ilike=("cliente", busca), order_by="id", desc=True)
        return list_rows(TABLE, page=page, order_by="id", desc=True)

    def criar(self, data: dict):
        try:
            obj = Cliente(**data).model_dump(exclude_none=True)
            return insert_row(TABLE, obj)
        except Exception as e:
            import streamlit as st
            st.error(f"❌ Erro de validação: {e}")
            raise

    def atualizar(self, row_id: int, data: dict):
        obj = Cliente(**{**data, "id": row_id}).model_dump(exclude={"id"}, exclude_none=True)
        return update_row(TABLE, row_id, obj, id_col="id")

    def excluir(self, row_id: int):
        return delete_row(TABLE, row_id, id_col="id")
