import streamlit as st
from core.services.recrutamento_service import RecrutamentoService
from app.components.tables import render_table
from app.components.filters import search_and_pagination

st.set_page_config(page_title="Candidatos", page_icon="🧑‍💻", layout="wide")
st.title("Recrutamento • Candidatos")

service = RecrutamentoService()

search, page = search_and_pagination()
with st.spinner("Carregando candidatos..."):
    data = service.listar_candidatos(page=page, busca=search)
render_table(data)

st.subheader("Novo candidato")
with st.form("novo_candidato"):
    nome = st.text_input("Nome")
    email = st.text_input("Email (opcional)")
    status = st.selectbox("Status", ["Novo", "Em análise", "Entrevista", "Aprovado", "Reprovado"])
    submitted = st.form_submit_button("Salvar")
    if submitted:
        try:
            obj = service.criar_candidato({"nome": nome, "email": email or None, "status": status})
            st.success(f"Candidato criado: {obj['id']}")
        except Exception as e:
            st.error(f"Erro: {e}")
