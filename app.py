# app.py
import streamlit as st
from modules.clientes import tela_clientes
from modules.vagas import tela_vagas   # (adicione depois quando migrar)
from modules.candidatos import tela_candidatos  # (idem)
from modules.comercial import tela_comercial   # (idem)
from modules.logs import tela_logs  # (idem)
from modules.supabase_utils import get_client

# -----------------------------------------------------------------------------
# CONFIGURAÇÃO BÁSICA
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Parma Consultoria",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.image("https://i.imgur.com/8LCCHtN.png", use_column_width=True)  # opcional, logo
st.sidebar.title("📋 Menu Principal")

# -----------------------------------------------------------------------------
# MENU LATERAL
# -----------------------------------------------------------------------------
pagina = st.sidebar.radio(
    "Navegação",
    [
        "Início",
        "Clientes",
        "Vagas",
        "Candidatos",
        "Comercial",
        "Logs"
    ],
    index=0
)

# -----------------------------------------------------------------------------
# FUNÇÃO DE TESTE DE CONEXÃO AO SUPABASE
# -----------------------------------------------------------------------------
@st.cache_data(ttl=60)
def ping_supabase():
    try:
        supa = get_client()
        res = supa.table("clientes").select("id").limit(1).execute()
        return True, len(res.data or [])
    except Exception as e:
        return False, str(e)

ok, info = ping_supabase()
if ok:
    st.sidebar.success(f"✅ Supabase conectado ({info} clientes)")
else:
    st.sidebar.error(f"❌ Erro na conexão: {info}")

# -----------------------------------------------------------------------------
# CONTEÚDO DAS PÁGINAS
# -----------------------------------------------------------------------------
if pagina == "Início":
    st.title("🏢 Parma Consultoria")
    st.subheader("Painel Administrativo")
    st.markdown(
        """
        Bem-vindo ao painel da **Parma Consultoria**.  
        Use o menu lateral para acessar os módulos:
        - 👥 Clientes  
        - 💼 Vagas  
        - 👤 Candidatos  
        - 📈 Comercial  
        - 🧾 Logs

        Todos os dados agora são sincronizados em tempo real com o **Supabase**.
        """
    )

elif pagina == "Clientes":
    tela_clientes()

elif pagina == "Vagas":
    st.info("🧩 Tela de Vagas ainda não migrada para Supabase.")

elif pagina == "Candidatos":
    st.info("🧩 Tela de Candidatos ainda não migrada para Supabase.")

elif pagina == "Comercial":
    st.info("🧩 Tela de Comercial ainda não migrada para Supabase.")

elif pagina == "Logs":
    st.info("🧩 Tela de Logs ainda não migrada para Supabase.")
