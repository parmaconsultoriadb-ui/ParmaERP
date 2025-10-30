import streamlit as st

def search_and_pagination(default_page: int = 1, prefix: str = ""):
    """Campo de busca + número de página com keys únicas para evitar conflitos"""
    col1, col2 = st.columns([3, 1])
    with col1:
        search = st.text_input("Buscar", key=f"search_{prefix}")
    with col2:
        current_page = st.session_state.get(f"page_{prefix}", default_page)
        try:
            current_page = int(current_page)
        except (ValueError, TypeError):
            current_page = default_page
        page = st.number_input(
            "Página",
            min_value=1,
            value=current_page,
            step=1,
            key=f"page_input_{prefix}",
        )
    st.session_state[f"page_{prefix}"] = int(page)
    return (search or None), int(page)
