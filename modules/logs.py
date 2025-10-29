import datetime as dt
from typing import Dict, List

import pandas as pd
import streamlit as st

from modules.supabase_utils import sb_delete_by_id, sb_insert, sb_listar_registros


def registrar_log(usuario: str, aba: str, acao: str, detalhe: str = "") -> None:
    """Função auxiliar para gravar logs diretamente no Supabase."""

    log = {
        "datahora": str(dt.datetime.now()),
        "usuario": usuario,
        "aba": aba,
        "acao": acao,
        "detalhe": detalhe,
    }
    try:
        sb_insert("logs", log)
    except RuntimeError as exc:
        st.error(f"Falha ao registrar log: {exc}")


def tela_logs() -> None:
    st.title("📜 Logs do Sistema")
    st.caption("Registro de atividades e alterações no sistema")

    try:
        registros = list(sb_listar_registros("logs"))
    except RuntimeError as exc:
        st.error(str(exc))
        registros = []

    df = pd.DataFrame(registros).fillna("")

    if st.button("🔄 Atualizar"):
        st.rerun()

    if df.empty:
        st.info("Nenhum log registrado até o momento.")
        return

    if "datahora" in df.columns:
        df["datahora"] = pd.to_datetime(df["datahora"], errors="coerce")

    col1, col2 = st.columns(2)
    with col1:
        usuarios = [None] + sorted(df["usuario"].dropna().unique().tolist()) if "usuario" in df.columns else [None]
        usuario_filtro = st.selectbox(
            "👤 Usuário",
            options=usuarios,
            format_func=lambda opt: "Todos" if opt in (None, "") else str(opt),
            key="logs_filtro_usuario",
        )
    with col2:
        abas = [None] + sorted(df["aba"].dropna().unique().tolist()) if "aba" in df.columns else [None]
        aba_filtro = st.selectbox(
            "📂 Aba",
            options=abas,
            format_func=lambda opt: "Todos" if opt in (None, "") else str(opt),
            key="logs_filtro_aba",
        )

    if usuario_filtro not in (None, "") and "usuario" in df.columns:
        df = df[df["usuario"] == usuario_filtro]
    if aba_filtro not in (None, "") and "aba" in df.columns:
        df = df[df["aba"] == aba_filtro]

    if df.empty:
        st.info("Nenhum log encontrado para os filtros selecionados.")
        return

    df = df.sort_values("datahora", ascending=False)

    display_cols = ["datahora", "usuario", "aba", "acao", "detalhe"]
    available_cols = [col for col in display_cols if col in df.columns]
    if available_cols:
        st.dataframe(df[available_cols], use_container_width=True, hide_index=True)
    else:
        st.info("A tabela de logs não possui campos suficientes para exibição.")
        return

    st.divider()
    st.subheader("🗑️ Limpeza de logs")

    col_a, col_b = st.columns([3, 1])
    with col_a:
        st.write("Esta ação remove todos os logs do sistema. Use com cautela.")
    with col_b:
        if st.button("🧹 Limpar todos os logs", use_container_width=True, key="botao_limpar_logs"):
            registros_para_excluir: List[Dict[str, Any]] = df.to_dict("records")
            erros: List[str] = []
            for registro in registros_para_excluir:
                registro_id = registro.get("id")
                if registro_id is None:
                    continue
                try:
                    sb_delete_by_id("logs", registro_id)
                except RuntimeError as exc:
                    erros.append(str(exc))
            if erros:
                st.error("Erros ao remover alguns logs: " + "; ".join(erros))
            else:
                st.warning("🗑️ Todos os logs foram excluídos.")
            st.rerun()
