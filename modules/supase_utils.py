# modules/supabase_utils.py
from supabase import create_client
import streamlit as st


@st.cache_resource
def get_client():
    """Retorna o cliente do Supabase com base nas chaves do secrets.toml"""
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_ANON_KEY"]
    return create_client(url, key)


def sb_listar_registros(tabela):
    """Lista todos os registros de uma tabela"""
    supa = get_client()
    res = supa.table(tabela).select("*").execute()
    return res.data or []


def sb_insert(tabela, payload):
    """Insere um novo registro"""
    supa = get_client()
    res = supa.table(tabela).insert(payload).execute()
    return res.data[0] if res.data else {}


def sb_update_by_id(tabela, id_registro, payload):
    """Atualiza um registro pelo ID"""
    supa = get_client()
    supa.table(tabela).update(payload).eq("id", id_registro).execute()
    return True


def sb_delete_by_id(tabela, id_registro):
    """Deleta um registro pelo ID"""
    supa = get_client()
    supa.table(tabela).delete().eq("id", id_registro).execute()
    return True
