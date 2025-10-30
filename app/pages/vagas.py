import streamlit as st
from core.services.recrutamento_service import RecrutamentoService
from app.components.filters import search_and_pagination
from app.components.tables import render_table
from core.services.log_service import registrar_log
from core.services.notificacao_service import enviar_email_vaga
from datetime import date

service = RecrutamentoService()
RECRUTADORES_PADRAO = ["A definir", "Lorrayne", "Kaline", "Nikole", "Leila", "Julia"]

def page():
    st.header("📄 Vagas")
    search, page_num = search_and_pagination()
    data = service.vagas_listar(page=page_num, busca_cliente=search)
    render_table(data)

    st.subheader("Nova vaga")
    with st.form("nova_vaga"):
        cliente = st.text_input("Cliente")
        cargo = st.text_input("Cargo")
        recrutador = st.selectbox("Recrutador", RECRUTADORES_PADRAO)
        status = st.selectbox("Status", ["Aberta", "Ag. Inicio", "Cancelada", "Fechada", "Reaberta", "Pausada"])
        salario1 = st.text_input("Salário 1 (opcional)")
        salario2 = st.text_input("Salário 2 (opcional)")
        reposicao = st.checkbox("Reposição?")
        if st.form_submit_button("Salvar"):
            obj = service.vaga_criar({
                "cliente": cliente, "cargo": cargo, "recrutador": recrutador, "status": status,
                "data_abertura": date.today().strftime("%Y-%m-%d"),
                "salario1": salario1 or None, "salario2": salario2 or None,
                "reposicao": "Sim" if reposicao else ""
            })
            registrar_log("Vagas", "Adicionar", item_id=str(obj.get("id")), detalhe=f"Vaga {cargo} para {cliente}")
            try:
                enviar_email_vaga(cliente, cargo)
            except Exception:
                st.warning("Não foi possível enviar o e-mail de confirmação.")
            st.success(f"Vaga criada: {obj.get('id')}")
            st.rerun()
