import streamlit as st
from core.services.recrutamento_service import RecrutamentoService
from app.components.tables import render_table
from app.components.filters import search_and_pagination

st.set_page_config(page_title="Vagas", page_icon="📄", layout="wide")
st.title("Recrutamento • Vagas")

service = RecrutamentoService()

search, page = search_and_pagination()
with st.spinner("Carregando vagas..."):
    data = service.listar_vagas(page=page, busca=search)
render_table(data)

st.subheader("Nova vaga")
with st.form("nova_vaga"):
    titulo = st.text_input("Título")
    status = st.selectbox("Status", ["Aberta", "Fechada", "Pausada"])
    submitted = st.form_submit_button("Salvar")
    if submitted:
        try:
            obj = service.criar_vaga({"titulo": titulo, "status": status})
            st.success(f"Vaga criada: {obj['id']}")
        except Exception as e:
            st.error(f"Erro: {e}")
