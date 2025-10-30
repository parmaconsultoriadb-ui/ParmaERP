import streamlit as st
from core.services.auth_service import login

def page():
    st.title("🔒 Login - Parma ERP")
    st.image("https://parmaconsultoria.com.br/wp-content/uploads/2023/10/logo-parma-1.png", width=200)

    with st.form("login_form"):
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        entrar = st.form_submit_button("Entrar", use_container_width=True)

        if entrar:
            ok, permissoes = login(usuario.strip(), senha.strip())
            if ok:
                st.session_state.logged_in = True
                st.session_state.usuario = usuario
                st.session_state.permissoes = permissoes
                st.success("✅ Login realizado com sucesso!")
                st.rerun()
            else:
                st.error("❌ Usuário ou senha inválidos.")

    st.caption("© 2025 Parma Consultoria • Sistema Interno ERP")
