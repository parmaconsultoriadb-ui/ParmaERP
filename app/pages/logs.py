import streamlit as st
from core.services.log_service import carregar_logs
from app.components.filters import search_and_pagination
from app.components.tables import render_table
from common.utils import download_button
import pandas as pd

def page():
    st.header("📜 Logs do Sistema")
    _, page_num = search_and_pagination()
    data = carregar_logs(page=page_num)
    if not data:
        st.info("Nenhum log registrado.")
        return
    render_table(data)
    df = pd.DataFrame(data)
    download_button(df, "logs.csv", label="⬇️ Baixar Logs")
