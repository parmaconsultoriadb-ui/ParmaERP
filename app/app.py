import streamlit as st
from app.pages import clientes, vagas, candidatos, comercial, logs

def main():
    # =====================================================
    # CONFIGURAÇÃO BASE
    # =====================================================
    st.set_page_config(page_title="Parma ERP", layout="wide")

    # CSS Global – Tema Parma
    st.markdown("""
    <style>
    :root {
        --color-primary: #004488;
        --color-primary-light: #E0F2F7;
        --color-text: #333333;
        --color-bg: #F8FAFC;
    }
    body {
        background-color: var(--color-bg);
        color: var(--color-text);
        font-family: 'Inter', sans-serif;
    }
    div[data-testid="stToolbar"] {visibility: hidden;}
    [data-testid="stHeader"] {
    background-color: white;}
    div.block-container {padding-top: 2rem;}
    .stTabs [data-baseweb="tab-list"] {gap: 10px;}
    .stTabs [data-baseweb="tab"] {
        background-color: var(--color-primary-light);
        color: var(--color-primary);
        font-weight: 600;
        border-radius: 8px;
        padding: 0.5rem 1rem;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: var(--color-primary);
        color: white;
    }
    div.stButton>button {
        border-radius: 8px;
        background: var(--color-primary);
        color: white;
        border: none;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
    }
    div.stButton>button:hover {
        background: #0066AA;
    }
    </style>
    """, unsafe_allow_html=True)

    # =====================================================
    # LOGIN CHECK
    # =====================================================
    if not st.session_state.get("logged_in"):
        from app.pages.login import page as login_page
        login_page()
        return

    # =====================================================
    # HEADER / IDENTIFICAÇÃO
    # =====================================================
    st.image("https://parmaconsultoria.com.br/wp-content/uploads/2023/10/logo-parma-1.png", width=180)
    st.caption(f"Usuário: {st.session_state.get('usuario', '').capitalize()}")

    # =====================================================
    # ABAS PRINCIPAIS
    # =====================================================
    tabs = st.tabs([
        "🏠 Início",
        "👥 Clientes",
        "📋 Vagas",
        "🧑‍💼 Candidatos",
        "💼 Comercial",
        "📜 Logs"
    ])

    # =====================================================
    # CONTEÚDO DAS ABAS
    # =====================================================
    with tabs[0]:
        st.title("Painel Parma ERP")
        st.write("Bem-vindo ao sistema interno da Parma Consultoria.")
        st.info("Use as abas acima para navegar entre os módulos.")
        # Pequeno dashboard de métricas
        try:
            c1, c2, c3 = st.columns(3)
            from core.services.clientes_service import listar_clientes
            from core.services.recrutamento_service import listar_vagas, listar_candidatos
            c1.metric("Clientes", len(listar_clientes()))
            c2.metric("Vagas", len(listar_vagas()))
            c3.metric("Candidatos", len(listar_candidatos()))
        except Exception:
            st.warning("ℹ️ Métricas indisponíveis temporariamente.")

    with tabs[1]:
        clientes.page()

    with tabs[2]:
        vagas.page()

    with tabs[3]:
        candidatos.page()

    with tabs[4]:
        comercial.page()

    with tabs[5]:
        logs.page()

    # =====================================================
    # RODAPÉ
    # =====================================================
    st.markdown("---")
    st.caption("© 2025 Parma Consultoria • ERP Interno")

if __name__ == "__main__":
    main()
