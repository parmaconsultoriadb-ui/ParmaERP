import streamlit as st
from modules.supabase_utils import (
    sb_listar_registros,
    sb_insert,
    sb_delete_by_id
)
import pandas as pd
import datetime as dt


def registrar_log(usuario, aba, acao, detalhe=""):
    """Função auxiliar para gravar logs diretamente no Supabase."""
    log = {
        "datahora": str(dt.datetime.now()),
        "usuario": usuario,
        "aba": aba,
        "acao": acao,
        "detalhe": detalhe,
    }
    sb_insert("logs", log)


def tela_logs():
    st.title("📜 Logs do Sistema")
    st.caption("Registro de atividades e alterações no sistema")

    # --- Carregar registros
    registros = list(sb_listar_registros("logs"))
    df = pd.DataFrame(registros)

    if st.button("🔄 Atualizar"):
        st.rerun()

    if df.empty:
        st.info("Nenhum log registrado até o momento.")
        return

    # Conversão de data/hora
    if "datahora" in df.columns:
        df["datahora"] = pd.to_datetime(df["datahora"], errors="coerce")

    # --- Filtros
    col1, col2 = st.columns(2)
    with col1:
        usuarios = ["Todos"] + sorted(df["usuario"].dropna().unique().tolist())
        usuario_filtro = st.selectbox("👤 Usuário", options=usuarios)
    with col2:
        abas = ["Todos"] + sorted(df["aba"].dropna().unique().tolist())
        aba_filtro = st.selectbox("📂 Aba", options=abas)

    if usuario_filtro != "Todos":
        df = df[df["usuario"] == usuario_filtro]
    if aba_filtro != "Todos":
        df = df[df["aba"] == aba_filtro]

    # --- Ordenar logs recentes primeiro
    df = df.sort_values("datahora", ascending=False)

    # --- Exibição
    st.dataframe(
        df[["datahora", "usuario", "aba", "acao", "detalhe"]],
        use_container_width=True,
        hide_index=True,
    )

    st.divider()
    st.subheader("🗑️ Limpeza de logs")

    col_a, col_b = st.columns([3, 1])
    with col_a:
        st.write("Esta ação remove todos os logs do sistema. Use com cautela.")
    with col_b:
        if st.button("🧹 Limpar todos os logs", use_container_width=True):
            for _, row in df.iterrows():
                sb_delete_by_id("logs", row["id"])
            st.warning("🗑️ Todos os logs foram excluídos.")
            st.rerun()

