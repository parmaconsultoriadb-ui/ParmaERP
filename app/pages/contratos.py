import streamlit as st
from core.services.comercial_service import ComercialService
from app.components.tables import render_table
from core.services.log_service import registrar_log

service = ComercialService()

def page():
    st.header("💰 Contratos")
    # Exibe apenas registros relevantes do funil
    relevantes = []
    for status in ["Proposta Enviada","Contrato Enviado","Negócio Fechado"]:
        relevantes.extend(service.listar(page=1, busca_status=status))
    if not relevantes:
        st.info("Nenhum registro de contrato encontrado.")
    else:
        render_table(relevantes)

    st.caption("Atualizações específicas (Pagamento, Contrato Enviado/Assinado, etc.) podem ser implementadas como inputs inline aqui, atualizando o registro no Supabase e registrando logs.")
