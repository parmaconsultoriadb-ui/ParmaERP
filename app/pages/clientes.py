import streamlit as st
import pandas as pd
from core.services.clientes_service import ClientesService
from app.components.filters import search_and_pagination
from core.services.log_service import registrar_log
from common.config import agora_formatado

def page():
    st.title("👥 Clientes")
    service = ClientesService()

    # Filtros
    search, page_num = search_and_pagination(prefix="clientes")

    # Listagem
    data = service.listar(page=page_num, busca=search)
    df = pd.DataFrame(data) if data else pd.DataFrame()

    if not df.empty:
        if "criado_em" in df.columns:
            df["criado_em"] = pd.to_datetime(df["criado_em"], errors="coerce").dt.strftime("%d/%m/%Y")
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhum cliente encontrado.")

    # Formulário de cadastro
    with st.expander("➕ Novo Cliente"):
        nome = st.text_input("Nome do Cliente", key="cli_nome")
        email = st.text_input("Email", key="cli_email")
        telefone = st.text_input("Telefone", key="cli_telefone")

        if st.button("Salvar Cliente", use_container_width=True):
            if nome:
                novo = {"nome": nome, "email": email, "telefone": telefone, "criado_em": agora_formatado()}
                service.criar(novo)
                registrar_log("Clientes", "Criar", campo="nome", valor_novo=nome)
                st.success("✅ Cliente cadastrado com sucesso!")
                st.rerun()
            else:
                st.warning("Informe ao menos o nome do cliente.")
