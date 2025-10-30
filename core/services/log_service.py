from adapters.supabase_repo import insert_row, list_rows
from common.config import agora_datetime, settings

TABLE = "logs"

def registrar_log(aba: str, acao: str, item_id=None, campo=None, valor_anterior=None, valor_novo=None, detalhe=None):
    novo_log = {
        "datahora": agora_datetime().strftime(settings.DATETIME_FORMAT),
        "aba": aba,
        "acao": acao,
        "item_id": item_id,
        "campo": campo,
        "valor_anterior": valor_anterior,
        "valor_novo": valor_novo,
        "detalhe": detalhe,
    }
    try:
        insert_row(TABLE, novo_log)
    except Exception as e:
        import streamlit as st
        st.warning(f"⚠️ Falha ao registrar log no Supabase: {e}")

def carregar_logs(page: int = 1):
    return list_rows(TABLE, page=page, order_by="datahora", desc=True)
