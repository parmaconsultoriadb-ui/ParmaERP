import datetime as dt
from typing import Any, Dict, List

import pandas as pd
import streamlit as st

from modules.supabase_utils import (
    sb_delete_by_id,
    sb_insert,
    sb_listar_registros,
    sb_update_by_id,
)


STATUS_OPCOES = ["Enviado", "Validado", "Não validado", "Desistência"]


def _safe_date(value: Any, default: dt.date) -> dt.date:
    if not value:
        return default

    try:
        parsed = pd.to_datetime(value, errors="coerce")
        if pd.isna(parsed):
            return default
        return parsed.date()  # type: ignore[return-value]
    except Exception:
        return default


def _format_candidato(option: Dict[str, Any]) -> str:
    nome = option.get("nome")
    cargo = option.get("cargo")
    if nome and cargo:
        return f"{nome} — {cargo}"
    if nome:
        return str(nome)
    return f"ID {option.get('id', '?')}"


def tela_candidatos() -> None:
    st.title("🧑‍💼 Candidatos")
    st.caption("Gestão de candidatos cadastrados no Supabase")

    try:
        candidatos = list(sb_listar_registros("candidatos"))
    except RuntimeError as exc:
        st.error(str(exc))
        candidatos = []

    df = pd.DataFrame(candidatos).fillna("")

    if st.button("🔄 Atualizar lista"):
        st.rerun()

    if df.empty:
        st.info("Nenhum candidato cadastrado ainda.")
    else:
        display_cols = [
            "id",
            "cliente",
            "cargo",
            "nome",
            "telefone",
            "recrutador",
            "status",
            "data_cadastro",
            "data_inicio",
        ]
        available_cols = [col for col in display_cols if col in df.columns]
        if available_cols:
            st.dataframe(df[available_cols], use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("➕ Novo candidato")

    with st.form("novo_candidato"):
        col1, col2, col3 = st.columns(3)
        with col1:
            cliente = st.text_input("Cliente *", key="novo_candidato_cliente")
            cargo = st.text_input("Cargo *", key="novo_candidato_cargo")
            nome = st.text_input("Nome *", key="novo_candidato_nome")
        with col2:
            telefone = st.text_input("Telefone *", key="novo_candidato_telefone")
            recrutador = st.text_input("Recrutador", key="novo_candidato_recrutador")
            status = st.selectbox(
                "Status",
                STATUS_OPCOES,
                index=0,
                key="novo_candidato_status",
            )
        with col3:
            data_cadastro = st.date_input(
                "Data de Cadastro",
                dt.date.today(),
                key="novo_candidato_data_cadastro",
            )
            informar_data_inicio = st.checkbox(
                "Definir data de início?",
                value=False,
                key="novo_candidato_usar_data_inicio",
            )
            data_inicio = st.date_input(
                "Data de Início",
                dt.date.today(),
                key="novo_candidato_data_inicio",
                disabled=not informar_data_inicio,
            )

        enviar = st.form_submit_button("Salvar candidato")

        if enviar:
            if not all([cliente.strip(), cargo.strip(), nome.strip(), telefone.strip()]):
                st.warning("⚠️ Campos obrigatórios não preenchidos.")
            else:
                novo = {
                    "cliente": cliente.strip(),
                    "cargo": cargo.strip(),
                    "nome": nome.strip(),
                    "telefone": telefone.strip(),
                    "recrutador": recrutador.strip(),
                    "status": status,
                    "data_cadastro": str(data_cadastro),
                    "data_inicio": str(data_inicio) if informar_data_inicio else None,
                    "atualizacao": str(dt.datetime.now()),
                }
                try:
                    res = sb_insert("candidatos", novo)
                except RuntimeError as exc:
                    st.error(str(exc))
                else:
                    st.success(
                        f"✅ Candidato '{nome.strip()}' cadastrado com sucesso (ID: {res.get('id', 'N/D')})."
                    )
                    st.rerun()

    st.divider()
    st.subheader("✏️ Editar / Excluir candidato")

    if df.empty or "id" not in df.columns:
        st.info("Cadastre candidatos para habilitar a edição e exclusão.")
        return

    registros: List[Dict[str, Any]] = df.to_dict("records")
    cand_sel = st.selectbox(
        "Selecione o candidato",
        options=[None] + registros,
        format_func=lambda opt: "Escolha um candidato" if opt is None else _format_candidato(opt),
        key="candidato_edicao_select",
    )

    if not cand_sel:
        return

    cand_row = cand_sel
    cand_id = cand_row.get("id")
    if cand_id is None:
        st.error("Registro selecionado não possui ID válido no Supabase.")
        return

    col1, col2 = st.columns(2)
    with col1:
        novo_cliente = st.text_input("Cliente", cand_row.get("cliente", ""), key=f"editar_candidato_cliente_{cand_id}")
        novo_cargo = st.text_input("Cargo", cand_row.get("cargo", ""), key=f"editar_candidato_cargo_{cand_id}")
        novo_nome = st.text_input("Nome", cand_row.get("nome", ""), key=f"editar_candidato_nome_{cand_id}")
        novo_telefone = st.text_input(
            "Telefone",
            cand_row.get("telefone", ""),
            key=f"editar_candidato_telefone_{cand_id}",
        )
    with col2:
        novo_recrutador = st.text_input(
            "Recrutador",
            cand_row.get("recrutador", ""),
            key=f"editar_candidato_recrutador_{cand_id}",
        )
        status_index = 0
        if cand_row.get("status") in STATUS_OPCOES:
            status_index = STATUS_OPCOES.index(cand_row.get("status"))
        novo_status = st.selectbox(
            "Status",
            STATUS_OPCOES,
            index=status_index,
            key=f"editar_candidato_status_{cand_id}",
        )
        nova_data_cad = st.date_input(
            "Data de Cadastro",
            value=_safe_date(cand_row.get("data_cadastro"), dt.date.today()),
            key=f"editar_candidato_data_cadastro_{cand_id}",
        )
        possui_data_inicio = bool(cand_row.get("data_inicio"))
        informar_data_inicio = st.checkbox(
            "Definir data de início?",
            value=possui_data_inicio,
            key=f"editar_candidato_usar_data_inicio_{cand_id}",
        )
        nova_data_ini = st.date_input(
            "Data de Início",
            value=_safe_date(cand_row.get("data_inicio"), dt.date.today()),
            key=f"editar_candidato_data_inicio_{cand_id}",
            disabled=not informar_data_inicio,
        )
