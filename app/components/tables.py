import streamlit as st
from typing import List, Dict, Any

def render_table(data: List[Dict[str, Any]]):
    if not data:
        st.info("Nenhum registro encontrado.")
        return
    st.dataframe(data, use_container_width=True)
