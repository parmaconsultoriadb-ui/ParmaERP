import streamlit as st
import pandas as pd
from core.services.recrutamento_service import RecrutamentoService
from app.components.filters import search_and_pagination
from core.services.log_service import registrar_log
from common.config import agora_formatado

STATUS_CANDIDATOS = ["Enviado", "Validado", "Não validado", "Desistência"]

def page():
    st.title("🧑‍💼 Candidatos")
    service = RecrutamentoService()

    # filtros + paginação
    search, page_num = search_and_pagination(prefix="candidatos")

    # listagem
    data = service.listar_candidatos(page=page_num, busca=search)
    df = pd.DataFrame(data) if data else pd.DataFrame()

    if not df.empty:
        for col in ["data_cadastro", "data_inicio", "atualizacao"]:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], dayfirst=True, errors="coerce").dt.strftime("%d/%m/%Y")
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhum candidato encontrado.")

    # cadastro
    with st.expander("➕ Novo Candidato"):
        cliente = st.text_input("Cliente", key="cand_cliente")
        cargo = st.text_input("Cargo", key="cand_cargo")

        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome", key="cand_nome")
            telefone = st.text_input("Telefone", key="cand_tel")
        with col2:
            recrutador = st.text_input("Recrutador", key="cand_recrut")
            status = st.selectbox("Status", STATUS_CANDIDATOS, index=0, key="cand_status")

        data_inicio = st.text_input("Data de Início (DD/MM/YYYY) — opcional", key="cand_inicio")

        if st.button("Salvar Candidato", use_container_width=True):
            if cliente and cargo and nome:
                novo = {
                    "cliente": cliente,
                    "cargo": cargo,
                    "nome": nome,
                    "telefone": telefone or None,
                    "recrutador": recrutador or None,
                    "status": status,
                    "data_inicio": data_inicio or None,
                    "atualizacao": None,  # será preenchido em atualizações de status
                }
                service.criar_candidato(novo)
                registrar_log("Candidatos", "Criar", campo="nome", valor_novo=f"{nome} ({cliente} • {cargo})")
                st.success("✅ Candidato cadastrado com sucesso!")
                st.rerun()
            else:
                st.warning("Informe Cliente, Cargo e Nome.")
