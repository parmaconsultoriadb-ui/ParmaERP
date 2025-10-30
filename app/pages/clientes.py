import streamlit as st
from core.services.clientes_service import ClientesService
from app.components.filters import search_and_pagination
from app.components.tables import render_table
from core.services.log_service import registrar_log

service = ClientesService()

def page():
    st.header("👥 Clientes")
    search, page_num = search_and_pagination(prefix="clientes")
    data = service.listar(page=page, busca=search)
    render_table(data)

    st.subheader("Novo cliente")
    with st.form("novo_cliente"):
        nome = st.text_input("Nome")
        email = st.text_input("Email (opcional)")
        cidade = st.text_input("Cidade (opcional)")
        uf = st.text_input("UF (opcional)", max_chars=2)
        telefone = st.text_input("Telefone (opcional)")
        if st.form_submit_button("Salvar"):
            obj = service.criar({"nome": nome, "email": email or None, "cidade": cidade or None, "uf": uf or None, "telefone": telefone or None})
            registrar_log("Clientes", "Adicionar", item_id=str(obj.get("id")), detalhe=f"Cliente {nome} criado.")
            st.success(f"Cliente criado: {obj.get('id')}")
            st.rerun()
