import streamlit as st
import pandas as pd
from core.services.clientes_service import ClientesService
from app.components.filters import search_and_pagination
from core.services.log_service import registrar_log
from common.config import agora_formatado

def page():
    st.title("👥 Clientes")
    service = ClientesService()

    search, page_num = search_and_pagination(prefix="clientes")

    data = service.listar(page=page_num, busca=search)
    df = pd.DataFrame(data) if data else pd.DataFrame()

    if not df.empty:
        if "data" in df.columns:
            df["data"] = pd.to_datetime(df["data"], errors="coerce").dt.strftime("%d/%m/%Y")
        if "created_at" in df.columns:
            df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce").dt.strftime("%d/%m/%Y %H:%M:%S")
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhum cliente encontrado.")

    with st.expander("➕ Novo Cliente"):
        cliente = st.text_input("Razão Social / Cliente", key="cliente_cliente")
        nome = st.text_input("Nome do Contato", key="cliente_nome")
        cidade = st.text_input("Cidade", key="cliente_cidade")
        uf = st.text_input("UF", key="cliente_uf", max_chars=2)
        telefone = st.text_input("Telefone", key="cliente_telefone")
        email = st.text_input("Email", key="cliente_email")

        if st.button("Salvar Cliente", use_container_width=True):
            if cliente:
                novo = {
                    "data": agora_formatado().split(" ")[0],
                    "cliente": cliente,
                    "nome": nome or None,
                    "cidade": cidade or None,
                    "uf": uf.upper() if uf else None,
                    "telefone": telefone or None,
                    "email": email or None,
                    "created_at": agora_formatado(),
                }
                service.criar(novo)
                registrar_log("Clientes", "Criar", campo="cliente", valor_novo=cliente)
                st.success("✅ Cliente cadastrado com sucesso!")
                st.rerun()
            else:
                st.warning("Informe ao menos o nome ou razão social do cliente.")
