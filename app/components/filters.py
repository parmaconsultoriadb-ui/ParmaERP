import streamlit as st

def search_and_pagination(default_page: int = 1):
    col1, col2 = st.columns([3,1])
    with col1:
        search = st.text_input("Buscar")
    with col2:
        page = st.number_input("Página", min_value=1, value=st.session_state.get("page", default_page), step=1)
    st.session_state["page"] = int(page)
    return search or None, int(page)
