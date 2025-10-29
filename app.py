# app.py
import streamlit as st

from modules.candidatos import tela_candidatos
from modules.clientes import tela_clientes
from modules.comercial import tela_comercial
from modules.logs import tela_logs
from modules.supabase_utils import get_client
from modules.vagas import tela_vagas


# -----------------------------------------------------------------------------
# CONFIGURAÇÃO BÁSICA
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Parma Consultoria",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.sidebar.image("https://i.imgur.com/8LCCHtN.png", use_column_width=True)
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
        "Logs",
    ],
    index=0,
)

# -----------------------------------------------------------------------------
# FUNÇÃO DE TESTE DE CONEXÃO AO SUPABASE
# -----------------------------------------------------------------------------
@st.cache_data(ttl=60)
def ping_supabase():
    try:
        supa = get_client()
        res = supa.table("clientes").select("id").limit(1).execute()
        total = len(res.data or [])  # type: ignore[arg-type]
        return True, total
    except Exception as e:  # pragma: no cover - streamlit app
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

        Todos os dados são sincronizados em tempo real com o **Supabase**.
        """
    )

elif pagina == "Clientes":
    tela_clientes()

elif pagina == "Vagas":
    tela_vagas()

elif pagina == "Candidatos":
    tela_candidatos()

elif pagina == "Comercial":
    tela_comercial()

elif pagina == "Logs":
    tela_logs()
