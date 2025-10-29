# modules/supabase_utils.py
from typing import Any, Dict, Iterable, List, Optional
import streamlit as st
from supabase import create_client, Client

# Lazy singleton
_client: Optional[Client] = None

def get_client() -> Client:
    global _client
    if _client is None:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_ANON_KEY"]  # use SERVICE_ROLE_KEY só no backend seguro
        _client = create_client(url, key)
    return _client

def sb_listar_registros(tabela: str, filtros: Optional[Dict[str, Any]]=None) -> Iterable[Dict[str, Any]]:
    supa = get_client()
    q = supa.table(tabela).select("*")
    if filtros:
        for k, v in filtros.items():
            q = q.eq(k, v)
    data = q.execute().data or []
    for row in data:
        yield row

def sb_carregar_registro(tabela: str, filtros: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    supa = get_client()
    q = supa.table(tabela).select("*")
    for k, v in filtros.items():
        q = q.eq(k, v)
    res = q.limit(1).execute()
    rows = res.data or []
    return rows[0] if rows else None

def sb_insert(tabela: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    supa = get_client()
    res = supa.table(tabela).insert(payload).select("*").single().execute()
    return res.data

def sb_upsert_registro(tabela: str, match_campos: Dict[str, Any], payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Faz upsert com base nos campos de match (equivalente ao 'on conflict do update').
    Requer uma unique constraint que cubra os campos usados no match, OU você pode fazer
    'select → insert/update' manualmente.
    """
    supa = get_client()
    # Estratégia simples: tenta buscar → se existe, update; senão, insert
    atual = sb_carregar_registro(tabela, match_campos)
    if atual:
        # build update filter
        q = supa.table(tabela).update(payload)
        for k, v in match_campos.items():
            q = q.eq(k, v)
        res = q.select("*").single().execute()
        return res.data
    else:
        res = supa.table(tabela).insert({**match_campos, **payload}).select("*").single().execute()
        return res.data

def sb_update_by_id(tabela: str, row_id: Any, payload: Dict[str, Any], id_col: str = "id") -> Dict[str, Any]:
    supa = get_client()
    res = supa.table(tabela).update(payload).eq(id_col, row_id).select("*").single().execute()
    return res.data

def sb_delete_by_id(tabela: str, row_id: Any, id_col: str = "id") -> None:
    supa = get_client()
    supa.table(tabela).delete().eq(id_col, row_id).execute()

def resolve_logo_source(url: Optional[str]) -> str:
    return (url or "").strip()
