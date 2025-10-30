from adapters.supabase_repo import insert_row, list_rows
from datetime import datetime
import streamlit as st

def registrar_log(aba, acao, item_id=None, campo=None, valor_anterior=None, valor_novo=None, detalhe=None):
    novo_log = {
        "datahora": agora_formatado(),
        "usuario": st.session_state.get("usuario", "admin"),
        "aba": str(aba),
        "acao": str(acao),
        "item_id": str(item_id) if item_id else None,
        "campo": str(campo) if campo else None,
        "valor_anterior": str(valor_anterior) if valor_anterior else None,
        "valor_novo": str(valor_novo) if valor_novo else None,
        "detalhe": str(detalhe) if detalhe else None
    }
    novo_log = {k: v for k, v in novo_log.items() if v is not None}

    try:
        insert_row("logs", novo_log)
    except Exception as e:
        st.warning(f"⚠️ Falha ao registrar log no Supabase: {e}")

def carregar_logs(page: int = 1):
    return list_rows("logs", page=page, order_by="datahora", desc=True)
