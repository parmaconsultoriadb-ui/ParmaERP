import streamlit as st
from common.config import settings
from app.components.theme import apply_parma_theme
from core.services.auth_service import login, get_permissoes

# páginas
from app.pages import clientes as pg_clientes
from app.pages import vagas as pg_vagas
from app.pages import candidatos as pg_candidatos
from app.pages import comercial as pg_comercial
from app.pages import contratos as pg_contratos
from app.pages import logs as pg_logs

MENU = [
    ("menu", "🏠 Menu Principal"),
    ("comercial", "💼 Comercial"),
    ("clientes", "👥 Clientes"),
    ("vagas", "📄 Vagas"),
    ("candidatos", "🧑‍💻 Candidatos"),
    ("contratos", "💰 Contratos"),
    ("logs", "📜 Logs")
]

def _top_nav(allowed_keys):
    cols = st.columns(len(allowed_keys) + 2)
    for i, k in enumerate(allowed_keys):
        label = dict(MENU)[k]
        if cols[i].button(label, use_container_width=True):
            st.session_state.page = k
            st.rerun()
    if cols[-2].button("🔄 Refresh", use_container_width=True):
        st.rerun()
    if cols[-1].button("Sair", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.page = "login"
        st.rerun()

def _menu_interno():
    st.image("https://parmaconsultoria.com.br/wp-content/uploads/2023/10/logo-parma-1.png", width=200)
    st.title("📊 Sistema Parma Consultoria")
    st.subheader("Bem-vindo! Escolha uma opção para começar.")
    c1, c2, c3 = st.columns(3)
    if c1.button("👥 Clientes", use_container_width=True):
        st.session_state.page = "clientes"; st.rerun()
    if c2.button("📄 Vagas", use_container_width=True):
        st.session_state.page = "vagas"; st.rerun()
    if c3.button("🧑‍💻 Candidatos", use_container_width=True):
        st.session_state.page = "candidatos"; st.rerun()
    st.divider()
    c4, c5, _ = st.columns(3)
    if c4.button("💼 Comercial", use_container_width=True):
        st.session_state.page = "comercial"; st.rerun()
    if c5.button("📜 Logs do Sistema", use_container_width=True):
        st.session_state.page = "logs"; st.rerun()

def main():
    st.set_page_config(page_title=settings.APP_NAME, page_icon="📦", layout="wide")
    apply_parma_theme()

    if "page" not in st.session_state: st.session_state.page = "login"
    if "logged_in" not in st.session_state: st.session_state.logged_in = False
    if "usuario" not in st.session_state: st.session_state.usuario = ""
    if "permissoes" not in st.session_state: st.session_state.permissoes = []

    st.caption(f"Ambiente: {settings.ENV}  •  Modo: {'ERRO credenciais Supabase' if settings.DEMO_MODE else 'Supabase conectado'}")

    if st.session_state.page == "login" or not st.session_state.logged_in:
        st.image("https://parmaconsultoria.com.br/wp-content/uploads/2023/10/logo-parma-1.png", width=200)
        st.title("🔒 Login - Parma Consultoria")
        with st.form("login_form"):
            usuario = st.text_input("Usuário")
            senha = st.text_input("Senha", type="password")
            if st.form_submit_button("Entrar", use_container_width=True):
                ok, perms = login(usuario, senha)
                if ok:
                    st.session_state.logged_in = True
                    st.session_state.usuario = usuario
                    st.session_state.permissoes = perms
                    st.session_state.page = "menu"
                    st.success("✅ Login realizado!")
                    st.rerun()
                else:
                    st.error("❌ Usuário ou senha inválidos.")
        return

    # Header/top-nav
    st.image("https://parmaconsultoria.com.br/wp-content/uploads/2023/10/logo-parma-1.png", width=160)
    st.caption(f"Usuário: {st.session_state.usuario}")

    all_keys = [k for k,_ in MENU]
    allowed = []
    perms = st.session_state.permissoes or []
    # sempre habilita "menu"
    if "menu" not in perms: perms = ["menu"] + perms
    for k, _ in MENU:
        if k == "menu" or k in perms or (k == "contratos" and "comercial" in perms):
            allowed.append(k)
    _top_nav(allowed)

    current = st.session_state.page
    st.markdown("<hr class='parma-hr' />", unsafe_allow_html=True)

    if current == "menu":
        _menu_interno()
    elif current == "clientes":
        pg_clientes.page()
    elif current == "vagas":
        pg_vagas.page()
    elif current == "candidatos":
        pg_candidatos.page()
    elif current == "comercial":
        pg_comercial.page()
    elif current == "contratos":
        pg_contratos.page()
    elif current == "logs":
        pg_logs.page()
    else:
        st.info("Página não encontrada.")

if __name__ == "__main__":
    main()
