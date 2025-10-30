import streamlit as st
from common.config import settings

st.set_page_config(page_title=settings.APP_NAME, page_icon="📦", layout="wide")

st.sidebar.title(settings.APP_NAME)
st.sidebar.write("Ambiente:", settings.ENV)
st.sidebar.write("Modo:", "DEMO (sem Supabase)" if settings.DEMO_MODE else "PROD (Supabase conectado)")

st.title(f"Bem-vindo ao {settings.APP_NAME}!")
st.markdown("""
Este é o hub principal.

Use o menu **Pages** (na esquerda) para acessar:
- **Clientes**
- **Comercial**
- **Vagas**
- **Candidatos**

> Dica: configure `SUPABASE_URL` e `SUPABASE_KEY` como variáveis de ambiente para usar o banco real.
""")
