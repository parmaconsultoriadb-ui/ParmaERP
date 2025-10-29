import streamlit as st
from modules.supabase_utils import (
    sb_listar_registros,
    sb_insert,
    sb_update_by_id,
    sb_delete_by_id
)
import pandas as pd
import datetime as dt


def tela_comercial():
    st.title("💼 Funil Comercial")
    st.caption("Gestão de oportunidades comerciais cadastradas no Supabase")

    # --- Carregar registros
    registros = list(sb_listar_registros("comercial"))
    df = pd.DataFrame(registros)

    if st.button("🔄 Atualizar lista"):
        st.rerun()

    if not df.empty:
        st.dataframe(
            df[
                [
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
            ],
            use_container_width=True,
        )
    else:
        st.info("Nenhum registro comercial encontrado.")

    st.divider()
    st.subheader("➕ Novo registro comercial")

    # --- Formulário de novo registro
    with st.form("novo_comercial"):
        col1, col2, col3 = st.columns(3)
        with col1:
            cliente = st.text_input("Cliente *")
            cidade = st.text_input("Cidade *")
            uf = st.text_input("UF", max_chars=2)
        with col2:
            nome = st.text_input("Contato *")
            telefone = st.text_input("Telefone *")
            email = st.text_input("E-mail")
        with col3:
            produto = st.selectbox(
                "Produto",
                ["", "Recrutamento", "Consultoria RH", "Marketing", "Outros"],
                index=0,
            )
            canal = st.selectbox(
                "Canal",
                ["", "Google", "Mídias Sociais", "Indicação", "Outros"],
                index=0,
            )
            status = st.selectbox(
                "Status",
                [
                    "Prospect",
                    "Lead Qualificado",
                    "Negociação",
                    "Proposta Enviada",
                    "Contrato Enviado",
                    "Negócio Fechado",
                    "Declinado",
                ],
                index=0,
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
                res = sb_insert("comercial", novo)
                st.success(f"✅ Registro '{cliente}' adicionado com sucesso (ID: {res.get('id')}).")
                st.rerun()

    st.divider()
    st.subheader("✏️ Editar / Excluir registro")

    if not df.empty:
        reg_sel = st.selectbox(
            "Selecione o cliente",
            df["cliente"].tolist(),
            index=None,
            placeholder="Escolha um registro para editar"
        )
        if reg_sel:
            row = df[df["cliente"] == reg_sel].iloc[0]
            col1, col2, col3 = st.columns(3)
            with col1:
                novo_cliente = st.text_input("Cliente", row["cliente"])
                nova_cidade = st.text_input("Cidade", row["cidade"])
                novo_uf = st.text_input("UF", row["uf"], max_chars=2)
            with col2:
                novo_nome = st.text_input("Contato", row["nome"])
                novo_telefone = st.text_input("Telefone", row["telefone"])
                novo_email = st.text_input("E-mail", row["email"])
            with col3:
                novo_produto = st.selectbox(
                    "Produto",
                    ["", "Recrutamento", "Consultoria RH", "Marketing", "Outros"],
                    index=["", "Recrutamento", "Consultoria RH", "Marketing", "Outros"].index(row["produto"]) if row["produto"] in ["", "Recrutamento", "Consultoria RH", "Marketing", "Outros"] else 0
                )
                novo_canal = st.selectbox(
                    "Canal",
                    ["", "Google", "Mídias Sociais", "Indicação", "Outros"],
                    index=["", "Google", "Mídias Sociais", "Indicação", "Outros"].index(row["canal"]) if row["canal"] in ["", "Google", "Mídias Sociais", "Indicação", "Outros"] else 0
                )
                novo_status = st.selectbox(
                    "Status",
                    [
                        "Prospect",
                        "Lead Qualificado",
                        "Negociação",
                        "Proposta Enviada",
                        "Contrato Enviado",
                        "Negócio Fechado",
                        "Declinado",
                    ],
                    index=[
                        "Prospect",
                        "Lead Qualificado",
                        "Negociação",
                        "Proposta Enviada",
                        "Contrato Enviado",
                        "Negócio Fechado",
                        "Declinado",
                    ].index(row["status"]) if row["status"] in [
                        "Prospect",
                        "Lead Qualificado",
                        "Negociação",
                        "Proposta Enviada",
                        "Contrato Enviado",
                        "Negócio Fechado",
                        "Declinado",
                    ] else 0
                )

            observacoes = st.text_area("Observações", value=row.get("observacoes", ""), height=120)

            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("💾 Atualizar registro", use_container_width=True):
                    sb_update_by_id(
                        "comercial",
                        row["id"],
                        {
                            "cliente": novo_cliente,
                            "cidade": nova_cidade,
                            "uf": novo_uf,
                            "nome": novo_nome,
                            "telefone": novo_telefone,
                            "email": novo_email,
                            "produto": novo_produto,
                            "canal": novo_canal,
                            "status": novo_status,
                            "observacoes": observacoes,
                            "atualizacao": str(dt.datetime.now()),
                        },
                    )
                    st.success("✅ Registro atualizado com sucesso!")
                    st.rerun()

            with col_b:
                if st.button("🗑️ Excluir registro", use_container_width=True):
                    sb_delete_by_id("comercial", row["id"])
                    st.warning("🗑️ Registro removido com sucesso.")
                    st.rerun()

