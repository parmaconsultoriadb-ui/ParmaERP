import streamlit as st
import pandas as pd
from core.services.log_service import carregar_logs
from app.components.filters import search_and_pagination

def page():
    st.title("📜 Logs do Sistema")

    search, page_num = search_and_pagination(prefix="logs")
    data = carregar_logs(page=page_num)
    df = pd.DataFrame(data) if data else pd.DataFrame()

    if not df.empty:
        if "datahora" in df.columns:
            df["datahora"] = pd.to_datetime(df["datahora"], errors="coerce").dt.strftime("%d/%m/%Y %H:%M:%S")
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhum log encontrado.")
