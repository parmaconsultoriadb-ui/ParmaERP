import streamlit as st
from modules.supabase_utils import (
    sb_listar_registros,
    sb_insert,
    sb_update_by_id,
    sb_delete_by_id
)
import pandas as pd
import datetime as dt


def tela_candidatos():
    st.title("🧑‍💼 Candidatos")
    st.caption("Gestão de candidatos cadastrados no Supabase")

    # --- Carregar registros
    candidatos = list(sb_listar_registros("candidatos"))
    df = pd.DataFrame(candidatos)

    if st.button("🔄 Atualizar lista"):
        st.rerun()

    if not df.empty:
        st.dataframe(
            df[
                [
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
            ],
            use_container_width=True,
        )
    else:
        st.info("Nenhum candidato cadastrado ainda.")

    st.divider()
    st.subheader("➕ Novo candidato")

    # --- Formulário de novo candidato
    with st.form("novo_candidato"):
        col1, col2, col3 = st.columns(3)
        with col1:
            cliente = st.text_input("Cliente *")
            cargo = st.text_input("Cargo *")
            nome = st.text_input("Nome *")
        with col2:
            telefone = st.text_input("Telefone *")
            recrutador = st.text_input("Recrutador")
            status = st.selectbox(
                "Status",
                ["Enviado", "Validado", "Não validado", "Desistência"],
                index=0,
            )
        with col3:
            data_cadastro = st.date_input("Data de Cadastro", dt.date.today())
            data_inicio = st.date_input("Data de Início (opcional)", None)

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
                    "data_inicio": str(data_inicio) if data_inicio else "",
                    "atualizacao": str(dt.datetime.now()),
                }
                res = sb_insert("candidatos", novo)
                st.success(f"✅ Candidato '{nome}' cadastrado com sucesso (ID: {res.get('id')}).")
                st.rerun()

    st.divider()
    st.subheader("✏️ Editar / Excluir candidato")

    if not df.empty:
        cand_sel = st.selectbox(
            "Selecione o candidato",
            df["nome"].tolist(),
            index=None,
            placeholder="Escolha um candidato para editar"
        )
        if cand_sel:
            cand_row = df[df["nome"] == cand_sel].iloc[0]
            col1, col2 = st.columns(2)
            with col1:
                novo_cliente = st.text_input("Cliente", cand_row["cliente"])
                novo_cargo = st.text_input("Cargo", cand_row["cargo"])
                novo_nome = st.text_input("Nome", cand_row["nome"])
                novo_telefone = st.text_input("Telefone", cand_row["telefone"])
            with col2:
                novo_recrutador = st.text_input("Recrutador", cand_row["recrutador"])
                novo_status = st.selectbox(
                    "Status",
                    ["Enviado", "Validado", "Não validado", "Desistência"],
                    index=["Enviado", "Validado", "Não validado", "Desistência"].index(cand_row["status"]) if cand_row["status"] in ["Enviado", "Validado", "Não validado", "Desistência"] else 0
                )
                nova_data_cad = st.date_input(
                    "Data de Cadastro",
                    value=pd.to_datetime(cand_row["data_cadastro"]).date() if cand_row["data_cadastro"] else dt.date.today()
                )
                nova_data_ini = st.date_input(
                    "Data de Início",
                    value=pd.to_datetime(cand_row["data_inicio"]).date() if cand_row["data_inicio"] else dt.date.today()
                )

            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("💾 Atualizar candidato", use_container_width=True):
                    sb_update_by_id(
                        "candidatos",
                        cand_row["id"],
                        {
                            "cliente": novo_cliente,
                            "cargo": novo_cargo,
                            "nome": novo_nome,
                            "telefone": novo_telefone,
                            "recrutador": novo_recrutador,
                            "status": novo_status,
                            "data_cadastro": str(nova_data_cad),
                            "data_inicio": str(nova_data_ini),
                            "atualizacao": str(dt.datetime.now()),
                        },
                    )
                    st.success("✅ Candidato atualizado com sucesso!")
                    st.rerun()

            with col_b:
                if st.button("🗑️ Excluir candidato", use_container_width=True):
                    sb_delete_by_id("candidatos", cand_row["id"])
                    st.warning("🗑️ Candidato removido com sucesso.")
                    st.rerun()
