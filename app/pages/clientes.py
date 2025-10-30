import streamlit as st
from core.services.clientes_service import ClientesService
from app.components.tables import render_table
from app.components.filters import search_and_pagination

st.set_page_config(page_title="Clientes", page_icon="👥", layout="wide")
st.title("Clientes")

service = ClientesService()

search, page = search_and_pagination()
with st.spinner("Carregando clientes..."):
    data = service.listar_clientes(page=page, busca=search)
render_table(data)

st.subheader("Novo cliente")
with st.form("novo_cliente"):
    nome = st.text_input("Nome", placeholder="Ex.: Empresa XYZ")
    email = st.text_input("Email (opcional)")
    cnpj = st.text_input("CNPJ (opcional, somente números)")
    submitted = st.form_submit_button("Salvar")
    if submitted:
        try:
            obj = service.criar_cliente({"nome": nome, "email": email or None, "cnpj": cnpj or None})
            st.success(f"Cliente criado: {obj['id']}")
        except Exception as e:
            st.error(f"Erro: {e}")
