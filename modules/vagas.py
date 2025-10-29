import streamlit as st
from modules.supabase_utils import (
    sb_listar_registros,
    sb_insert,
    sb_update_by_id,
    sb_delete_by_id
)
import pandas as pd
import datetime as dt


def tela_vagas():
    st.title("💼 Vagas")
    st.caption("Gestão das vagas cadastradas no Supabase")

    # --- Carregar registros
    vagas = list(sb_listar_registros("vagas"))
    df = pd.DataFrame(vagas)

    if st.button("🔄 Atualizar lista"):
        st.rerun()

    if not df.empty:
        st.dataframe(
            df[
                [
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
            ],
            use_container_width=True,
        )
    else:
        st.info("Nenhuma vaga cadastrada ainda.")

    st.divider()
    st.subheader("➕ Nova vaga")

    # --- Formulário de nova vaga
    with st.form("nova_vaga"):
        col1, col2, col3 = st.columns(3)
        with col1:
            data_de_abertura = st.date_input("Data de abertura", dt.date.today())
            cliente = st.text_input("Cliente *")
            cargo = st.text_input("Cargo *")
        with col2:
            recrutador = st.text_input("Recrutador")
            status = st.selectbox(
                "Status",
                ["Aberta", "Ag. Inicio", "Cancelada", "Fechada", "Reaberta", "Pausada"],
                index=0,
            )
        with col3:
            salario_1 = st.text_input("Salário base")
            salario_2 = st.text_input("Salário variável")
            salario_final = st.text_input("Salário final")
            reposicao = st.selectbox("Reposição", ["", "Sim"], index=0)

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
                res = sb_insert("vagas", nova)
                st.success(f"✅ Vaga '{cargo}' adicionada com sucesso (ID: {res.get('id')}).")
                st.rerun()

    st.divider()
    st.subheader("✏️ Editar / Excluir vaga")

    if not df.empty:
        vaga_sel = st.selectbox(
            "Selecione a vaga",
            df["cargo"].tolist(),
            index=None,
            placeholder="Escolha uma vaga para editar"
        )
        if vaga_sel:
            vaga_row = df[df["cargo"] == vaga_sel].iloc[0]
            col1, col2 = st.columns(2)
            with col1:
                novo_cliente = st.text_input("Cliente", vaga_row["cliente"])
                novo_cargo = st.text_input("Cargo", vaga_row["cargo"])
                novo_recrutador = st.text_input("Recrutador", vaga_row["recrutador"])
                novo_status = st.selectbox(
                    "Status",
                    ["Aberta", "Ag. Inicio", "Cancelada", "Fechada", "Reaberta", "Pausada"],
                    index=["Aberta", "Ag. Inicio", "Cancelada", "Fechada", "Reaberta", "Pausada"].index(vaga_row["status"]) if vaga_row["status"] in ["Aberta", "Ag. Inicio", "Cancelada", "Fechada", "Reaberta", "Pausada"] else 0
                )
            with col2:
                novo_salario_1 = st.text_input("Salário base", vaga_row["salario_1"])
                novo_salario_2 = st.text_input("Salário variável", vaga_row["salario_2"])
                novo_salario_final = st.text_input("Salário final", vaga_row["salario_final"])
                nova_reposicao = st.selectbox(
                    "Reposição", ["", "Sim"], index=1 if vaga_row["reposicao"] == "Sim" else 0
                )
                nova_data = st.date_input(
                    "Data de abertura",
                    value=pd.to_datetime(vaga_row["data_de_abertura"]).date() if vaga_row["data_de_abertura"] else dt.date.today()
                )

            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("💾 Atualizar vaga", use_container_width=True):
                    sb_update_by_id(
                        "vagas",
                        vaga_row["id"],
                        {
                            "data_de_abertura": str(nova_data),
                            "cliente": novo_cliente,
                            "cargo": novo_cargo,
                            "recrutador": novo_recrutador,
                            "status": novo_status,
                            "salario_1": novo_salario_1,
                            "salario_2": novo_salario_2,
                            "salario_final": novo_salario_final,
                            "reposicao": nova_reposicao,
                            "atualizacao": str(dt.datetime.now()),
                        },
                    )
                    st.success("✅ Vaga atualizada com sucesso!")
                    st.rerun()

            with col_b:
                if st.button("🗑️ Excluir vaga", use_container_width=True):
                    sb_delete_by_id("vagas", vaga_row["id"])
                    st.warning("🗑️ Vaga removida com sucesso.")
                    st.rerun()

