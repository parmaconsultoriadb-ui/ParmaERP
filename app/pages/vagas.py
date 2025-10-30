import streamlit as st
import pandas as pd
from core.services.recrutamento_service import RecrutamentoService
from app.components.filters import search_and_pagination
from core.services.log_service import registrar_log
from common.config import agora_formatado

STATUS_VAGAS = ["Aberta", "Ag. Inicio", "Cancelada", "Fechada", "Reaberta", "Pausada"]

def page():
    st.title("📋 Vagas")
    service = RecrutamentoService()

    # filtros + paginação (keys únicas)
    search, page_num = search_and_pagination(prefix="vagas")

    # listagem
    data = service.listar_vagas(page=page_num, busca=search)
    df = pd.DataFrame(data) if data else pd.DataFrame()

    if not df.empty:
        # formatações de data
        for col in ["data_de_abertura", "atualizacao"]:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], dayfirst=True, errors="coerce").dt.strftime("%d/%m/%Y")
        if "created_at" in df.columns:
            df["created_at"] = pd.to_datetime(df["created_at"], dayfirst=True, errors="coerce").dt.strftime("%d/%m/%Y %H:%M:%S")
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhuma vaga encontrada.")

    # cadastro
    with st.expander("➕ Nova Vaga"):
        cliente = st.text_input("Cliente", key="vaga_cliente")
        cargo = st.text_input("Cargo", key="vaga_cargo")
        recrutador = st.text_input("Recrutador", key="vaga_recrutador")
        status = st.selectbox("Status", STATUS_VAGAS, index=0, key="vaga_status")
        col1, col2, col3 = st.columns(3)
        with col1:
            salario_1 = st.text_input("Salário 1", key="vaga_sal1")
        with col2:
            salario_2 = st.text_input("Salário 2", key="vaga_sal2")
        with col3:
            salario_final = st.text_input("Salário Final", key="vaga_salfinal")
        reposicao = st.checkbox("Vaga de Reposição?", key="vaga_reposicao")

        if st.button("Salvar Vaga", use_container_width=True):
            if cliente and cargo:
                nova = {
                    "cliente": cliente,
                    "cargo": cargo,
                    "recrutador": recrutador or None,
                    "status": status,
                    "salario_1": salario_1 or None,
                    "salario_2": salario_2 or None,
                    "salario_final": salario_final or None,
                    "reposicao": "Sim" if reposicao else None,
                    "created_at": agora_formatado(),
                }
                service.criar_vaga(nova)
                registrar_log("Vagas", "Criar", campo="cargo", valor_novo=f"{cargo} ({cliente})")
                st.success("✅ Vaga cadastrada com sucesso!")
                st.rerun()
            else:
                st.warning("Informe ao menos Cliente e Cargo.")
