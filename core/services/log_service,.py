from adapters.supabase_repo import insert_row, list_rows
from datetime import datetime
import streamlit as st

def registrar_log(aba, acao, item_id=None, campo=None, valor_anterior=None, valor_novo=None, detalhe=None):
    novo_log = {
        "datahora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "usuario": st.session_state.get("usuario", "admin"),
        "aba": aba, "acao": acao,
        "item_id": item_id, "campo": campo,
        "valor_anterior": valor_anterior, "valor_novo": valor_novo,
        "detalhe": detalhe
    }
    insert_row("logs", novo_log)

def carregar_logs(page: int = 1):
    return list_rows("logs", page=page, order_by="datahora", desc=True)
