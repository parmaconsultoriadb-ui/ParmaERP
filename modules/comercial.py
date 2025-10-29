import datetime as dt
from typing import Any, Dict, List
from typing import Dict, List

import pandas as pd
import streamlit as st

from modules.supabase_utils import (
    sb_delete_by_id,
    sb_insert,
    sb_listar_registros,
    sb_update_by_id,
)


STATUS_OPCOES = [
    "Prospect",
    "Lead Qualificado",
    "Negociação",
    "Proposta Enviada",
    "Contrato Enviado",
    "Negócio Fechado",
    "Declinado",
]
PRODUTOS = ["", "Recrutamento", "Consultoria RH", "Marketing", "Outros"]
CANAIS = ["", "Google", "Mídias Sociais", "Indicação", "Outros"]


def _format_registro(option: Dict[str, Any]) -> str:
    cliente = option.get("cliente")
    cidade = option.get("cidade")
    if cliente and cidade:
        return f"{cliente} — {cidade}"
    if cliente:
        return str(cliente)
    return f"ID {option.get('id', '?')}"


def tela_comercial() -> None:
    st.title("💼 Funil Comercial")
    st.caption("Gestão de oportunidades comerciais cadastradas no Supabase")

    try:
        registros = list(sb_listar_registros("comercial"))
    except RuntimeError as exc:
        st.error(str(exc))
        registros = []

    df = pd.DataFrame(registros).fillna("")

    if st.button("🔄 Atualizar lista"):
        st.rerun()

    if df.empty:
        st.info("Nenhum registro comercial encontrado.")
    else:
        display_cols = [
            "id",
            "data",
            "cliente",
            "cidade",
            "uf",
            "nome",
            "telefone",
            "email",
            "produto",
            "canal",
            "status",
        ]
        available_cols = [col for col in display_cols if col in df.columns]
        if available_cols:
            st.dataframe(df[available_cols], use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("➕ Novo registro comercial")

    with st.form("novo_comercial"):
        col1, col2, col3 = st.columns(3)
        with col1:
            cliente = st.text_input("Cliente *", key="novo_comercial_cliente")
            cidade = st.text_input("Cidade *", key="novo_comercial_cidade")
            uf = st.text_input("UF", max_chars=2, key="novo_comercial_uf")
        with col2:
            nome = st.text_input("Contato *", key="novo_comercial_nome")
            telefone = st.text_input("Telefone *", key="novo_comercial_telefone")
            email = st.text_input("E-mail", key="novo_comercial_email")
        with col3:
            produto = st.selectbox(
                "Produto",
                PRODUTOS,
                index=0,
                key="novo_comercial_produto",
            )
            canal = st.selectbox(
                "Canal",
                CANAIS,
                index=0,
                key="novo_comercial_canal",
            )
            status = st.selectbox(
                "Status",
                STATUS_OPCOES,
                index=0,
                key="novo_comercial_status",
            )

        enviar = st.form_submit_button("Salvar registro")

        if enviar:
            if not all([cliente.strip(), cidade.strip(), nome.strip(), telefone.strip()]):
                st.warning("⚠️ Campos obrigatórios não preenchidos.")
            else:
                novo = {
                    "data": str(dt.date.today()),
                    "cliente": cliente.strip(),
                    "cidade": cidade.strip(),
                    "uf": uf.strip().upper(),
                    "nome": nome.strip(),
                    "telefone": telefone.strip(),
                    "email": email.strip(),
                    "produto": produto,
                    "canal": canal,
                    "status": status,
                    "observacoes": "",
                    "atualizacao": str(dt.datetime.now()),
                }
                try:
                    res = sb_insert("comercial", novo)
                except RuntimeError as exc:
                    st.error(str(exc))
                else:
                    st.success(
                        f"✅ Registro '{cliente.strip()}' adicionado com sucesso (ID: {res.get('id', 'N/D')})."
                    )
                    st.rerun()

    st.divider()
    st.subheader("✏️ Editar / Excluir registro")

    if df.empty or "id" not in df.columns:
        st.info("Cadastre oportunidades para habilitar a edição e exclusão.")
        return

   registros_dict: List[Dict[str, Any]] = [row for row in df.to_dict("records") if row.get("id") is not None]
    if not registros_dict:
        st.info("Os registros retornados não possuem identificadores válidos para edição.")
        return

    registros_por_id = {row["id"]: row for row in registros_dict}
    opcoes = [None] + list(registros_por_id.keys())

    def _formatar_id(opcao: Any) -> str:
        if opcao is None:
            return "Escolha um registro"
        registro = registros_por_id.get(opcao)
        if registro:
            return _format_registro(registro)
        return f"ID {opcao}"

    reg_sel = st.selectbox(
        "Selecione o cliente",
        options=opcoes,
        format_func=_formatar_id,
        key="comercial_edicao_select",
    )

    if reg_sel is None:
        return

    row = registros_por_id.get(reg_sel)
    if not row:
        st.error("Não foi possível carregar os dados do registro selecionado.")
        return

    reg_id = reg_sel

    col1, col2, col3 = st.columns(3)
    with col1:
        novo_cliente = st.text_input("Cliente", row.get("cliente", ""), key=f"editar_comercial_cliente_{reg_id}")
        nova_cidade = st.text_input("Cidade", row.get("cidade", ""), key=f"editar_comercial_cidade_{reg_id}")
        novo_uf = st.text_input("UF", row.get("uf", ""), max_chars=2, key=f"editar_comercial_uf_{reg_id}")
    with col2:
        novo_nome = st.text_input("Contato", row.get("nome", ""), key=f"editar_comercial_nome_{reg_id}")
        novo_telefone = st.text_input(
            "Telefone",
            row.get("telefone", ""),
            key=f"editar_comercial_telefone_{reg_id}",
        )
        novo_email = st.text_input("E-mail", row.get("email", ""), key=f"editar_comercial_email_{reg_id}")
    with col3:
        produto_index = PRODUTOS.index(row.get("produto")) if row.get("produto") in PRODUTOS else 0
        novo_produto = st.selectbox(
            "Produto",
            PRODUTOS,
            index=produto_index,
            key=f"editar_comercial_produto_{reg_id}",
        )
        canal_index = CANAIS.index(row.get("canal")) if row.get("canal") in CANAIS else 0
        novo_canal = st.selectbox(
            "Canal",
            CANAIS,
            index=canal_index,
            key=f"editar_comercial_canal_{reg_id}",
        )
        status_index = STATUS_OPCOES.index(row.get("status")) if row.get("status") in STATUS_OPCOES else 0
        novo_status = st.selectbox(
            "Status",
            STATUS_OPCOES,
            index=status_index,
            key=f"editar_comercial_status_{reg_id}",
        )

    observacoes = st.text_area(
        "Observações",
        value=row.get("observacoes", ""),
        height=120,
        key=f"editar_comercial_observacoes_{reg_id}",
    )

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("💾 Atualizar registro", use_container_width=True, key=f"botao_atualizar_comercial_{reg_id}"):
            try:
                sb_update_by_id(
                    "comercial",
                    reg_id,
                    {
                        "cliente": novo_cliente.strip(),
                        "cidade": nova_cidade.strip(),
                        "uf": novo_uf.strip().upper(),
                        "nome": novo_nome.strip(),
                        "telefone": novo_telefone.strip(),
                        "email": novo_email.strip(),
                        "produto": novo_produto,
                        "canal": novo_canal,
                        "status": novo_status,
                        "observacoes": observacoes.strip(),
                        "atualizacao": str(dt.datetime.now()),
                    },
                )
            except RuntimeError as exc:
                st.error(str(exc))
            else:
                st.success("✅ Registro atualizado com sucesso!")
                st.rerun()

    with col_b:
        if st.button("🗑️ Excluir registro", use_container_width=True, key=f"botao_excluir_comercial_{reg_id}"):
            try:
                sb_delete_by_id("comercial", reg_id)
            except RuntimeError as exc:
                st.error(str(exc))
            else:
                st.warning("🗑️ Registro removido com sucesso.")
                st.rerun()
