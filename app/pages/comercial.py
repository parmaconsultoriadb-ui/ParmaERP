import streamlit as st
from core.services.comercial_service import ComercialService
from app.components.tables import render_table
from app.components.filters import search_and_pagination

st.set_page_config(page_title="Comercial", page_icon="💼", layout="wide")
st.title("Comercial • Oportunidades")

service = ComercialService()

search, page = search_and_pagination()
with st.spinner("Carregando oportunidades..."):
    data = service.listar_oportunidades(page=page, busca=search)
render_table(data)

st.subheader("Nova oportunidade")
with st.form("nova_opp"):
    cliente_id = st.text_input("ID do Cliente")
    valor = st.number_input("Valor (R$)", min_value=0.0, step=100.0)
    fase = st.selectbox("Fase", ["Lead", "Qualificação", "Proposta", "Fechamento", "Ganho", "Perdido"])
    submitted = st.form_submit_button("Salvar")
    if submitted:
        try:
            obj = service.criar_oportunidade({"cliente_id": cliente_id, "valor": float(valor), "fase": fase})
            st.success(f"Oportunidade criada: {obj['id']}")
        except Exception as e:
            st.error(f"Erro: {e}")
