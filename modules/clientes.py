import datetime as dt
from typing import Any, Dict, List

import pandas as pd
import streamlit as st

from .supabase_utils import (
    sb_delete_by_id,
    sb_insert,
    sb_listar_registros,
    sb_update_by_id,
)


def _safe_date(value: Any, default: dt.date) -> dt.date:
    """Converte strings em data, retornando um valor padrão em caso de falha."""

    if not value:
        return default

    try:
        return pd.to_datetime(value, errors="coerce").date()  # type: ignore[return-value]
    except Exception:
        return default


def _format_option(option: Dict[str, Any]) -> str:
    nome = option.get("cliente") or option.get("nome")
    if nome:
        return str(nome)
    return f"ID {option.get('id', '?')}"


def tela_clientes() -> None:
    st.title("👥 Clientes")
    st.caption("Cadastro e gerenciamento de clientes Parma Consultoria")

    try:
        clientes = list(sb_listar_registros("clientes"))
    except RuntimeError as exc:
        st.error(str(exc))
        clientes = []

    df = pd.DataFrame(clientes).fillna("")

    if st.button("🔄 Atualizar lista"):
        st.rerun()

    if df.empty:
        st.info("Nenhum cliente cadastrado ainda.")
    else:
        display_cols = [
            "id",
            "data",
            "cliente",
            "nome",
            "cidade",
            "uf",
            "telefone",
            "email",
        ]
        available_cols = [col for col in display_cols if col in df.columns]
        if available_cols:
            st.dataframe(df[available_cols], use_container_width=True, hide_index=True)
        else:
            st.info("A tabela de clientes não possui colunas para exibição.")

    st.divider()
    st.subheader("➕ Novo cliente")

    with st.form("novo_cliente"):
        col1, col2 = st.columns(2)
        with col1:
            data = st.date_input("Data", dt.date.today(), key="novo_cliente_data")
            cliente = st.text_input("Cliente *", key="novo_cliente_nome_cliente")
            nome = st.text_input("Nome", key="novo_cliente_nome_contato")
            cidade = st.text_input("Cidade", key="novo_cliente_cidade")
        with col2:
            uf = st.text_input("UF", max_chars=2, key="novo_cliente_uf")
            telefone = st.text_input("Telefone", key="novo_cliente_telefone")
            email = st.text_input("E-mail", key="novo_cliente_email")

        enviar = st.form_submit_button("Salvar cliente")

        if enviar:
            if not cliente.strip():
                st.warning("⚠️ Campo 'Cliente' é obrigatório.")
            else:
                novo = {
                    "data": str(data),
                    "cliente": cliente.strip(),
                    "nome": nome.strip(),
                    "cidade": cidade.strip(),
                    "uf": uf.strip().upper(),
                    "telefone": telefone.strip(),
                    "email": email.strip(),
                }
                try:
                    res = sb_insert("clientes", novo)
                except RuntimeError as exc:
                    st.error(str(exc))
                else:
                    st.success(
                        f"✅ Cliente '{cliente.strip()}' adicionado com sucesso (ID: {res.get('id', 'N/D')})."
                    )
                    st.rerun()

    st.divider()
    st.subheader("✏️ Editar / Excluir Cliente")

    if df.empty or "id" not in df.columns:
        st.info("Cadastre clientes para habilitar a edição e exclusão.")
        return

    registros: List[Dict[str, Any]] = [row for row in df.to_dict("records") if row.get("id") is not None]
    if not registros:
        st.info("Os registros retornados não possuem identificadores válidos para edição.")
        return

    registros_por_id = {row["id"]: row for row in registros}
    opcoes = [None] + list(registros_por_id.keys())

    
    def _formatar_id(opcao: Any) -> str:
        if opcao is None:
            return "Escolha um cliente"
        registro = registros_por_id.get(opcao)
        if registro:
            return _format_option(registro)
        return f"ID {opcao}"
    cliente_sel = st.selectbox(
        "Selecione o cliente",
        options=opcoes,
        format_func=_formatar_id,
        key="cliente_edicao_select",
    )

    if cliente_sel is None:
        return

    cliente_row = registros_por_id.get(cliente_sel)
    if not cliente_row:
        st.error("Não foi possível carregar os dados do cliente selecionado.")
        return

    cliente_id = cliente_sel
    col1, col2 = st.columns(2)
    with col1:
        novo_nome = st.text_input("Nome", cliente_row.get("nome", ""), key="editar_cliente_nome")
        nova_cidade = st.text_input("Cidade", cliente_row.get("cidade", ""), key="editar_cliente_cidade")
        novo_uf = st.text_input("UF", cliente_row.get("uf", ""), max_chars=2, key="editar_cliente_uf")
        novo_telefone = st.text_input("Telefone", cliente_row.get("telefone", ""), key="editar_cliente_telefone")
    with col2:
        novo_email = st.text_input("E-mail", cliente_row.get("email", ""), key="editar_cliente_email")
        nova_data = st.date_input(
            "Data",
            value=_safe_date(cliente_row.get("data"), dt.date.today()),
            key="editar_cliente_data",
        )

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("💾 Atualizar cliente", use_container_width=True, key="botao_atualizar_cliente"):
            try:
                sb_update_by_id(
                    "clientes",
                    cliente_id,
                    {
                        "data": str(nova_data),
                        "nome": novo_nome.strip(),
                        "cidade": nova_cidade.strip(),
                        "uf": novo_uf.strip().upper(),
                        "telefone": novo_telefone.strip(),
                        "email": novo_email.strip(),
                    },
                )
            except RuntimeError as exc:
                st.error(str(exc))
            else:
                st.success("✅ Cliente atualizado com sucesso!")
                st.rerun()
    with col_b:
        if st.button("🗑️ Excluir cliente", use_container_width=True, key="botao_excluir_cliente"):
            try:
                sb_delete_by_id("clientes", cliente_id)
            except RuntimeError as exc:
                st.error(str(exc))
            else:
                st.warning("🗑️ Cliente removido.")
                st.rerun()
