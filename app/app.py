import streamlit as st
from core.services.clientes_service import ClientesService
from core.services.comercial_service import ComercialService
from core.services.recrutamento_service import RecrutamentoService
from app.components.tables import render_table
from app.components.filters import search_and_pagination

# ---------------- CONFIGURAÇÃO ----------------
st.set_page_config(page_title="ParmaERP", page_icon="📦", layout="wide")
st.markdown(
    """
    <style>
    .topnav {
        background-color: #1E88E5;
        overflow: hidden;
        border-radius: 6px;
    }
    .topnav a {
        float: left;
        color: #f2f2f2;
        text-align: center;
        padding: 10px 16px;
        text-decoration: none;
        font-size: 16px;
        font-weight: 600;
    }
    .topnav a:hover {
        background-color: #1565C0;
        color: white;
    }
    .topnav a.active {
        background-color: #0D47A1;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- MENU ----------------
menu_items = {
    "Clientes": "👥",
    "Comercial": "💼",
    "Vagas": "📄",
    "Candidatos": "🧑‍💻",
}
if "pagina" not in st.session_state:
    st.session_state["pagina"] = "Clientes"

cols = st.columns(len(menu_items))
for idx, (nome, icon) in enumerate(menu_items.items()):
    if cols[idx].button(f"{icon} {nome}", use_container_width=True):
        st.session_state["pagina"] = nome

st.markdown("<hr>", unsafe_allow_html=True)

# ---------------- ROTEAMENTO ----------------
pagina = st.session_state["pagina"]

if pagina == "Clientes":
    st.header("👥 Clientes")
    service = ClientesService()
    search, page = search_and_pagination()
    data = service.listar_clientes(page=page, busca=search)
    render_table(data)
    with st.form("novo_cliente"):
        nome = st.text_input("Nome")
        email = st.text_input("Email")
        cnpj = st.text_input("CNPJ")
        if st.form_submit_button("Salvar"):
            obj = service.criar_cliente({"nome": nome, "email": email, "cnpj": cnpj})
            st.success(f"Cliente criado: {obj['id']}")

elif pagina == "Comercial":
    st.header("💼 Oportunidades Comerciais")
    service = ComercialService()
    search, page = search_and_pagination()
    data = service.listar_oportunidades(page=page, busca=search)
    render_table(data)
    with st.form("nova_opp"):
        cliente_id = st.text_input("ID do Cliente")
        valor = st.number_input("Valor (R$)", min_value=0.0, step=100.0)
        fase = st.selectbox("Fase", ["Lead", "Qualificação", "Proposta", "Fechamento", "Ganho", "Perdido"])
        if st.form_submit_button("Salvar"):
            obj = service.criar_oportunidade({"cliente_id": cliente_id, "valor": valor, "fase": fase})
            st.success(f"Oportunidade criada: {obj['id']}")

elif pagina == "Vagas":
    st.header("📄 Vagas")
    service = RecrutamentoService()
    search, page = search_and_pagination()
    data = service.listar_vagas(page=page, busca=search)
    render_table(data)
    with st.form("nova_vaga"):
        titulo = st.text_input("Título da Vaga")
        status = st.selectbox("Status", ["Aberta", "Fechada", "Pausada"])
        if st.form_submit_button("Salvar"):
            obj = service.criar_vaga({"titulo": titulo, "status": status})
            st.success(f"Vaga criada: {obj['id']}")

elif pagina == "Candidatos":
    st.header("🧑‍💻 Candidatos")
    service = RecrutamentoService()
    search, page = search_and_pagination()
    data = service.listar_candidatos(page=page, busca=search)
    render_table(data)
    with st.form("novo_candidato"):
        nome = st.text_input("Nome")
        email = st.text_input("Email")
        status = st.selectbox("Status", ["Novo", "Em análise", "Entrevista", "Aprovado", "Reprovado"])
        if st.form_submit_button("Salvar"):
            obj = service.criar_candidato({"nome": nome, "email": email, "status": status})
            st.success(f"Candidato criado: {obj['id']}")
