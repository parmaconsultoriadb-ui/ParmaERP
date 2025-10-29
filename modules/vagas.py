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


STATUS_OPCOES = ["Aberta", "Ag. Inicio", "Cancelada", "Fechada", "Reaberta", "Pausada"]


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


def _format_vaga(option: Dict[str, Any]) -> str:
    cargo = option.get("cargo")
    cliente = option.get("cliente")
    if cargo and cliente:
        return f"{cargo} — {cliente}"
    if cargo:
        return str(cargo)
    return f"ID {option.get('id', '?')}"


def tela_vagas() -> None:
    st.title("💼 Vagas")
    st.caption("Gestão das vagas cadastradas no Supabase")

    try:
        vagas = list(sb_listar_registros("vagas"))
    except RuntimeError as exc:
        st.error(str(exc))
        vagas = []

    df = pd.DataFrame(vagas).fillna("")

    if st.button("🔄 Atualizar lista"):
        st.rerun()

    if df.empty:
        st.info("Nenhuma vaga cadastrada ainda.")
    else:
        display_cols = [
            "id",
            "data_de_abertura",
            "cliente",
            "cargo",
            "recrutador",
            "status",
            "salario_1",
            "salario_2",
            "salario_final",
            "reposicao",
        ]
        available_cols = [col for col in display_cols if col in df.columns]
        if available_cols:
            st.dataframe(df[available_cols], use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("➕ Nova vaga")

    with st.form("nova_vaga"):
        col1, col2, col3 = st.columns(3)
        with col1:
            data_de_abertura = st.date_input(
                "Data de abertura",
                dt.date.today(),
                key="nova_vaga_data_abertura",
            )
            cliente = st.text_input("Cliente *", key="nova_vaga_cliente")
            cargo = st.text_input("Cargo *", key="nova_vaga_cargo")
        with col2:
            recrutador = st.text_input("Recrutador", key="nova_vaga_recrutador")
            status = st.selectbox(
                "Status",
                STATUS_OPCOES,
                index=0,
                key="nova_vaga_status",
            )
        with col3:
            salario_1 = st.text_input("Salário base", key="nova_vaga_salario_1")
            salario_2 = st.text_input("Salário variável", key="nova_vaga_salario_2")
            salario_final = st.text_input("Salário final", key="nova_vaga_salario_final")
            reposicao = st.selectbox(
                "Reposição",
                ["", "Sim"],
                index=0,
                key="nova_vaga_reposicao",
            )

        enviar = st.form_submit_button("Salvar vaga")

        if enviar:
            if not cliente.strip() or not cargo.strip():
                st.warning("⚠️ Campos 'Cliente' e 'Cargo' são obrigatórios.")
            else:
                nova = {
                    "data_de_abertura": str(data_de_abertura),
                    "cliente": cliente.strip(),
                    "cargo": cargo.strip(),
                    "recrutador": recrutador.strip(),
                    "status": status,
                    "salario_1": salario_1.strip(),
                    "salario_2": salario_2.strip(),
                    "salario_final": salario_final.strip(),
                    "reposicao": reposicao,
                    "atualizacao": str(dt.datetime.now()),
                }
                try:
                    res = sb_insert("vagas", nova)
                except RuntimeError as exc:
                    st.error(str(exc))
                else:
                    st.success(
                        f"✅ Vaga '{cargo.strip()}' adicionada com sucesso (ID: {res.get('id', 'N/D')})."
                    )
                    st.rerun()

    st.divider()
    st.subheader("✏️ Editar / Excluir vaga")

    if df.empty or "id" not in df.columns:
        st.info("Cadastre vagas para habilitar a edição e exclusão.")
        return

    registros: List[Dict[str, Any]] = [row for row in df.to_dict("records") if row.get("id") is not None]
    if not registros:
        st.info("As vagas retornadas não possuem identificadores válidos para edição.")
        return

    registros_por_id = {row["id"]: row for row in registros}
    opcoes = [None] + list(registros_por_id.keys())

    def _formatar_id(opcao: Any) -> str:
        if opcao is None:
            return "Escolha uma vaga"
        registro = registros_por_id.get(opcao)
        if registro:
            return _format_vaga(registro)
        return f"ID {opcao}"
        
    vaga_sel = st.selectbox(
        "Selecione a vaga",
        options=opcoes,
        format_func=_formatar_id,
        key="vaga_edicao_select",
    )

    if vaga_sel is None:
        return

    vaga_row = registros_por_id.get(vaga_sel)
    if not vaga_row:
        st.error("Não foi possível carregar os dados da vaga selecionada.")
        return
    
    vaga_id = vaga_sel
    
    col1, col2 = st.columns(2)
    with col1:
        novo_cliente = st.text_input("Cliente", vaga_row.get("cliente", ""), key=f"editar_vaga_cliente_{vaga_id}")
        novo_cargo = st.text_input("Cargo", vaga_row.get("cargo", ""), key=f"editar_vaga_cargo_{vaga_id}")
        novo_recrutador = st.text_input(
            "Recrutador",
            vaga_row.get("recrutador", ""),
            key=f"editar_vaga_recrutador_{vaga_id}",
        )
        status_index = 0
        if vaga_row.get("status") in STATUS_OPCOES:
            status_index = STATUS_OPCOES.index(vaga_row.get("status"))
        novo_status = st.selectbox(
            "Status",
            STATUS_OPCOES,
            index=status_index,
            key=f"editar_vaga_status_{vaga_id}",
        )
    with col2:
        novo_salario_1 = st.text_input(
            "Salário base",
            vaga_row.get("salario_1", ""),
            key=f"editar_vaga_salario1_{vaga_id}",
        )
        novo_salario_2 = st.text_input(
            "Salário variável",
            vaga_row.get("salario_2", ""),
            key=f"editar_vaga_salario2_{vaga_id}",
        )
        novo_salario_final = st.text_input(
            "Salário final",
            vaga_row.get("salario_final", ""),
            key=f"editar_vaga_salariofinal_{vaga_id}",
        )
        reposicao_index = 1 if vaga_row.get("reposicao") == "Sim" else 0
        nova_reposicao = st.selectbox(
            "Reposição",
            ["", "Sim"],
            index=reposicao_index,
            key=f"editar_vaga_reposicao_{vaga_id}",
        )
        nova_data = st.date_input(
            "Data de abertura",
            value=_safe_date(vaga_row.get("data_de_abertura"), dt.date.today()),
            key=f"editar_vaga_data_abertura_{vaga_id}",
        )

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("💾 Atualizar vaga", use_container_width=True, key=f"botao_atualizar_vaga_{vaga_id}"):
            try:
                sb_update_by_id(
                    "vagas",
                    vaga_id,
                    {
                        "data_de_abertura": str(nova_data),
                        "cliente": novo_cliente.strip(),
                        "cargo": novo_cargo.strip(),
                        "recrutador": novo_recrutador.strip(),
                        "status": novo_status,
                        "salario_1": novo_salario_1.strip(),
                        "salario_2": novo_salario_2.strip(),
                        "salario_final": novo_salario_final.strip(),
                        "reposicao": nova_reposicao,
                        "atualizacao": str(dt.datetime.now()),
                    },
                )
            except RuntimeError as exc:
                st.error(str(exc))
            else:
                st.success("✅ Vaga atualizada com sucesso!")
                st.rerun()

    with col_b:
        if st.button("🗑️ Excluir vaga", use_container_width=True, key=f"botao_excluir_vaga_{vaga_id}"):
            try:
                sb_delete_by_id("vagas", vaga_id)
            except RuntimeError as exc:
                st.error(str(exc))
            else:
                st.warning("🗑️ Vaga removida com sucesso.")
                st.rerun()
