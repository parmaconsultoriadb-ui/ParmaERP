import streamlit as st
import pandas as pd
from core.services.recrutamento_service import RecrutamentoService
from app.components.filters import search_and_pagination
from core.services.log_service import registrar_log
from common.config import agora_formatado

service = RecrutamentoService()
RECRUTADORES_PADRAO = ["A definir", "Lorrayne", "Kaline", "Nikole", "Leila", "Julia"]

def page():
    st.title("🧑‍💼 Candidatos")
    service = RecrutamentoService()

    search, page_num = search_and_pagination(prefix="candidatos")

    data = service.listar_candidatos(page=page_num, busca=search)
    df = pd.DataFrame(data) if data else pd.DataFrame()

    if not df.empty:
        if "criado_em" in df.columns:
            df["criado_em"] = pd.to_datetime(df["criado_em"], errors="coerce").dt.strftime("%d/%m/%Y")
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhum candidato encontrado.")

    with st.expander("➕ Novo Candidato"):
        nome = st.text_input("Nome", key="cand_nome")
        email = st.text_input("Email", key="cand_email")
        telefone = st.text_input("Telefone", key="cand_telefone")

        if st.button("Salvar Candidato", use_container_width=True):
            if nome:
                novo = {"nome": nome, "email": email, "telefone": telefone, "criado_em": agora_formatado()}
                service.criar_candidato(novo)
                registrar_log("Candidatos", "Criar", campo="nome", valor_novo=nome)
                st.success("✅ Candidato cadastrado com sucesso!")
                st.rerun()
            else:
                st.warning("Informe ao menos o nome do candidato.")
