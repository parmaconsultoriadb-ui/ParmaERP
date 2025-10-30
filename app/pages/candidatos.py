import streamlit as st
from core.services.recrutamento_service import RecrutamentoService
from app.components.filters import search_and_pagination
from app.components.tables import render_table
from core.services.log_service import registrar_log
from datetime import date

service = RecrutamentoService()
RECRUTADORES_PADRAO = ["A definir", "Lorrayne", "Kaline", "Nikole", "Leila", "Julia"]

def page():
    st.header("🧑‍💻 Candidatos")
    search, page_num = search_and_pagination()
    data = service.candidatos_listar(page=page_num, busca_nome=search)
    render_table(data)

    st.subheader("Novo candidato")
    with st.form("novo_candidato"):
        cliente = st.text_input("Cliente")
        cargo = st.text_input("Cargo")
        nome = st.text_input("Nome")
        telefone = st.text_input("Telefone (opcional)")
        recrutador = st.selectbox("Recrutador", RECRUTADORES_PADRAO)
        status = st.selectbox("Status", ["Enviado", "Validado", "Não validado", "Desistência"])
        if st.form_submit_button("Salvar"):
            obj = service.candidato_criar({
                "cliente": cliente, "cargo": cargo, "nome": nome, "telefone": telefone or None,
                "recrutador": recrutador, "status": status, "data_cadastro": date.today().strftime("%Y-%m-%d")
            })
            registrar_log("Candidatos", "Adicionar", item_id=str(obj.get("id")), detalhe=f"Candidato {nome} para {cliente} - {cargo}")
            st.success(f"Candidato criado: {obj.get('id')}")
            st.rerun()
