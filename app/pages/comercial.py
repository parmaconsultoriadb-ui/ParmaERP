import streamlit as st
from core.services.comercial_service import ComercialService
from app.components.filters import search_and_pagination
from app.components.tables import render_table
from core.services.log_service import registrar_log
from datetime import date

service = ComercialService()
FUNIL = ["Prospect","Lead Qualificado","Negociação","Proposta Enviada","Contrato Enviado","Negócio Fechado","Declinado"]

def page():
    st.header("💼 Comercial")
    modo = st.radio("Visualização:", ["Kanban", "Lista"], horizontal=True)

    # Cadastro rápido
    with st.expander("➕ Novo registro comercial"):
        with st.form("novo_comercial"):
            col1, col2, col3 = st.columns(3)
            with col1:
                cliente = st.text_input("Cliente")
                cidade = st.text_input("Cidade")
                uf = st.text_input("UF", max_chars=2)
            with col2:
                contato = st.text_input("Contato")
                telefone = st.text_input("Telefone")
                email = st.text_input("E-mail")
            with col3:
                produto = st.selectbox("Produto", ["Recrutamento", "Consultoria RH", "Marketing", "Outros"])
                canal = st.selectbox("Canal", ["Google", "Mídias Sociais", "Indicação", "Outros"])
                status = st.selectbox("Status", FUNIL)
            if st.form_submit_button("Salvar"):
                obj = service.criar({
                    "data": date.today().strftime("%Y-%m-%d"),
                    "cliente": cliente, "cidade": cidade, "uf": uf,
                    "nome": contato, "telefone": telefone, "email": email,
                    "produto": produto, "canal": canal, "status": status, "observacoes": ""
                })
                registrar_log("Comercial", "Adicionar", item_id=str(obj.get("id")), detalhe=f"{cliente}")
                st.success("Registro adicionado")
                st.rerun()

    if modo == "Lista":
        search, page_num = search_and_pagination(prefix="comercial")
        data = service.listar(page=page_num, busca_status=search)
        render_table(data)
    else:
        # Kanban simples
        cols = st.columns(len(FUNIL))
        for i, status in enumerate(FUNIL):
            col = cols[i]
            col.subheader(f"{status}")
            subset = service.listar(page=1, busca_status=status)
            if not subset:
                col.info("—")
            else:
                for row in subset:
                    with col.container(border=True):
                        st.markdown(f"**{row.get('cliente')}**  \n{row.get('produto','')}/{row.get('canal','')}")
                        a1, a2 = st.columns(2)
                        with a1:
                            if st.button("⮜", key=f"left_{status}_{row['id']}", help="Mover para a coluna anterior"):
                                idx = FUNIL.index(status)
                                if idx > 0:
                                    novo = FUNIL[idx-1]
                                    service.mover_status(row["id"], novo)
                                    registrar_log("Comercial","Mover", item_id=str(row["id"]), campo="status", valor_anterior=status, valor_novo=novo)
                                    st.rerun()
                        with a2:
                            if st.button("⮞", key=f"right_{status}_{row['id']}", help="Mover para a próxima coluna"):
                                idx = FUNIL.index(status)
                                if idx < len(FUNIL)-1:
                                    novo = FUNIL[idx+1]
                                    service.mover_status(row["id"], novo)
                                    registrar_log("Comercial","Mover", item_id=str(row["id"]), campo="status", valor_anterior=status, valor_novo=novo)
                                    st.rerun()
