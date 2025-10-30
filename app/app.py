import streamlit as st
from app.pages import clientes, vagas, candidatos, comercial, logs

LOGO_URL = "https://parmaconsultoria.com.br/wp-content/uploads/2023/10/logo-parma-1.png"

def main():
    # =====================================================
    # CONFIGURAÇÃO BASE
    # =====================================================
    st.set_page_config(page_title="Parma ERP", layout="wide")

    # =====================================================
    # CSS GLOBAL — Tema Branco Moderno
    # =====================================================
    st.markdown("""
<style>
[data-testid="stHeader"] {
    display: none;
}
div.block-container {padding-top: 1.5rem;}
.stTabs [data-baseweb="tab-list"] {gap: 8px;}
.stTabs [data-baseweb="tab"] {
    background-color: #F5F7FA;
    color: #004488;
    font-weight: 600;
    border-radius: 6px;
    padding: 0.4rem 1rem;
}
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background-color: #004488;
    color: white;
}
div.stButton>button {
    border-radius: 8px;
    background: #004488;
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
    # LOGIN
    # =====================================================
    if not st.session_state.get("logged_in"):
        from app.pages.login import page as login_page
        login_page()
        return

    # =====================================================
    # HEADER (LOGO + PERFIL)
    # =====================================================
    usuario = st.session_state.get("usuario", "Usuário")
    empresa = "Parma Consultoria"

    nav_container = st.container()
    with nav_container:
        st.image(LOGO_URL, width=180)

    st.markdown("---")

    # =====================================================
    # ABAS DE NAVEGAÇÃO
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

        # Pequeno dashboard resumido
        try:
            c1, c2, c3 = st.columns(3)
            from core.services.clientes_service import ClientesService
            from core.services.recrutamento_service import RecrutamentoService
            cli = ClientesService()
            rec = RecrutamentoService()
            c1.metric("Clientes", len(cli.listar()))
            c2.metric("Vagas", len(rec.listar_vagas()))
            c3.metric("Candidatos", len(rec.listar_candidatos()))
        except Exception:
            st.warning("ℹ️ Métricas indisponíveis no momento.")

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
