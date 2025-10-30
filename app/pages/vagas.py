import streamlit as st
import pandas as pd
from core.services.recrutamento_service import RecrutamentoService
from app.components.filters import search_and_pagination
from core.services.log_service import registrar_log
from common.config import agora_formatado

def page():
    st.title("📋 Vagas")
    service = RecrutamentoService()

    search, page_num = search_and_pagination(prefix="vagas")
    data = service.listar_vagas(page=page_num, busca=search)
    df = pd.DataFrame(data) if data else pd.DataFrame()

    if not df.empty:
        if "criado_em" in df.columns:
            df["criado_em"] = pd.to_datetime(df["criado_em"], errors="coerce").dt.strftime("%d/%m/%Y")
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhuma vaga encontrada.")

    with st.expander("➕ Nova Vaga"):
        titulo = st.text_input("Título da Vaga", key="vaga_titulo")
        descricao = st.text_area("Descrição", key="vaga_desc")
        status = st.selectbox("Status", ["Aberta", "Fechada", "Pausada"], key="vaga_status")

        if st.button("Salvar Vaga", use_container_width=True):
            if titulo:
                nova = {"titulo": titulo, "descricao": descricao, "status": status, "criado_em": agora_formatado()}
                service.criar_vaga(nova)
                registrar_log("Vagas", "Criar", campo="titulo", valor_novo=titulo)
                st.success("✅ Vaga cadastrada com sucesso!")
                st.rerun()
            else:
                st.warning("Informe ao menos o título da vaga.")
