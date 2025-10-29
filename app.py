import streamlit as st
from modules.supabase_utils import get_client, sb_listar_registros, sb_insert

st.set_page_config(page_title="Parma Consultoria", layout="wide")

# teste rápido de conexão
@st.cache_data(ttl=30)
def ping_supabase():
    try:
        supa = get_client()
        # faz uma consulta simples (ajuste para uma tabela existente, ex.: clientes)
        rows = list(sb_listar_registros("clientes"))
        return True, len(rows)
    except Exception as e:
        return False, str(e)

ok, info = ping_supabase()
if ok:
    st.success(f"✅ Conectado ao Supabase. Registros em 'clientes': {info}")
else:
    st.error(f"❌ Falha ao conectar Supabase: {info}")
